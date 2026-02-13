import { useEffect, useState } from "react";
import { fetchTimeline } from "../services/api";

export default function Timeline() {
  const [timeline, setTimeline] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadTimeline = async () => {
      try {
        const data = await fetchTimeline();
        setTimeline(data); // backend already sorted DESC
      } catch (err) {
        console.error("Failed to load timeline", err);
      } finally {
        setLoading(false);
      }
    };

    loadTimeline();
  }, []);

  const getStyles = (item) => {
    if (item.archived) {
      return {
        dot: "bg-gray-500",
        card: "bg-slate-800 border border-slate-700 opacity-40",
        badge: true
      };
    }

    if (item.state === "strong") {
      return {
        dot: "bg-indigo-500",
        card: "bg-slate-800 border border-indigo-500",
        badge: false
      };
    }

    if (item.state === "weak") {
      return {
        dot: "bg-indigo-400",
        card: "bg-slate-800 border border-slate-600 opacity-80",
        badge: false
      };
    }

    return {
      dot: "bg-slate-600",
      card: "bg-slate-800 border border-slate-700 opacity-60",
      badge: false
    };
  };

  return (
    <div className="min-h-full flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold">Memory Timeline</h1>
        <p className="text-slate-400 text-sm">
          Visual evolution of your memories over time
        </p>
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        {loading ? (
          <p className="text-slate-400 text-sm">Loading timeline...</p>
        ) : timeline.length === 0 ? (
          <p className="text-slate-400 text-sm">
            No memories available yet.
          </p>
        ) : (
          <div className="relative border-l border-slate-700 pl-6 space-y-6">
            {timeline.map((item, index) => {
              const styles = getStyles(item);

              return (
                <div key={index} className="relative">
                  {/* Dot */}
                  <div
                    className={`absolute -left-[9px] top-1 w-4 h-4 rounded-full ${styles.dot}`}
                  />

                  {/* Card */}
                  <div className={`rounded-lg p-4 ${styles.card}`}>
                    <div className="flex justify-between items-start">
                      <p className="text-slate-200 text-sm">
                        {item.content}
                      </p>

                      {styles.badge && (
                        <span className="text-xs bg-gray-700 text-gray-300 px-2 py-1 rounded">
                          Archived
                        </span>
                      )}
                    </div>

                    <p className="text-xs text-slate-500 mt-2">
                      {new Date(item.created_at).toLocaleString()}
                    </p>

                    <p className="text-xs text-slate-500 mt-1">
                      Strength: {item.strength}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
