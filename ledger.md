# 405Network — detailed ledger

[Current overview](README.md)

## 2026-09-14 — Verbatim README before migration

```markdown
# 405Network Website Rebuild

## Original Site Content (405network.com)

Source: Google Sites (to be migrated to Azure Static Web Apps)

---

## Company Information

| Field | Value |
|-------|-------|
| **Company Name** | 405Network Inc. |
| **Tagline** | "Information Technology, Reimagined" |
| **Location** | Orange County, CA |
| **Established** | 2011 |
| **Experience** | 25+ years combined IT expertise |
| **Target Market** | Small to Medium Businesses (SMB) |
| **Business Type** | Managed Service Provider (MSP) |

---

## Mission Statement

> At 405Network, we offer comprehensive IT support plans tailored to meet the unique needs of your business.

> Let 405Network be your Chief Technology (CTO), Cloud, Infrastructure and AI Officer.

---

## Services Offered

### Support & Communication
- Text-based support from technical experts
- Slack/Microsoft Teams integration for real-time collaboration

### Device Management
- Windows device management and optimization
- macOS device management

### Cloud & Administration
- G-Suite administration and support
- Microsoft Azure cloud and DevOps services

### Infrastructure
- Server performance optimization and maintenance
- Network monitoring and management

---

## Pricing

**Pricing Philosophy**: "Simple, Transparent Pricing"

### Silver Plan
- **Target**: Small businesses with essential IT support needs
- **Theme Color**: Blue (#007bff)
- **Features**:
  - ✅ Remote Monitoring and Management (RMM)
  - ✅ Help Desk Support
  - ✅ Patch Management
  - ✅ Antivirus and Anti-malware Protection
  - ✅ Basic Backup and Disaster Recovery (BDR)
- **CTA**: [Learn More](https://docs.google.com/forms/d/e/1FAIpQLSeBRCLx9K78KhcanobwXIDd9fmf3AgdXb6NbJpk-oio46CU_g/viewform)

### Gold Plan
- **Target**: Medium-sized businesses needing advanced IT support
- **Theme Color**: Gold (#ffb700)
- **Features**:
  - ✅ All Silver Plan Services
  - ✅ Extended Help Desk Support (12x5)
  - ✅ Bi-weekly Patch Management
  - ✅ Advanced Threat Detection
  - ✅ Comprehensive Backup and Disaster Recovery
- **CTA**: [Learn More](https://docs.google.com/forms/d/1QTDIVDihcClO4fauoLUmUKPQvABHGS5RqsEDi3f6aTw/prefill)

### Platinum Plan
- **Target**: Large businesses with complex IT needs
- **Theme Color**: Platinum (#e5e4e2)
- **Features**:
  - ✅ All Gold Plan Services
  - ✅ 24x7 Help Desk Support
  - ✅ Weekly Patch Management
  - ✅ Full Suite Security Solutions
  - ✅ Advanced Business Continuity
  - ✅ Strategic IT Consulting
- **CTA**: [Learn More](https://docs.google.com/forms/d/1QTDIVDihcClO4fauoLUmUKPQvABHGS5RqsEDi3f6aTw/prefill)

---

## Team

### Leadership
- **Owner/Senior Engineer**: Extensive background in IT infrastructure
- **Senior Relationship Manager**: Focus on operational efficiency

---

## Brand Guidelines

### Name Usage
- Full: **405Network Inc.**
- Short: **405Network** or **405 Network**
- The "405" references the famous 405 freeway in Los Angeles/Orange County area

### Tone
- Professional but approachable
- Modern and tech-forward
- Trustworthy and reliable

---

## New Site Requirements

### Pages
1. **Landing Page** (index.html)
   - Hero with tagline
   - Services overview
   - CTA to pricing

2. **Pricing Page** (pricing.html)
   - Pricing tiers
   - Feature comparison
   - Contact CTA

### Technical Stack
- **Hosting**: Azure Static Web Apps
- **CI/CD**: GitHub Actions
- **Analytics**: Application Insights
- **Domain**: 405network.com (pending DNS configuration)

### Design Options Created
1. `designs/design-1-minimal/` - Clean, whitespace, subtle animations
2. `designs/design-2-bold/` - Oversized typography, vibrant colors
3. `designs/design-3-gradient/` - Glassmorphism, gradient backgrounds
4. `designs/design-4-dark/` - Dark mode, neon accents
5. `designs/design-5-corporate/` - Navy, enterprise, trust-building

---

## Azure Resources

| Resource | Name | URL |
|----------|------|-----|
| Resource Group | 405network-website | westus |
| Static Web App | 405network-site | https://blue-wave-0b1655b10.2.azurestaticapps.net |
| Application Insights | 405network-insights | Traffic tracking enabled |
| GitHub Repo | vyente-ruffin/405networkSite | CI/CD configured |

---

## Azure DevOps

**Project**: https://dev.azure.com/vyente/405site

### Completed
- Epic 1: Infrastructure Setup
- Epic 2: Validation (TDD)

### In Progress
- Epic 3: Build 405Network Site
  - Task 3.1: Initialize Astro Project
  - Task 3.2: Build Landing Page
  - Task 3.3: Build Pricing Page
  - Task 3.4: Configure Custom Domain

---

## Contact Information

> *Update with actual contact details*

- **Phone**: TBD
- **Email**: TBD
- **Address**: Orange County, CA

---

## Copyright

© 2024 405Network Inc. All rights reserved.

```

## 2026-09-14 — Candidate import and delivery preparation

Imported only the ten reviewed supplied website files into website/. Original design, copy, images and motion are unchanged. Existing repository history and archived designs remain outside the deployed tree. Public-tree existence test failed first, then passed after import. No public-domain release yet.

## 2026-09-14 — Static delivery safeguards and verification

Nine Python unittest checks pass: supplied-file inventory and bytes; public allowlist; local assets/fragments/labels; intentionally disabled contact/fallback; legacy routes and genuine-not-found policy; reference security headers without unused backend; main-only production and feature-only named preview. Four behavior slices were observed RED before import/configuration and GREEN afterward. Workflows use separate concurrency and the site-specific deployment secret, uploading website/ only. Independent review and hosted acceptance are pending, not reported as completed.

Official anchors: https://docs.python.org/3/library/unittest.html ; https://learn.microsoft.com/azure/static-web-apps/configuration ; https://learn.microsoft.com/azure/static-web-apps/build-configuration ; https://learn.microsoft.com/azure/static-web-apps/named-environments .

## 2026-09-14 — Independent source review passed

Independent read-only review found no blocking security or logic issues and independently ran all nine unittest checks successfully. Hosted redirects, headers, browser journeys and environment isolation remain the next acceptance task.

## 2026-09-14 — Hosted validator correction

First preview run 34903945045 passed nine tests but Azure rejected duplicate route `/home/`: trailing-slash variants normalize to the same route. Corrected the configuration to one rule per normalized legacy route; the test still checks all four requested URL forms and now rejects duplicate normalized rules (observed RED then GREEN). Actual hosted HTTP verification of all four remains required. No supplied design bytes changed. The reference-pinned action emits an unexpected deployment_environment input metadata warning; the input is passed into its container, but actual preview isolation is not assumed until Azure readback.

## 2026-09-14 — Effective touch-area correction

Hosted phone hit-testing found seven small links whose effective vertical hit areas were below the blueprint 44px gate. Added transparent positioned pseudo-elements to expand only link hit areas, without changing text, image, layout, link targets or motion. Native local hit-testing passed all 18 desktop/phone samples afterward; element layout heights stayed unchanged. Original ten-file manifest remains intact: the byte-preservation test permits only the exact reviewed additive motion.css suffix. New regression observed RED then GREEN; ten unittest tests now pass. Hosted recheck and independent review pending.

## 2026-09-14T23:03:19.290457+00:00 — Hosted preview acceptance passed; public cutover pending

Application revision `006e0de8db5c3e87004a18fee07127f2fd8becab` passed [GitHub preview run 34905585765](https://github.com/vyente-ruffin/405networkSite/actions/runs/34905585765). The named migration environment is Ready at https://happy-tree-04726481e-migration.westus2.4.azurestaticapps.net/ . The default environment and public Google Site remain unchanged.

Verified: ten unittest tests; 22 final HTTP checks (all ten application files match, all four legacy URL forms redirect correctly, eight private/missing paths return genuine404); security headers; 78 corrected desktop and66 corrected phone internal interactions across all three service personas on first/repeat visits; 24 corrected external opens with actual loaded titles; 12 typed contact journeys with no sending/storage/false success; keyboard first/repeat focus, reduced motion, no-script safety and data-saving preference; 18 effective44px target samples; 35 section checks across five viewport widths and actual image decoding.

Failed attempts remain recorded in the private project engineering ledger: duplicate normalized routes rejected by Azure before the minimal fix; background-tab rendering/scroll timing and a browser transport interruption corrected in the test setup; small touch targets corrected without visible layout changes. Do not treat the old hash-only browser rows as final viewport acceptance. The reference-pinned uploader emits an input-metadata warning, but actual Azure readback proves named-preview isolation and unchanged default.

The Free domain zone was created, but its configuration is access-blocked; no authoritative DNS, registration, email or public website destination was changed. Full configuration parity, received analytics reports and public-release acceptance are not complete. This documentation-only update uses GitHub's documented skip instruction to avoid redeploying unchanged application files; it does not waive tests on a future release.
