import { useEffect, useState } from "react";
import { fetchTimeline, fetchGraph } from "../services/api";
import { motion } from "framer-motion";

export default function Dashboard() {
  const [stats, setStats] = useState({
    total: 0,
    active: 0,
    archived: 0,
    connections: 0,
    strong: 0,
    weak: 0,
    fading: 0,
  });

  useEffect(() => {
    const loadData = async () => {
      try {
        const timeline = await fetchTimeline();
        const graph = await fetchGraph();

        const total = timeline.length;
        const archived = timeline.filter((m) => m.archived).length;
        const active = total - archived;

        const strong = timeline.filter((m) => m.state === "strong").length;
        const weak = timeline.filter((m) => m.state === "weak").length;
        const fading = timeline.filter((m) => m.state === "fading").length;

        const connections = graph.edges.length;

        setStats({
          total,
          active,
          archived,
          connections,
          strong,
          weak,
          fading,
        });
      } catch (err) {
        console.error("Dashboard load failed", err);
      }
    };

    loadData();
  }, []);

  const Card = ({ title, value, color }) => {
    const colorMap = {
      indigo: "bg-indigo-500/70",
      green: "bg-green-500/70",
      gray: "bg-gray-500/70",
      purple: "bg-purple-500/70",
      yellow: "bg-yellow-500/70",
      blue: "bg-blue-500/70",
    };

    return (
      <motion.div
        whileHover={{ scale: 1.05 }}
        initial={{ opacity: 0, y: 25 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="
          relative rounded-xl p-5
          bg-slate-900/60 backdrop-blur-xl
          border border-slate-800
          transition-all duration-300

          hover:scale-[1.04]
          hover:border-indigo-500/40
          hover:shadow-[0_0_40px_rgba(99,102,241,0.35)]
          "
      >
        {/* Glow Top Line */}
        <div className={`absolute top-0 left-0 w-full h-[2px] ${colorMap[color]}`} />

        <p className="text-sm text-slate-400">{title}</p>

        <motion.h3
          key={value}
          initial={{ scale: 0.9 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.2 }}
          className="
          text-4xl font-extrabold mt-2
          tracking-tight
          bg-gradient-to-r from-white to-slate-300
          bg-clip-text text-transparent
          "
        >
          {value}
        </motion.h3>
      </motion.div>
    );
  };

  return (
    <div className="space-y-10">

      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <h1 className="
          text-3xl font-bold tracking-tight
          bg-gradient-to-r from-indigo-400 via-purple-400 to-cyan-400
          bg-clip-text text-transparent
        ">
          Memora Dashboard
        </h1>
        <p className="text-slate-400 mt-1">
          Cognitive system overview
        </p>
      </motion.div>

      {/* Top Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5">
        <Card title="Total Memories" value={stats.total} color="indigo" />
        <Card title="Active" value={stats.active} color="green" />
        <Card title="Archived" value={stats.archived} color="gray" />
        <Card title="Connections" value={stats.connections} color="purple" />
      </div>

      {/* State Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <Card title="Strong" value={stats.strong} color="green" />
        <Card title="Weak" value={stats.weak} color="yellow" />
        <Card title="Fading" value={stats.fading} color="blue" />
      </div>

      {/* System Status */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="
          bg-slate-900/60 backdrop-blur-xl
          border border-slate-800
          rounded-xl p-6
          shadow-lg
        "
      >
        <h3 className="text-lg font-semibold mb-2 text-indigo-400">
          System Status
        </h3>

        <p className="text-slate-300">
          Memora OS is running with{" "}
          <span className="text-green-400 font-semibold">
            {stats.active}
          </span>{" "}
          active memories and{" "}
          <span className="text-purple-400 font-semibold">
            {stats.connections}
          </span>{" "}
          knowledge connections.
        </p>
      </motion.div>

    </div>
  );
}