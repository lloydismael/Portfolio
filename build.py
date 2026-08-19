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
import shutil
from pathlib import Path

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
        avatar=data.AVATAR,
        invert=data.INVERT,
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
