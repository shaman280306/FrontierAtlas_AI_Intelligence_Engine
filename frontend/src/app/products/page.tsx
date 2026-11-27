"use client";

import React, { useState, useEffect } from "react";
import Header from "@/components/layout/Header";
import Badge from "@/components/common/Badge";
import { api } from "@/lib/api";
import { Product, PaginatedResponse } from "@/types";
import {
  Package,
  Search,
  Filter,
  ExternalLink,
  Loader2,
  ChevronLeft,
  ChevronRight,
  X,
  CheckSquare,
  Square,
  ArrowRightLeft
} from "lucide-react";

export default function ProductsPage() {
  const [data, setData] = useState<PaginatedResponse<Product> | null>(null);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [pricingFilter, setPricingFilter] = useState("");
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);

  // Comparison State
  const [comparisonIds, setComparisonIds] = useState<number[]>([]);
  const [comparisonProducts, setComparisonProducts] = useState<Product[]>([]);
  const [comparisonModalOpen, setComparisonModalOpen] = useState(false);
  const [comparingLoading, setComparingLoading] = useState(false);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const res = await api.getProducts({
          page,
          page_size: 20,
          search: search || undefined,
          pricing_model: pricingFilter || undefined,
        });
        setData(res);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    const timer = setTimeout(load, 200);
    return () => clearTimeout(timer);
  }, [page, search, pricingFilter]);

  const toggleComparison = (id: number) => {
    if (comparisonIds.includes(id)) {
      setComparisonIds(comparisonIds.filter((item) => item !== id));
    } else {
      if (comparisonIds.length >= 4) {
        alert("You can compare up to 4 products simultaneously.");
        return;
      }
      setComparisonIds([...comparisonIds, id]);
    }
  };

  const handleOpenComparison = async () => {
    if (comparisonIds.length === 0) return;
    setComparingLoading(true);
    setComparisonModalOpen(true);
    try {
      const res = await api.compareProducts(comparisonIds);
      setComparisonProducts(res.products);
    } catch (err) {
      console.error(err);
    } finally {
      setComparingLoading(false);
    }
  };

  const getPricingBadgeVariant = (model: string | null) => {
    switch (model) {
      case "FREE":
        return "emerald";
      case "FREEMIUM":
        return "blue";
      case "PAID":
        return "violet";
      case "ENTERPRISE":
        return "amber";
      default:
        return "slate";
    }
  };

  return (
    <div className="min-h-screen bg-[#0B1020] pb-12">
      <Header
        title="AI Products"
        subtitle="1,000 Verified Commercial & Open AI Products"
        breadcrumbs={[{ label: "FrontierAtlas" }, { label: "Products" }]}
      />

      <div className="px-3 sm:px-6 py-4 sm:py-6 space-y-4 sm:space-y-6 max-w-7xl mx-auto w-full">
        {/* Controls Bar */}
        <div className="p-3.5 sm:p-4 rounded-2xl bg-[#111A2E] border border-[#1E2D4A] flex flex-col lg:flex-row lg:items-center justify-between gap-3 sm:gap-4">
          <div className="relative flex-1 w-full lg:max-w-md">
            <Search className="absolute left-3 top-3 w-4 h-4 text-[#98A7BD]" />
            <input
              type="text"
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
              placeholder="Search product name, company, description..."
              className="w-full pl-9 pr-4 py-2 bg-[#17233A] border border-[#1E2D4A] rounded-xl text-xs text-[#F4F7FC] placeholder-[#98A7BD] focus:outline-none focus:border-[#36D6E7]"
            />
          </div>

          <div className="flex flex-col sm:flex-row flex-wrap items-stretch sm:items-center gap-2.5 sm:gap-3">
            {/* Pricing Model Filter */}
            <select
              value={pricingFilter}
              onChange={(e) => {
                setPricingFilter(e.target.value);
                setPage(1);
              }}
              className="w-full sm:w-auto px-3 py-2 bg-[#17233A] border border-[#1E2D4A] rounded-xl text-xs text-[#F4F7FC] focus:outline-none focus:border-[#36D6E7]"
            >
              <option value="">All Pricing Tiers</option>
              <option value="FREE">FREE</option>
              <option value="FREEMIUM">FREEMIUM</option>
              <option value="PAID">PAID</option>
              <option value="ENTERPRISE">ENTERPRISE</option>
            </select>

            {/* Compare Button */}
            {comparisonIds.length > 0 && (
              <button
                onClick={handleOpenComparison}
                className="w-full sm:w-auto px-3.5 py-2 rounded-xl bg-[#4F8CFF] hover:bg-[#3B7BE8] text-xs font-semibold text-white flex items-center justify-center gap-2 shadow-lg shadow-blue-500/20"
              >
                <ArrowRightLeft className="w-4 h-4" />
                Compare ({comparisonIds.length})
              </button>
            )}

            <div className="text-xs font-mono text-[#98A7BD] self-center sm:self-auto">
              {data ? `${data.total.toLocaleString()} products` : "Loading..."}
            </div>
          </div>
        </div>

        {/* Products Grid */}
        {loading ? (
          <div className="py-24 text-center">
            <Loader2 className="w-8 h-8 text-[#36D6E7] animate-spin mx-auto mb-2" />
            <span className="text-xs font-mono text-[#98A7BD]">Loading AI product directory...</span>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5 sm:gap-4">
            {data?.items.map((prod) => {
              const isSelected = comparisonIds.includes(prod.id);
              return (
                <div
                  key={prod.id}
                  onClick={() => setSelectedProduct(prod)}
                  className="p-5 rounded-2xl bg-[#111A2E] border border-[#1E2D4A] hover:border-[#36D6E7]/50 transition-all flex flex-col justify-between cursor-pointer group relative"
                >
                  <div>
                    {/* Header: Company & Checkbox */}
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-[11px] font-mono text-[#98A7BD] uppercase truncate max-w-[180px]">
                        {prod.startup_name}
                      </span>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          toggleComparison(prod.id);
                        }}
                        className="text-[#98A7BD] hover:text-[#4F8CFF] p-1"
                        title={isSelected ? "Remove from comparison" : "Add to comparison"}
                      >
                        {isSelected ? (
                          <CheckSquare className="w-4 h-4 text-[#4F8CFF]" />
                        ) : (
                          <Square className="w-4 h-4" />
                        )}
                      </button>
                    </div>

                    {/* Product Name */}
                    <h3 className="text-base font-bold text-white group-hover:text-[#36D6E7] transition-colors line-clamp-1">
                      {prod.product_name}
                    </h3>

                    {/* Description */}
                    <p className="text-xs text-[#98A7BD] mt-2 line-clamp-2 leading-relaxed">
                      {prod.description || `AI system listed by ${prod.startup_name} on ${prod.source_name}.`}
                    </p>
                  </div>

                  {/* Footer: Pricing & Source Link */}
                  <div className="pt-4 mt-4 border-t border-[#1E2D4A]/60 flex items-center justify-between">
                    <Badge variant={getPricingBadgeVariant(prod.pricing_model)}>
                      {prod.pricing_model || "TIER UNKNOWN"}
                    </Badge>
                    <a
                      href={prod.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      onClick={(e) => e.stopPropagation()}
                      className="text-xs text-[#4F8CFF] hover:underline flex items-center gap-1 font-mono"
                    >
                      Source <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Pagination */}
        {data && data.total_pages > 1 && (
          <div className="p-4 rounded-xl bg-[#111A2E] border border-[#1E2D4A] flex items-center justify-between text-xs">
            <span className="text-[#98A7BD]">
              Page <span className="text-white font-mono">{data.page}</span> of{" "}
              <span className="text-white font-mono">{data.total_pages}</span>
            </span>
            <div className="flex items-center space-x-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={data.page <= 1}
                className="p-1.5 rounded-lg bg-[#17233A] border border-[#1E2D4A] text-white disabled:opacity-30"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                onClick={() => setPage((p) => Math.min(data.total_pages, p + 1))}
                disabled={data.page >= data.total_pages}
                className="p-1.5 rounded-lg bg-[#17233A] border border-[#1E2D4A] text-white disabled:opacity-30"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {/* Product Comparison Modal */}
        {comparisonModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-black/80 backdrop-blur-md">
            <div className="w-full max-w-4xl rounded-2xl bg-[#0B1020] border border-[#1E2D4A] shadow-2xl p-4 sm:p-6 relative max-h-[92vh] flex flex-col">
              <div className="flex items-center justify-between pb-4 border-b border-[#1E2D4A]">
                <div className="flex items-center gap-2">
                  <ArrowRightLeft className="w-5 h-5 text-[#4F8CFF]" />
                  <h3 className="text-base font-bold text-white">Product Comparison Matrix</h3>
                </div>
                <button
                  onClick={() => setComparisonModalOpen(false)}
                  className="p-1.5 rounded-lg text-[#98A7BD] hover:text-white hover:bg-[#17233A]"
                  aria-label="Close Comparison"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {comparingLoading ? (
                <div className="py-20 text-center">
                  <Loader2 className="w-6 h-6 text-[#4F8CFF] animate-spin mx-auto mb-2" />
                  <span className="text-xs text-[#98A7BD]">Fetching comparison attributes...</span>
                </div>
              ) : (
                <div className="overflow-x-auto py-4 -mx-4 sm:mx-0 px-4 sm:px-0">
                  <table className="w-full text-left text-xs min-w-[500px]">
                    <thead>
                      <tr className="border-b border-[#1E2D4A]">
                        <th className="py-3 px-3 text-[#98A7BD] uppercase font-mono w-32">Attribute</th>
                        {comparisonProducts.map((cp) => (
                          <th key={cp.id} className="py-3 px-3 font-bold text-white text-sm">
                            {cp.product_name}
                          </th>
                        ))}
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#1E2D4A]/50">
                      <tr>
                        <td className="py-3 px-3 text-[#98A7BD] font-mono">Company / Creator</td>
                        {comparisonProducts.map((cp) => (
                          <td key={cp.id} className="py-3 px-3 font-semibold text-white">
                            {cp.startup_name}
                          </td>
                        ))}
                      </tr>
                      <tr>
                        <td className="py-3 px-3 text-[#98A7BD] font-mono">Pricing Tier</td>
                        {comparisonProducts.map((cp) => (
                          <td key={cp.id} className="py-3 px-3">
                            <Badge variant={getPricingBadgeVariant(cp.pricing_model)}>
                              {cp.pricing_model || "UNKNOWN"}
                            </Badge>
                          </td>
                        ))}
                      </tr>
                      <tr>
                        <td className="py-3 px-3 text-[#98A7BD] font-mono">Ingestion Source</td>
                        {comparisonProducts.map((cp) => (
                          <td key={cp.id} className="py-3 px-3 text-[#98A7BD]">
                            {cp.source_name}
                          </td>
                        ))}
                      </tr>
                      <tr>
                        <td className="py-3 px-3 text-[#98A7BD] font-mono">Description</td>
                        {comparisonProducts.map((cp) => (
                          <td key={cp.id} className="py-3 px-3 text-[#F4F7FC] leading-relaxed">
                            {cp.description || "N/A"}
                          </td>
                        ))}
                      </tr>
                      <tr>
                        <td className="py-3 px-3 text-[#98A7BD] font-mono">Verified Link</td>
                        {comparisonProducts.map((cp) => (
                          <td key={cp.id} className="py-3 px-3">
                            <a
                              href={cp.source_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-[#4F8CFF] hover:underline inline-flex items-center gap-1"
                            >
                              Source <ExternalLink className="w-3 h-3" />
                            </a>
                          </td>
                        ))}
                      </tr>
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Product Detail Modal */}
        {selectedProduct && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-black/80 backdrop-blur-sm">
            <div className="w-full max-w-xl rounded-2xl bg-[#0B1020] border border-[#1E2D4A] shadow-2xl p-4 sm:p-6 relative space-y-4 max-h-[92vh] overflow-y-auto">
              <button
                onClick={() => setSelectedProduct(null)}
                className="absolute top-3 right-3 sm:top-4 sm:right-4 p-1.5 rounded-lg text-[#98A7BD] hover:text-white hover:bg-[#17233A]"
                aria-label="Close Product Details"
              >
                <X className="w-5 h-5" />
              </button>

              <div className="flex items-center gap-3 pr-8">
                <div className="p-2.5 sm:p-3 rounded-xl bg-[#36D6E7]/15 border border-[#36D6E7]/30 text-[#36D6E7] flex-shrink-0">
                  <Package className="w-5 h-5 sm:w-6 sm:h-6" />
                </div>
                <div className="min-w-0">
                  <h3 className="text-base sm:text-lg font-bold text-white truncate">{selectedProduct.product_name}</h3>
                  <p className="text-xs text-[#98A7BD] truncate">Created by {selectedProduct.startup_name}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 py-3 border-y border-[#1E2D4A] text-xs">
                <div>
                  <span className="text-[#98A7BD] block mb-1">Pricing Model</span>
                  <Badge variant={getPricingBadgeVariant(selectedProduct.pricing_model)}>
                    {selectedProduct.pricing_model || "UNKNOWN"}
                  </Badge>
                </div>
                <div>
                  <span className="text-[#98A7BD] block mb-1">Source Directory</span>
                  <span className="font-semibold text-white">{selectedProduct.source_name}</span>
                </div>
                <div>
                  <span className="text-[#98A7BD] block mb-1">Fingerprint (SHA-256)</span>
                  <span className="font-mono text-[10px] text-[#98A7BD] break-all">{selectedProduct.fingerprint}</span>
                </div>
                <div>
                  <span className="text-[#98A7BD] block mb-1">Collection Date</span>
                  <span className="font-mono text-white">{new Date(selectedProduct.collected_at).toLocaleDateString()}</span>
                </div>
              </div>

              {selectedProduct.description && (
                <div>
                  <h4 className="text-xs font-semibold text-[#98A7BD] uppercase mb-1">Description</h4>
                  <p className="text-xs text-[#F4F7FC] leading-relaxed bg-[#111A2E] p-3 rounded-xl border border-[#1E2D4A]">
                    {selectedProduct.description}
                  </p>
                </div>
              )}

              <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-2.5 pt-2">
                <button
                  onClick={() => {
                    toggleComparison(selectedProduct.id);
                    setSelectedProduct(null);
                  }}
                  className="px-4 py-2 rounded-xl bg-[#17233A] hover:bg-[#1E2D4A] border border-[#1E2D4A] text-xs text-white text-center"
                >
                  {comparisonIds.includes(selectedProduct.id) ? "Remove from Compare" : "Add to Compare"}
                </button>
                <a
                  href={selectedProduct.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 rounded-xl bg-[#36D6E7] hover:bg-[#20BACB] text-xs font-semibold text-black flex items-center justify-center gap-1.5"
                >
                  Open Original Product <ExternalLink className="w-3.5 h-3.5" />
                </a>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
