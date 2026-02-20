<template>
  <div class="graph-wrapper">
    <div class="graph-container" ref="networkContainer"></div>
    <div class="graph-controls" v-if="network">
      <button @click="zoomIn" title="Zoom In">+</button>
      <button @click="zoomOut" title="Zoom Out">−</button>
      <button @click="fitGraph" title="Reset View">⛶</button>
    </div>
  </div>
</template>

<script>
import { Network } from "vis-network";
import "vis-network/styles/vis-network.css";

export default {
  props: {
    graphData: Object,
    suspiciousAccounts: Array,
    focusedNodes: Array // Optional: list of IDs to highlight/focus
  },
  data() {
    return { network: null };
  },
  mounted() { this.renderGraph(); },
  watch: {
    graphData: { deep: true, handler() { this.renderGraph(); } },
    focusedNodes: { deep: true, handler() { this.renderGraph(); } }
  },
  methods: {
    renderGraph() {
      if (!this.graphData || !this.graphData.nodes) return;
      if (this.network) this.network.destroy();

      const suspiciousIds = new Set(this.suspiciousAccounts?.map(a => a.account_id));
      const focusedIds = new Set(this.focusedNodes || []);

      const nodes = this.graphData.nodes.map(node => {
        const isSuspicious = suspiciousIds.has(node.id);
        const isFocused = focusedIds.size === 0 || focusedIds.has(node.id);

        return {
          id: node.id,
          label: isFocused ? node.id : "", // Only show IDs for focused nodes to reduce clutter
          shape: "icon",
          icon: {
            face: "'FontAwesome'",
            code: isSuspicious ? "\uf023" : "\uf007", // Lock for suspicious, User for normal
            size: isSuspicious ? 40 : 30,
            color: isSuspicious ? "#f87171" : "#60a5fa"
          },
          // Fallback to dot if fontawesome fails or to add glow
          shape: "dot",
          size: isSuspicious ? 18 : 12,
          color: isSuspicious
            ? {
                background: "#ef4444",
                border: "#7f1d1d",
                highlight: { background: "#f87171", border: "#ef4444" }
              }
            : {
                background: "#2563eb",
                border: "#1e3a8a",
                highlight: { background: "#3b82f6", border: "#2563eb" }
              },
          borderWidth: isSuspicious ? 3 : 1.5,
          opacity: isFocused ? 1 : 0.2, // Dim nodes not in focus
          font: { color: "#f0f6ff", size: 12, face: "Inter", strokeWidth: 2, strokeColor: "#020b18" },
          shadow: {
            enabled: isSuspicious,
            color: "rgba(239, 68, 68, 0.6)",
            size: 15,
            x: 0, y: 0
          }
        };
      });

      const edges = this.graphData.edges.map(edge => {
        const isFocused = focusedIds.size === 0 || (focusedIds.has(edge.source) && focusedIds.has(edge.target));
        return {
          from: edge.source,
          to: edge.target,
          arrows: "to",
          width: isFocused ? 2 : 0.5,
          color: {
            color: isFocused ? "rgba(59, 130, 246, 0.6)" : "rgba(59, 130, 246, 0.05)",
            highlight: "rgba(0, 212, 255, 0.9)",
            hover: "rgba(0, 212, 255, 1)"
          },
          smooth: { type: "curvedCW", roundness: 0.2 },
          opacity: isFocused ? 1 : 0.1
        };
      });

      const options = {
        physics: {
          enabled: true,
          stabilization: { iterations: 150 },
          barnesHut: {
            gravitationalConstant: -10000,
            centralGravity: 0.3,
            springLength: 150
          }
        },
        interaction: {
          zoomView: true,
          dragView: true,
          hover: true,
          tooltipDelay: 100
        },
        nodes: { shadow: true },
        edges: { shadow: false },
        background: "rgba(0,0,0,0)"
      };

      this.network = new Network(this.$refs.networkContainer, { nodes, edges }, options);

      this.network.once("stabilizationIterationsDone", () => {
        this.network.fit({ animation: { duration: 1000, easingFunction: "easeInOutQuad" } });
        this.network.setOptions({ physics: false });
      });
    },
    zoomIn() { this.network.moveTo({ scale: this.network.getScale() * 1.5 }); },
    zoomOut() { this.network.moveTo({ scale: this.network.getScale() / 1.5 }); },
    fitGraph() { this.network.fit({ animation: true }); }
  }
};
</script>

<style scoped>
.graph-wrapper {
  position: relative;
  width: 100%;
  height: 600px;
  border-radius: 16px;
  overflow: hidden;
  background: radial-gradient(circle at center, rgba(10, 25, 47, 0.8) 0%, rgba(2, 11, 24, 0.95) 100%);
  border: 1px solid rgba(59, 130, 246, 0.15);
  box-shadow: inset 0 0 40px rgba(0, 0, 0, 0.5);
}

.graph-container {
  width: 100%;
  height: 100%;
}

.graph-controls {
  position: absolute;
  bottom: 20px;
  right: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  z-index: 10;
}

.graph-controls button {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: rgba(15, 35, 70, 0.85);
  border: 1px solid rgba(59, 130, 246, 0.3);
  color: #f0f6ff;
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
  backdrop-filter: blur(4px);
}

.graph-controls button:hover {
  background: var(--blue-500);
  border-color: var(--blue-300);
  transform: scale(1.05);
}
</style>
