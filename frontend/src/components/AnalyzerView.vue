<template>
  <div class="analyzer-root">

    <!-- ══════════════════ MAIN CONTENT ══════════════════ -->
    <div class="analyzer" :class="{ 'with-sidebar': data }">

      <!-- Back button -->
      <button class="back-btn" @click="$emit('back')">← Back to Home</button>

      <!-- Header -->
      <div class="analyzer-header">
        <div class="nav-logo">
          <span class="logo-icon">⬡</span>
          <span class="logo-text">FinTrace <span class="logo-ai">AI</span></span>
        </div>
        <div class="analyzer-badge">
          <span class="badge-dot"></span>
          Analyzer Engine Active
        </div>
      </div>

      <!-- Upload Zone -->
      <div class="upload-section" v-if="!data">
        <div
          class="dropzone"
          :class="{ dragging: isDragging, loading: isLoading }"
          @dragover.prevent="isDragging = true"
          @dragleave="isDragging = false"
          @drop.prevent="handleDrop"
          @click="triggerFileInput"
        >
          <input ref="fileInput" type="file" accept=".csv" style="display:none" @change="handleFile" />

          <div v-if="!isLoading" class="dz-content">
            <div class="dz-icon">📂</div>
            <h2>Upload Transaction CSV</h2>
            <p>Drag &amp; drop your file here or click to browse</p>
            <span class="dz-hint">.csv files only — up to 50MB</span>
            <div class="dz-actions" v-if="selectedFile">
              <div class="file-chip">
                <span>📄</span>
                <span>{{ selectedFile.name }}</span>
              </div>
              <button class="btn-primary" @click.stop="handleUpload">
                <span class="btn-glow"></span>
                🔍 Run Analysis
              </button>
            </div>
          </div>

          <div v-else class="dz-loading">
            <div class="loader-ring"></div>
            <p>Analyzing transaction graph…</p>
            <span class="load-sub">Building network • Running ML models • Scoring risks</span>
          </div>
        </div>

        <div v-if="error" class="error-banner">
          ⚠️ {{ error }}
        </div>
      </div>

      <!-- RESULTS -->
      <div v-if="data" class="results">

        <div class="results-header">
          <h2>Analysis Complete <span class="check">✓</span></h2>
          <div class="results-actions">
            <button class="btn-ghost-sm" @click="reset">↩ New Analysis</button>
            <button class="btn-primary-sm" @click="downloadJSON">⬇ Download JSON Report</button>
          </div>
        </div>

        <div class="summary-grid">
          <div class="summary-card" v-for="s in summaryCards" :key="s.label" :class="s.variant">
            <div class="sc-icon">{{ s.icon }}</div>
            <div class="sc-val">{{ s.value }}</div>
            <div class="sc-label">{{ s.label }}</div>
          </div>
        </div>

        <!-- 1. Network Visualization -->
        <div class="panel main-graph-panel">
          <div class="panel-header">
            <span class="panel-icon">🕸️</span>
            <h3>Network Visualization</h3>
            <div class="legend">
              <span class="leg-item"><span class="leg-dot red"></span> Suspicious</span>
              <span class="leg-item"><span class="leg-dot blue"></span> Clean</span>
            </div>
          </div>
          <GraphView 
            :graphData="data.graph" 
            :suspiciousAccounts="data.suspicious_accounts" 
            :focusedNodes="focusedNodes"
          />
        </div>

        <!-- 2. Intelligence Dashboard (Charts) -->
        <div class="intel-dashboard">
          <div class="panel chart-panel">
            <div class="panel-header">
              <span class="panel-icon">📊</span>
              <h3>Risk Distribution</h3>
            </div>
            <div class="chart-container">
              <BarChart :data="riskDistributionData" :options="chartOptions" />
            </div>
          </div>
          <div class="panel chart-panel">
            <div class="panel-header">
              <span class="panel-icon">🍩</span>
              <h3>Threat Breakdown</h3>
            </div>
            <div class="chart-container">
              <DoughnutChart :data="threatBreakdownData" :options="chartOptions" />
            </div>
          </div>
        </div>

        <!-- 3. Fraud Ring Series (Quick Focus) -->
        <div class="series-section" v-if="data.fraud_rings && data.fraud_rings.length">
          <div class="panel-header">
            <span class="panel-icon">📉</span>
            <h3>Fraud Ring Series</h3>
            <p class="panel-hint">Select a case to focus the transaction graph</p>
          </div>
          <div class="ring-carousel">
            <div 
              class="ring-card-series" 
              v-for="ring in data.fraud_rings" 
              :key="ring.ring_id"
              :class="{ active: selectedRingId === ring.ring_id }"
              @click="focusRing(ring)"
            >
              <div class="rcs-header">
                <span class="rcs-badge">{{ ring.pattern_type }}</span>
                <span class="rcs-risk" :class="riskLevel(ring.risk_score)">{{ (ring.risk_score * 100).toFixed(0) }}% Risk</span>
              </div>
              <div class="rcs-title">Case {{ ring.ring_id }}</div>
              <div class="rcs-meta">
                <span>👥 {{ ring.member_accounts.length }} Members</span>
                <span>🔗 {{ getRingTxCount(ring) }} Txns</span>
              </div>
              <div class="rcs-footer">
                <button class="btn-focus">Focus Cluster</button>
              </div>
            </div>
          </div>
        </div>

        <!-- 4. Flagged Accounts Intelligence (AI Explanations) -->
        <div class="panel" v-if="data.suspicious_accounts && data.suspicious_accounts.length">
          <div class="panel-header">
            <span class="panel-icon">🚨</span>
            <h3>Flagged Accounts Intelligence</h3>
            <span class="count-badge red">{{ data.suspicious_accounts.length }} flagged</span>
          </div>
          <div class="flagged-list">
            <div class="flagged-row" v-for="acc in data.suspicious_accounts" :key="acc.account_id">
              <div class="fr-main">
                <div class="fr-account">
                  <span class="mule-icon">👤</span>
                  <span class="mule-id">{{ acc.account_id }}</span>
                </div>
                <div class="fr-explanation">
                  {{ getAccountExplanation(acc.account_id) }}
                </div>
                <div class="fr-patterns">
                  <span v-for="p in acc.detected_patterns" :key="p" class="pattern-tag">{{ p }}</span>
                </div>
              </div>
              <div class="fr-score-box" :class="riskLevel(acc.suspicion_score / 100)">
                <div class="fr-score-val">{{ acc.suspicion_score.toFixed(0) }}</div>
                <div class="fr-score-label">Risk Score</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 5. Detected Fraud Rings Table -->
        <div class="panel" v-if="data.fraud_rings && data.fraud_rings.length">
          <div class="panel-header">
            <span class="panel-icon">🔴</span>
            <h3>Detailed Fraud Rings</h3>
            <span class="count-badge">{{ data.fraud_rings.length }} rings</span>
          </div>
          <div class="table-wrap">
            <table class="pro-table">
              <thead>
                <tr>
                  <th>Ring ID</th>
                  <th>Pattern Type</th>
                  <th>Members</th>
                  <th>Risk Score</th>
                  <th>Account IDs</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="ring in data.fraud_rings" :key="ring.ring_id">
                  <td><code class="ring-id">{{ ring.ring_id }}</code></td>
                  <td><span class="pattern-badge">{{ ring.pattern_type }}</span></td>
                  <td><span class="count-tag">{{ ring.member_accounts.length }}</span></td>
                  <td>
                    <div class="risk-bar">
                      <div class="risk-track">
                        <div class="risk-fill" :class="riskLevel(ring.risk_score)" :style="{ width: (ring.risk_score * 100) + '%' }"></div>
                      </div>
                      <span class="risk-num">{{ (ring.risk_score * 100).toFixed(0) }}%</span>
                    </div>
                  </td>
                  <td>
                    <div class="account-tags">
                      <span v-for="acc in ring.member_accounts.slice(0,4)" :key="acc" class="acc-tag">{{ acc }}</span>
                      <span v-if="ring.member_accounts.length > 4" class="acc-more">+{{ ring.member_accounts.length - 4 }}</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Final Actions -->
        <div class="final-actions">
           <button class="btn-primary" @click="downloadJSON" style="padding: 16px 40px; font-size: 18px;">
             <span class="btn-glow"></span>
             ⬇ Download Full JSON Report
           </button>
           <p class="final-hint">The report contains all suspicious accounts, fraud rings, and summary data in the specified JSON format.</p>
        </div>

      </div>
    </div>

    <!-- ══════════════════ AI SUMMARY SIDEBAR ══════════════════ -->
    <aside class="ai-sidebar" v-if="data">
      <div class="sidebar-header">
        <div class="sidebar-title-row">
          <span class="ai-icon">✦</span>
          <span class="sidebar-title">AI Summary</span>
        </div>
      </div>

      <!-- Loading state -->
      <div class="ai-loading" v-if="aiLoading">
        <div class="ai-loader">
          <span></span><span></span><span></span>
        </div>
        <p>Generating summary…</p>
      </div>

      <!-- Error state -->
      <div class="ai-error" v-else-if="aiError">
        <span class="ai-error-icon">⚠️</span>
        <p>{{ aiError }}</p>
        <button class="retry-btn" @click="generateSummary">↩ Retry</button>
      </div>

      <!-- Summary content -->
      <div class="ai-content" v-else-if="aiSummary">

        <!-- Verdict banner -->
        <div class="verdict-banner" :class="verdictClass">
          <span class="verdict-icon">{{ verdictIcon }}</span>
          <div>
            <div class="verdict-label">Overall Verdict</div>
            <div class="verdict-text">{{ verdictText }}</div>
          </div>
        </div>

        <!-- Intelligence Points -->
        <div class="summary-points">
          <div
            class="summary-point"
            v-for="(point, i) in parsedPoints"
            :key="i"
          >
            <span class="pt-dot"></span>
            {{ point }}
          </div>
        </div>

        <!-- Quick numbers -->
        <div class="quick-stats">
          <div class="qs-item">
            <span class="qs-val">{{ data.summary?.total_accounts_analyzed ?? '—' }}</span>
            <span class="qs-label">Accounts</span>
          </div>
          <div class="qs-divider"></div>
          <div class="qs-item">
            <span class="qs-val qs-danger">{{ data.summary?.fraud_rings_detected ?? '—' }}</span>
            <span class="qs-label">Fraud Rings</span>
          </div>
          <div class="qs-divider"></div>
          <div class="qs-item">
            <span class="qs-val qs-warn">{{ data.summary?.suspicious_accounts_flagged ?? '—' }}</span>
            <span class="qs-label">Suspicious</span>
          </div>
        </div>

        <button class="copy-btn" @click="copySummary">
          {{ copied ? '✓ Copied!' : '⎘ Copy Summary' }}
        </button>

        <!-- ════════ AI CHATBOT ════════ -->
        <div class="ai-chat-container">
          <div class="chat-header">
            <span class="chat-status-dot"></span>
            <h4>AML Intelligence Chat</h4>
          </div>
          
          <div class="chat-messages" ref="chatBox">
            <div class="chat-msg ai-msg">
              <span class="msg-bot-icon">🤖</span>
              <p>Study analysis complete. You can ask me chained questions about specific clusters, risk scores, or laundering patterns found in this dataset.</p>
            </div>
            
            <div 
              v-for="(msg, i) in chatMessages" 
              :key="i"
              class="chat-msg"
              :class="msg.role === 'user' ? 'user-msg' : 'ai-msg'"
            >
              <span v-if="msg.role === 'assistant'" class="msg-bot-icon">🤖</span>
              <p>{{ msg.content }}</p>
            </div>

            <div v-if="isChatLoading" class="chat-msg ai-msg loading">
              <div class="typing-dots"><span></span><span></span><span></span></div>
            </div>
          </div>

          <div class="chat-input-row">
            <input 
              type="text" 
              v-model="userInput" 
              placeholder="Ask about this study..." 
              @keyup.enter="sendChat"
              :disabled="isChatLoading"
            />
            <button @click="sendChat" :disabled="!userInput.trim() || isChatLoading">
              <span v-if="!isChatLoading">Send</span>
              <span v-else>...</span>
            </button>
          </div>
        </div>
      </div>
    </aside>

  </div>
</template>

<script>
import { analyzeCSV } from "../api";
import GraphView from "./GraphView.vue";
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js';
import { Bar, Doughnut } from 'vue-chartjs';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);

const BACKEND_URL = "https://fintrace-ai.onrender.com";

async function callBackendSummarize(payload) {
  const res = await fetch(`${BACKEND_URL}/summarize`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Backend error: ${res.status}`);
  }
  const json = await res.json();
  return json.summary;
}

async function callBackendChat(messages, context) {
  const res = await fetch(`${BACKEND_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages, context })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Chat error: ${res.status}`);
  }
  return await res.json();
}

export default {
  components: { 
    GraphView, 
    BarChart: Bar, 
    DoughnutChart: Doughnut 
  },
  emits: ["back"],

  data() {
    return {
      selectedFile: null,
      data: null,
      isLoading: false,
      isDragging: false,
      error: null,
      aiSummary: "",
      aiLoading: false,
      aiError: null,
      copied: false,
      selectedRingId: null,
      focusedNodes: [],
      // Chat
      chatMessages: [],
      userInput: "",
      isChatLoading: false
    };
  },

  computed: {
    summaryCards() {
      if (!this.data) return [];
      return [
        { icon: "📊", label: "Accounts Analyzed",    value: this.data.summary?.total_accounts_analyzed ?? "—",        variant: "" },
        { icon: "🔴", label: "Fraud Rings Detected", value: this.data.summary?.fraud_rings_detected ?? "—",           variant: "danger" },
        { icon: "⚠️", label: "Suspicious Accounts",  value: this.data.summary?.suspicious_accounts_flagged ?? "—",    variant: "warning" },
        { icon: "⚡", label: "Processing Time",       value: (this.data.summary?.processing_time_seconds ?? "—") + "s", variant: "success" }
      ];
    },

    verdictClass() {
      const rings = this.data?.summary?.fraud_rings_detected ?? 0;
      if (rings === 0) return "clean";
      if (rings <= 2)  return "medium";
      return "critical";
    },
    verdictIcon() {
      return { clean: "✅", medium: "⚠️", critical: "🚨" }[this.verdictClass];
    },
    verdictText() {
      return {
        clean:    "No significant fraud detected",
        medium:   "Low-to-medium risk activity found",
        critical: "High-risk fraud rings detected"
      }[this.verdictClass];
    },

    parsedPoints() {
      if (!this.aiSummary) return [];
      return this.aiSummary
        .split("\n")
        .map(l => l.trim())
        .filter(l => l.startsWith("-") || l.startsWith("•") || /^\d+\./.test(l))
        .map(l => l.replace(/^[-•\d.]+\s*/, "").replace(/\*\*/g, ""));
    },

    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            labels: { color: '#94a3b8', font: { size: 10 } }
          }
        },
        scales: {
          y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
          x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
        }
      };
    },

    riskDistributionData() {
      if (!this.data?.suspicious_accounts) return { labels: [], datasets: [] };
      const buckets = { '0-20': 0, '21-40': 0, '41-60': 0, '61-80': 0, '81-100': 0 };
      this.data.suspicious_accounts.forEach(a => {
        const s = a.suspicion_score;
        if (s <= 20) buckets['0-20']++;
        else if (s <= 40) buckets['21-40']++;
        else if (s <= 60) buckets['41-60']++;
        else if (s <= 80) buckets['61-80']++;
        else buckets['81-100']++;
      });
      return {
        labels: Object.keys(buckets),
        datasets: [{
          label: 'Accounts',
          data: Object.values(buckets),
          backgroundColor: ['#3b82f677', '#3b82f699', '#f59e0b99', '#ef444499', '#ef4444cc'],
          borderColor: '#3b82f6',
          borderWidth: 1
        }]
      };
    },

    threatBreakdownData() {
      if (!this.data?.fraud_rings) return { labels: [], datasets: [] };
      const counts = {};
      this.data.fraud_rings.forEach(r => {
        const t = r.pattern_type || 'unknown';
        counts[t] = (counts[t] || 0) + 1;
      });
      return {
        labels: Object.keys(counts),
        datasets: [{
          data: Object.values(counts),
          backgroundColor: ['#6366f1', '#f43f5e', '#10b981', '#f59e0b', '#06b6d4'],
          borderWidth: 0
        }]
      };
    }
  },

  methods: {
    triggerFileInput() {
      if (!this.isLoading) this.$refs.fileInput.click();
    },
    handleFile(e) {
      this.selectedFile = e.target.files[0];
      this.error = null;
    },
    handleDrop(e) {
      this.isDragging = false;
      const f = e.dataTransfer.files[0];
      if (f && f.name.endsWith(".csv")) { this.selectedFile = f; this.error = null; }
      else this.error = "Please upload a valid .csv file.";
    },

    async handleUpload() {
      if (!this.selectedFile) return;
      this.isLoading = true;
      this.error = null;
      try {
        this.data = await analyzeCSV(this.selectedFile);
        await this.generateSummary();
      } catch (e) {
        this.error = "Analysis failed. Make sure the backend is running and the CSV is valid.";
      } finally {
        this.isLoading = false;
      }
    },

    async generateSummary() {
      if (!this.data) return;
      this.aiLoading = true;
      this.aiError = null;
      this.aiSummary = "";

      try {
        const s = this.data.summary ?? {};
        const rings_detail = (this.data.fraud_rings ?? [])
          .map(r => `Ring ${r.ring_id}: ${r.pattern_type}, ${r.member_accounts?.length ?? 0} members, risk ${((r.risk_score ?? 0) * 100).toFixed(0)}%`)
          .join("; ");
        
        const reasons = (this.data.suspicious_accounts ?? [])
          .slice(0, 5)
          .map(a => `${a.account_id}: ${a.detected_patterns.join(',')}`)
          .join("; ");

        this.aiSummary = await callBackendSummarize({
          total_accounts:      s.total_accounts_analyzed      ?? 0,
          fraud_rings:         s.fraud_rings_detected         ?? 0,
          suspicious_accounts: s.suspicious_accounts_flagged  ?? 0,
          avg_risk_score:      s.avg_risk_score               ?? 0,
          rings_detail,
          top_flagged_reasons: reasons,
          graph_hubs:          (this.data.suspicious_accounts ?? []).slice(0,3).map(a => a.account_id).join(',')
        });
      } catch (err) {
        this.aiError = `Could not generate summary: ${err.message}`;
        console.error("Summary error:", err);
      } finally {
        this.aiLoading = false;
      }
    },

    getAccountExplanation(accountId) {
      if (!this.data?.explanations) return "Analysis in progress...";
      const e = this.data.explanations.find(ex => ex.account_id === accountId);
      return e ? e.text : "No specific anomaly explanation provided.";
    },

    focusRing(ring) {
      if (this.selectedRingId === ring.ring_id) {
        this.selectedRingId = null;
        this.focusedNodes = [];
      } else {
        this.selectedRingId = ring.ring_id;
        this.focusedNodes = [...ring.member_accounts];
      }
    },

    getRingTxCount(ring) {
      if (!this.data.graph?.edges) return 0;
      const members = new Set(ring.member_accounts);
      return this.data.graph.edges.filter(e => members.has(e.source) && members.has(e.target)).length;
    },

    downloadJSON() {
      const exportData = {
        suspicious_accounts: (this.data.suspicious_accounts || []).map(acc => ({
          account_id: acc.account_id,
          suspicion_score: acc.suspicion_score,
          detected_patterns: acc.detected_patterns,
          ring_id: acc.ring_id
        })),
        fraud_rings: (this.data.fraud_rings || []).map(ring => ({
          ring_id: ring.ring_id,
          member_accounts: ring.member_accounts,
          pattern_type: ring.pattern_type,
          risk_score: ring.risk_score
        })),
        summary: this.data.summary
      };

      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: "application/json" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "fintrace_report.json";
      link.click();
    },

    reset() {
      this.data = null;
      this.selectedFile = null;
      this.error = null;
      this.aiSummary = "";
      this.aiError = null;
      this.selectedRingId = null;
      this.focusedNodes = [];
    },

    riskLevel(score) {
      if (score >= 0.7) return "high";
      if (score >= 0.4) return "med";
      return "low";
    },

    async copySummary() {
      try {
        await navigator.clipboard.writeText(this.aiSummary);
        this.copied = true;
        setTimeout(() => (this.copied = false), 2500);
      } catch {}
    },

    async sendChat() {
      if (!this.userInput.trim() || this.isChatLoading) return;
      
      const text = this.userInput.trim();
      this.userInput = "";
      this.chatMessages.push({ role: "user", content: text });
      
      this.$nextTick(() => { this.scrollToBottom(); });
      
      this.isChatLoading = true;
      try {
        const s = this.data.summary ?? {};
        const context = {
          total_accounts: s.total_accounts_analyzed,
          fraud_rings: s.fraud_rings_detected,
          avg_risk_score: s.avg_risk_score,
          top_flagged_reasons: (this.data.suspicious_accounts ?? []).slice(0,5).map(a => a.account_id).join(','),
          graph_hubs: (this.data.suspicious_accounts ?? []).slice(0,3).map(a => a.account_id).join(',')
        };
        
        const res = await callBackendChat(this.chatMessages, context);
        this.chatMessages.push({ role: "assistant", content: res.content });
      } catch (err) {
        this.chatMessages.push({ role: "assistant", content: "Sorry, I had trouble processing that request: " + err.message });
      } finally {
        this.isChatLoading = false;
        this.$nextTick(() => { this.scrollToBottom(); });
      }
    },

    scrollToBottom() {
      const box = this.$refs.chatBox;
      if (box) box.scrollTop = box.scrollHeight;
    }
  }
};
</script>

<style scoped>
/* ── Root layout ── */
.analyzer-root {
  display: flex;
  align-items: flex-start;
  gap: 0;
  min-height: 100vh;
}

.analyzer {
  flex: 1;
  min-width: 0;
  padding: 32px;
  max-width: 1200px;
  margin: 0 auto;
  animation: fadeIn 0.4s ease;
  transition: max-width 0.4s ease;
}
.analyzer.with-sidebar {
  max-width: 100%;
  margin: 0;
}

/* ── Back / Header ── */
.back-btn {
  background: transparent;
  border: 1px solid rgba(59,130,246,0.3);
  color: var(--text-secondary);
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 13px;
  cursor: pointer;
  margin-bottom: 28px;
  transition: all 0.2s;
  font-family: var(--font-primary);
}
.back-btn:hover { border-color: var(--blue-300); color: var(--text-primary); }

.analyzer-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 40px; flex-wrap: wrap; gap: 12px;
}
.nav-logo { display: flex; align-items: center; gap: 10px; font-family: var(--font-display); font-size: 22px; font-weight: 700; }
.logo-icon { font-size: 22px; color: var(--accent-cyan); filter: drop-shadow(0 0 8px rgba(0,212,255,0.6)); }
.logo-ai { background: var(--gradient-accent); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.analyzer-badge {
  display: flex; align-items: center; gap: 8px;
  background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3);
  color: #6ee7b7; font-size: 12px; font-weight: 600;
  padding: 6px 14px; border-radius: 99px; letter-spacing: 0.5px;
}
.badge-dot { width: 7px; height: 7px; background: var(--accent-success); border-radius: 50%; box-shadow: 0 0 6px var(--accent-success); animation: pulse-glow 2s ease infinite; }

/* ── Upload ── */
.upload-section { margin-bottom: 40px; }
.dropzone {
  border: 2px dashed rgba(59,130,246,0.35); border-radius: 20px;
  padding: 64px 32px; text-align: center; cursor: pointer;
  background: var(--gradient-card); transition: all 0.3s;
  position: relative; overflow: hidden;
}
.dropzone::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(ellipse at center, rgba(37,99,235,0.06), transparent 70%);
  pointer-events: none;
}
.dropzone.dragging { border-color: var(--accent-cyan); background: rgba(0,212,255,0.05); }
.dropzone.loading  { cursor: default; }
.dropzone:hover:not(.loading) { border-color: rgba(59,130,246,0.6); }
.dz-content { position: relative; }
.dz-icon { font-size: 56px; margin-bottom: 16px; }
.dropzone h2 { font-size: 24px; margin-bottom: 8px; }
.dropzone p { color: var(--text-secondary); font-size: 15px; margin-bottom: 6px; }
.dz-hint { font-size: 12px; color: var(--text-muted); }
.dz-actions { margin-top: 28px; display: flex; flex-direction: column; align-items: center; gap: 14px; }
.file-chip {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(59,130,246,0.12); border: 1px solid rgba(59,130,246,0.3);
  color: var(--blue-200); padding: 8px 16px; border-radius: 8px; font-size: 14px;
}
.dz-loading { position: relative; }
.loader-ring {
  width: 56px; height: 56px; border-radius: 50%;
  border: 3px solid rgba(59,130,246,0.2); border-top-color: var(--accent-cyan);
  animation: spin-slow 0.9s linear infinite; margin: 0 auto 20px;
}
.dz-loading p { font-size: 18px; font-weight: 600; margin-bottom: 6px; }
.load-sub { font-size: 12px; color: var(--text-muted); letter-spacing: 0.5px; }
.error-banner {
  margin-top: 16px; background: rgba(239,68,68,0.1);
  border: 1px solid rgba(239,68,68,0.3); color: #fca5a5;
  border-radius: 10px; padding: 12px 20px; font-size: 14px;
}

/* ── Buttons ── */
.btn-primary {
  position: relative; overflow: hidden; background: var(--gradient-accent);
  color: #fff; border: none; padding: 13px 28px; border-radius: 10px;
  font-size: 15px; font-weight: 600; cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s; font-family: var(--font-primary);
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(37,99,235,0.4); }
.btn-glow { position: absolute; inset: 0; background: linear-gradient(135deg, rgba(255,255,255,0.15), transparent); pointer-events: none; }
.btn-primary-sm {
  background: var(--gradient-accent); color: #fff; border: none;
  padding: 9px 18px; border-radius: 8px; font-size: 13px; font-weight: 600;
  cursor: pointer; font-family: var(--font-primary); transition: opacity 0.2s, transform 0.2s;
}
.btn-primary-sm:hover { opacity: 0.88; transform: translateY(-1px); }
.btn-ghost-sm {
  background: transparent; color: var(--text-secondary);
  border: 1px solid rgba(59,130,246,0.3); padding: 9px 18px;
  border-radius: 8px; font-size: 13px; cursor: pointer;
  font-family: var(--font-primary); transition: all 0.2s;
}
.btn-ghost-sm:hover { border-color: var(--blue-300); color: var(--text-primary); }

/* ── Results ── */
.results-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 28px; flex-wrap: wrap; gap: 12px;
}
.results-header h2 { font-size: 26px; }
.check { color: var(--accent-success); font-size: 22px; }
.results-actions { display: flex; gap: 10px; }

.summary-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 18px; margin-bottom: 32px;
}
.summary-card {
  background: var(--gradient-card); border: 1px solid var(--border-subtle);
  border-radius: 14px; padding: 24px 20px;
  display: flex; flex-direction: column; gap: 6px;
  transition: transform 0.2s, box-shadow 0.2s;
}
.summary-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-blue); }
.summary-card.danger  { border-color: rgba(239,68,68,0.2); }
.summary-card.danger  .sc-val { color: #f87171; }
.summary-card.warning { border-color: rgba(245,158,11,0.2); }
.summary-card.warning .sc-val { color: #fcd34d; }
.summary-card.success { border-color: rgba(16,185,129,0.2); }
.summary-card.success .sc-val { color: #6ee7b7; }
.sc-icon { font-size: 28px; }
.sc-val  { font-size: 32px; font-weight: 800; font-family: var(--font-display); }
.sc-label { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }

.panel-hint { font-size: 11px; color: var(--text-muted); margin-left: auto; text-transform: uppercase; letter-spacing: 0.5px; }

/* ── Ring Series Carousel ── */
.ring-carousel {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding: 4px 4px 20px 4px;
  margin-bottom: 32px;
  scrollbar-width: thin;
  scrollbar-color: rgba(59, 130, 246, 0.3) transparent;
}
.ring-carousel::-webkit-scrollbar { height: 6px; }
.ring-carousel::-webkit-scrollbar-thumb { background: rgba(59, 130, 246, 0.3); border-radius: 10px; }

.ring-card-series {
  flex: 0 0 260px;
  background: var(--gradient-card);
  border: 1px solid var(--border-subtle);
  border-radius: 16px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
}
.ring-card-series::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 3px;
  background: var(--gradient-accent);
  opacity: 0;
  transition: opacity 0.3s;
}
.ring-card-series:hover {
  transform: translateY(-8px);
  border-color: rgba(59, 130, 246, 0.4);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4), 0 0 20px rgba(37, 99, 235, 0.1);
}
.ring-card-series.active {
  border-color: var(--accent-cyan);
  background: rgba(0, 212, 255, 0.05);
  box-shadow: 0 0 25px rgba(0, 212, 255, 0.15);
}
.ring-card-series.active::before { opacity: 1; }

.rcs-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.rcs-badge {
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  background: rgba(139, 92, 246, 0.15); color: #c4b5fd;
  padding: 3px 8px; border-radius: 50px; border: 1px solid rgba(139, 92, 246, 0.3);
}
.rcs-risk { font-size: 10px; font-weight: 700; text-transform: uppercase; }
.rcs-risk.high { color: #f87171; }
.rcs-risk.med { color: #fbbf24; }
.rcs-risk.low { color: #6ee7b7; }

.rcs-title { font-size: 20px; font-weight: 700; color: var(--text-primary); margin-bottom: 6px; }
.rcs-meta { display: flex; flex-direction: column; gap: 4px; font-size: 12px; color: var(--text-secondary); margin-bottom: 16px; }

.btn-focus {
  width: 100%; padding: 8px; border-radius: 8px;
  background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.2);
  color: var(--blue-200); font-size: 12px; font-weight: 600;
  cursor: pointer; transition: all 0.2s;
}
.ring-card-series:hover .btn-focus { background: var(--blue-500); color: white; border-color: var(--blue-400); }
.ring-card-series.active .btn-focus { background: var(--accent-cyan); color: #020b18; border-color: var(--accent-cyan); }

.main-graph-panel { margin-top: 20px; }

.final-actions {
  margin-top: 48px;
  padding: 40px;
  background: var(--gradient-card);
  border: 1px solid var(--border-glow);
  border-radius: 20px;
  text-align: center;
  animation: fadeInUp 0.8s ease both;
}
.final-hint {
  margin-top: 16px;
  font-size: 13px;
  color: var(--text-muted);
}

/* ── Panels ── */
.panel {
  background: var(--gradient-card); border: 1px solid var(--border-subtle);
  border-radius: 16px; padding: 28px; margin-bottom: 24px;
}
.panel-header { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
.panel-icon { font-size: 20px; }
.panel h3 { font-size: 18px; font-weight: 700; color: var(--text-primary); flex: 1; }

/* Intelligence Dashboard */
.intel-dashboard {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}
.chart-panel { margin-bottom: 0; }
.chart-container { height: 260px; position: relative; }

/* Flagged list */
.flagged-list { display: flex; flex-direction: column; gap: 12px; }
.flagged-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 20px;
  background: rgba(10, 25, 50, 0.4);
  border: 1px solid rgba(59, 130, 246, 0.1);
  border-radius: 12px;
  transition: all 0.2s ease;
}
.flagged-row:hover { border-color: rgba(59, 130, 246, 0.3); transform: translateX(5px); }
.fr-main { flex: 1; min-width: 0; padding-right: 20px; }
.fr-account { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
.mule-icon { font-size: 14px; opacity: 0.6; }
.mule-id { font-size: 15px; font-weight: 700; color: var(--blue-200); font-family: var(--font-display); }
.fr-explanation { font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px; }
.fr-patterns { display: flex; flex-wrap: wrap; gap: 6px; }
.pattern-tag {
  font-size: 10px; font-weight: 700; text-transform: uppercase;
  background: rgba(37, 99, 235, 0.15); color: #93c5fd;
  padding: 2px 8px; border-radius: 4px; border: 1px solid rgba(37, 99, 235, 0.2);
}

.fr-score-box {
  width: 70px; height: 70px; border-radius: 14px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  border: 1px solid;
}
.fr-score-box.high { background: rgba(239, 68, 68, 0.1); border-color: rgba(239, 68, 68, 0.3); }
.fr-score-box.med  { background: rgba(245, 158, 11, 0.1); border-color: rgba(245, 158, 11, 0.3); }
.fr-score-box.low  { background: rgba(16, 185, 129, 0.1); border-color: rgba(16, 185, 129, 0.3); }

.fr-score-val { font-size: 24px; font-weight: 800; font-family: var(--font-display); line-height: 1; }
.fr-score-box.high .fr-score-val { color: #f87171; }
.fr-score-box.med .fr-score-val  { color: #fbbf24; }
.fr-score-box.low .fr-score-val  { color: #34d399; }
.fr-score-label { font-size: 9px; font-weight: 700; text-transform: uppercase; color: var(--text-muted); margin-top: 4px; }
.legend { display: flex; gap: 14px; flex-wrap: wrap; }
.leg-item { display: flex; align-items: center; gap: 5px; font-size: 12px; color: var(--text-secondary); }
.leg-dot { width: 10px; height: 10px; border-radius: 50%; }
.leg-dot.red { background: #ef4444; }
.leg-dot.blue { background: #4a90e2; }
.count-badge {
  background: rgba(59,130,246,0.15); border: 1px solid rgba(59,130,246,0.3);
  color: var(--blue-200); padding: 3px 10px; border-radius: 99px; font-size: 12px; font-weight: 600;
}
.count-badge.red { background: rgba(239,68,68,0.12); border-color: rgba(239,68,68,0.3); color: #fca5a5; }

/* ── Table ── */
.table-wrap { overflow-x: auto; }
.pro-table { width: 100%; border-collapse: collapse; }
.pro-table th {
  text-align: left; padding: 12px 16px;
  font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;
  color: var(--text-muted); border-bottom: 1px solid rgba(59,130,246,0.12);
}
.pro-table td { padding: 14px 16px; font-size: 14px; border-bottom: 1px solid rgba(59,130,246,0.06); }
.pro-table tr:last-child td { border-bottom: none; }
.pro-table tbody tr:hover { background: rgba(59,130,246,0.04); }
.ring-id { font-family: monospace; color: var(--accent-cyan); font-size: 13px; }
.pattern-badge {
  background: rgba(139,92,246,0.15); border: 1px solid rgba(139,92,246,0.3);
  color: #c4b5fd; padding: 3px 10px; border-radius: 6px; font-size: 12px; font-weight: 500;
}
.count-tag {
  background: rgba(59,130,246,0.15); color: var(--blue-200);
  padding: 2px 10px; border-radius: 99px; font-size: 13px; font-weight: 600;
}
.risk-bar { display: flex; align-items: center; gap: 8px; }
.risk-track { flex: 1; height: 6px; background: rgba(255,255,255,0.07); border-radius: 99px; overflow: hidden; }
.risk-fill { height: 100%; border-radius: 99px; transition: width 1s ease; }
.risk-fill.high { background: linear-gradient(90deg, #f87171, #ef4444); }
.risk-fill.med  { background: linear-gradient(90deg, #fbbf24, #f59e0b); }
.risk-fill.low  { background: linear-gradient(90deg, #6ee7b7, #10b981); }
.risk-num { font-size: 12px; color: var(--text-secondary); min-width: 30px; }
.account-tags { display: flex; gap: 5px; flex-wrap: wrap; }
.acc-tag {
  background: rgba(15,35,70,0.8); border: 1px solid rgba(59,130,246,0.2);
  color: var(--blue-200); padding: 2px 7px; border-radius: 5px;
  font-size: 11px; font-family: monospace;
}
.acc-more { font-size: 11px; color: var(--text-muted); align-self: center; }

/* ── Flagged ── */
.flagged-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }
.flagged-card {
  background: rgba(239,68,68,0.05); border: 1px solid rgba(239,68,68,0.18);
  border-radius: 10px; padding: 16px; transition: transform 0.2s;
}
.flagged-card:hover { transform: translateY(-2px); }
.fa-id { font-family: monospace; color: #f87171; font-size: 14px; font-weight: 700; margin-bottom: 4px; }
.fa-reason { font-size: 12px; color: var(--text-secondary); margin-bottom: 6px; }
.fa-score { font-size: 12px; color: var(--text-muted); }
.fa-score b { color: #fcd34d; }

/* ══════════════════════════════════════
   AI SUMMARY SIDEBAR
══════════════════════════════════════ */
.ai-sidebar {
  width: 340px;
  flex-shrink: 0;
  min-height: 100vh;
  background: rgba(5, 14, 30, 0.95);
  border-left: 1px solid rgba(59, 130, 246, 0.15);
  padding: 32px 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: sticky;
  top: 0;
  max-height: 100vh;
  overflow-y: auto;
  animation: slideInRight 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideInRight {
  from { opacity: 0; transform: translateX(40px); }
  to   { opacity: 1; transform: translateX(0); }
}

.sidebar-header {
  border-bottom: 1px solid rgba(59,130,246,0.1);
  padding-bottom: 16px;
}
.sidebar-title-row {
  display: flex; align-items: center; gap: 8px; margin-bottom: 6px;
}
.ai-icon {
  font-size: 18px;
  background: var(--gradient-accent);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  font-style: normal;
}
.sidebar-title {
  font-size: 16px; font-weight: 700; font-family: var(--font-display);
  color: var(--text-primary); flex: 1;
}
/* Summary intelligence points */
.summary-points { display: flex; flex-direction: column; gap: 14px; }
.summary-point {
  display: flex; align-items: flex-start; gap: 10px;
  font-size: 13.5px; color: var(--text-secondary); line-height: 1.6;
}
.pt-dot {
  width: 5px; height: 5px; border-radius: 50%;
  background: var(--accent-electric); flex-shrink: 0; margin-top: 8px;
  box-shadow: 0 0 6px rgba(0, 212, 255, 0.4);
}

/* AI Loading dots */
.ai-loading { display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 32px 0; }
.ai-loader { display: flex; gap: 6px; }
.ai-loader span {
  width: 8px; height: 8px; border-radius: 50%;
  background: var(--accent-electric);
  animation: dot-bounce 1.2s ease infinite;
}
.ai-loader span:nth-child(1) { animation-delay: 0s; }
.ai-loader span:nth-child(2) { animation-delay: 0.2s; }
.ai-loader span:nth-child(3) { animation-delay: 0.4s; }
@keyframes dot-bounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
  40%            { transform: scale(1);   opacity: 1; }
}
.ai-loading p { font-size: 13px; color: var(--text-secondary); }

/* AI Error */
.ai-error {
  background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.25);
  border-radius: 10px; padding: 16px; text-align: center;
}
.ai-error-icon { font-size: 24px; display: block; margin-bottom: 8px; }
.ai-error p { font-size: 13px; color: #fca5a5; margin-bottom: 12px; }
.retry-btn {
  background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.3);
  color: #fca5a5; padding: 6px 14px; border-radius: 7px; font-size: 12px;
  cursor: pointer; font-family: var(--font-primary); transition: all 0.2s;
}
.retry-btn:hover { background: rgba(239,68,68,0.25); }

/* Verdict banner */
.verdict-banner {
  display: flex; align-items: center; gap: 12px;
  border-radius: 12px; padding: 14px 16px;
  border: 1px solid;
}
.verdict-banner.clean    { background: rgba(16,185,129,0.08); border-color: rgba(16,185,129,0.3); }
.verdict-banner.medium   { background: rgba(245,158,11,0.08); border-color: rgba(245,158,11,0.3); }
.verdict-banner.critical { background: rgba(239,68,68,0.08);  border-color: rgba(239,68,68,0.3); }
.verdict-icon { font-size: 26px; flex-shrink: 0; }
.verdict-label { font-size: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px; }
.verdict-text  { font-size: 13px; font-weight: 600; color: var(--text-primary); }

/* Quick stats strip */
.quick-stats {
  display: flex; align-items: center; justify-content: space-around;
  background: rgba(10,25,50,0.6); border: 1px solid rgba(59,130,246,0.12);
  border-radius: 12px; padding: 14px;
}
.qs-item { display: flex; flex-direction: column; align-items: center; gap: 2px; }
.qs-val  { font-size: 22px; font-weight: 800; font-family: var(--font-display); color: var(--text-primary); }
.qs-val.qs-danger { color: #f87171; }
.qs-val.qs-warn   { color: #fcd34d; }
.qs-label { font-size: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
.qs-divider { width: 1px; height: 32px; background: rgba(59,130,246,0.12); }

/* Copy button */
.copy-btn {
  background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.25);
  color: var(--blue-200); padding: 9px 16px; border-radius: 8px;
  font-size: 13px; cursor: pointer; font-family: var(--font-primary);
  transition: all 0.2s; width: 100%; text-align: center;
}
.copy-btn:hover { background: rgba(59,130,246,0.2); border-color: rgba(59,130,246,0.5); }

/* AI Intelligence Chat */
.ai-chat-container {
  margin-top: 32px;
  background: rgba(10, 25, 45, 0.4);
  border: 1px solid rgba(59, 130, 246, 0.1);
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  height: 480px;
}

.chat-header {
  padding: 12px 16px;
  background: rgba(59, 130, 246, 0.05);
  border-bottom: 1px solid rgba(59, 130, 246, 0.1);
  display: flex;
  align-items: center;
  gap: 8px;
}
.chat-status-dot {
  width: 8px; height: 8px; border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 8px #10b981;
}
.chat-header h4 { font-size: 13px; font-weight: 700; color: var(--text-primary); letter-spacing: 0.5px; }

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  scrollbar-width: thin;
  scrollbar-color: rgba(59, 130, 246, 0.2) transparent;
}
.chat-messages::-webkit-scrollbar { width: 4px; }
.chat-messages::-webkit-scrollbar-thumb { background: rgba(59, 130, 246, 0.2); border-radius: 4px; }

.chat-msg { display: flex; gap: 10px; align-items: flex-start; max-width: 90%; }
.chat-msg p {
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 13px;
  line-height: 1.5;
}

.ai-msg { align-self: flex-start; }
.ai-msg p {
  background: rgba(30, 41, 59, 0.7);
  color: var(--text-secondary);
  border-bottom-left-radius: 2px;
}
.msg-bot-icon { font-size: 16px; margin-top: 8px; opacity: 0.8; }

.user-msg { align-self: flex-end; flex-direction: row-reverse; }
.user-msg p {
  background: var(--blue-600);
  color: white;
  border-bottom-right-radius: 2px;
}

/* Typing animation */
.typing-dots { display: flex; gap: 4px; padding: 4px 0; }
.typing-dots span {
  width: 6px; height: 6px; background: var(--text-muted);
  border-radius: 50%; opacity: 0.4;
  animation: typing 1.4s infinite;
}
.typing-dots span:nth-child(2) { animation-delay: 0.2s; }
.typing-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); opacity: 1; }
}

.chat-input-row {
  padding: 12px;
  background: rgba(10, 25, 45, 0.8);
  border-top: 1px solid rgba(59, 130, 246, 0.12);
  display: flex;
  gap: 8px;
}
.chat-input-row input {
  flex: 1;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(59, 130, 246, 0.15);
  border-radius: 8px;
  padding: 10px 14px;
  color: white;
  font-size: 13px;
  outline: none;
  transition: all 0.2s;
}
.chat-input-row input:focus {
  border-color: var(--blue-500);
  background: rgba(255, 255, 255, 0.08);
}
.chat-input-row button {
  background: var(--blue-600);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0 16px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}
.chat-input-row button:hover { background: var(--blue-500); transform: translateY(-1px); }
.chat-input-row button:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }

/* Sidebar scrollbar */
.ai-sidebar::-webkit-scrollbar { width: 4px; }
.ai-sidebar::-webkit-scrollbar-thumb { background: rgba(59,130,246,0.25); border-radius: 99px; }

@media (max-width: 900px) {
  .analyzer-root { flex-direction: column; }
  .ai-sidebar { width: 100%; min-height: auto; position: static; border-left: none; border-top: 1px solid rgba(59,130,246,0.15); }
}
</style>
