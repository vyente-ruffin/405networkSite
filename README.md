# 405Network

## What
The small-business IT website uses the existing Azure Static Web App and Cloudflare routing. Its contact form posts directly to FormSubmit, the established form-to-email provider, with default spam verification and a hidden honeypot. The Google inquiry link remains available. Production-origin activation and actual email receipt must be verified separately from source/deployment checks. Earlier Microsoft 365 mailbox acceptance is separate from this contact form. [Release evidence and remaining acceptance](ledger.md).

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
codex/405-contact-email     -> Python + Node checks -> named migration preview
main                       -> Python + Node checks -> Azure default
Public: apex -> Cloudflare permanent redirect -> canonical www
Public: www -> Cloudflare proxy -> Azure default
Public browser -> separate free Cloudflare page-load/source/country reports
Contact form -> FormSubmit spam check -> configured owner email
Recovery: original Google Site remains published, not current traffic
Unchanged: GoDaddy registration and existing business-email services
```

Plain HTML/CSS/JavaScript; Python 3 and Node 22 run the source checks:

```sh
python3 -m unittest discover -s tests -v
node --test tests/contact.test.cjs
python3 -m http.server 8000 --bind 127.0.0.1 --directory website
```

The deployment workflows use a distinct site-specific secret and upload only `website/`. Source checks are not substitutes for hosted browser acceptance.

## Contact delivery

The form works through a native browser POST, including when JavaScript is unavailable. Keep the default FormSubmit CAPTCHA enabled and `_honey` empty; do not add CC, automatic replies, attachments or webhooks without a separate reason. The visitor's `email` field supplies Reply-To. The provider shows its own confirmation page; no custom redirect is configured.

FormSubmit may require an activation link in the recipient's inbox for this website. Activation of another website with the same email does not establish activation here. Confirm a uniquely labeled production inquiry arrives before describing delivery as verified. FormSubmit documents 30-day submission retention; neither the site nor a redirect can establish Gmail inbox placement. The native form uses the provider's spam controls, without an Azure contact API or custom shared quota.

The origin CSP permits only FormSubmit in addition to same-origin form actions, and retains the Cloudflare analytics script allowance. No business-mail DNS changes are required. [Provider documentation](https://formsubmit.co/documentation) and [activation help](https://formsubmit.co/help).

[Complete history, release evidence and operating details](ledger.md).
