import openpyxl
import urllib.parse
from datetime import datetime, timezone, timedelta
from dateutil import parser as date_parser

wb = openpyxl.load_workbook('data/exports/frontier_atlas_intelligence.xlsx', read_only=True)
now_utc = datetime.now(timezone.utc)
print(f"Current UTC Time for Audit: {now_utc.isoformat()}")

# Check 2: Uniqueness of startups, products, papers
print("\n=== 2. UNIQUENESS AUDIT ===")
for sheet_name, key_col, key_name in [('Startups', 4, 'Canonical Name'), ('Products', 5, 'Product Name'), ('Research Papers', 2, 'Paper Title')]:
    ws = wb[sheet_name]
    rows = list(ws.iter_rows(values_only=True))[1:]
    keys = [r[key_col] for r in rows if r[key_col]]
    unique_keys = set(keys)
    print(f"{sheet_name:15}: {len(rows)} total records | {len(unique_keys)} unique {key_name}s ({len(unique_keys)/len(rows)*100:.1f}% unique)")

# Check 3: Source URLs & Provenance
print("\n=== 3. SOURCE URLS & PROVENANCE AUDIT ===")
for sheet_name, url_col in [('Startups', 3), ('Products', 3), ('Research Papers', 4), ('Jobs', 3), ('News', 3), ('Entity Mapping Log', 4)]:
    ws = wb[sheet_name]
    rows = list(ws.iter_rows(values_only=True))[1:]
    invalid_urls = 0
    domains = set()
    for r in rows:
        url = str(r[url_col] or '').strip()
        if not (url.startswith('http://') or url.startswith('https://')):
            invalid_urls += 1
        else:
            netloc = urllib.parse.urlparse(url).netloc
            if netloc:
                domains.add(netloc)
    print(f"{sheet_name:20}: {len(rows)} records | Invalid/Missing URLs: {invalid_urls} | Distinct Domains: {len(domains)}")

# Check 4: Timestamps against current UTC time
print("\n=== 4. FRESHNESS AUDIT (STRICT <= 24 HOURS) ===")
for sheet_name, date_col in [('Jobs', 6), ('News', 5)]:
    ws = wb[sheet_name]
    rows = list(ws.iter_rows(values_only=True))[1:]
    stale_count = 0
    max_age_hrs = 0.0
    min_age_hrs = 999.0
    for r in rows:
        d_str = r[date_col]
        dt = date_parser.parse(d_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        diff_hrs = (now_utc - dt).total_seconds() / 3600.0
        if diff_hrs > 24.0 or diff_hrs < -0.25: # allow 15 min clock drift
            stale_count += 1
        max_age_hrs = max(max_age_hrs, diff_hrs)
        min_age_hrs = min(min_age_hrs, diff_hrs)
    print(f"{sheet_name:10}: {len(rows)} records | Stale (>24h): {stale_count} | Age Range: {min_age_hrs:.2f}h to {max_age_hrs:.2f}h | Freshness: {((len(rows)-stale_count)/len(rows))*100:.1f}%")

# Check 5: Research Papers with vs without GitHub repos
print("\n=== 5. GITHUB METRICS & OBSERVATION AUDIT ===")
ws = wb['Research Papers']
rows = list(ws.iter_rows(values_only=True))[1:]
with_repo = [r for r in rows if r[5]]
without_repo = [r for r in rows if not r[5]]
with_stars = [r for r in rows if r[6] is not None and str(r[6]).strip() != '']
with_obs_ts = [r for r in rows if r[7] is not None and str(r[7]).strip() != '']
print(f"Total Research Papers: {len(rows)}")
print(f"  - Papers WITH GitHub repository:    {len(with_repo)}")
print(f"  - Papers WITHOUT GitHub repository: {len(without_repo)}")
print(f"  - Papers with live GitHub stars:    {len(with_stars)}")
print(f"  - Papers with traceable obs time:   {len(with_obs_ts)}")
if with_stars:
    sample = with_stars[0]
    print(f"Sample: '{sample[2][:45]}...' | Repo: {sample[5]} | Stars: {sample[6]} | Retrieved At: {sample[7]}")
