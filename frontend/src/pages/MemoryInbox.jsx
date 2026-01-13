import { useState } from "react";
import { addMemory } from "../services/memoryService";

export default function MemoryInbox() {
  const [content, setContent] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAddMemory = async () => {
    if (!content.trim()) {
      setStatus("⚠️ Please enter some content");
      return;
    }

    try {
      setLoading(true);
      setStatus("");

      await addMemory({
        content: content,
        source: "user", // MUST match backend schema
      });

      setStatus("✅ Memory added successfully");
      setContent("");
    } catch (error) {
      console.error("Add memory failed:", error);
      setStatus("❌ Failed to add memory");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-full flex flex-col gap-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-semibold">Memory Inbox</h1>
        <p className="text-slate-400">
          Store thoughts, notes, and events into Memora OS.
        </p>
      </div>

      {/* Input Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col gap-4">
        <textarea
          className="w-full h-32 resize-none rounded-lg bg-slate-950 border border-slate-700 p-4 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          placeholder="Write a new memory..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />

        <div className="flex items-center justify-between">
          <span className="text-sm text-slate-400">{status}</span>

          <button
            onClick={handleAddMemory}
            disabled={loading}
            className="px-5 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-sm font-medium transition disabled:opacity-50"
          >
            {loading ? "Saving..." : "Add Memory"}
          </button>
        </div>
      </div>

      {/* Info Box */}
      <div className="bg-slate-900/50 border border-slate-800 rounded-xl p-4 text-sm text-slate-400">
        <strong className="text-slate-300">Tip:</strong> Memories saved here are
        embedded, indexed, and linked to your knowledge graph automatically.
      </div>
    </div>
  );
}
