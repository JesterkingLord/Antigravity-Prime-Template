# 🛠️ Layer 3: Tools (Execution)

## 📌 Purpose
This directory contains the **Atomic, Deterministic Scripts** that perform actual work.

### ⚙️ Guidelines
- **Deterministic**: Same input = Same output. Always.
- **Isolated**: Tools do not know about "state" or "context" outside their arguments.
- **Safe**: Built with error handling and validation.

### 📂 Categories
- `scripts/`: Python/Bash/Node scripts for automation.
- `utils/`: Helper functions.
- `connectors/`: API wrappers for external services.

---
*This layer is the "Hands" doing the work.*
