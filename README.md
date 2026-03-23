# SMBFlow - Lightweight AI Workflow Scheduler for Small Businesses

SMBFlow is an open-source, lightweight workflow automation tool designed specifically for small businesses who want AI-powered automation without the complexity of enterprise tools.

## Features

- 📋 **Pre-built Workflow Templates** - Ready-to-use templates for common SMB processes
- 🔌 **Simple Integrations** - Connect to Notion, Google Sheets, Slack, Email
- 🤖 **AI-Powered** - Local AI agent support via Ollama or OpenAI
- 🔒 **Run Locally** - Your data stays on your machine
- ⚡ **No-Code** - Simple visual workflow builder for non-technical users

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Run
python src/app.py

# Access at http://localhost:5000
```

## Default Workflow Templates

1. **Client Onboarding** - Automated welcome sequence for new clients
2. **Invoice Follow-up** - Automatic payment reminder workflow
3. **Weekly Report** - Auto-generate and send weekly KPI reports
4. **Lead Nurture** - Follow-up sequence for new leads
5. **Support Ticket** - Auto-categorize and route support requests

## Architecture

```
smbflow/
├── src/           # Core application code
├── workflows/     # Workflow templates
└── tests/         # Test suite
```

## License

MIT