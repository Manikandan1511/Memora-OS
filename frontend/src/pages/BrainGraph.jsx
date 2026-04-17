import { useEffect, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
import { fetchGraph } from "../services/api";

export default function BrainGraph() {
  const [graphData, setGraphData] = useState({
    nodes: [],
    links: [],
  });

  const [hoverNode, setHoverNode] = useState(null);

  useEffect(() => {
    const loadGraph = async () => {
      try {
        const data = await fetchGraph();

        console.log("GRAPH DATA:", data);

        const nodes = data.nodes.map((node) => ({
          id: node.id,
          name: node.content,
          state: node.state || "weak",
        }));

        const links = data.edges.map((edge) => ({
          source: edge.source || edge.from, 
          target: edge.target || edge.to,
          label: edge.type,
        }));

        setGraphData({ nodes, links });

      } catch (err) {
        console.error("Graph load failed", err);
      }
    };

    loadGraph();
  }, []);

  return (
    <div className="space-y-6">

      {/* Header */}
      <div>
        <h2 className="text-2xl font-semibold">🧠 Brain Graph</h2>
        <p className="text-slate-400">
          Interactive memory connections
        </p>
      </div>

      {/* Graph */}
      <div className="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden">
        <ForceGraph2D
          graphData={graphData}
          nodeRelSize={8}
          backgroundColor="#020617"

          // 🔥 Hover interaction
          onNodeHover={(node) => {
            setHoverNode(node);
            document.body.style.cursor = node ? "pointer" : null;
          }}

          // 🔥 LINK COLOR 
          linkColor={(link) => {
            if (!hoverNode) return "#334155";

            return (
              link.source.id === hoverNode.id ||
              link.target.id === hoverNode.id
            )
              ? "#22c55e"
              : "#1e293b";
          }}

          // 🔥 LINK WIDTH
          linkWidth={(link) => {
            if (!hoverNode) return 1;

            return (
              link.source.id === hoverNode.id ||
              link.target.id === hoverNode.id
            )
              ? 2.5
              : 0.5;
          }}

          // 🔥 FLOW PARTICLES
          linkDirectionalParticles={2}
          linkDirectionalParticleWidth={2}
          linkDirectionalParticleSpeed={0.003}

          // 🧠 NODE DRAWING
          nodeCanvasObject={(node, ctx, globalScale) => {
            const label = node.name.slice(0, 20);
            const fontSize = 12 / globalScale;

            let color = "#6366f1";

            if (node.state === "strong") color = "#22c55e";
            else if (node.state === "weak") color = "#eab308";
            else if (node.state === "fading") color = "#3b82f6";
            else if (node.state === "archived") color = "#9ca3af";

            // 🧠 Highlight logic
            if (hoverNode) {
              const isConnected =
                node.id === hoverNode.id ||
                graphData.links.some(
                  (l) =>
                    (l.source.id === hoverNode.id && l.target.id === node.id) ||
                    (l.target.id === hoverNode.id && l.source.id === node.id)
                );

              if (!isConnected) {
                ctx.globalAlpha = 0.2; 
              }
            }

            // Draw node
            ctx.beginPath();
            ctx.arc(node.x, node.y, 6, 0, 2 * Math.PI);
            ctx.fillStyle = color;
            ctx.fill();

            // Glow effect
            ctx.shadowColor = color;
            ctx.shadowBlur = node.id === hoverNode?.id ? 20 : 8;

            // Label
            ctx.fillStyle = "white";
            ctx.font = `${fontSize}px Sans-Serif`;
            ctx.fillText(label, node.x + 8, node.y + 3);

            ctx.globalAlpha = 1;
            ctx.shadowBlur = 0;
          }}
        />
      </div>

      {/* Footer */}
      <p className="text-sm text-slate-500">
        Drag nodes, zoom, and explore how memories connect.
      </p>
    </div>
  );
}