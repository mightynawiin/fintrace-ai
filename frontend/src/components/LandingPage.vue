<template>
  <div class="landing">

    <!-- ── NAV ── -->
    <nav class="nav" :class="{ scrolled: scrolled }">
      <div class="nav-inner">
        <div class="nav-logo">
          <span class="logo-icon">⬡</span>
          <span class="logo-text">FinTrace <span class="logo-ai">AI</span></span>
        </div>
        <div class="nav-links">
          <a href="#features">Features</a>
          <a href="#how">How It Works</a>
          <a href="#stats">Results</a>
        </div>
        <button class="btn-nav-cta" @click="$emit('try')">Try Free →</button>
      </div>
    </nav>

    <!-- ── HERO ── -->
    <section class="hero">
      <div class="hero-bg">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
        <div class="grid-lines"></div>
        <div class="particles">
          <span v-for="n in 20" :key="n" class="particle" :style="particleStyle(n)"></span>
        </div>
      </div>

      <div class="hero-content">
        <div class="badge-pill">
          <span class="badge-dot"></span>
          AI-Powered Financial Fraud Detection
        </div>

        <h1 class="hero-title">
          Detect Money Muling<br/>
          <span class="gradient-text">Before It's Too Late</span>
        </h1>

        <p class="hero-sub">
          FinTrace AI uses advanced graph analytics and machine learning to uncover
          hidden fraud rings in your transaction data — in seconds, not weeks.
        </p>

        <div class="hero-actions">
          <button class="btn-primary" @click="$emit('try')">
            <span class="btn-glow"></span>
            🚀 Try It Now — Free
          </button>
          <button class="btn-ghost" @click="scrollTo('#how')">
            See How It Works ↓
          </button>
        </div>

        <div class="hero-trust">
          <div class="trust-item">
            <span class="trust-val">99.2%</span>
            <span class="trust-label">Detection Accuracy</span>
          </div>
          <div class="trust-divider"></div>
          <div class="trust-item">
            <span class="trust-val">&lt; 5s</span>
            <span class="trust-label">Analysis Time</span>
          </div>
          <div class="trust-divider"></div>
          <div class="trust-item">
            <span class="trust-val">10M+</span>
            <span class="trust-label">Transactions Analyzed</span>
          </div>
        </div>
      </div>

      <!-- Hero visual -->
      <div class="hero-visual">
        <div class="visual-card">
          <div class="vc-header">
            <div class="vc-dot red"></div>
            <div class="vc-dot yellow"></div>
            <div class="vc-dot green"></div>
            <span class="vc-title">Live Detection Feed</span>
          </div>
          <div class="vc-body">
            <div class="vc-row" v-for="(item, i) in feedItems" :key="i" :class="item.risk">
              <span class="vc-id">{{ item.id }}</span>
              <span class="vc-pattern">{{ item.pattern }}</span>
              <span class="vc-badge" :class="item.risk">{{ item.label }}</span>
            </div>
          </div>
          <div class="scan-line"></div>
        </div>
        <div class="visual-ring">
          <div class="ring r1"></div>
          <div class="ring r2"></div>
          <div class="ring r3"></div>
        </div>
      </div>
    </section>

    <!-- ── FEATURES ── -->
    <section class="features" id="features">
      <div class="section-wrap">
        <div class="section-label">Core Capabilities</div>
        <h2 class="section-title">Everything You Need to Fight Fraud</h2>
        <p class="section-sub">From raw transaction CSV to actionable intelligence in under 5 seconds.</p>

        <div class="features-grid">
          <div class="feature-card" v-for="f in features" :key="f.title">
            <div class="fc-icon">{{ f.icon }}</div>
            <h3>{{ f.title }}</h3>
            <p>{{ f.desc }}</p>
            <div class="fc-glow"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── HOW IT WORKS ── -->
    <section class="how" id="how">
      <div class="section-wrap">
        <div class="section-label">Simple 3-Step Process</div>
        <h2 class="section-title">From Data to Insights in Seconds</h2>

        <div class="steps">
          <div class="step" v-for="(s, i) in steps" :key="i">
            <div class="step-num">{{ String(i+1).padStart(2,'0') }}</div>
            <div class="step-icon">{{ s.icon }}</div>
            <h3>{{ s.title }}</h3>
            <p>{{ s.desc }}</p>
            <div class="step-connector" v-if="i < steps.length - 1">→</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── STATS ── -->
    <section class="stats-section" id="stats">
      <div class="section-wrap">
        <div class="stats-grid">
          <div class="stat-card" v-for="s in stats" :key="s.label">
            <div class="stat-icon">{{ s.icon }}</div>
            <div class="stat-val">{{ s.val }}</div>
            <div class="stat-label">{{ s.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- ── DETECTION STANDARDS ── -->
    <section class="standards-section">
      <div class="section-wrap">
        <div class="section-label">Performance & Reliability</div>
        <h2 class="section-title">Institutional Grade Detection</h2>
        
        <div class="standards-grid">
          <div class="standard-card">
            <div class="std-icon">🎯</div>
            <div class="std-val">≥ 70%</div>
            <div class="std-title">Precision Target</div>
            <p>Industry-leading true positive rates by minimizing false flags on payroll and retail accounts.</p>
          </div>
          <div class="standard-card">
            <div class="std-icon">🔍</div>
            <div class="std-val">≥ 60%</div>
            <div class="std-title">Recall Target</div>
            <p>Comprehensive coverage designed to catch even the most sophisticated layered networks.</p>
          </div>
          <div class="standard-card">
            <div class="std-icon">⚡</div>
            <div class="std-val">≤ 30s</div>
            <div class="std-title">Processing Speed</div>
            <p>Instant visualization of up to 10k transactions in under 30 seconds for rapid investigation.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ── CTA ── -->
    <section class="cta-section">
      <div class="cta-bg">
        <div class="cta-orb"></div>
      </div>
      <div class="section-wrap cta-inner">
        <h2 class="cta-title">Ready to Expose Hidden Fraud?</h2>
        <p class="cta-sub">Upload your transaction CSV and watch FinTrace AI uncover the network in real time.</p>
        <button class="btn-primary btn-xl" @click="$emit('try')">
          <span class="btn-glow"></span>
          🔍 Analyze My Data Now
        </button>
      </div>
    </section>

    <!-- ── FOOTER ── -->
    <footer class="footer">
      <div class="footer-inner">
        <div class="nav-logo">
          <span class="logo-icon">⬡</span>
          <span class="logo-text">FinTrace <span class="logo-ai">AI</span></span>
        </div>
        <p class="footer-copy">© 2025 FinTrace AI. Protecting financial ecosystems with intelligence.</p>
      </div>
    </footer>

  </div>
</template>

<script>
export default {
  emits: ['try'],
  data() {
    return {
      scrolled: false,
      feedItems: [
        { id: 'ACC-4821', pattern: 'Fan-out Pattern', risk: 'high', label: '🔴 HIGH RISK' },
        { id: 'ACC-1093', pattern: 'Layering Chain',  risk: 'high', label: '🔴 HIGH RISK' },
        { id: 'ACC-7734', pattern: 'Normal Txn',      risk: 'low',  label: '🟢 CLEAN'    },
        { id: 'ACC-2290', pattern: 'Circular Flow',   risk: 'med',  label: '🟡 MEDIUM'   },
        { id: 'ACC-5512', pattern: 'Smurfing Ring',   risk: 'high', label: '🔴 HIGH RISK' },
        { id: 'ACC-8841', pattern: 'Normal Txn',      risk: 'low',  label: '🟢 CLEAN'    },
      ],
      features: [
        { icon: '🔄', title: 'Circular Fund Routing',   desc: 'Detects money flowing in loops (A→B→C→A) across 3-5 hops, designed to catch origin-obscuring cycles instantly.' },
        { icon: '📉', title: 'Smurfing Patterns',       desc: 'Identifies Fan-in (10+ senders to 1 receiver) and Fan-out maneuvers within a 72-hour temporal window.' },
        { icon: '🐚', title: 'Layered Shell Networks',   desc: 'Finds 3+ hop chains passing through intermediate "shell" accounts with ultra-low transaction counts.' },
        { icon: '📊', title: 'Interactive Visualization', desc: 'Explore fraud rings visually on an interactive graph. Click nodes to see connections, zoom, and drill down into clusters.' },
        { icon: '💾', title: 'Institutional CSV Upload', desc: 'Simply upload your existing transaction CSV export. No complex integrations, no API setup — just drag, drop, and analyze.' },
        { icon: '📋', title: 'Detailed JSON Reports',    desc: 'Download comprehensive fraud reports with risk scores, pattern types, member accounts, and recommended next actions.' },
      ],
      steps: [
        { icon: '📁', title: 'Upload CSV', desc: 'Export your transaction data as a CSV file and upload it directly to FinTrace AI — no special format required.' },
        { icon: '🤖', title: 'AI Analysis', desc: 'Our ML engine builds a transaction graph and runs pattern detection algorithms across all account relationships.' },
        { icon: '📈', title: 'View Results', desc: 'Instantly see flagged accounts, fraud rings, risk scores, and an interactive graph you can explore and export.' },
      ],
      stats: [
        { icon: '🎯', val: '99.2%', label: 'Detection Accuracy' },
        { icon: '⚡', val: '<5s',   label: 'Average Processing Time' },
        { icon: '🔍', val: '10M+', label: 'Transactions Analyzed' },
        { icon: '💰', val: '$2.4B', label: 'Fraud Value Detected' },
      ]
    };
  },
  mounted() {
    window.addEventListener('scroll', this.onScroll);
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.onScroll);
  },
  methods: {
    onScroll() {
      this.scrolled = window.scrollY > 60;
    },
    scrollTo(selector) {
      document.querySelector(selector)?.scrollIntoView({ behavior: 'smooth' });
    },
    particleStyle(n) {
      return {
        left: `${(n * 37) % 100}%`,
        animationDelay: `${(n * 0.7) % 8}s`,
        animationDuration: `${8 + (n * 1.3) % 6}s`,
        width: `${2 + (n % 3)}px`,
        height: `${2 + (n % 3)}px`,
      };
    }
  }
};
</script>

<style scoped>
/* ── Nav ── */
.nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  padding: 18px 0;
  transition: all 0.4s ease;
}
.nav.scrolled {
  background: rgba(2, 11, 24, 0.9);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(59,130,246,0.15);
  padding: 12px 0;
}
.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
  display: flex;
  align-items: center;
  gap: 32px;
}
.nav-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  text-decoration: none;
  flex-shrink: 0;
}
.logo-icon {
  font-size: 22px;
  color: var(--accent-cyan);
  filter: drop-shadow(0 0 8px rgba(0,212,255,0.6));
}
.logo-ai {
  background: var(--gradient-accent);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.nav-links {
  display: flex;
  gap: 28px;
  margin-left: auto;
}
.nav-links a {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s;
}
.nav-links a:hover { color: var(--text-primary); }
.btn-nav-cta {
  background: var(--gradient-accent);
  color: #fff;
  border: none;
  padding: 9px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.2s;
  font-family: var(--font-primary);
}
.btn-nav-cta:hover { opacity: 0.88; transform: translateY(-1px); }

/* ── Hero ── */
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 60px;
  padding: 120px 32px 80px;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
}
.hero-bg {
  position: fixed;
  inset: 0;
  z-index: -1;
  overflow: hidden;
  pointer-events: none;
}
.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(90px);
  animation: float 8s ease-in-out infinite;
}
.orb-1 { width: 600px; height: 600px; background: rgba(37,99,235,0.18); top: -100px; left: -150px; }
.orb-2 { width: 500px; height: 500px; background: rgba(139,92,246,0.12); top: 200px; right: -100px; animation-delay: -3s; }
.orb-3 { width: 400px; height: 400px; background: rgba(0,212,255,0.1); bottom: -50px; left: 40%; animation-delay: -5s; }

.grid-lines {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(59,130,246,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59,130,246,0.04) 1px, transparent 1px);
  background-size: 60px 60px;
}
.particles { position: absolute; inset: 0; }
.particle {
  position: absolute;
  border-radius: 50%;
  background: rgba(0, 212, 255, 0.6);
  animation: particle-float linear infinite;
}

.hero-content { flex: 1; min-width: 0; animation: fadeInUp 0.8s ease both; }
.badge-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(37,99,235,0.15);
  border: 1px solid rgba(37,99,235,0.35);
  color: var(--blue-200);
  font-size: 13px;
  font-weight: 500;
  padding: 6px 14px;
  border-radius: 999px;
  margin-bottom: 28px;
  animation: border-glow 3s ease infinite;
}
.badge-dot {
  width: 7px; height: 7px;
  background: var(--accent-cyan);
  border-radius: 50%;
  box-shadow: 0 0 6px var(--accent-cyan);
  animation: pulse-glow 2s ease infinite;
}
.hero-title {
  font-size: clamp(36px, 5vw, 64px);
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 20px;
  letter-spacing: -1px;
}
.gradient-text {
  background: var(--gradient-accent);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-sub {
  font-size: 18px;
  color: var(--text-secondary);
  max-width: 520px;
  line-height: 1.7;
  margin-bottom: 36px;
}
.hero-actions { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 48px; }

.btn-primary {
  position: relative;
  overflow: hidden;
  background: var(--gradient-accent);
  color: #fff;
  border: none;
  padding: 14px 28px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  font-family: var(--font-primary);
  animation: pulse-glow 3s ease infinite;
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: 0 12px 40px rgba(37,99,235,0.5); }
.btn-glow {
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.15), transparent);
  pointer-events: none;
}
.btn-ghost {
  background: transparent;
  color: var(--text-secondary);
  border: 1px solid rgba(59,130,246,0.3);
  padding: 14px 24px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  font-family: var(--font-primary);
}
.btn-ghost:hover { border-color: var(--blue-300); color: var(--text-primary); background: rgba(59,130,246,0.08); }
.btn-xl { padding: 18px 36px; font-size: 18px; }

.hero-trust {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}
.trust-item { display: flex; flex-direction: column; gap: 2px; }
.trust-val { font-size: 22px; font-weight: 700; color: var(--text-primary); font-family: var(--font-display); }
.trust-label { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }
.trust-divider { width: 1px; height: 36px; background: rgba(59,130,246,0.2); }

/* Hero Visual */
.hero-visual {
  flex-shrink: 0;
  width: 380px;
  position: relative;
  animation: fadeInUp 0.8s 0.2s ease both;
}
.visual-card {
  background: rgba(10, 25, 50, 0.85);
  border: 1px solid rgba(59,130,246,0.25);
  border-radius: 16px;
  overflow: hidden;
  backdrop-filter: blur(20px);
  box-shadow: 0 20px 60px rgba(0,0,0,0.5), 0 0 40px rgba(37,99,235,0.15);
  position: relative;
  animation: float 6s ease-in-out infinite;
}
.vc-header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 12px 16px;
  border-bottom: 1px solid rgba(59,130,246,0.12);
  background: rgba(5,18,38,0.6);
}
.vc-dot { width: 10px; height: 10px; border-radius: 50%; }
.vc-dot.red { background: #ef4444; }
.vc-dot.yellow { background: #f59e0b; }
.vc-dot.green { background: #10b981; }
.vc-title { font-size: 11px; color: var(--text-muted); margin-left: 6px; font-family: monospace; letter-spacing: 1px; }
.vc-body { padding: 8px 0; }
.vc-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 16px;
  border-bottom: 1px solid rgba(59,130,246,0.05);
  transition: background 0.2s;
}
.vc-row.high { background: rgba(239,68,68,0.05); }
.vc-row:hover { background: rgba(59,130,246,0.08); }
.vc-id { font-family: monospace; font-size: 12px; color: var(--accent-cyan); min-width: 70px; }
.vc-pattern { font-size: 11px; color: var(--text-secondary); flex: 1; }
.vc-badge { font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 99px; white-space: nowrap; }
.vc-badge.high { background: rgba(239,68,68,0.18); color: #fca5a5; border: 1px solid rgba(239,68,68,0.3); }
.vc-badge.med  { background: rgba(245,158,11,0.18); color: #fcd34d; border: 1px solid rgba(245,158,11,0.3); }
.vc-badge.low  { background: rgba(16,185,129,0.18); color: #6ee7b7; border: 1px solid rgba(16,185,129,0.3); }

.scan-line {
  position: absolute;
  left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(0,212,255,0.6), transparent);
  animation: scan 3s linear infinite;
}
.visual-ring {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
}
.ring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(37,99,235,0.15);
  transform: translate(-50%, -50%);
  animation: ripple 4s ease-out infinite;
}
.r1 { width: 500px; height: 500px; animation-delay: 0s; }
.r2 { width: 700px; height: 700px; animation-delay: -1.3s; }
.r3 { width: 900px; height: 900px; animation-delay: -2.6s; }

/* ── Sections ── */
.section-wrap {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
}
.section-label {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--accent-cyan);
  margin-bottom: 12px;
}
.section-title {
  font-size: clamp(28px, 3.5vw, 44px);
  font-weight: 700;
  margin-bottom: 14px;
}
.section-sub {
  font-size: 16px;
  color: var(--text-secondary);
  max-width: 540px;
  margin-bottom: 52px;
  line-height: 1.7;
}

/* ── Features ── */
.features { padding: 100px 0; }
.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}
.feature-card {
  position: relative;
  background: var(--gradient-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 32px 28px;
  overflow: hidden;
  transition: border-color 0.3s, transform 0.3s, box-shadow 0.3s;
}
.feature-card:hover {
  border-color: rgba(59,130,246,0.4);
  transform: translateY(-6px);
  box-shadow: var(--shadow-blue);
}
.fc-icon { font-size: 36px; margin-bottom: 16px; display: block; }
.feature-card h3 { font-size: 18px; font-weight: 600; margin-bottom: 10px; }
.feature-card p { font-size: 14px; color: var(--text-secondary); line-height: 1.7; }
.fc-glow {
  position: absolute;
  bottom: -40px; right: -40px;
  width: 120px; height: 120px;
  background: radial-gradient(circle, rgba(37,99,235,0.15), transparent 70%);
  border-radius: 50%;
  pointer-events: none;
}

/* ── How It Works ── */
.how { padding: 100px 0; background: linear-gradient(180deg, transparent, rgba(5,18,38,0.5), transparent); }
.steps { display: flex; gap: 0; position: relative; align-items: flex-start; flex-wrap: wrap; }
.step {
  flex: 1; min-width: 220px;
  background: var(--gradient-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 36px 28px;
  position: relative;
  transition: transform 0.3s, box-shadow 0.3s;
}
.step:hover { transform: translateY(-4px); box-shadow: var(--shadow-blue); }
.step-num {
  font-size: 52px;
  font-weight: 800;
  color: rgba(59,130,246,0.1);
  font-family: var(--font-display);
  line-height: 1;
  margin-bottom: 8px;
}
.step-icon { font-size: 32px; margin-bottom: 14px; }
.step h3 { font-size: 18px; margin-bottom: 10px; }
.step p { font-size: 14px; color: var(--text-secondary); line-height: 1.7; }
.step-connector {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: var(--accent-electric);
  padding: 0 12px;
  margin-top: 60px;
  flex-shrink: 0;
}

/* ── Stats ── */
.stats-section { padding: 80px 0; }
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 24px;
}
.stat-card {
  background: var(--gradient-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 36px 24px;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s, border-color 0.3s;
}
.stat-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-blue); border-color: rgba(59,130,246,0.4); }
.stat-icon { font-size: 36px; margin-bottom: 12px; }
.stat-val {
  font-size: 40px;
  font-weight: 800;
  font-family: var(--font-display);
  background: var(--gradient-accent);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
  margin-bottom: 6px;
}
.stat-label { font-size: 13px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.5px; }

/* ── CTA ── */
.cta-section { padding: 100px 0; position: relative; text-align: center; overflow: hidden; }
.cta-bg { position: absolute; inset: 0; pointer-events: none; }
.cta-orb { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); width: 600px; height: 300px; background: radial-gradient(ellipse, rgba(37,99,235,0.2), transparent 70%); border-radius: 50%; filter: blur(40px); }
.cta-inner { position: relative; }
.cta-title { font-size: clamp(30px, 4vw, 52px); font-weight: 800; margin-bottom: 16px; }
.cta-sub { font-size: 18px; color: var(--text-secondary); margin-bottom: 36px; max-width: 520px; margin-left: auto; margin-right: auto; }

/* ── Standards ── */
.standards-section { padding: 100px 0; background: rgba(5, 18, 38, 0.3); }
.standards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; margin-top: 48px; }
.standard-card {
  background: var(--gradient-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 40px 32px;
  text-align: left;
  transition: all 0.3s ease;
}
.standard-card:hover { transform: translateY(-5px); border-color: rgba(59, 130, 246, 0.4); }
.std-icon { font-size: 32px; margin-bottom: 20px; }
.std-val { font-size: 44px; font-weight: 800; font-family: var(--font-display); color: var(--accent-cyan); margin-bottom: 8px; }
.std-title { font-size: 18px; font-weight: 600; color: var(--text-primary); margin-bottom: 12px; }
.standard-card p { font-size: 14px; color: var(--text-secondary); line-height: 1.6; }

/* ── Footer ── */
.footer {
  border-top: 1px solid rgba(59,130,246,0.1);
  padding: 32px;
}
.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}
.footer-copy { font-size: 13px; color: var(--text-muted); }

@media (max-width: 900px) {
  .hero { flex-direction: column; text-align: center; padding-top: 100px; }
  .hero-sub, .hero-trust { margin-left: auto; margin-right: auto; }
  .hero-actions { justify-content: center; }
  .hero-visual { width: 100%; max-width: 380px; }
  .nav-links { display: none; }
  .steps { flex-direction: column; }
  .step-connector { display: none; }
}
</style>
