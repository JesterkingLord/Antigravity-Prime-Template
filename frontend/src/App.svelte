<script>
  import { onMount, onDestroy } from 'svelte';
  import Chat from './lib/components/Chat.svelte';
  import { fade, slide } from 'svelte/transition';

  // State
  let skills = [];
  let health = null;
  let loading = true;
  let error = null;
  let activeTab = 'dashboard'; // 'dashboard', 'chat', 'system', 'logs'

  // Config
  const API_URL = 'http://localhost:8000/api';
  let pollInterval;

  async function fetchData() {
    try {
      const [skillsRes, healthRes] = await Promise.all([
        fetch(`${API_URL}/skills`),
        fetch(`${API_URL}/health`)
      ]);
      
      if (skillsRes.ok) skills = await skillsRes.json();
      if (healthRes.ok) health = await healthRes.json();
      
      error = null;
    } catch (e) {
      error = e.message;
    } finally {
      loading = false;
    }
  }

  onMount(() => {
    fetchData();
    pollInterval = setInterval(fetchData, 5000); // Live updates
  });

  onDestroy(() => {
    clearInterval(pollInterval);
  });
</script>

<main class="app-container">
  <!-- Sidebar -->
  <aside class="sidebar">
    <div class="brand">
      <div class="logo">🚀</div>
      <h1>Antigravity Prime</h1>
    </div>
    
    <nav>
      <button class:active={activeTab === 'dashboard'} on:click={() => activeTab = 'dashboard'}>
        Dashboard
      </button>
      <button class:active={activeTab === 'chat'} on:click={() => activeTab = 'chat'}>
        Agent Chat
      </button>
      <button class:active={activeTab === 'system'} on:click={() => activeTab = 'system'}>
        System Health
      </button>
      <button class:active={activeTab === 'logs'} on:click={() => activeTab = 'logs'}>
        Logs
      </button>
    </nav>
    
    <div class="system-status">
      {#if error}
         <div class="status-dot offline"></div>
         <span>System Offline</span>
      {:else}
         <div class="status-dot online"></div>
         <span>System Online</span>
      {/if}
    </div>
  </aside>

  <!-- Main Content -->
  <section class="content">
    
    <!-- Header -->
    <header>
      <h2>
        {activeTab === 'dashboard' ? 'Skill Registry' : 
         activeTab === 'chat' ? 'Interactive Agent' : 
         activeTab === 'system' ? 'System Diagnostics' : 'Event Logs'}
      </h2>
      {#if health}
        <div class="uptime-badge">
           <span>⏱️ Uptime: {Math.floor(health.uptime_seconds)}s</span>
           {#if health.vector_support}
             <span class="vector-tag">🧠 Memory Active</span>
           {/if}
        </div>
      {/if}
    </header>

    <!-- Error Banner -->
    {#if error}
      <div class="banner error" transition:slide>
        <strong>Connection Error:</strong> {error}. Ensure backend is running (`python antigravity.py start`).
      </div>
    {/if}

    <!-- Dashboard View -->
    {#if activeTab === 'dashboard'}
      {#if loading}
        <div class="loader">Loading Neural Interface...</div>
      {:else}
        <div class="grid" transition:fade>
          {#each skills as skill}
            <div class="card" class:enabled={skill.enabled}>
              <div class="card-header">
                <span class="badge {skill.category}">{skill.category}</span>
                {#if skill.metadata?.type}
                  <span class="type-tag">{skill.metadata.type}</span>
                {/if}
              </div>
              <h3>{skill.metadata?.name || skill.id}</h3>
              <p class="description">
                {skill.metadata?.description || `Path: ${skill.path}`}
              </p>
              
              {#if skill.metadata?.dependencies}
                <div class="deps">
                  {#each skill.metadata.dependencies as dep}
                    <span class="dep-pill">{dep}</span>
                  {/each}
                </div>
              {/if}

              <div class="actions">
                <div class="toggle">
                  <span class="status-text">{skill.enabled ? 'Active' : 'Disabled'}</span>
                  <div class="indicator" class:on={skill.enabled}></div>
                </div>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    {/if}

    <!-- Chat View -->
    {#if activeTab === 'chat'}
      <div class="chat-wrapper" transition:fade>
        <Chat />
      </div>
    {/if}

    <!-- System View -->
    {#if activeTab === 'system'}
      <div class="system-panel" transition:fade>
        <div class="metric-card">
          <h3>CPU Usage</h3>
          <div class="value">{health?.cpu_usage || 0}%</div>
          <div class="bar">
            <div class="fill" style="width: {health?.cpu_usage || 0}%"></div>
          </div>
        </div>
        <div class="metric-card">
          <h3>Memory Usage</h3>
          <div class="value">{Math.round(health?.memory_usage || 0)} MB</div>
        </div>
        <div class="metric-card">
          <h3>Platform</h3>
          <div class="value">{health?.platform || 'Unknown'}</div>
        </div>
        <div class="metric-card">
          <h3>Protocol</h3>
          <div class="value">B.L.A.S.T.</div>
        </div>
        <div class="metric-card full-width">
          <h3>Vector Memory Status</h3>
          <div class="value small">
            {health?.vector_support ? '✅ Active (ChromaDB + SentenceTransformers)' : '❌ Inactive (Install dependencies)'}
          </div>
        </div>
      </div>
    {/if}

    <!-- Logs View -->
    {#if activeTab === 'logs'}
      <div class="logs-panel" transition:fade>
        <div class="log-entry info">[SYSTEM] Antigravity Engine Initialized...</div>
        <div class="log-entry success">[SKILL] Loaded {skills.length} skills into registry.</div>
        <div class="log-entry info">[API] Health check passed by Frontend.</div>
        {#if health?.vector_support}
           <div class="log-entry success">[MEMORY] Vector DB initialized successfully.</div>
        {/if}
      </div>
    {/if}

  </section>
</main>

<style>
  :global(body) {
    background-color: #0f172a;
    color: #f1f5f9;
    font-family: 'Inter', system-ui, sans-serif;
    margin: 0;
    overflow: hidden;
  }

  .app-container {
    display: flex;
    height: 100vh;
  }

  /* Sidebar */
  .sidebar {
    width: 260px;
    background: #1e293b;
    border-right: 1px solid #334155;
    padding: 2rem;
    display: flex;
    flex-direction: column;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 3rem;
  }

  .logo { font-size: 2rem; }
  
  .brand h1 {
    font-size: 1.25rem;
    font-weight: 800;
    background: linear-gradient(to right, #60a5fa, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
  }

  nav button {
    width: 100%;
    text-align: left;
    background: transparent;
    border: none;
    color: #94a3b8;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 0.5rem;
  }

  nav button:hover {
    background: #334155;
    color: white;
  }

  nav button.active {
    background: #2563eb;
    color: white;
  }

  /* Content */
  .content {
    flex: 1;
    padding: 2rem 3rem;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
  }

  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    border-bottom: 1px solid #334155;
    padding-bottom: 1rem;
    flex-shrink: 0;
  }
  
  h2 { margin: 0; font-size: 1.5rem; color: #e2e8f0; }

  .uptime-badge {
    display: flex;
    gap: 1rem;
    align-items: center;
    font-family: monospace;
    color: #64748b;
  }
  
  .vector-tag {
    background: #064e3b;
    color: #34d399;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
  }

  /* Chat Wrapper */
  .chat-wrapper {
    flex: 1;
    min-height: 0; /* Important for flex child scrolling */
  }

  /* Grid & Cards (Same as before) */
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1.5rem;
  }

  .card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.2s;
    position: relative;
    overflow: hidden;
  }

  .card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    border-color: #60a5fa;
  }

  .card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; width: 4px; height: 100%;
    background: #334155;
    transition: background 0.2s;
  }

  .card.enabled::before { background: #10b981; }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
  }

  .badge {
    font-size: 0.7rem;
    padding: 0.25rem 0.5rem;
    border-radius: 4px;
    text-transform: uppercase;
    font-weight: 700;
  }

  .badge.memory { background: #064e3b; color: #34d399; }
  .badge.routing { background: #1e3a8a; color: #60a5fa; }
  .badge.tools { background: #4c1d95; color: #a78bfa; }
  .badge.diagnostics { background: #7f1d1d; color: #f87171; }
  .badge.ui { background: #be185d; color: #f472b6; }
  .badge.planning { background: #a16207; color: #facc15; }
  .badge.template_core { background: #27272a; color: #94a3b8; border: 1px solid #52525b; }

  h3 { margin: 0 0 0.5rem 0; font-size: 1.1rem; color: #f8fafc; }

  .description {
    color: #94a3b8;
    font-size: 0.875rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
    flex-grow: 1;
  }
  
  .deps { display: flex; gap: 0.5rem; margin-bottom: 1rem; flex-wrap: wrap; }
  .dep-pill { background: #334155; padding: 0.1rem 0.4rem; border-radius: 4px; font-size: 0.7rem; color: #cbd5e1; }

  .status-text { font-size: 0.8rem; color: #64748b; font-weight: 600; text-transform: uppercase; }
  .indicator { width: 10px; height: 10px; border-radius: 50%; background: #334155; margin-left: auto; }
  .indicator.on { background: #10b981; box-shadow: 0 0 10px rgba(16, 185, 129, 0.4); }

  /* System View */
  .system-panel {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
  .metric-card { background: #1e293b; padding: 2rem; border-radius: 12px; border: 1px solid #334155; }
  .metric-card.full-width { grid-column: span 2; }
  .metric-card h3 { color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; }
  .metric-card .value { font-size: 2.5rem; font-weight: 700; color: #f8fafc; }
  .metric-card .value.small { font-size: 1.5rem; font-weight: 500; }
  .bar { height: 6px; background: #334155; border-radius: 3px; margin-top: 1rem; overflow: hidden; }
  .fill { height: 100%; background: #60a5fa; transition: width 0.5s ease; }

  .system-status {
    margin-top: auto;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #64748b;
    font-size: 0.9rem;
  }
  .status-dot { width: 8px; height: 8px; border-radius: 50%; }
  .status-dot.online { background: #10b981; }
  .status-dot.offline { background: #ef4444; }

  /* Logs */
  .logs-panel {
    background: #000;
    padding: 1.5rem;
    border-radius: 8px;
    font-family: monospace;
    color: #22c55e;
    height: 400px;
    overflow-y: auto;
    border: 1px solid #333;
  }
  .log-entry { margin-bottom: 0.5rem; }
  .log-entry.info { color: #60a5fa; }
  .log-entry.success { color: #22c55e; }

  .banner.error {
    background: #ef4444;
    color: white;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 2rem;
  }
</style>
