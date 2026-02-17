# 🗺️ Template Map

This file provides a visual map of the project structure to help you navigate quickly.

```mermaid
graph TD
    Root[Antigravity Template] --> Arch[architecture/]
    Root --> Nav[navigation/]
    Root --> Tools[tools/]
    Root --> Anti[antigravity/]
    Root --> Info[information/]
    Root --> API[api/]
    Root --> Front[frontend/]

    Arch --> SOPs[SOP_TEMPLATE.md]
    
    Anti --> Skills[skills/]
    Anti --> Configs[configs/]
    Anti --> Registry[skill_registry.json]

    Skills --> Memory[memory/]
    Skills --> Routing[routing/]
    Skills --> ToolsCat[tools/]
    Skills --> Diag[diagnostics/]
    Skills --> Plan[planning/]
    Skills --> UI[ui/]

    API --> Main[main.py]
    API --> Req[requirements.txt]

    Front --> App[App.svelte]
    Front --> Chat[Chat.svelte]
```

## Quick Links
- **[Start Here](README.md)**
- **[System Architecture](architecture/README.md)**
- **[Skill Registry](antigravity/skill_registry.json)**
- **[Frontend Dashboard](frontend/README.md)**
