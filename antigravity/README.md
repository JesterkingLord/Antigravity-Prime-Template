# 🧠 Antigravity Core

## 📌 Purpose
This directory houses the **Intelligence and Capabilities** of the system. It is the "Brain" to the "Body" (Tools) and "Mind" (Architecture).

### 📂 Structure
- **`skills/`**: Modular capabilities (Memory, Planning, UI generation, etc.).
- **`configs/`**: System-wide configuration files (e.g., `mcp_config.json`).
- **`skill_registry.json`**: The Master List of all active capabilities.

## 🔗 Connection
- **Inputs**: Used by `api/` to expose capabilities.
- **Logic**: Defines *what* the agent can do.
- **Outputs**: Consumed by `navigation/` to route requests.

---
*If it's smart, it lives here.*
