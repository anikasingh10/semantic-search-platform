"use client";

import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState<string>("");
  const [results, setResults] = useState<string[]>([]);
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>("");

  const handleSearch = async () => {
    if (!query) return;

    try {
      const res = await fetch(`http://127.0.0.1:8000/search?query=${query}`);
      const data = await res.json();

      setResults(data.results);
    } catch (error) {
      console.error("Search failed:", error);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      setUploadStatus(data.message || "Upload successful");
    } catch (error) {
      console.error("Upload failed:", error);
      setUploadStatus("Upload failed");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center p-10">

      <h1 className="text-3xl font-bold mb-6">
        Semantic Search Platform
      </h1>

      {/* Upload Section */}

      <div className="mb-6 flex gap-3">
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => {
            if (e.target.files) {
              setFile(e.target.files[0]);
            }
          }}
          className="border p-2 rounded"
        />

        <button
          onClick={handleUpload}
          className="bg-blue-600 text-white px-4 py-2 rounded"
        >
          Upload PDF
        </button>
      </div>

      {uploadStatus && (
        <p className="text-sm text-gray-600 mb-6">{uploadStatus}</p>
      )}

      {/* Search Section */}

      <div className="flex gap-3">
        <input
          type="text"
          placeholder="Search anything..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="border p-2 rounded w-80"
        />

        <button
          onClick={handleSearch}
          className="bg-black text-white px-4 py-2 rounded"
        >
          Search
        </button>
      </div>


      <div className="mt-8 w-full max-w-xl">
        {results.map((item, index) => (
          <div
            key={index}
            className="border p-3 mb-2 rounded bg-gray-50"
          >
            {item}
          </div>
        ))}
      </div>

    </div>
  );
}