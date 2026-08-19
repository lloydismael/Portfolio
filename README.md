# Lloyd Ismael — Portfolio

A professional portfolio **written in Python** (Jinja2 static-site generator) and
architected for **Azure Static Web Apps**, with a **Python Azure Functions** API for the
contact form.

## Features
- ✨ Liquid-glass, professional design with **light/dark mode** (remembers your choice)
- 🧩 **Official technology icons** (Devicon + bundled SVGs) across skills, certs & education
- 📈 Live **GitHub activity** for [`lloydismael`](https://github.com/lloydismael) (contribution graph + stats, theme-synced)
- 🗂️ **Projects**: Request Hub, Azure CSP Calculator, Learning Development Portal, Puto Copy
- 💼 **Consulting tiers** (Advisory → Build & Deploy → Managed Partner)
- 💬 **Floating chat button** + contact form → message directly via **SMS or email**
- 🐍 100% Python build pipeline, no Node build step

## Project structure
```
portfolio/
├─ build.py                 # Python static-site generator (Jinja2)
├─ data.py                  # ← EDIT THIS: all your content (CV wording, contact, links)
├─ templates/index.html.j2  # page template
├─ static/                  # css, js, bundled svg icons (source)
├─ public/                  # GENERATED output — this is what SWA serves
├─ api/                     # Python Azure Functions (contact endpoint)
│  ├─ contact/__init__.py
│  ├─ host.json
│  └─ requirements.txt
├─ staticwebapp.config.json # routing, security headers
└─ .github/workflows/       # CI/CD to Azure Static Web Apps
```

## 1) Personalize
Open **`data.py`** and update:
- `CONTACT` → your real **email** and **phone** (the phone drives the SMS button; use international format like `+639171234567`)
- `PROFILE`, `SKILLS`, `PROJECTS`, `CERTIFICATIONS`, `EDUCATION`, `CONSULTING` → paste your exact CV wording

## 2) Build & preview locally
```bash
pip install -r requirements.txt
python build.py --serve
# open http://localhost:8000
```
`python build.py` (without `--serve`) just regenerates `public/`.

## 3) Deploy to Azure Static Web Apps
**Option A — GitHub (recommended):**
1. Push this folder to a GitHub repo (e.g. `lloydismael/portfolio`).
2. In the Azure Portal → **Create a resource → Static Web App**.
3. Connect the repo. When asked for build details, either use the included
   workflow or set: **App location** `public`, **Api location** `api`, **Output location** empty.
4. Azure adds a deployment secret (for this app: `AZURE_STATIC_WEB_APPS_API_TOKEN_CALM_RIVER_0BD571400`) and the workflow deploys on every push. Keep the generated workflow filename (`azure-static-web-apps-calm-river-0bd571400.yml`); Azure OIDC auth requires that exact name.

**Option B — SWA CLI:**
```bash
npm i -g @azure/static-web-apps-cli
python build.py
swa deploy ./public --api-location ./api --env production
```

## 4) (Optional) Enable real email delivery
The contact endpoint validates & logs by default. To actually send mail, add these
app settings to the Static Web App (Configuration) and uncomment
`azure-communication-email` in `api/requirements.txt`:
- `ACS_CONNECTION_STRING`
- `SENDER_ADDRESS`
- `TO_ADDRESS`

Without configuration, the front-end gracefully falls back to opening the visitor's
email client via `mailto:` — so the form always works.

## Notes
- The SMS (`sms:`) and email (`mailto:`) links open the visitor's native apps.
- Dev logos load from the Devicon CDN; Power Platform, Azure Functions, Immich and the
  graduation icon are bundled locally in `static/img/` so nothing renders broken.
- Custom domain: map `www.clouditechsolution.com` (or a subdomain) in the SWA **Custom domains** blade.
