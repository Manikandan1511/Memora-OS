import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";

function App() {
  return (
    <BrowserRouter>
      <div style={{ height: "100vh", background: "#0f172a", color: "white" }}>
        <Navbar />

        <div style={{ display: "flex", height: "calc(100vh - 56px)" }}>
          <Sidebar />

          <main style={{ flex: 1, padding: "24px" }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
