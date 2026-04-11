import { Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";
import MemoryInbox from "./pages/MemoryInbox";
import AskBrain from "./pages/AskBrain";
import Timeline from "./pages/Timeline";
import BrainGraph from "./pages/BrainGraph";

export default function App() {
  return (
    <div className="
      h-screen w-screen text-white flex
      bg-gradient-to-br from-[#020617] via-[#020617] to-[#0f172a]
    ">
      
      {/* Sidebar */}
      <Sidebar />

      {/* Main Area */}
      <div className="flex flex-col flex-1 min-w-0 relative overflow-hidden">

        {/* Glow Effect */}
        <div className="
          absolute top-[-200px] right-[-200px]
          w-[500px] h-[500px]
          bg-indigo-500/10
          blur-3xl rounded-full
          pointer-events-none
        "></div>

        <Navbar />

        <main className="flex-1 min-h-0 overflow-y-auto p-8">
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/inbox" element={<MemoryInbox />} />
            <Route path="/ask" element={<AskBrain />} />
            <Route path="/timeline" element={<Timeline />} />
            <Route path="/graph" element={<BrainGraph />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}