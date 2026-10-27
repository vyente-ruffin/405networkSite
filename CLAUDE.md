# Repository guidance

The current production site is https://www.405network.com/ . Azure origin is https://happy-tree-04726481e.4.azurestaticapps.net/ , app `swa-405network`, resource group `rg-405network-prod`, Youni subscription, West US 2, Free tier. Use README.md and the latest ledger.md entries for operating details.

Publish `website/` only. Root HTML, `sites/`, `designs/`, `mini-copy/`, and `hello-cli/` are separate historical/design projects and are not the current website. Preserve supplied styling, real portrait, existing redirects and business-mail DNS.

The release is plain HTML/CSS/JavaScript with no build or Azure API. Contact messages use native FormSubmit delivery and its default spam verification. Do not reintroduce the old submission-blocking script, disable CAPTCHA, or claim email delivery from source checks alone. Activation and receipt from the actual public website require separate evidence. Microsoft 365 mailbox deliverability work is a different task.

Run source checks before deployment:

```sh
python3 -m unittest discover -s tests -v
node --test tests/contact.test.cjs
python3 -m http.server 8000 --bind 127.0.0.1 --directory website
```

Main pushes alone deploy the Azure production environment. The listed preview branches deploy only the named `migration` environment. Use the site-specific GitHub deployment secret; never print it. Private execution evidence and credentials stay outside this public repository.

Cloudflare Web Analytics supplies page-load/source reporting. The origin policy includes its script host; retain security headers when changing the contact form. The existing Application Insights resource is not evidence that its JavaScript is used by this published site.
