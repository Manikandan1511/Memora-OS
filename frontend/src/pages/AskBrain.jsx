import { useState } from "react";

function AskBrain() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const searchBrain = () => {
    if (!query.trim()) return;

    // UI-only mock results (backend later)
    setResults([
      {
        text: "This is a related memory based on your query.",
        score: 0.91,
      },
      {
        text: "Another similar memory found in the system.",
        score: 0.84,
      },
    ]);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-semibold">Ask Brain</h2>
        <p className="text-slate-400">
          Search and recall memories using semantic understanding.
        </p>
      </div>

      {/* Search Box */}
      <div className="bg-slate-950 border border-slate-800 rounded-lg p-4">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask something from your memories..."
          className="w-full bg-slate-900 text-slate-100 p-3 rounded-md border border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <div className="flex justify-end mt-3">
          <button
            onClick={searchBrain}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-md text-white text-sm"
          >
            Search
          </button>
        </div>
      </div>

      {/* Results */}
      <div className="space-y-3">
        {results.length === 0 && (
          <p className="text-slate-500 text-sm">
            No results yet. Try asking something.
          </p>
        )}

        {results.map((r, index) => (
          <div
            key={index}
            className="bg-slate-950 border border-slate-800 rounded-md p-4"
          >
            <p className="text-slate-100">{r.text}</p>
            <p className="text-xs text-slate-500 mt-2">
              Similarity score: {r.score}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AskBrain;
