# 405Network

## What
The supplied small-business IT support and consulting website is verified on the Azure production origin, with both custom-host certificates ready. Cloudflare authority and the apex-to-www redirect are active; the original Google Site still serves the public domain pending the separate cutover. The on-page contact form is intentionally disabled; the existing inquiry-form link remains available. [Release evidence and remaining acceptance](ledger.md).

## Where
- Current public site: https://www.405network.com/
- Tested preview: https://happy-tree-04726481e-migration.westus2.4.azurestaticapps.net/
- Verified production origin: https://happy-tree-04726481e.4.azurestaticapps.net/
- Repository: https://github.com/vyente-ruffin/405networkSite
- Release content: `website/` only. Historical root pages and design archives are not uploaded.
- Hosting target: existing `swa-405network`, Free / West US 2, origin `happy-tree-04726481e.4.azurestaticapps.net`.

## Why
Preserve the supplied design while moving to tested, isolated preview and production delivery. Registration and business email remain separate from website hosting.

## How
```text
feature/405network-migration -> Python checks -> named migration preview
main                       -> Python checks -> Azure default
Current public: Visitors -> canonical www -> original Google Site
Future public cutover: Visitors -> Cloudflare -> Azure default
Unchanged: GoDaddy registration and existing business-email services
```

Plain HTML/CSS/JavaScript; Python 3 is the only local test dependency:

```sh
python3 -m unittest discover -s tests -v
python3 -m http.server 8000 --bind 127.0.0.1 --directory website
```

The deployment workflows use a distinct site-specific secret and upload only `website/`. Source checks are not substitutes for hosted browser acceptance.

[Complete history, release evidence and operating details](ledger.md).
