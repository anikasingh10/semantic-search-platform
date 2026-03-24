"use client";

import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState<string>("");
  const [results, setResults] = useState<string[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>("");

  const [isSearching, setIsSearching] = useState<boolean>(false);
  const [isUploading, setIsUploading] = useState<boolean>(false);

  const validatePDFFile = (file: File): string | null => {
    // Check if file exists
    if (!file) return "No file selected";

    // Check file size (limit to 50MB)
    const maxSize = 50 * 1024 * 1024; // 50MB in bytes
    if (file.size > maxSize) return "File size must be less than 50MB";

    // Check MIME type
    const allowedTypes = ["application/pdf"];
    if (!allowedTypes.includes(file.type)) {
      return "Please select a valid PDF file";
    }

    // Check file extension
    const fileName = file.name.toLowerCase();
    if (!fileName.endsWith(".pdf")) {
      return "File must have a .pdf extension";
    }

    return null; // Valid file
  };

  const handleSearch = async () => {
    if (!query) return;

    try {
      setIsSearching(true);

      const res = await fetch(`http://127.0.0.1:8000/search?query=${query}`);
      const data = await res.json();

      setResults(data.results);
    } catch (error) {
      console.error("Search failed:", error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    // Validate PDF file
    const validationError = validatePDFFile(file);
    if (validationError) {
      setUploadStatus(validationError);
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setIsUploading(true);
      setUploadStatus(""); // Clear any previous status

      const res = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        setUploadStatus(data.error || "Upload failed");
      } else {
        setUploadStatus(data.message || "Upload successful");
      }
    } catch (error) {
      console.error("Upload failed:", error);
      setUploadStatus("Upload failed");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-6 py-10 bg-[radial-gradient(circle_at_top,_rgba(99,102,241,0.25),_transparent_55%),radial-gradient(circle_at_bottom,_rgba(236,72,153,0.2),_transparent_55%),var(--background)]">
      <div className="w-full max-w-3xl rounded-3xl border border-white/20 bg-white/50 backdrop-blur-xl shadow-[0_24px_60px_rgba(0,0,0,0.18)] p-10">
        <header className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h1 className="text-3xl sm:text-4xl font-semibold tracking-tight text-slate-900">
              Semantic Search
            </h1>
            <p className="mt-1 text-sm text-slate-600">
              Upload your PDF and ask questions about its contents.
            </p>
          </div>
        </header>

        <div className="mt-4 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <label className="flex cursor-pointer items-center justify-between gap-3 rounded-full border border-white/30 bg-white/60 px-4 py-2 text-sm font-medium text-slate-700 shadow-sm transition hover:bg-white/80 hover:shadow-md">
            <span className="text-sm font-semibold">Choose PDF</span>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => {
                if (e.target.files) {
                  setFile(e.target.files[0]);
                }
              }}
              className="hidden"
            />
          </label>

          <button
            onClick={handleUpload}
            disabled={isUploading || !file}
            className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-indigo-500 via-fuchsia-500 to-rose-500 px-6 py-2 text-sm font-semibold text-white shadow-lg shadow-indigo-500/30 transition hover:shadow-indigo-500/50 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isUploading ? "Uploading…" : "Upload"}
          </button>
        </div>

        {uploadStatus && (
          <div className="mt-6 rounded-2xl border border-white/40 bg-white/60 px-4 py-3 text-sm text-slate-700 shadow-inner">
            {uploadStatus}
          </div>
        )}

        <section className="mt-8">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
            <input
              type="text"
              placeholder="Ask something about your document…"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full rounded-2xl border border-white/40 bg-white/60 px-4 py-3 text-sm text-slate-900 shadow-sm outline-none transition focus:border-indigo-400 focus:ring-2 focus:ring-indigo-400/40"
            />

            <button
              onClick={handleSearch}
              disabled={isSearching || !query}
              className="inline-flex h-12 items-center justify-center rounded-2xl bg-slate-900 px-6 text-sm font-semibold text-white shadow-lg shadow-slate-900/20 transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isSearching ? "Searching…" : "Search"}
            </button>
          </div>
        </section>

        <div className="mt-6 grid gap-4">
          {results.length === 0 ? (
            <div className="rounded-2xl border border-white/30 bg-white/40 p-6 text-sm text-slate-700 shadow-inner">
              Your results will appear here.
            </div>
          ) : (
            results.map((item, index) => (
              <div
                key={index}
                className="rounded-3xl border border-white/25 bg-white/50 p-6 text-sm text-slate-800 shadow-[0_10px_30px_rgba(15,23,42,0.12)]"
              >
                {item}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
