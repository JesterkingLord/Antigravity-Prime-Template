
"""
🚀 Antigravity Prime CLI
The Command Center for your Agent System.

Usage:
  python antigravity.py start       # Launch both Backend & Frontend (requires npm & uvicorn)
  python antigravity.py health      # Check system health & dependencies
  python antigravity.py new-skill   # Interactive wizard to create a new skill
  python antigravity.py docker      # Launch system using Docker Compose
  python antigravity.py test        # Run automated tests (pytest)
  python antigravity.py lint        # Check code quality (ruff)
  python antigravity.py clean       # Remove temporary files (.tmp, pycache)

"""
import sys
import os
import subprocess
import time
import json
from pathlib import Path

# Configuration
c = {
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "reset": "\033[0m",
    "bold": "\033[1m"
}

ROOT_DIR = Path(__file__).parent
API_DIR = ROOT_DIR / "api"
FRONTEND_DIR = ROOT_DIR / "frontend"
SKILLS_DIR = ROOT_DIR / "antigravity" / "skills"

def log(msg, type="info"):
    if type == "info": print(f"{c['blue']}ℹ️  {msg}{c['reset']}")
    elif type == "success": print(f"{c['green']}✅ {msg}{c['reset']}")
    elif type == "warn": print(f"{c['yellow']}⚠️  {msg}{c['reset']}")
    elif type == "error": print(f"{c['red']}❌ {msg}{c['reset']}")
    elif type == "header": print(f"\n{c['bold']}{c['blue']}=== {msg} ==={c['reset']}")

def check_health():
    log("Running System Diagnostics...", "header")
    
    # 1. Environment
    if (ROOT_DIR / ".env").exists():
        log(".env file found.", "success")
    else:
        log(".env file missing!", "error")

    # 2. API Dependencies
    try:
        import fastapi
        import uvicorn
        log("API dependencies installed.", "success")
    except ImportError:
        log("API dependencies missing. Run: pip install -r api/requirements.txt", "error")

    # 3. Frontend Dependencies
    if (FRONTEND_DIR / "node_modules").exists():
        log("Frontend dependencies installed.", "success")
    else:
        log("Frontend node_modules missing. Run: cd frontend && npm install", "warn")

    # 4. Registry Integrity
    registry_path = ROOT_DIR / "antigravity" / "skill_registry.json"
    if registry_path.exists():
        try:
            with open(registry_path) as f:
                data = json.load(f)
                count = len(data.get("skills", []))
            log(f"Skill Registry loaded. {count} skills active.", "success")
        except:
            log("Skill Registry corrupted.", "error")
    else:
        log("Skill Registry missing!", "error")

def start_system():
    log("Igniting Antigravity Prime Engines (Local Mode)...", "header")
    
    # Check dependencies first
    if not (FRONTEND_DIR / "node_modules").exists():
        log("Installing Frontend Dependencies...", "warn")
        subprocess.run(["npm", "install"], cwd=FRONTEND_DIR, shell=True)
    
    # Start Backend
    log("Starting FastAPI Backend (Port 8000)...", "info")
    backend = subprocess.Popen(
        ["uvicorn", "main:app", "--reload"], 
        cwd=API_DIR,
        shell=True
    )
    
    # Start Frontend
    log("Starting Svelte Frontend (Port 5173)...", "info")
    frontend = subprocess.Popen(
        ["npm", "run", "dev"], 
        cwd=FRONTEND_DIR,
        shell=True
    )
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log("Shutting down...", "warn")
        backend.terminate()
        frontend.terminate()

def start_docker():
    log("Igniting Antigravity Prime Engines (Docker Mode)...", "header")
    if not (ROOT_DIR / "docker-compose.yml").exists():
        log("docker-compose.yml missing!", "error")
        return

    log("Building and Starting Containers...", "info")
    try:
        subprocess.run(["docker-compose", "up", "--build"], cwd=ROOT_DIR, shell=True)
    except KeyboardInterrupt:
        log("Shutting down Docker containers...", "warn")
        subprocess.run(["docker-compose", "down"], cwd=ROOT_DIR, shell=True)

def new_skill_wizard():
    log("Skill Generation Wizard", "header")
    
    name = input(f"{c['yellow']}Skill Name (e.g. email-sender): {c['reset']}").strip()
    category = input(f"{c['yellow']}Category (memory/routing/tools/ui): {c['reset']}").strip()
    description = input(f"{c['yellow']}Description: {c['reset']}").strip()
    
    if not name or not category:
        log("Name and Category required.", "error")
        return

    # Create Directory
    skill_path = SKILLS_DIR / category / name.replace("-", "_")
    skill_path.mkdir(parents=True, exist_ok=True)
    
    # Create SKILL.md
    with open(skill_path / "SKILL.md", "w") as f:
        f.write(f"""---
name: {name}
description: {description}
---

# {name.replace("-", " ").title()} Skill

## Purpose
{description}

## Usage
[Add usage instructions here]
""")
    
    # Create Metadata
    with open(skill_path / "metadata.json", "w") as f:
        json.dump({
            "skill_id": name.replace("-", "_"),
            "category": category,
            "layer": "tools",
            "ui_exposed": True
        }, f, indent=2)

    log(f"Skill created at: antigravity/skills/{category}/{name}", "success")
    log("Don't forget to register it in skill_registry.json!", "warn")

def run_tests():
    log("Running Test Suite...", "header")
    try:
        import pytest
        subprocess.run(["pytest"], cwd=ROOT_DIR)
    except ImportError:
        log("pytest not installed. Run: pip install -r api/requirements.txt", "error")

def run_lint():
    log("Running Linter (Ruff)...", "header")
    try:
        subprocess.run(["ruff", "check", "."], cwd=ROOT_DIR)
        log("Linting complete.", "success")
    except FileNotFoundError:
        log("ruff not installed. Run: pip install -r api/requirements.txt", "error")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]
    if cmd == "start": start_system()
    elif cmd == "health": check_health()
    elif cmd == "new-skill": new_skill_wizard()
    elif cmd == "docker": start_docker()
    elif cmd == "test": run_tests()
    elif cmd == "lint": run_lint()
    elif cmd == "clean": 
        # Implement clean logic if needed
        pass
    else:
        print(__doc__)

if __name__ == "__main__":
    main()
