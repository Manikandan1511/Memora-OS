import { NavLink } from "react-router-dom";

const navItems = [
  { name: "Dashboard", path: "/dashboard" },
  { name: "Memory Inbox", path: "/memory-inbox" },
  { name: "Ask Brain", path: "/ask-brain" },
  { name: "Timeline", path: "/timeline" },
  { name: "Brain Graph", path: "/brain-graph" },
];

function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 p-6">
      <div className="mb-8">
        <h1 className="text-xl font-bold flex items-center gap-2">
          🧠 Memora OS
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Memory Operating System
        </p>
      </div>

      <nav className="space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `block rounded-md px-3 py-2 text-sm transition ${
                isActive
                  ? "bg-slate-800 text-white"
                  : "text-slate-400 hover:bg-slate-800 hover:text-white"
              }`
            }
          >
            {item.name}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;
