"use client";

import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState<string>("");
  const [results, setResults] = useState<string[]>([]);

  const handleSearch = async () => {
    if (!query) return;

    const res = await fetch(`http://localhost:8000/search?query=${query}`);
    const data = await res.json();

    setResults(data.results);
  };

  return (
    <div className="min-h-screen flex flex-col items-center p-10">
      <h1 className="text-3xl font-bold mb-6">
        Semantic Search Platform
      </h1>

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
          <div key={index} className="border p-3 mb-2 rounded">
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}