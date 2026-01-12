function Navbar() {
  return (
    <div
      style={{
        height: "56px",
        background: "#020617",
        color: "white",
        display: "flex",
        alignItems: "center",
        padding: "0 20px",
        borderBottom: "1px solid #1e293b",
      }}
    >
      <strong>🧠 Memora OS</strong>
      <span style={{ marginLeft: "12px", opacity: 0.6 }}>
        Memory Operating System
      </span>
    </div>
  );
}

export default Navbar;
