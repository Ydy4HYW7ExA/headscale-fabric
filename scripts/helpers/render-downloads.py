#!/usr/bin/env python3
"""Render downloads portal files from Jinja2 templates."""
from pathlib import Path

try:
    import jinja2
    import yaml
except ImportError:
    raise SystemExit("pip install jinja2 pyyaml")

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = ROOT / "assets" / "templates" / "downloads"
VARS = ROOT / "scripts" / "ansible" / "inventories" / "production" / "group_vars" / "all.yml"
OUT_DIR = ROOT / "build" / "downloads"

context = yaml.safe_load(VARS.read_text()) or {}
env = jinja2.Environment(loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)))

OUT_DIR.mkdir(parents=True, exist_ok=True)

for tmpl_path in TEMPLATES_DIR.glob("*.j2"):
    tmpl = env.get_template(tmpl_path.name)
    rendered = tmpl.render(**context)
    out_file = OUT_DIR / tmpl_path.name.replace(".j2", "")
    out_file.write_text(rendered)
    print(f"rendered: {out_file}")

print(f"\n{len(list(TEMPLATES_DIR.glob('*.j2')))} templates -> {OUT_DIR}")
