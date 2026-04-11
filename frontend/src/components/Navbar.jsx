import { Search, Bell, User } from "lucide-react";

export default function Navbar() {
  return (
    <header className="
      h-16 px-6 flex items-center justify-between
      bg-slate-950/70 backdrop-blur-xl
      border-b border-slate-800
    ">
      
      {/* Left */}
      <div>
        <h2 className="text-lg font-semibold tracking-tight">
          <span className="text-slate-400">🧠</span>{" "}
          <span className="bg-gradient-to-r from-indigo-400 to-cyan-400 bg-clip-text text-transparent">
            Memora OS
          </span>
        </h2>
      </div>

      {/* Center - Search */}
      <div className="hidden md:flex items-center w-[400px] bg-slate-900/60 border border-slate-800 rounded-xl px-3 py-2">
        <Search size={16} className="text-slate-400 mr-2" />
        <input
          type="text"
          placeholder="Search memories..."
          className="bg-transparent outline-none text-sm w-full text-white placeholder-slate-500"
        />
      </div>

      {/* Right */}
      <div className="flex items-center gap-4">
        <Bell className="text-slate-400 hover:text-white cursor-pointer" />
        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-indigo-500 to-cyan-500 flex items-center justify-center">
          <User size={16} />
        </div>
      </div>
    </header>
  );
}