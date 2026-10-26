"""Regenerate the DigiKey v4 clients in ``digikey/v4/`` from the committed specs.

Usage::

    python openapi/generate.py            # regenerate from openapi/specs/*.json
    python openapi/generate.py --fetch    # download fresh specs first, then regenerate

Requires Java 11+ on PATH. The pinned openapi-generator jar is downloaded once to
``.cache/`` and verified against a pinned SHA-256.

Only the standard library is used, so this runs without installing the project.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPECS = ROOT / "openapi" / "specs"
TARGET = ROOT / "digikey" / "v4"
CACHE = ROOT / ".cache"

GENERATOR_VERSION = "7.26.0"
GENERATOR_SHA256 = "1760050094997b9cc790cc1350be095f15da8c08a996b184d3eadc4ccda5e35e"
GENERATOR_URL = (
    "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/"
    f"{GENERATOR_VERSION}/openapi-generator-cli-{GENERATOR_VERSION}.jar"
)

PORTAL = "https://developer.digikey.com"

# One entry per generated API. Adding a DigiKey API means adding an entry here,
# running ``--fetch`` and wiring the new methods into ``digikey/client.py``.
# ``node`` is the developer-portal node behind the "Download Swagger File" button;
# ``page`` is any portal page of that API (sent as referer, the portal requires it).
APIS: dict[str, dict[str, object]] = {
    "productsearch": {
        "node": 2357,
        "page": "/products/product-information-v4/productsearch/keywordsearch",
    },
    "orderstatus": {
        "node": 2291,
        "page": "/products/order-status/orderstatus/retrievesalesorder",
    },
}


def fetch_specs() -> None:
    SPECS.mkdir(parents=True, exist_ok=True)
    for name, api in APIS.items():
        request = urllib.request.Request(
            f"{PORTAL}/node/{api['node']}/oas-download",
            headers={"User-Agent": "Mozilla/5.0", "Referer": f"{PORTAL}{api['page']}"},
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            spec = json.load(response)
        # Normalised formatting keeps diffs between spec versions readable.
        path = SPECS / f"{name}.json"
        path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        print(f"fetched {path.relative_to(ROOT)} (spec version {spec['info'].get('version')})")


def preprocess(spec: dict) -> dict:
    """Make the generated models tolerant of API evolution.

    DigiKey adds enum values (order states, filter types, ...) without bumping the
    API version. Generated pydantic models reject unknown enum values, which would
    break every response containing one. Enum constraints are therefore moved into
    the field description; the server still validates requests.
    """
    spec = copy.deepcopy(spec)
    for schema in spec.get("definitions", {}).values():
        for prop in schema.get("properties", {}).values():
            for target in (prop, prop.get("items", {})):
                values = target.pop("enum", None)
                if values:
                    allowed = "Known values: " + ", ".join(map(str, values))
                    description = target.get("description", "").rstrip()
                    target["description"] = f"{description} {allowed}".strip()
    return spec


def generator_jar() -> Path:
    jar = CACHE / f"openapi-generator-cli-{GENERATOR_VERSION}.jar"
    if not jar.exists():
        CACHE.mkdir(exist_ok=True)
        print(f"downloading openapi-generator {GENERATOR_VERSION}")
        urllib.request.urlretrieve(GENERATOR_URL, jar)
    digest = hashlib.sha256(jar.read_bytes()).hexdigest()
    if digest != GENERATOR_SHA256:
        jar.unlink()
        sys.exit(f"checksum mismatch for {jar.name}: {digest}")
    return jar


def generate(name: str, jar: Path) -> None:
    package = f"digikey.v4.{name}"
    spec = preprocess(json.loads((SPECS / f"{name}.json").read_text(encoding="utf-8")))
    with tempfile.TemporaryDirectory() as tmp:
        spec_path = Path(tmp) / "spec.json"
        spec_path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
        out = Path(tmp) / "out"
        subprocess.run(
            [
                "java",
                "-jar",
                str(jar),
                "generate",
                "--generator-name",
                "python",
                "--input-spec",
                str(spec_path),
                "--output",
                str(out),
                "--package-name",
                package,
                "--additional-properties",
                f"generateSourceCodeOnly=true,projectName=digikey-api,packageVersion={GENERATOR_VERSION}",
                "--global-property",
                "apiTests=false,modelTests=false,apiDocs=false,modelDocs=false",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        source = out.joinpath(*package.split("."))
        destination = TARGET / name
        shutil.rmtree(destination, ignore_errors=True)
        shutil.copytree(source, destination, ignore=shutil.ignore_patterns("*.md", "py.typed"))
    print(f"generated {destination.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--fetch", action="store_true", help="download the latest specs from the developer portal first"
    )
    args = parser.parse_args()

    if args.fetch:
        fetch_specs()
    jar = generator_jar()
    for name in APIS:
        generate(name, jar)
    (TARGET / "__init__.py").write_text(
        '"""Generated DigiKey v4 clients. Do not edit: run ``python openapi/generate.py``."""\n',
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
