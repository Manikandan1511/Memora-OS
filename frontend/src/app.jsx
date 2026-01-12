import { Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/Sidebar";

import Dashboard from "./pages/Dashboard";
import MemoryInbox from "./pages/MemoryInbox";
import AskBrain from "./pages/AskBrain";
import Timeline from "./pages/Timeline";
import BrainGraph from "./pages/BrainGraph";

function App() {
  return (
    <div className="flex h-screen w-screen bg-slate-950 text-slate-100">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-6">
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/memory-inbox" element={<MemoryInbox />} />
          <Route path="/ask-brain" element={<AskBrain />} />
          <Route path="/timeline" element={<Timeline />} />
          <Route path="/brain-graph" element={<BrainGraph />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
