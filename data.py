"""
Central content model for the portfolio site.
Edit THIS file to match your exact CV wording, then run `python build.py`.
Everything on the site is generated from the dictionary below.
"""

# ---- Icon resolver -----------------------------------------------------------
# Dev/tech logos come from Devicon (reliable, official brand SVGs on jsDelivr).
# A few not in Devicon are bundled locally in static/img/ (official-style SVGs).
_DEV = "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/"

ICONS = {
    "azure":         _DEV + "azure/azure-original.svg",
    "azuredevops":   _DEV + "azuredevops/azuredevops-original.svg",
    "docker":        _DEV + "docker/docker-original.svg",
    "dotnet":        _DEV + "dotnetcore/dotnetcore-original.svg",
    "csharp":        _DEV + "csharp/csharp-original.svg",
    "python":        _DEV + "python/python-original.svg",
    "powershell":    _DEV + "powershell/powershell-original.svg",
    "git":           _DEV + "git/git-original.svg",
    "github":        _DEV + "github/github-original.svg",       # monochrome -> inverts in dark
    "visualstudio":  _DEV + "visualstudio/visualstudio-original.svg",
    "vscode":        _DEV + "vscode/vscode-original.svg",
    "django":        _DEV + "django/django-plain.svg",          # monochrome -> inverts in dark
    "linkedin":      _DEV + "linkedin/linkedin-original.svg",
    # Bundled locally (not on Devicon):
    "powerplatform":  "img/powerplatform.svg",
    "azurefunctions": "img/azurefunctions.svg",
    "immich":         "img/immich.svg",
    "graduation":     "img/graduation.svg",
    "microsoft365":   "img/microsoft365.svg",
    # Non-Microsoft issuers + Applied Skills + generic credential:
    "aws":            "img/aws.svg",
    "googlecloud":    "img/googlecloud.svg",
    "comptia":        "img/comptia.svg",
    "cisco":          "img/cisco.svg",
    "appliedskills":  "img/appliedskills.svg",
    "credential":     "img/credential.svg",   # generic fallback for any issuer
    "kubernetes":     "img/gitops.svg",        # (kept for compatibility)
    # Official Microsoft Learn certification badges:
    "ms_expert":       "img/ms-az305.svg",
    "ms_associate":    "img/ms-az104.svg",
    "ms_fundamentals": "img/ms-az900.svg",
    "ms_az305":        "img/ms-az305.svg",
    "ms_az104":        "img/ms-az104.svg",
    "ms_az900":        "img/ms-az900.svg",
    "google":          "img/google.svg",
    "fabric":          "img/fabric.svg",
    "gitops":          "img/gitops.svg",
    "itil":            "img/itil.svg",
    # Official Philippine institution logos (from their own domains):
    "tesda":           "https://www.google.com/s2/favicons?domain=tesda.gov.ph&sz=128",
    "ama":             "https://www.google.com/s2/favicons?domain=ama.edu.ph&sz=128",
    "jenkins":         _DEV + "jenkins/jenkins-original.svg",
    "kubernetes_cert": _DEV + "kubernetes/kubernetes-plain.svg",
    # Local fallbacks for the official-domain favicons above:
    "tesda_local":     "img/tesda.svg",
    "ama_local":       "img/ama.svg",
}

# Fallback icon key used if a remote icon fails to load (handled in template).
ICON_FALLBACK = {
    "tesda": "tesda_local",
    "ama":   "ama_local",
}
# Icons that are near-black and need inverting in dark mode:
INVERT = {"github", "django", "jenkins"}


CONTACT = {
    # >>> Update these with your real details <<<
    "email": "lloydismael@gmail.com",
    "phone_e164": "+639123507286",          # SMS button (international format)
    "phone_display": "0912 350 7286",
    "location": "Makati City, Philippines",
    "github": "lloydismael",
    "github_url": "https://github.com/lloydismael",
    "linkedin_url": "https://www.linkedin.com/in/lloydchristianismael/",
    "website": "https://clouditechsolution.com",
}

# Profile photo: tries LinkedIn avatar first (via unavatar), then falls back to the
# GitHub avatar (always available), then to the initials monogram if both fail.
AVATAR = {
    "linkedin_username": "lloydchristianismael",
    "primary": "https://unavatar.io/linkedin/lloydchristianismael?fallback=https://github.com/lloydismael.png",
    "fallback": "https://github.com/lloydismael.png",
}

PROFILE = {
    "name": "Lloyd Christian M. Ismael",
    "initials": "LI",
    "role": "Systems Support Engineer · Cloud & DevOps",
    "hero_title": "Azure Solutions Architect Expert",
    "tagline": "I build and operate cloud-native platforms on Azure — from CSP billing tools "
               "to containerized web apps — with a bias for automation, clean delivery and cost efficiency.",
    "short_bio": (
        "Systems Support Engineer and Microsoft Cloud Solution Provider (CSP) partner based in "
        "Makati City. I work across the full delivery lifecycle: designing Azure infrastructure, "
        "modernizing .NET applications, wiring up CI/CD with Azure DevOps and GitHub, and shipping "
        "Docker workloads to Azure App Service and VMs. I care about pragmatic architecture, "
        "traceable automation, and keeping cloud spend honest."
    ),
    "stats": [
        {"value": "9+",  "label": "Years in IT & Cloud"},
        {"value": "4",   "label": "Platforms shipped"},
        {"value": "CSP", "label": "Microsoft Partner"},
        {"value": "24/7","label": "Automated pipelines"},
    ],
}

SKILLS = [
    {
        "group": "Cloud & Infrastructure",
        "items": [
            {"name": "Microsoft Azure", "icon": "azure"},
            {"name": "Azure DevOps",    "icon": "azuredevops"},
            {"name": "Docker",          "icon": "docker"},
            {"name": "Azure Functions", "icon": "azurefunctions"},
        ],
    },
    {
        "group": "Development",
        "items": [
            {"name": ".NET",       "icon": "dotnet"},
            {"name": "C#",         "icon": "csharp"},
            {"name": "Python",     "icon": "python"},
            {"name": "PowerShell", "icon": "powershell"},
        ],
    },
    {
        "group": "Tooling & Platforms",
        "items": [
            {"name": "Git",             "icon": "git"},
            {"name": "GitHub",          "icon": "github"},
            {"name": "Visual Studio",   "icon": "visualstudio"},
            {"name": "VS Code",         "icon": "vscode"},
            {"name": "Power Platform",  "icon": "powerplatform"},
        ],
    },
]

PROJECTS = [
    {
        "name": "Request Hub",
        "subtitle": "ESG request & workflow platform",
        "description": "A ticketing / request-management portal that centralizes ESG-related "
                       "submissions, approvals and tracking with role-based access.",
        "url": "https://esgrequesthub.dreadops.site/accounts/login/",
        "tags": ["Web App", "Workflow", "Auth"],
        "icon": "django",
        "favicon": "img/favicon-requesthub.png",
        "accent": "#0C4B33",
    },
    {
        "name": "Azure CSP Calculator",
        "subtitle": "Consumption & billing portal",
        "description": "A CSP billing portal that estimates and reconciles Azure consumption, "
                       "helping partners track customer spend and Azure Credit Offers.",
        "url": "https://azureconsumption.clouditechsolution.com/",
        "tags": ["Azure", "Billing", "CSP"],
        "icon": "azure",
        "favicon": "img/favicon-csp.png",
        "accent": "#0078D4",
    },
    {
        "name": "Learning Development Portal",
        "subtitle": "Leadership Development Program",
        "description": "A learning platform for a Leadership Development Program — course delivery, "
                       "sign-in and participant progress, deployed on Azure App Service.",
        "url": "https://ldp.clouditechsolution.com/",
        "tags": ["LMS", "App Service", "SSO"],
        "icon": "graduation",
        "favicon": "img/favicon-ldp.svg",
        "accent": "#6D28D9",
    },
    {
        "name": "Puto Copy",
        "subtitle": "Self-hosted media & backup",
        "description": "A self-hosted photo and media management deployment (Immich) running in "
                       "Docker on an Azure VM with a custom domain and SSL.",
        "url": "https://putocopy.clouditechsolution.com/auth/login",
        "tags": ["Docker", "Self-hosted", "Azure VM"],
        "icon": "immich",
        "favicon": "img/favicon-putocopy.png",
        "accent": "#4250AF",
    },
]

# =============================================================================
# CERTIFICATIONS & CREDENTIALS  — ADD YOUR REAL ITEMS FROM YOUR CV HERE.
# -----------------------------------------------------------------------------
# The section renders GROUPED by "category". Each item supports:
#   name     : full credential title
#   issuer   : who issued it (Microsoft, Amazon Web Services, Cisco, CompTIA, ...)
#   status   : "Certified" | "In progress" | "Targeted"
#   icon     : logo key — any of:
#              Microsoft:  azure | azuredevops | powerplatform | microsoft365 | appliedskills
#              Non-MS:     aws | googlecloud | comptia | cisco | oracle | kubernetes | linux | docker_cert
#              Fallback:   credential  (generic award badge for anything else)
#
# NOTE: Your CV did not attach, so only the credential I had a genuine signal for
# (AZ-400 prep) is filled in. Paste your real list — Microsoft, non-Microsoft, and
# Microsoft Applied Skills — replacing the examples below, then run `python build.py`.
# =============================================================================
CERTIFICATIONS = [
    {"name": "Azure Solutions Architect Expert", "issuer": "Microsoft Certified",
     "badge": "AZ-305", "icon": "ms_az305"},
    {"name": "Azure Administrator Associate", "issuer": "Microsoft Certified",
     "badge": "AZ-104", "icon": "ms_az104"},
    {"name": "Azure Fundamentals", "issuer": "Microsoft Certified",
     "badge": "AZ-900", "icon": "ms_az900"},
    {"name": "Google IT Support Professional Certificate", "issuer": "Google",
     "badge": "Professional Certificate", "icon": "google"},
    {"name": "GitHub Foundations", "issuer": "GitHub",
     "badge": "Foundations", "icon": "github"},
    {"name": "Azure Container Apps in Action", "issuer": "Microsoft Applied Skills",
     "badge": "Applied Skills", "icon": "azure"},
    {"name": "Building Clouds with Fabric Warehouses", "issuer": "Microsoft Applied Skills",
     "badge": "Applied Skills", "icon": "fabric"},
    {"name": "Jenkins", "issuer": "The Linux Foundation",
     "badge": "LFS167", "icon": "jenkins"},
    {"name": "Kubernetes", "issuer": "The Linux Foundation",
     "badge": "LFS158", "icon": "kubernetes_cert"},
    {"name": "GitOps", "issuer": "The Linux Foundation",
     "badge": "LFS169", "icon": "gitops"},
    {"name": "CompTIA A+", "issuer": "CompTIA · IBM",
     "badge": "A+", "icon": "comptia"},
    {"name": "ITIL 4 Foundation", "issuer": "AXELOS",
     "badge": "ITIL 4", "icon": "itil"},
    {"name": "TESDA National Certificate II", "issuer": "TESDA",
     "badge": "NC II", "icon": "tesda"},
]

EDUCATION = [
    {
        "school": "BS in Information Technology",
        "detail": "AMA Computer College — 2017",
        "icon": "ama",
    },
]

CONSULTING = [
    {
        "name": "Advisory",
        "price": "Starter",
        "best_for": "Quick expert direction",
        "features": [
            "1:1 Azure / DevOps consultation",
            "Architecture & cost review",
            "Written recommendations",
            "Email follow-up",
        ],
        "featured": False,
    },
    {
        "name": "Build & Deploy",
        "price": "Most popular",
        "best_for": "Ship a working solution",
        "features": [
            "Everything in Advisory",
            "Azure infra + CI/CD setup",
            "Dockerized app deployment",
            "Custom domain & SSL",
            "Handover documentation",
        ],
        "featured": True,
    },
    {
        "name": "Managed Partner",
        "price": "Enterprise",
        "best_for": "Ongoing cloud operations",
        "features": [
            "Everything in Build & Deploy",
            "CSP subscription management",
            "Cost optimization & monitoring",
            "Priority support SLA",
            "Quarterly roadmap reviews",
        ],
        "featured": False,
    },
]

SITE = {
    "title": f"{PROFILE['name']} — Cloud & DevOps Engineer",
    "description": "Portfolio of Lloyd Christian M. Ismael — Azure, DevOps, .NET and cloud engineering.",
}
