import { NavLink } from "react-router-dom";
import {
  LayoutDashboard,
  Inbox,
  Brain,
  Clock,
  Network,
} from "lucide-react";

const links = [
  { name: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
  { name: "Memory Inbox", path: "/inbox", icon: Inbox },
  { name: "Ask Brain", path: "/ask", icon: Brain },
  { name: "Timeline", path: "/timeline", icon: Clock },
  { name: "Brain Graph", path: "/graph", icon: Network },
];

export default function Sidebar() {
  return (
    <aside className="w-64 h-full 
      bg-gradient-to-b from-slate-950 via-slate-900 to-black
      border-r border-slate-800 p-6 flex flex-col">

      {/* Logo */}
      <div className="mb-10">
        <h1 className="text-2xl font-bold tracking-tight flex items-center gap-2">
          🧠 <span className="bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">
            Memora OS
          </span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Memory Operating System
        </p>
      </div>

      {/* Navigation */}
      <nav className="space-y-2 flex-1">
        {links.map((link) => {
          const Icon = link.icon;

          return (
            <NavLink
              key={link.path}
              to={link.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200
                ${
                  isActive
                    ? "bg-gradient-to-r from-indigo-500/20 to-cyan-500/20 text-white shadow-lg border border-indigo-500/20"
                    : "text-slate-400 hover:text-white hover:bg-slate-800/60"
                }`
              }
            >
              <Icon size={18} />
              {link.name}
            </NavLink>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="pt-6 border-t border-slate-800">
        <p className="text-xs text-slate-500">
          Memora OS v2.0
        </p>
      </div>
    </aside>
  );
}