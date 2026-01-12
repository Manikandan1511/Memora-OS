import React from "react";

const stats = [
  {
    title: "Total Memories",
    value: 128,
    description: "Stored cognitive units",
    accent: "from-indigo-500 to-indigo-700",
  },
  {
    title: "Brain Queries",
    value: 42,
    description: "Questions processed",
    accent: "from-emerald-500 to-emerald-700",
  },
  {
    title: "Timeline Events",
    value: 86,
    description: "Memory evolution points",
    accent: "from-amber-500 to-amber-700",
  },
  {
    title: "Knowledge Links",
    value: 19,
    description: "Connected concepts",
    accent: "from-pink-500 to-pink-700",
  },
];

export default function Dashboard() {
  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-semibold text-slate-100">
          Dashboard
        </h1>
        <p className="text-slate-400 mt-1">
          Overview of your memory operating system
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6">
        {stats.map((item) => (
          <div
            key={item.title}
            className="relative rounded-xl bg-slate-900/60 border border-slate-800 p-6 
                       hover:border-slate-600 transition-all duration-300
                       hover:shadow-xl hover:shadow-black/40"
          >
            {/* Accent Bar */}
            <div
              className={`absolute top-0 left-0 h-1 w-full rounded-t-xl bg-gradient-to-r ${item.accent}`}
            />

            <div className="flex flex-col gap-2">
              <span className="text-sm text-slate-400">
                {item.title}
              </span>

              <span className="text-3xl font-bold text-slate-100">
                {item.value}
              </span>

              <span className="text-xs text-slate-500">
                {item.description}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* System Status */}
      <div className="mt-10 rounded-xl border border-slate-800 bg-slate-900/60 p-6">
        <h2 className="text-lg font-semibold text-slate-100 mb-2">
          System Status
        </h2>
        <p className="text-slate-400 text-sm leading-relaxed">
          Memora OS is running normally. Memory ingestion, semantic recall,
          and knowledge evolution modules are active and healthy.
        </p>
      </div>
    </div>
  );
}
