"""Bygger index.html ved å bygge inn bibliotekene i src/template.html.
Kjør fra roten av repoet:  npm ci && python3 src/build.py
"""
import base64
from pathlib import Path

root = Path(__file__).resolve().parent.parent
nm = root / "node_modules"
libs = {
    "/*__JSZIP__*/": nm / "jszip/dist/jszip.min.js",
    "/*__PDFLIB__*/": nm / "pdf-lib/dist/pdf-lib.min.js",
    "/*__PDFJS__*/": nm / "pdfjs-dist/legacy/build/pdf.min.js",
    "/*__PDFJSWORKER__*/": nm / "pdfjs-dist/legacy/build/pdf.worker.min.js",
}
html = (root / "src/template.html").read_text(encoding="utf-8")
for marker, path in libs.items():
    code = path.read_text(encoding="utf-8")
    if "</script" in code.lower():
        raise SystemExit(f"{path} inneholder </script og kan ikke bygges inn trygt")
    html = html.replace(marker, code)
image = base64.b64encode((root / "src/wiseflow-offline-vurdering.png").read_bytes()).decode("ascii")
html = html.replace("__HELPIMAGE__", "data:image/png;base64," + image)
(root / "index.html").write_text(html, encoding="utf-8")
print("Skrev index.html")
