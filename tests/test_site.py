"""Static release checks using Python's documented unittest and pathlib APIs.

https://docs.python.org/3/library/unittest.html
These source checks complement, not replace, hosted browser acceptance.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "website"
PUBLIC_FILES = {
    "index.html", "styles.css", "motion.css", "contact.css", "motion.js",
    "contact.js", "assets/modern-office.jpg", "assets/it-workspace.jpg",
    "assets/business-network.jpg", "assets/vyente-ruffin.jpg",
}


ACCESSIBLE_TAP_AREAS = '''
/* Expand effective tap areas without changing supplied layout or visible design.
   Generated child boxes: https://drafts.csswg.org/css-pseudo/#generated-content */
.wordmark,.text-link,.site-header nav>a,.contact-fallback{position:relative}
.wordmark::after,.text-link::after,.site-header nav>a::after,.contact-fallback::after{
  content:"";position:absolute;left:0;right:0;top:50%;height:100%;min-height:44px;
  transform:translateY(-50%);
}
'''


class Document(HTMLParser):
    """Collect actual markup references without a browser dependency."""

    def __init__(self, text):
        """Parse the supplied HTML into tag/attribute pairs."""
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        """Retain tags for local-reference and disabled-control assertions."""
        self.tags.append((tag, dict(attrs)))


class PackageTests(unittest.TestCase):
    """Keep the reviewed public subtree separate from repository history."""

    def test_legacy_routes_and_real_not_found_policy(self):
        """Hosting must redirect old Google URLs without a catch-all success."""
        import json
        config_path = SITE / "staticwebapp.config.json"
        self.assertTrue(config_path.is_file(), "Azure hosting configuration is missing")
        config = json.loads(config_path.read_text())
        expected = {"/home": "/", "/home/": "/",
                    "/pricing-and-services": "/#help", "/pricing-and-services/": "/#help"}
        # Azure's live validator treats trailing-slash forms as the same route.
        # Preserve all four URL expectations without submitting duplicate rules.
        rules = config["routes"]
        self.assertEqual(len({r["route"].rstrip("/") for r in rules}), len(rules),
                         "Azure rejects duplicate normalized route patterns")
        for request, destination in expected.items():
            matches = [r for r in rules if r["route"].rstrip("/") == request.rstrip("/")]
            self.assertEqual(len(matches), 1, request)
            self.assertEqual(matches[0]["redirect"], destination)
            self.assertEqual(matches[0]["statusCode"], 301)
        self.assertNotIn("navigationFallback", config)
        self.assertNotIn("responseOverrides", config)

    def test_production_delivery_is_main_only_public_tree(self):
        """A feature or PR must never reach the production uploader."""
        flow = (ROOT / ".github/workflows/azure-static-web-apps.yml").read_text()
        self.assertIn("app_location: website", flow)
        self.assertIn("branches: [main]", flow)
        self.assertIn("if: github.event_name == 'push' && github.ref == 'refs/heads/main'", flow)
        self.assertIn("production_branch: main", flow)
        self.assertNotIn("deployment_environment:", flow)
        self.assertNotIn("pull_request:", flow)
        self.assertNotIn("workflow_dispatch:", flow)
        self.assertIn("api_location: ''", flow)
        self.assertIn("output_location: ''", flow)
        self.assertIn("skip_app_build: true", flow)
        self.assertIn("AZURE_STATIC_WEB_APPS_405NETWORK_API_TOKEN", flow)
        self.assertLess(flow.index("python3 -m unittest discover -s tests -v"),
                        flow.index("uses: Azure/static-web-apps-deploy@"))
        self.assertIn("cancel-in-progress: false", flow)

    def test_preview_delivery_cannot_target_default(self):
        """The approved feature branch must always use named migration preview."""
        preview = ROOT / ".github/workflows/azure-preview.yml"
        self.assertTrue(preview.is_file(), "Preview-only workflow is missing")
        flow = preview.read_text()
        self.assertIn("branches: [feature/405network-migration]", flow)
        self.assertIn("if: github.event_name == 'push' && github.ref == 'refs/heads/feature/405network-migration'", flow)
        self.assertIn("deployment_environment: migration", flow)
        self.assertNotIn("production_branch:", flow)
        self.assertNotIn("pull_request:", flow)
        self.assertNotIn("workflow_dispatch:", flow)
        self.assertIn("app_location: website", flow)
        self.assertIn("api_location: ''", flow)
        self.assertIn("output_location: ''", flow)
        self.assertIn("skip_app_build: true", flow)
        self.assertIn("AZURE_STATIC_WEB_APPS_405NETWORK_API_TOKEN", flow)
        self.assertIn("group: 405network-migration", flow)
        self.assertIn("cancel-in-progress: true", flow)
        self.assertLess(flow.index("python3 -m unittest discover -s tests -v"),
                        flow.index("uses: Azure/static-web-apps-deploy@"))

    def test_public_tree_has_no_extra_files_or_symlinks(self):
        """Only the approved website and hosting configuration may be uploaded."""
        actual = {p.relative_to(SITE).as_posix() for p in SITE.rglob("*") if p.is_file()}
        self.assertEqual(actual, PUBLIC_FILES | {"staticwebapp.config.json"})
        self.assertFalse(any(p.is_symlink() for p in SITE.rglob("*")))

    def test_supplied_design_bytes_are_preserved(self):
        """Characterize the reviewed supplied bytes, not a re-created design."""
        manifest = json.loads((ROOT / "tests/public-manifest.json").read_text())
        self.assertEqual(set(manifest), PUBLIC_FILES)
        for name, digest in manifest.items():
            with self.subTest(file=name):
                content = (SITE / name).read_bytes()
                # Keep the original manifest intact: only this reviewed additive
                # hit-area patch may differ, never the supplied visible design.
                if name == "motion.css" and content.endswith(ACCESSIBLE_TAP_AREAS.encode()):
                    content = content[:-len(ACCESSIBLE_TAP_AREAS.encode())]
                self.assertEqual(hashlib.sha256(content).hexdigest(), digest)

    def test_effective_tap_area_patch_is_present(self):
        """Guard the precise additive fix; real pointer hit-testing is in T2."""
        self.assertTrue((SITE / "motion.css").read_text().endswith(ACCESSIBLE_TAP_AREAS))

    def test_local_assets_fragments_and_labels_resolve(self):
        """Local hyperlinks, CSS images and accessible labels must have targets."""
        document = Document((SITE / "index.html").read_text())
        ids = [attrs["id"] for _, attrs in document.tags if "id" in attrs]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate HTML IDs")
        for tag, attrs in document.tags:
            if tag == "label":
                self.assertIn(attrs["for"], ids)
            for key in ("aria-labelledby", "aria-describedby"):
                for target in attrs.get(key, "").split():
                    self.assertIn(target, ids)
            for key in ("src", "href"):
                value = attrs.get(key, "")
                uri = urlsplit(value)
                if uri.scheme or uri.netloc:
                    continue
                if uri.path:
                    self.assertTrue((SITE / unquote(uri.path)).is_file(), value)
                if uri.fragment:
                    self.assertIn(uri.fragment, ids)
        for css in SITE.glob("*.css"):
            for value in re.findall(r"url\(['\"]?([^)'\"]+)", css.read_text()):
                if not urlsplit(value).scheme:
                    self.assertTrue((css.parent / value).is_file(), value)

    def test_disabled_contact_has_honest_notice_and_external_fallback(self):
        """Characterize disabled delivery without transmitting a test inquiry."""
        html = (SITE / "index.html").read_text()
        document = Document(html)
        buttons = [a for t, a in document.tags if t == "button" and a.get("type") == "submit"]
        self.assertEqual(len(buttons), 1)
        self.assertIn("disabled", buttons[0])
        self.assertIn("This form does not send or save messages.", html)
        self.assertTrue(any(t == "a" and a.get("href", "").startswith(
            "https://docs.google.com/forms/d/e/") for t, a in document.tags))
        script = (SITE / "contact.js").read_text()
        self.assertIn("event.preventDefault()", script)
        for forbidden in ("fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage"):
            self.assertNotIn(forbidden, script)

    def test_security_headers_match_reference_without_unused_backend(self):
        """Use the reference origin policy; analytics allowance is a later edge rule."""
        config = json.loads((SITE / "staticwebapp.config.json").read_text())
        headers = config["globalHeaders"]
        self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(headers["X-Frame-Options"], "DENY")
        self.assertEqual(headers["Referrer-Policy"], "strict-origin-when-cross-origin")
        self.assertIn("script-src 'self';", headers["Content-Security-Policy"])
        self.assertIn("frame-ancestors 'none';", headers["Content-Security-Policy"])
        self.assertNotIn("unsafe-inline", headers["Content-Security-Policy"])
        self.assertNotIn("platform", config)

    def test_supplied_public_files_exist(self):
        """The supplied ten-file website must be present before delivery."""
        actual = {p.relative_to(SITE).as_posix() for p in SITE.rglob("*") if p.is_file()}
        self.assertTrue(PUBLIC_FILES.issubset(actual), PUBLIC_FILES - actual)


if __name__ == "__main__":
    unittest.main()
