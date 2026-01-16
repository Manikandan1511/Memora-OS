import { useEffect, useState } from "react";
import { fetchTimeline } from "../services/api";

export default function Timeline() {
  const [timeline, setTimeline] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadTimeline = async () => {
      try {
        const data = await fetchTimeline();

        // 🔥 UX decision: show latest memory first
        const sorted = [...data].reverse();

        setTimeline(sorted);
      } catch (err) {
        console.error("Failed to load timeline", err);
      } finally {
        setLoading(false);
      }
    };

    loadTimeline();
  }, []);

  return (
    <div className="min-h-full flex flex-col gap-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-semibold">Memory Timeline</h1>
        <p className="text-slate-400 text-sm">
          Visual evolution of your memories over time
        </p>
      </div>

      {/* Content */}
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        {loading ? (
          <p className="text-slate-400 text-sm">Loading timeline...</p>
        ) : timeline.length === 0 ? (
          <p className="text-slate-400 text-sm">
            No memories available yet.
          </p>
        ) : (
          <div className="relative border-l border-slate-700 pl-6 space-y-6">
            {timeline.map((item, index) => (
              <div key={index} className="relative">
                {/* Dot */}
                <div className="absolute -left-[9px] top-1 w-4 h-4 bg-indigo-500 rounded-full" />

                {/* Card */}
                <div className="bg-slate-800 border border-slate-700 rounded-lg p-4">
                  <p className="text-slate-200 text-sm">
                    {item.content}
                  </p>

                  <p className="text-xs text-slate-500 mt-2">
                    {new Date(item.created_at).toLocaleString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}