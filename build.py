#!/usr/bin/env python3
"""
Static site generator for the portfolio.

Renders templates/index.html.j2 -> public/index.html using the content in data.py,
and copies static assets into public/. The `public/` folder is what Azure Static
Web Apps serves (app_location output).

Usage:
    python build.py            # build once
    python build.py --serve    # build, then serve locally at http://localhost:8000
"""
import argparse
import datetime as _dt
import json
import shutil
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from jinja2 import Environment, FileSystemLoader, select_autoescape

import data

ROOT = Path(__file__).resolve().parent
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
PUBLIC = ROOT / "public"


def icon_url(key: str) -> str:
    """Resolve a logical icon key to a URL (Devicon CDN or local bundled asset)."""
    return data.ICONS.get(key, "img/graduation.svg")


def favicon_url(url: str, sz: int = 64) -> str:
    """Return the site's own favicon via Google's favicon service (reliable, cached)."""
    from urllib.parse import urlparse
    host = urlparse(url).netloc or url
    return f"https://www.google.com/s2/favicons?domain={host}&sz={sz}"


def favicon_fallback(url: str) -> str:
    """Fallback favicon via DuckDuckGo icon service."""
    from urllib.parse import urlparse
    host = urlparse(url).netloc or url
    return f"https://icons.duckduckgo.com/ip3/{host}.ico"


def shot_url(url: str, w: int = 1280, h: int = 860) -> str:
    """Primary full-page screenshot via WordPress mShots (free, unlimited, no key).

    mShots renders the full desktop landing page. It generates asynchronously, so the
    front-end auto-retries until the real screenshot is ready (see main.js)."""
    from urllib.parse import quote
    return f"https://s.wordpress.com/mshots/v1/{quote(url, safe='')}?w={w}&h={h}"


def shot_fallback(url: str, w: int = 1280, h: int = 860) -> str:
    """Fallback full-page screenshot via microlink.io (free tier, clean, no watermark)."""
    from urllib.parse import quote
    u = quote(url, safe="")
    return (f"https://api.microlink.io/?url={u}&screenshot=true&meta=false"
            f"&embed=screenshot.url&viewport.width={w}&viewport.height={h}")


def _canonical() -> str:
    return data.SITE["canonical"].rstrip("/")


def json_ld() -> str:
    """One @graph for WebSite + Person + ProfessionalService + FAQPage."""
    origin = _canonical()
    person_id = f"{origin}/#person"
    website_id = f"{origin}/#website"
    service_id = f"{origin}/#service"
    graph = [
        {
            "@type": "WebSite",
            "@id": website_id,
            "url": f"{origin}/",
            "name": data.SITE["site_name"],
            "description": data.SITE["description"],
            "inLanguage": "en",
            "publisher": {"@id": person_id},
        },
        {
            "@type": "Person",
            "@id": person_id,
            "name": data.PROFILE["name"],
            "jobTitle": data.PROFILE["role"],
            "url": f"{origin}/",
            "image": data.AVATAR["fallback"],
            "email": f"mailto:{data.CONTACT['email']}",
            "telephone": data.CONTACT["phone_e164"],
            "address": {
                "@type": "PostalAddress",
                "addressLocality": "Makati City",
                "addressCountry": "PH",
            },
            "sameAs": [
                data.CONTACT["github_url"],
                data.CONTACT["linkedin_url"],
            ],
            "worksFor": {"@id": service_id},
        },
        {
            "@type": "ProfessionalService",
            "@id": service_id,
            "name": f"{data.PROFILE['name']} — Azure & DevOps consulting",
            "url": f"{origin}/",
            "image": f"{origin}{data.SITE['og_image']}",
            "description": data.SITE["description"],
            "areaServed": ["PH", "Remote"],
            "serviceType": [
                "Azure consulting",
                "DevOps automation",
                "Cloud architecture",
            ],
            "founder": {"@id": person_id},
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": item["q"],
                    "acceptedAnswer": {"@type": "Answer", "text": item["a"]},
                }
                for item in data.FAQ
            ],
        },
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def write_robots(dest: Path) -> None:
    dest.write_text(
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {_canonical()}/sitemap.xml\n",
        encoding="utf-8",
    )


def write_sitemap(dest: Path, lastmod: str) -> None:
    origin = _canonical()
    dest.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        "  <url>\n"
        f"    <loc>{xml_escape(origin)}/</loc>\n"
        f"    <lastmod>{xml_escape(lastmod)}</lastmod>\n"
        "    <changefreq>weekly</changefreq>\n"
        "    <priority>1.0</priority>\n"
        "  </url>\n"
        "</urlset>\n",
        encoding="utf-8",
    )


def ensure_og_image() -> None:
    """Generate a 1200x630 social card if one is not already checked in."""
    out = STATIC / "img" / "og-image.png"
    if out.exists():
        return
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("! Pillow not installed — skip og-image.png (pip install pillow)")
        return

    w, h = 1200, 630
    img = Image.new("RGB", (w, h), "#070b16")
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 18, h), fill="#0078d4")
    draw.ellipse((820, -180, 1380, 380), fill="#0b1a3a")
    draw.ellipse((-80, 360, 420, 860), fill="#1a1130")

    def _font(size: int) -> ImageFont.ImageFont:
        for name in ("segoeui.ttf", "arial.ttf", "calibri.ttf"):
            try:
                return ImageFont.truetype(name, size)
            except OSError:
                continue
        return ImageFont.load_default()

    title_font = _font(54)
    sub_font = _font(28)
    small_font = _font(22)
    draw.text((72, 150), "Lloyd Christian M. Ismael", fill="#eef2ff", font=title_font)
    draw.text((72, 230), "Azure Cloud & DevOps Engineer", fill="#3ea0ff", font=sub_font)
    draw.text((72, 300), "Makati City  ·  Consulting  ·  CSP Partner", fill="#b3bdd4", font=small_font)
    draw.text((72, 520), "lloydismael.com", fill="#94a3b8", font=small_font)

    avatar_path = STATIC / "img" / "avatar-linkedin.png"
    if avatar_path.exists():
        av = Image.open(avatar_path).convert("RGBA")
        size = 220
        side = min(av.size)
        left = (av.width - side) // 2
        top = max(0, (av.height - side) // 5)
        av = av.crop((left, top, left + side, top + side)).resize((size, size), Image.Resampling.LANCZOS)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, size, size), radius=36, fill=255)
        img.paste(av, (880, 200), mask)

    img.save(out, "PNG", optimize=True)
    print(f"✓ Generated {out.name} ({w}x{h})")


def build() -> None:
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    env.globals["icon_url"] = icon_url
    env.globals["shot_url"] = shot_url
    env.globals["shot_fallback"] = shot_fallback
    env.globals["favicon_url"] = favicon_url
    env.globals["favicon_fallback"] = favicon_fallback
    env.globals["icon_fallback"] = lambda key: icon_url(
        getattr(data, "ICON_FALLBACK", {}).get(key, "credential"))

    ensure_og_image()
    today = _dt.date.today().isoformat()

    template = env.get_template("index.html.j2")
    html = template.render(
        site=data.SITE,
        profile=data.PROFILE,
        contact=data.CONTACT,
        skills=data.SKILLS,
        projects=data.PROJECTS,
        certifications=data.CERTIFICATIONS,
        education=data.EDUCATION,
        consulting=data.CONSULTING,
        how_i_work=data.HOW_I_WORK,
        faq=data.FAQ,
        avatar=data.AVATAR,
        invert=data.INVERT,
        json_ld=json_ld(),
        year=_dt.date.today().year,
    )

    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True)

    (PUBLIC / "index.html").write_text(html, encoding="utf-8")
    shutil.copytree(STATIC / "css", PUBLIC / "css")
    shutil.copytree(STATIC / "js", PUBLIC / "js")
    shutil.copytree(STATIC / "img", PUBLIC / "img")

    # Browsers request /favicon.ico at the site root by default.
    favicon = STATIC / "img" / "favicon.ico"
    if favicon.exists():
        shutil.copy(favicon, PUBLIC / "favicon.ico")

    write_robots(PUBLIC / "robots.txt")
    write_sitemap(PUBLIC / "sitemap.xml", today)

    manifest = STATIC / "site.webmanifest"
    if manifest.exists():
        shutil.copy(manifest, PUBLIC / "site.webmanifest")

    # Config for Azure Static Web Apps (fallback routing + headers)
    swa = ROOT / "staticwebapp.config.json"
    if swa.exists():
        shutil.copy(swa, PUBLIC / "staticwebapp.config.json")

    print(f"✓ Built site -> {PUBLIC/'index.html'}")


def serve() -> None:
    import http.server
    import socketserver
    import os

    os.chdir(PUBLIC)
    port = 8000
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving at http://localhost:{port}  (Ctrl+C to stop)")
        httpd.serve_forever()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--serve", action="store_true", help="serve after building")
    args = ap.parse_args()
    build()
    if args.serve:
        serve()
