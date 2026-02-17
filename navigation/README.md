# 🧭 Layer 2: Navigation (Routing)

## 📌 Purpose
This directory houses the **Decision logic** that routes requests between Strategy (Layer 1) and Execution (Layer 3).

### 🚦 Functions
- **Router**: Determines which Skill or Tool to call based on user intent.
- **Orchestrator**: Manages multi-step workflows.
- **Guardrails**: Filters requests before they reach sensitive tools.

## 🔗 Connection
- **Inputs**: User requests, API calls.
- **Logic**: Uses `antigravity/skills/routing/` logic.
- **Outputs**: Directs traffic to `tools/`.

---
*This layer is the "Brain" making choices in real-time.*
