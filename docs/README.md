# Dev‑Automation‑Script  
**A script for every developer build to automate work with Git and Docker.**  
*Successor to **Git‑Automation‑Script***  

---  

## Table of Contents  

| Section | Description |
|---------|-------------|
| **[Overview](#overview)** | What the project does and why you’d use it |
| **[Installation](#installation)** | How to get the script up and running |
| **[Configuration](#configuration)** | Setting up the `.dev-automation.yaml` file |
| **[Usage](#usage)** | CLI commands, flags, and interactive mode |
| **[API Documentation](#api-documentation)** | Python module reference for developers who want to embed the functionality |
| **[Examples](#examples)** | Real‑world scenarios (Git flow, Docker CI, combined pipelines) |
| **[Troubleshooting & FAQ](#troubleshooting--faq)** | Common pitfalls and solutions |
| **[Contributing](#contributing)** | How to help improve the project |
| **[License](#license)** | Open‑source terms |

---  

## Overview  

`Dev-Automation-Script` (short **DAS**) is a lightweight, opinionated automation layer that wraps the most common Git and Docker commands developers need in day‑to‑day workflows.  

* **One‑liner builds** – `das build` clones, checks out a branch, builds a Docker image, tags it, and pushes it to a registry in a single command.  
* **Safety first** – All destructive actions (force‑push, image prune, etc.) require explicit `--yes` or interactive confirmation.  
* **Extensible API** – The core logic lives in a Python package (`dev_automation`) that can be imported and used programmatically.  
* **Cross‑platform** – Works on Linux, macOS, and Windows (via WSL or native Docker).  

---  

## Installation  

### Prerequisites  

| Tool | Minimum version | Why |
|------|----------------|-----|
| **Python** | 3.9+ | Runtime for the script |
| **Git** | 2.30+ | Underlying VCS operations |
| **Docker Engine** | 20.10+ | Required for image build/run |
| **pip** | 21.0+ | Python package manager |

> **Tip:** If you already have `pipx`, use it to isolate the tool from your global environment.

### Option 1 – Install from PyPI (recommended)

```bash
# Install globally (requires sudo on Linux/macOS)
pip install dev-automation-script

# Or install user‑local
pip install --user dev-automation-script
```

### Option 2 – Install with pipx (isolated, no sudo)

```bash
pipx install dev-automation-script
```

### Option 3 – Install from source (development mode)

```bash
# Clone the repo
git clone https://github.com/your-org/Dev-Automation-Script.git
cd Dev-Automation-Script

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install the package in editable mode
pip install -e .
```

### Verify the installation  

```bash
das --version
# Expected output: dev-automation-script 1.4.0
```

---  

## Configuration  

`Dev-Automation-Script` looks for a configuration file named **`.dev-automation.yaml`** in the current working directory (or any parent directory).  
If none is found, it falls back to the global config at `~/.dev-automation.yaml`.

### Minimal example  

```yaml
# .dev-automation.yaml
git:
  default_remote: origin
  default_branch: main
  commit_message_template: "[{ticket}] {summary}"
docker:
  registry: ghcr.io/your-org
  build_context: .
  dockerfile: Dockerfile
  tags:
    - latest
    - "{git.sha}"
```

### Available keys  

| Section | Key | Description | Example |
|---------|-----|-------------|---------|
| `git` | `default_remote` | Remote name used for push/pull | `origin` |
| `git` | `default_branch` | Branch to checkout when none is supplied | `main` |
| `git` | `commit_message_template` | Template for auto‑generated commits (supports `{ticket}`, `{summary}`, `{sha}`) | `"[{ticket}] {summary}"` |
| `docker` | `registry` | Target registry (including namespace) | `ghcr.io/your-org` |
| `docker` | `build_context` | Path passed to `docker build` | `.` |
| `docker` | `dockerfile` | Dockerfile location | `Dockerfile` |
| `docker` | `tags` | List of tags; can contain Jinja‑style placeholders (`{git.sha}`) | `["latest", "{git.sha}"]` |
| `hooks` | `pre_commit` | Shell command(s) executed before a commit | `["npm run lint"]` |
| `hooks` | `post_push` | Shell command(s) executed after a successful push | `["curl -X POST $CI_WEBHOOK"]` |

> **Note:** All placeholders are resolved at runtime using the `git` and `docker` context objects (see API docs).

---  

## Usage  

`das` is the entry‑point CLI. All commands share a common `--config` flag to point at an alternative config file.

```bash
das [global options] <command> [command options] [args...]
```

### Global Options  

| Flag | Alias | Description |
|------|-------|-------------|
| `--config <path>` | `-c` | Path to a custom YAML config file |
| `--verbose` | `-v` | Enable DEBUG‑level logging |
| `--quiet` | `-q` | Suppress non‑essential output |
| `--version` | `-V` | Print version and exit |
| `--help` | `-h` | Show help for the current command |

### Core Commands  

| Command | Synopsis | Description |
|---------|----------|-------------|
| `init` | `das init [--force]` | Scaffold a `.dev-automation.yaml` with sensible defaults. |
| `clone` | `das clone <repo-url> [--branch <name>]` | Clone a repo, optionally checking out a branch. |
| `checkout` | `das checkout <branch>` | Switch to an existing branch (creates it locally if missing). |
| `commit` | `das commit [-m <msg>] [--amend]` | Stage all changes and commit. If `-m` omitted, uses the template from config. |
| `push` | `das push [--remote <name>] [--tags]` | Push current branch (and optionally tags). |
| `branch` | `das branch <new-branch>` | Create and switch to a new branch. |
| `docker-build` | `das docker-build [--no-cache] [--target <stage>]` | Build Docker image using config tags. |
| `docker-run` | `das docker-run [--detach] [--env KEY=VAL...]` | Run the built image locally. |
| `docker-push` | `das docker-push [--all-tags]` | Push image(s) to the configured registry. |
| `pipeline` | `das pipeline` | Execute the full “clone → checkout → build → push” workflow in one go. |
| `status` | `das status` | Show a concise Git + Docker status summary. |
| `clean` | `das clean [--docker] [--git]` | Remove dangling Docker images and/or Git refs. |

#### Example: Full CI‑like pipeline  

```bash
das pipeline \
    --repo https://github.com/your-org/my-service.git \
    --branch feature/awesome \
    --docker-tag v1.2.3 \
    --yes
```

What happens under the hood:

1. **Clone** the repo (or fetch if already present).  
2. **Checkout** `feature/awesome`.  
3. **Run** any `hooks.pre_commit` (e.g., lint).  
4. **Commit** any pending changes using the template.  
5. **Push** the branch and tags.  
6. **Docker build** with tags `latest` and `v1.2.3`.  
7. **Docker push** to `ghcr.io/your-org/my-service`.  

---  

## API Documentation  

The package is importable as `dev_automation`. Below is a concise reference; full docstrings are available via `help()` or generated Sphinx docs (`make html` in `docs/`).

### Package layout  

```
dev_automation/
├─ __init__.py
├─ cli.py                # Click‑based command line entry point
├─ config.py             # Config loader &