import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <div
      style={{
        width: "220px",
        background: "#020617",
        color: "white",
        borderRight: "1px solid #1e293b",
        padding: "20px",
      }}
    >
      <div style={{ marginBottom: "16px", fontWeight: "bold" }}>
        Modules
      </div>

      <nav style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        <Link to="/" style={linkStyle}>Dashboard</Link>
      </nav>
    </div>
  );
}

const linkStyle = {
  color: "#cbd5f5",
  textDecoration: "none",
};

export default Sidebar;
