function Timeline() {
  const mockTimeline = [
    {
      time: "Today • 10:30 AM",
      text: "Started building Memora OS frontend.",
    },
    {
      time: "Yesterday • 9:00 PM",
      text: "Finalized backend APIs with FastAPI and Neo4j.",
    },
    {
      time: "2 days ago • 6:15 PM",
      text: "Designed memory architecture and system flow.",
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-semibold">Timeline</h2>
        <p className="text-slate-400">
          Chronological view of your memories and events.
        </p>
      </div>

      {/* Timeline */}
      <div className="space-y-4">
        {mockTimeline.map((item, index) => (
          <div
            key={index}
            className="relative pl-6 border-l border-slate-700"
          >
            <div className="absolute left-[-6px] top-2 w-3 h-3 rounded-full bg-blue-500" />
            <p className="text-sm text-slate-400">{item.time}</p>
            <p className="text-slate-100 mt-1">{item.text}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Timeline;
