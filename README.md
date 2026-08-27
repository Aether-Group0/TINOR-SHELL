# Tinor Shell

[![License](https://img.shields.io/github/license/Aether-Group0/TINOR-SHELL)](LICENSE) [![Last Commit](https://img.shields.io/github/last-commit/Aether-Group0/TINOR-SHELL)](https://github.com/Aether-Group0/TINOR-SHELL/commits) [![Top Language](https://img.shields.io/github/languages/top/Aether-Group0/TINOR-SHELL)](https://github.com/Aether-Group0/TINOR-SHELL) [![Open Issues](https://img.shields.io/github/issues/Aether-Group0/TINOR-SHELL)](https://github.com/Aether-Group0/TINOR-SHELL/issues) [![Made with Python](https://img.shields.io/badge/python-3.8%2B-blue?logo=python)](https://www.python.org/)

Tinor Shell is a wrapper around the Windows cmd experience that provides additional convenience features and a small set of network, chat and lookup utilities. It is intended for experimental and educational use only.

Important: Tinor Shell includes code that launches network scans, starts servers and launches external tools. These capabilities are potentially dangerous if misused or run on production networks. Read the Security & Safe Usage section before running anything.

---

## Table of Contents

- [Features](#features)
- [Quick Warnings](#quick-warnings)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Available Commands](#available-commands)
- [Examples](#examples)
- [Developer Notes](#developer-notes)
- [Security & Safe Usage](#security--safe-usage)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- Interactive shell wrapper around OS shell commands.
- Simple commands for:
  - Ping / network mapping (nmap)
  - Port scans
  - Lookup (opens a browser search tab)
  - LAN/WAN chat server & client helpers
  - SSH client/server helpers
  - Social Finder GUI helper (Tkinter-based)
- Desktop error notifications (Windows)

This is not a hardened production shell — it is a convenience/learning tool.

---

## Quick Warnings

- The project runs external programs (nmap, Fern-Multi-Tool, etc.) and starts network services. Use in a controlled/test environment only.
- Do not run on networks where you do not have authorization to scan or host services.
- The code executes user-supplied shell commands (the project uses `subprocess.run(..., shell=True)` in places). This is inherently unsafe if untrusted input may reach it.

---

## Requirements

The repository's `Tinor Shell/Requirements.txt` lists dependencies; here are practical recommendations:

- Windows 10 / 11 (recommended — some code uses winotify and `cls`)
- Python 3.8+ (3.10+ recommended)
- External tools (installed separately, available on PATH):
  - Nmap
  - Fern-Multi-Tool (if using `find_info` functionality)
- Python packages (install via pip):
  - requests
  - winotify (Windows notifications)
  - tkinter (usually included with Windows Python; used by social finder GUI)

Note: the listed Requirements.txt includes an item `python 1.14` which is incorrect — use Python 3.x.

---

## Installation

1. Clone the repo:
   > git clone https://github.com/Aether-Group0/TINOR-SHELL.git

2. Install Python dependencies (in a virtual environment recommended):
   > python -m venv venv
   > venv\Scripts\activate
   > pip install -r "Tinor Shell/Requirements.txt"

   Manually install external binaries (nmap, Fern-Multi-Tool) per the project code paths and ensure they are on PATH.

3. (Optional) If running on Windows, ensure `winotify` is installed and you have permission to show desktop notifications.

---

## Usage

Start the shell wrapper by running the main script:

> python "Tinor Shell/Processor.py"

Then enter commands at the `>` prompt. The wrapper interprets a number of small commands and otherwise executes the input as a shell command.

---

## Available Commands

(These reflect the behavior implemented in `Processor.py`)

- ping
- SSH -c <args> — start SSH client helper (module dependent)
- SSH -s <args> — start SSH server helper
- SF -s — start Social Finder GUI (Tkinter)
- nm <args> — network mapping helper (calls nmap)
- LANC -c — start LAN chat client handler
- LANC -s — start LAN chat server handler
- WAN -c — start WAN chat client handler
- WAN -s — start WAN chat server handler
- sop <args> — scan for open ports (calls nmap)
- lp <search query> — Lookup: opens a Google search in your browser
- clear — clears console and shows the Tinor Shell banner
- fi <args> — find info (calls an external tool; in-progress)
- help — displays the help text
- exit — exits the shell

Notes:
- Many helpers call external programs or expect other modules to be present; ensure those dependencies are installed and configured.
- Commands like `Run_Command` will execute arbitrary shell input. Use only trusted input.

---

## Examples

- Run a lookup:
  > lp python subprocess security

  This will open a Google search for `python subprocess security`.

- Scan for open ports (example; requires nmap):
  > sop 192.168.1.0/24

- Start the LAN server:
  > LANC -s

(These examples assume the external tools are installed and available on your PATH.)

---

## Developer Notes

- Entry point: `Tinor Shell/Processor.py`
- Utils are in `Tinor Shell/Utils/` — server and client code for LAN/WAN chat, SSH helpers, network utilities, and a small Tkinter GUI for social finder.
- Notifications: `Tinor Shell/Utils/__Notification_Util__.py` uses `winotify` (Windows-only).
- Some helper files and directories may contain stub or in-progress code — review before running.

---

## Security & Safe Usage

Before running or publishing:
- Always run the project in an isolated environment (virtual machine, disposable VM/container) when testing network or server features.
- Do not run on networks where you are not authorized to scan or host services.
- Avoid running as an administrator or root account.
- Sanitize or avoid passing untrusted input into functions that call `subprocess` with `shell=True`.
- If you plan to publish the repository, search for and remove secrets from code and commit history (API keys, private keys, credentials).
- Rotate any credentials that were accidentally exposed.

Suggested code hardening:
- Avoid shell=True. Use argument lists for subprocess.run (e.g., `subprocess.run(["program", "arg1"])`).
- Validate and whitelist inputs that are forwarded to external programs.
- Bind servers to localhost by default (127.0.0.1) and require explicit configuration to listen on external interfaces.

---

## Contributing

- This project appears to be an in-progress prototype. If you would like contributions:
  - Open issues describing intended behavior, security hardening tasks, or feature requests.
  - Provide clear tests and environment setup instructions for anything that starts network services.

---

## License

Review the repository LICENSE file for licensing details.

---

## Contact / Further help

If you want, I can:
- commit a recommended `.gitignore` for you,
- scan the entire repo for secret-looking patterns (API keys, private keys, IP addresses, absolute paths),
- or propose code changes to reduce subprocess risks (remove shell=True and add input validation).

Please tell me which of these you want next.
