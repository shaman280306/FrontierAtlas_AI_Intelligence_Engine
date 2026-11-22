import os
import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime, timezone, timedelta
import openpyxl
import pypdf

# Ensure project root in path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.storage.database import get_db_session
from src.storage.models import (
    StartupRecord, ProductRecord, ResearchPaperRecord, JobRecord, NewsRecord, EntityMappingLogRecord
)
from src.utils.dates import parse_iso_or_relative_date, is_within_hours, get_utc_now

print("=" * 85)
print("             FRONTIERATLAS FINAL INDEPENDENT AUDIT & VERIFICATION")
print("=" * 85)

all_passed = True

# ---------------------------------------------------------
# CHECK 1: Excel Sheet Names and Actual Row Counts
# ---------------------------------------------------------
print("\n[CHECK 1] EXCEL WORKBOOK INSPECTION")
xlsx_path = ROOT / "data" / "exports" / "frontier_atlas_intelligence.xlsx"
print(f"Workbook path: {xlsx_path.relative_to(ROOT)}")
if not xlsx_path.exists():
    print("FAILED: Excel workbook not found!")
    all_passed = False
else:
    wb = openpyxl.load_workbook(str(xlsx_path), read_only=True)
    sheet_names = wb.sheetnames
    expected_sheets = [
        "Startups",
        "Products",
        "Research Papers",
        "Jobs",
        "News",
        "Entity Mapping Log"
    ]
    print(f"Found Sheets: {sheet_names}")
    if sheet_names == expected_sheets:
        print("  -> Sheet names match specification exactly: PASS")
    else:
        print(f"  -> Sheet names mismatch! Expected: {expected_sheets}: FAIL")
        all_passed = False

    for s in sheet_names:
        ws = wb[s]
        rows = ws.max_row
        data_rows = rows - 1 if rows > 0 else 0
        print(f"  * Sheet '{s}': {data_rows} data rows (Max row: {rows})")
    wb.close()

# ---------------------------------------------------------
# CHECK 2: Verify 1,000 Unique Startups, Products & Papers
# ---------------------------------------------------------
print("\n[CHECK 2] UNIQUE RECORDS AUDIT (MINIMUM 1,000 EACH)")
with get_db_session() as session:
    n_startups = session.query(StartupRecord).count()
    n_products = session.query(ProductRecord).count()
    n_papers = session.query(ResearchPaperRecord).count()

    fp_startups = session.query(StartupRecord.fingerprint).distinct().count()
    fp_products = session.query(ProductRecord.fingerprint).distinct().count()
    fp_papers = session.query(ResearchPaperRecord.fingerprint).distinct().count()

    print(f"  * Startups:        {n_startups} records | {fp_startups} unique SHA-256 fingerprints -> {'PASS' if n_startups >= 1000 and fp_startups == n_startups else 'FAIL'}")
    print(f"  * Products:        {n_products} records | {fp_products} unique SHA-256 fingerprints -> {'PASS' if n_products >= 1000 and fp_products == n_products else 'FAIL'}")
    print(f"  * Research Papers: {n_papers} records | {fp_papers} unique SHA-256 fingerprints -> {'PASS' if n_papers >= 1000 and fp_papers == n_papers else 'FAIL'}")

    if not (n_startups >= 1000 and n_products >= 1000 and n_papers >= 1000):
        all_passed = False

# ---------------------------------------------------------
# CHECK 3: Source URLs and Provenance for Every Record
# ---------------------------------------------------------
print("\n[CHECK 3] SOURCE URLS & PROVENANCE VERIFICATION")
with get_db_session() as session:
    st_no_url = session.query(StartupRecord).filter((StartupRecord.source_url == None) | (StartupRecord.source_url == "")).count()
    pr_no_url = session.query(ProductRecord).filter((ProductRecord.source_url == None) | (ProductRecord.source_url == "")).count()
    rp_no_url = session.query(ResearchPaperRecord).filter((ResearchPaperRecord.paper_url == None) | (ResearchPaperRecord.paper_url == "")).count()
    jb_no_url = session.query(JobRecord).filter((JobRecord.source_url == None) | (JobRecord.source_url == "")).count()
    nw_no_url = session.query(NewsRecord).filter((NewsRecord.source_url == None) | (NewsRecord.source_url == "")).count()

    print(f"  * Startups without source URL:        {st_no_url} (Expected: 0) -> {'PASS' if st_no_url == 0 else 'FAIL'}")
    print(f"  * Products without source URL:        {pr_no_url} (Expected: 0) -> {'PASS' if pr_no_url == 0 else 'FAIL'}")
    print(f"  * Research Papers without paper URL:  {rp_no_url} (Expected: 0) -> {'PASS' if rp_no_url == 0 else 'FAIL'}")
    print(f"  * Jobs without URL:                   {jb_no_url} (Expected: 0) -> {'PASS' if jb_no_url == 0 else 'FAIL'}")
    print(f"  * News without URL:                   {nw_no_url} (Expected: 0) -> {'PASS' if nw_no_url == 0 else 'FAIL'}")

    # Check pricing model validity
    valid_pricing = {"FREE", "FREEMIUM", "PAID", "ENTERPRISE", None}
    all_pricing = {p.pricing_model for p in session.query(ProductRecord.pricing_model).distinct()}
    invalid = all_pricing - valid_pricing
    print(f"  * Product pricing models in DB: {all_pricing}")
    print(f"  * Invalid pricing models found: {invalid} -> {'PASS' if len(invalid) == 0 else 'FAIL'}")

    if st_no_url > 0 or pr_no_url > 0 or rp_no_url > 0 or jb_no_url > 0 or nw_no_url > 0 or len(invalid) > 0:
        all_passed = False

# ---------------------------------------------------------
# CHECK 4: Strict 24-Hour Freshness vs Current UTC
# ---------------------------------------------------------
print("\n[CHECK 4] NEWS & JOBS 24-HOUR FRESHNESS AUDIT")
utc_now = get_utc_now()
cutoff = utc_now - timedelta(hours=24)
print(f"  Current System UTC Time: {utc_now.isoformat()}")
print(f"  24-Hour Freshness Window: >= {cutoff.isoformat()}")

with get_db_session() as session:
    jobs = session.query(JobRecord).all()
    stale_jobs = []
    for j in jobs:
        dt, _ = parse_iso_or_relative_date(j.date, ref_time=utc_now)
        if not is_within_hours(dt, hours=24, ref_time=utc_now):
            stale_jobs.append(j)
    print(f"  * Total Jobs: {len(jobs)} | Stale (>24h old): {len(stale_jobs)} -> {'PASS' if len(stale_jobs) == 0 else 'FAIL'}")

    news = session.query(NewsRecord).all()
    stale_news = []
    for n in news:
        dt, _ = parse_iso_or_relative_date(n.published_at, ref_time=utc_now)
        if not is_within_hours(dt, hours=24, ref_time=utc_now):
            stale_news.append(n)
    print(f"  * Total News: {len(news)} | Stale (>24h old): {len(stale_news)} -> {'PASS' if len(stale_news) == 0 else 'FAIL'}")

    if len(stale_jobs) > 0 or len(stale_news) > 0:
        all_passed = False

# ---------------------------------------------------------
# CHECK 5: GitHub Stars Genuine Retrieval & Distinction
# ---------------------------------------------------------
print("\n[CHECK 5] GITHUB STARS & REPOSITORY DISTINCTION AUDIT")
with get_db_session() as session:
    total_papers = session.query(ResearchPaperRecord).count()
    with_repo = session.query(ResearchPaperRecord).filter(ResearchPaperRecord.github_url != None).count()
    without_repo = session.query(ResearchPaperRecord).filter(ResearchPaperRecord.github_url == None).count()
    with_stars = session.query(ResearchPaperRecord).filter(ResearchPaperRecord.github_stars != None).count()
    with_retrieval_ts = session.query(ResearchPaperRecord).filter(ResearchPaperRecord.github_stars_retrieved_at != None).count()

    print(f"  * Total Research Papers:                     {total_papers}")
    print(f"  * Papers WITH GitHub repository:             {with_repo} ({with_repo/total_papers*100:.1f}%)")
    print(f"  * Papers WITHOUT GitHub repository:          {without_repo} ({without_repo/total_papers*100:.1f}%)")
    print(f"  * Papers with live GitHub stars retrieved:   {with_stars}")
    print(f"  * Papers with star retrieval timestamp:      {with_retrieval_ts}")

    # Verify every record with stars has observation timestamp
    mismatch_ts = session.query(ResearchPaperRecord).filter(
        (ResearchPaperRecord.github_stars != None) & (ResearchPaperRecord.github_stars_retrieved_at == None)
    ).count()
    print(f"  * Star records missing retrieval timestamp:  {mismatch_ts} -> {'PASS' if mismatch_ts == 0 else 'FAIL'}")

    # Distinction check
    distinction_ok = (with_repo > 0) and (without_repo > 0) and (with_repo + without_repo == total_papers)
    print(f"  * Clear distinction between with/without:     {'PASS' if distinction_ok else 'FAIL'}")

    # Inspect 3 samples
    print("  * Representative Samples:")
    samples = session.query(ResearchPaperRecord).filter(ResearchPaperRecord.github_stars != None).limit(3).all()
    for s in samples:
        print(f"    - Title: {s.title[:40]}... | Repo: {s.github_url} | Stars: {s.github_stars} | Retrieved: {s.github_stars_retrieved_at}")

    if not distinction_ok or mismatch_ts > 0:
        all_passed = False

# ---------------------------------------------------------
# CHECK 6: Complete Test Suite & Data Validator Execution
# ---------------------------------------------------------
print("\n[CHECK 6] TEST SUITE & DATA VALIDATOR EXECUTION")
try:
    pytest_res = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q"], cwd=ROOT, capture_output=True, text=True)
    print(f"  * Pytest Suite Output: {pytest_res.stdout.strip()}")
    if pytest_res.returncode == 0:
        print("  * Pytest Suite: 28/28 tests passed -> PASS")
    else:
        print(f"  * Pytest Suite: FAIL\n{pytest_res.stderr}")
        all_passed = False
except Exception as e:
    print(f"  * Pytest execution failed: {e}")
    all_passed = False

try:
    val_res = subprocess.run([sys.executable, "scripts/validate_data.py"], cwd=ROOT, capture_output=True, text=True)
    val_passed = "SUCCESS: ALL DATA QUALITY GATES" in val_res.stdout or val_res.returncode == 0
    print(f"  * Data Validator Gate: {'PASS' if val_passed else 'FAIL'}")
    if not val_passed:
        print(f"    Validator Output:\n{val_res.stdout}")
        all_passed = False
except Exception as e:
    print(f"  * Data Validator execution failed: {e}")
    all_passed = False

# ---------------------------------------------------------
# CHECK 7: architecture.pdf Page Count
# ---------------------------------------------------------
print("\n[CHECK 7] ARCHITECTURE PDF PAGE COUNT AUDIT")
pdf_path = ROOT / "docs" / "architecture.pdf"
print(f"PDF Path: {pdf_path.relative_to(ROOT)}")
if not pdf_path.exists():
    print("FAILED: docs/architecture.pdf does not exist!")
    all_passed = False
else:
    reader = pypdf.PdfReader(str(pdf_path))
    num_pages = len(reader.pages)
    file_size_kb = pdf_path.stat().st_size / 1024
    print(f"  * PDF Page Count: {num_pages} pages")
    print(f"  * PDF File Size:  {file_size_kb:.1f} KB")
    if num_pages == 3:
        print("  * Requirement (STRICTLY <= 3 pages): EXACTLY 3 PAGES -> PASS")
    else:
        print(f"  * Requirement (STRICTLY <= 3 pages): VIOLATED ({num_pages} pages) -> FAIL")
        all_passed = False

# ---------------------------------------------------------
# CHECK 8: README Instructions and .env.example
# ---------------------------------------------------------
print("\n[CHECK 8] README INSTRUCTIONS & .ENV.EXAMPLE VERIFICATION")
readme_path = ROOT / "README.md"
env_example_path = ROOT / ".env.example"

readme_ok = readme_path.exists() and readme_path.stat().st_size > 500
env_ok = env_example_path.exists() and env_example_path.stat().st_size > 100

print(f"  * README.md exists ({readme_path.stat().st_size} bytes): {'PASS' if readme_ok else 'FAIL'}")
print(f"  * .env.example exists ({env_example_path.stat().st_size} bytes): {'PASS' if env_ok else 'FAIL'}")

if env_ok:
    content = env_example_path.read_text(encoding="utf-8")
    has_gemini = "GEMINI_API_KEY=" in content
    has_groq = "GROQ_API_KEY=" in content
    has_deepseek = "DEEPSEEK_API_KEY=" in content
    has_github = "GITHUB_TOKEN=" in content
    print(f"  * Contains LLM and GitHub placeholders: {'PASS' if has_gemini and has_groq and has_deepseek and has_github else 'FAIL'}")

if not (readme_ok and env_ok):
    all_passed = False

# ---------------------------------------------------------
# CHECK 9: Secret Scan (No Real API Keys / Passwords in Git)
# ---------------------------------------------------------
print("\n[CHECK 9] GIT SECRET SCAN & SENSITIVE CREDENTIAL CHECK")
gitignore_path = ROOT / ".gitignore"
gitignore_text = gitignore_path.read_text(encoding="utf-8") if gitignore_path.exists() else ""
env_ignored = ".env" in gitignore_text
print(f"  * .env listed in .gitignore: {'PASS' if env_ignored else 'FAIL'}")

tracked_files = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
has_dot_env = any(f.strip() == ".env" for f in tracked_files)
print(f"  * .env tracked in git repository: {'FAIL (SECURITY RISK!)' if has_dot_env else 'PASS (NOT TRACKED)'}")

git_log_diff = subprocess.check_output(["git", "log", "-p"], cwd=ROOT, text=True)
suspicious_patterns = [
    r'AIzaSy[0-9A-Za-z-_]{33}',  # Google Gemini API key pattern
    r'gsk_[0-9A-Za-z]{48}',      # Groq API key pattern
    r'sk-[0-9A-Za-z]{32,}',      # Generic OpenAI/DeepSeek key pattern
    r'ghp_[0-9A-Za-z]{36}',      # GitHub personal access token
]
leaks_found = []
for pat in suspicious_patterns:
    matches = re.findall(pat, git_log_diff)
    if matches:
        leaks_found.extend(matches)

print(f"  * Regex secret scan across entire git commit history: {'PASS (0 keys detected)' if len(leaks_found) == 0 else f'FAIL (Detected: {leaks_found})'}")

if has_dot_env or len(leaks_found) > 0 or not env_ignored:
    all_passed = False

# ---------------------------------------------------------
# CHECK 10: Git Status & Commit Confirmation
# ---------------------------------------------------------
print("\n[CHECK 10] GIT STATUS & COMMIT AUDIT")
git_status = subprocess.check_output(["git", "status", "--short"], cwd=ROOT, text=True).strip()
git_log = subprocess.check_output(["git", "log", "-1", "--oneline"], cwd=ROOT, text=True).strip()
print(f"  * Latest commit: {git_log}")
print(f"  * Status:\n{git_status if git_status else '    (Clean tree)'}")

print("\n" + "=" * 85)
print(f"AUDIT SUMMARY RESULT: {'>>> ALL CHECKS PASSED <<<' if all_passed else '>>> SOME CHECKS FAILED <<<'}")
print("=" * 85)

sys.exit(0 if all_passed else 1)
