function Navbar() {
  return (
    <header className="h-14 flex items-center px-6 bg-slate-950 border-b border-slate-800">
      <div className="flex items-center gap-3">
        <span className="text-lg">🧠</span>
        <div>
          <p className="text-sm font-semibold text-white">
            Memora OS
          </p>
          <p className="text-xs text-slate-400 leading-none">
            Memory Operating System
          </p>
        </div>
      </div>
    </header>
  );
}

export default Navbar;
