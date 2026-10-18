"""Builds this site's pages from the private daily-app repo's docs/privacy-policy.md (the part below the '---' line).
Run from this repo's root: python3 tools/build.py <path to daily-app>/docs/privacy-policy.md
Needs the `markdown` package (pip install markdown)."""
import re, sys, html
from pathlib import Path
import markdown

out = Path(".")
src = Path(sys.argv[1]).read_text()
pub = src.split("\n---\n", 1)[1]
# Placeholders that can't stay on a public page until Jason confirms them.
pub = pub.replace("Effective date: [EFFECTIVE DATE]",
                  "**Draft.** This policy describes the Daily Lift beta and takes effect when the beta opens on Google Play. Last updated October 18, 2026.")
pub = pub.replace("is made by [DEVELOPER NAME], an independent developer.", "is made by an independent developer.")
pub = pub.replace("[DEVELOPER NAME], jz.dailyapp@gmail.com", "Daily Lift, jz.dailyapp@gmail.com")
pub = pub.replace("[12 months]", "12 months")
pub = pub.replace("**App lock (optional)** uses your phone's own screen lock (fingerprint, face or device PIN).",
                  "**App lock (optional)** asks for a PIN you set (or, where the app offers it, your phone's own screen lock) before the app opens.")
assert "[" not in re.sub(r"\[[^\]]+\]\([^)]+\)", "", pub), "placeholder left: " + str(re.findall(r"\[[^\]]+\](?!\()", pub))
body = markdown.markdown(pub.strip(), extensions=["extra", "sane_lists"])
body = body.replace("<h1>", '<h1 id="top">', 1)

CSS = """
:root { --bg: #f7f7f5; --fg: #1d1d1b; --muted: #5b5b57; --card: #ffffff; --line: #e3e3de; --ac: #2f6b4f; }
@media (prefers-color-scheme: dark) { :root { --bg: #141413; --fg: #ecece8; --muted: #a8a8a2; --card: #1e1e1c; --line: #33332f; --ac: #7fc4a0; } }
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--bg); color: var(--fg); font: 17px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
main { max-width: 720px; margin: 0 auto; padding: 32px 16px 64px; }
header.site { display: flex; gap: 12px; align-items: baseline; justify-content: space-between; flex-wrap: wrap; border-bottom: 1px solid var(--line); padding-bottom: 12px; margin-bottom: 24px; }
header.site a.home { font-weight: 700; font-size: 20px; color: var(--fg); text-decoration: none; }
nav a { margin-left: 16px; }
a { color: var(--ac); }
h1 { font-size: 30px; line-height: 1.2; margin: 8px 0 12px; }
h2 { font-size: 21px; margin: 32px 0 8px; }
ul { padding-left: 22px; }
li { margin: 4px 0; }
p, li { overflow-wrap: anywhere; }
.card { background: var(--card); border: 1px solid var(--line); border-radius: 14px; padding: 16px 18px; margin: 16px 0; }
footer { color: var(--muted); font-size: 14px; margin-top: 48px; border-top: 1px solid var(--line); padding-top: 12px; }
"""

def page(title, desc, content):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="icon" href="icon-192.png" sizes="192x192">
<meta name="theme-color" content="#12142b">
<style>{CSS}</style>
</head>
<body>
<main>
<header class="site"><a class="home" href="./"><img src="icon.svg" alt="" width="28" height="28" style="vertical-align: -6px; border-radius: 22%; margin-right: 8px">Daily Lift</a><nav><a href="privacy.html">Privacy</a><a href="mailto:jz.dailyapp@gmail.com">Contact</a></nav></header>
{content}
<footer>Daily Lift · <a href="mailto:jz.dailyapp@gmail.com">jz.dailyapp@gmail.com</a></footer>
</main>
</body>
</html>
"""

out.mkdir(parents=True, exist_ok=True)
(out / "privacy.html").write_text(page("Daily Lift privacy policy", "What the Daily Lift app does with your information.", body))
(out / "index.html").write_text(page("Daily Lift", "A lifting log that knows the rest of your day: workouts, a daily supplement and medication checklist, and insights across both.", """
<h1>Daily Lift</h1>
<p>A lifting log that knows the rest of your day. Log workouts with real progression, keep a daily checklist for supplements and medications, and see how sleep, protein, gut and dose changes line up with your strength.</p>
<div class="card">
<p><strong>Coming to Google Play.</strong> A closed beta for Android starts soon. No account, no ads, no analytics: what you log stays on your phone.</p>
</div>
<ul>
<li><a href="privacy.html">Privacy policy</a></li>
<li>Questions or feedback: <a href="mailto:jz.dailyapp@gmail.com">jz.dailyapp@gmail.com</a></li>
</ul>
"""))
(out / ".nojekyll").write_text("")
(out / "README.md").write_text("""# daily-lift-site

Public pages for the Daily Lift Android app, served by GitHub Pages: the home page and the privacy policy.

The privacy policy is written in the private app repo (`docs/privacy-policy.md`) and built into `privacy.html` with `python3 tools/build.py <daily-app>/docs/privacy-policy.md`; edit it there, not here. No app code lives in this repo.
""")
print("built", sorted(p.name for p in out.iterdir()))
