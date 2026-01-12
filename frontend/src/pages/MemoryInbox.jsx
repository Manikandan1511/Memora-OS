import { useState } from "react";

function MemoryInbox() {
  const [memory, setMemory] = useState("");
  const [memories, setMemories] = useState([]);

  const addMemory = () => {
    if (!memory.trim()) return;
    setMemories([{ text: memory, time: new Date() }, ...memories]);
    setMemory("");
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-semibold">Memory Inbox</h2>
        <p className="text-slate-400">
          Capture thoughts, notes, or events as memories.
        </p>
      </div>

      {/* Input Box */}
      <div className="bg-slate-950 border border-slate-800 rounded-lg p-4">
        <textarea
          value={memory}
          onChange={(e) => setMemory(e.target.value)}
          placeholder="Write a new memory..."
          className="w-full h-24 bg-slate-900 text-slate-100 p-3 rounded-md border border-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
        />
        <div className="flex justify-end mt-3">
          <button
            onClick={addMemory}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-md text-white text-sm"
          >
            Add Memory
          </button>
        </div>
      </div>

      {/* Memory List */}
      <div className="space-y-3">
        {memories.length === 0 && (
          <p className="text-slate-500 text-sm">
            No memories yet. Add your first one above.
          </p>
        )}

        {memories.map((m, index) => (
          <div
            key={index}
            className="bg-slate-950 border border-slate-800 rounded-md p-4"
          >
            <p className="text-slate-100">{m.text}</p>
            <p className="text-xs text-slate-500 mt-2">
              {m.time.toLocaleString()}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default MemoryInbox;
