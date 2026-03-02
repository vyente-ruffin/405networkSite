# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

405Network Inc. website rebuild - migrating from Google Sites to Azure Static Web Apps. This is a B2B Managed Service Provider (MSP) serving small-to-medium businesses in Orange County, CA.

**Production URL**: https://blue-wave-0b1655b10.2.azurestaticapps.net

## Tech Stack

- **Frontend**: Vanilla HTML/CSS/JavaScript (no framework or bundler)
- **Libraries** (via CDN): Three.js (3D particles), GSAP (animations), ScrollTrigger
- **Hosting**: Azure Static Web Apps
- **CI/CD**: GitHub Actions → auto-deploys on push to main
- **Analytics**: Application Insights

## Development

This is a static site with no build step. Edit HTML files directly and push to deploy.

### Local Preview
```bash
# Any static file server works
python -m http.server 8000
# or
npx serve .
```

### Deployment
Push to `main` branch triggers automatic deployment via GitHub Actions.

## Project Structure

```
/                           # Root site (index.html is main landing page)
├── sites/                  # Production design variations (8 versions)
│   ├── arctic-minimalism/  # ✅ Approved - Scandinavian minimal
│   ├── warm-brutalism/     # ✅ Approved (in designs/ as v23)
│   └── ...                 # Other design options
├── designs/                # Design development archive (25 iterations)
│   └── DESIGN_PREFERENCES.md  # Design guidelines and approvals
└── hello-cli/              # Separate Python CLI sub-project
```

## Design Guidelines

See `designs/DESIGN_PREFERENCES.md` for full details.

**Approved aesthetics**: Clean minimal Scandinavian, warm organic brutalism, premium holographic
**Rejected aesthetics**: Cyberpunk/neon, terminal/command-line, "hacker" vibes

All designs must be:
- Mobile responsive (breakpoints: 480px, 768px, 1024px)
- WCAG 2.1 AA compliant
- Gracefully degrade without Three.js

## hello-cli (Python Sub-Project)

A separate Typer-based CLI in `/hello-cli/` used for testing workflows.

```bash
cd hello-cli

# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -e .

# Run tests
pytest tests/ -v

# Run CLI
hello Alice
```

## Azure Resources

| Resource | Name |
|----------|------|
| Resource Group | 405network-website |
| Static Web App | 405network-site |
| Application Insights | 405network-insights |
| Region | westus |
