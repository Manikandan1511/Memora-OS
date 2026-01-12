function BrainGraph() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-semibold">Brain Graph</h2>
        <p className="text-slate-400">
          Visual representation of how memories and knowledge evolve.
        </p>
      </div>

      {/* Placeholder Graph */}
      <div className="bg-slate-950 border border-slate-800 rounded-lg h-[400px] flex items-center justify-center">
        <p className="text-slate-500 text-sm">
          Knowledge graph visualization will appear here.
        </p>
      </div>

      {/* Explanation */}
      <div className="text-sm text-slate-400 max-w-xl">
        This graph will be powered by Neo4j and will show relationships between
        memories, concepts, and how they evolve over time.
      </div>
    </div>
  );
}

export default BrainGraph;
