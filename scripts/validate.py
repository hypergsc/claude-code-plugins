"""Offline validation and optional ZIP export of a public HyperGSC plugin repo."""

import argparse
import json
import re
import struct
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/hypergsc"
SKILLS = {"search-review", "ctr-opportunities", "indexing-check"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_json(path):
    return json.loads(path.read_text())


def validate():
    manifests = [
        path
        for path in (
            PLUGIN / ".claude-plugin/plugin.json",
            PLUGIN / ".codex-plugin/plugin.json",
        )
        if path.exists()
    ]
    require(len(manifests) == 1, "Expected exactly one platform manifest")
    manifest_path = manifests[0]
    claude = manifest_path.parent.name == ".claude-plugin"
    manifest = read_json(manifest_path)
    require(manifest["name"] == "hypergsc", "Unexpected plugin identity")
    require(re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]), "Invalid version")
    require(
        "hooks" not in manifest and "apps" not in manifest,
        "Unexpected executable components",
    )
    endpoint = "https://hypergsc.com/mcp" + ("" if claude else "/openai")
    server = {"type": "http", "url": endpoint} if claude else {"url": endpoint}
    require(
        read_json(PLUGIN / ".mcp.json") == {"mcpServers": {"hypergsc": server}},
        "Unexpected MCP configuration",
    )
    catalog_path = ROOT / (
        ".claude-plugin/marketplace.json"
        if claude
        else ".agents/plugins/marketplace.json"
    )
    catalog = read_json(catalog_path)
    require(
        catalog["name"] == "hypergsc" and len(catalog["plugins"]) == 1,
        "Invalid marketplace",
    )
    entry = catalog["plugins"][0]
    source = (
        "./plugins/hypergsc"
        if claude
        else {"source": "local", "path": "./plugins/hypergsc"}
    )
    require(
        entry["name"] == "hypergsc" and entry["source"] == source,
        "Marketplace must resolve to this package",
    )
    expected = {
        manifest_path.relative_to(PLUGIN).as_posix(),
        ".mcp.json",
        "assets/logo.png",
    }
    expected.update(f"skills/{name}/SKILL.md" for name in SKILLS)
    actual = set()
    for path in PLUGIN.rglob("*"):
        require(not path.is_symlink(), "Package symlinks are not allowed")
        if path.is_file():
            require(
                path.resolve().is_relative_to(PLUGIN.resolve()), "Escaping package path"
            )
            actual.add(path.relative_to(PLUGIN).as_posix())
    require(
        actual == expected, f"Unexpected or missing package files: {actual ^ expected}"
    )
    data = (PLUGIN / "assets/logo.png").read_bytes()
    require(data[:8] == b"\x89PNG\r\n\x1a\n", "Expected PNG icon")
    width, height = struct.unpack(">II", data[16:24])
    require(
        48 <= width == height <= 4096 and len(data) <= 5 * 1024 * 1024,
        "Invalid icon dimensions or size",
    )
    for name in SKILLS:
        text = (PLUGIN / f"skills/{name}/SKILL.md").read_text()
        require(
            re.match(rf"^---\nname: {name}\ndescription: [^\n]+\n---\n", text),
            f"Invalid skill: {name}",
        )
    if not claude:
        require(
            manifest["mcpServers"] == "./.mcp.json"
            and manifest["skills"] in {"./skills", "./skills/"},
            "Invalid component paths",
        )
        interface = manifest["interface"]
        require(
            0 < len(interface["shortDescription"]) <= 30, "Invalid listing subtitle"
        )
        require(
            interface["logo"] == interface["composerIcon"] == "./assets/logo.png",
            "Invalid icon paths",
        )
        review = manifest["extensions"]["com.openai"]["review"]
        require(
            "test_credentials" not in review and "reviewer_instructions" not in review,
            "Keep reviewer access private",
        )
        require(
            len(review["test_cases"]["positive"]) == 5
            and len(review["test_cases"]["negative"]) == 3,
            "Missing review cases",
        )
    return manifest, sorted(actual)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zip", type=Path, help="Write a plugin-root ZIP to this path")
    args = parser.parse_args()
    manifest, files = validate()
    print(
        f"Validated HyperGSC {manifest['version']}: {len(files)} public package files."
    )
    if args.zip:
        require(not args.zip.exists(), "Refusing to overwrite an existing ZIP")
        args.zip.parent.mkdir(parents=True, exist_ok=True)
        with ZipFile(args.zip, "w", compression=ZIP_DEFLATED) as archive:
            for name in files:
                info = ZipInfo(name, (2026, 10, 3, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, (PLUGIN / name).read_bytes())
        print(f"Created {args.zip}. Platform scans and live OAuth tests are separate.")


if __name__ == "__main__":
    main()
