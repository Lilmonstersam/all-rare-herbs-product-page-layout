#!/usr/bin/env python3
"""Build the GitHub Pages copy of the ARH product page mockup.
Usage: build.py <mockup-dir> <out-dir>"""
import sys, os, re, shutil
src_dir, out = sys.argv[1], sys.argv[2]
HTML = "Alocasia Frydek Variegated Plant _ All Rare Herbs.html"
FILES = "Alocasia Frydek Variegated Plant _ All Rare Herbs_files"
s = open(os.path.join(src_dir, HTML), encoding="utf-8").read()

# 1. Strip client tracking so the public copy never sends hits to ARH's GA/GTM/Meta/Mailchimp
scripts = list(re.finditer(r'<script\b([^>]*)>(.*?)</script>', s, flags=re.S))
TRACK_SRC = ('recaptcha__', 'gtm.js', 'fbevents.js', '9361d954', 'facebook-for-woocommerce-signals', 'mailchimp-woocommerce',
             'pixel-tracking', 'pixel-events', 'clientParamBuilder', 'gtag-events', 'api.js', 'index(2).js')
TRACK_ID = ('wc-facebook-signals', 'mailchimp-woocommerce', 'wc-facebook-pixel', 'facebook-capi', 'google-recaptcha',
            'wpcf7-recaptcha', 'facebook-for-woocommerce-inline', 'gla-gtag-events')
TRACK_BODY = ('googletagmanager.com', 'connect.facebook.net', 'fbq(', "gtag('js'", 'gtag("event"', 'gtag("config"')
removed = 0
for m in reversed(scripts):
    attrs, body = m.group(1), m.group(2)
    if attrs.strip().startswith('type="application/ld+json"'):
        continue
    if 'arh-sticky-cta' in attrs or 'arh-' in body[:200]:
        continue
    if (any(k in attrs for k in TRACK_SRC) or any(k in attrs for k in TRACK_ID) or any(k in body for k in TRACK_BODY)):
        s = s[:m.start()] + s[m.end():]; removed += 1
s = re.sub(r'<!-- Google Tag Manager \(noscript\) -->.*?<!-- End Google Tag Manager \(noscript\) -->', '', s, flags=re.S)
# 2. Strip browser-extension leftovers captured when the page was saved (Imageye, Glasp)
s = re.sub(r'<style[^>]*>\s*\.imageye-selected\s*\{.*?</style>', '', s, flags=re.S)
s = re.sub(r'<style data-glasp[^>]*>.*?</style>', '', s, flags=re.S)
s = re.sub(r'<div[^>]*class="glasp-[^"]*"[^>]*>\s*</div>', '', s)
# 2b. Drop the saved reCAPTCHA badge iframe (its key is locked to the live domain)
s = re.sub(r'<div><div class="grecaptcha-badge".*?</textarea></div><iframe[^>]*></iframe></div>', '', s, count=1, flags=re.S)
s = re.sub(r'<div class="glasp-extension-toaster[^"]*"[^>]*><template[^>]*></template></div>', '', s)
# 3. Stubs so remaining theme code calling gtag/fbq doesn't throw; noindex so the copy never competes with the live page
head_inject = ('\n<meta name="robots" content="noindex, nofollow">\n'
               '<script>window.dataLayer=[];function gtag(){};window.fbq=function(){};window._fbq=window.fbq;</script>\n')
s = re.sub(r'(<head(?:\s[^>]*)?>)', lambda m: m.group(1) + head_inject, s, count=1)

# 4. Copy assets to ./assets with web-safe names
adir = os.path.join(out, "assets"); os.makedirs(adir, exist_ok=True)
rename = {}
for f in sorted(os.listdir(os.path.join(src_dir, FILES))):
    p = os.path.join(src_dir, FILES, f)
    if not os.path.isfile(p): continue
    n = re.sub(r'\((\d+)\)', r'-\1', f).replace(' ', '-')
    if '.' not in n:  # extensionless Google Fonts CSS ("css", "css2")
        n += '.css'
    rename[f] = n
    shutil.copyfile(p, os.path.join(adir, n))
for f in sorted(rename, key=len, reverse=True):
    s = s.replace('./' + FILES + '/' + f, './assets/' + rename[f])
s = s.replace('./' + FILES + '/', './assets/')
# 5. Icon fonts weren't captured by "Save page as": ship vendored copies and repoint the CSS
vendor = sys.argv[3] if len(sys.argv) > 3 else None
if vendor:
    for sub in ("fonts", "webfonts"):
        shutil.copytree(os.path.join(vendor, sub), os.path.join(adir, sub), dirs_exist_ok=True)
    for f in os.listdir(adir):
        if not f.endswith(".css"): continue
        cp = os.path.join(adir, f); c = open(cp, encoding="utf-8", errors="surrogateescape").read(); o = c
        c = c.replace("../webfonts/", "webfonts/").replace("../fonts/slick.", "fonts/slick.")
        c = re.sub(r"\.\./fonts/eicons\.(\w+)\?(5\.\d+\.\d+)", lambda m: "fonts/eicons-%s.%s?%s" % (m.group(2), m.group(1), m.group(2)), c)
        if c != o: open(cp, "w", encoding="utf-8", errors="surrogateescape").write(c)
open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(s)
print("scripts removed:", removed, "| assets:", len(rename), "| leftover old refs:", s.count(FILES))
