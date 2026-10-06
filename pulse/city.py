"""P0.2 city-package manifest and validation."""
from dataclasses import dataclass
from pathlib import Path
import hashlib, json

REQUIRED_FILES = frozenset({"manifest.json", "cost-model.json", "reference_network.json"})

@dataclass(frozen=True, slots=True)
class CityPackage:
    root: Path
    manifest: dict

    @classmethod
    def load(cls, root: str | Path) -> "CityPackage":
        path = Path(root)
        manifest_path = path / "manifest.json"
        if not manifest_path.is_file(): raise ValueError("CITY-MANIFEST-001: manifest.json is missing")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        errors = validate_manifest(path, manifest)
        if errors: raise ValueError("Invalid city package: " + "; ".join(errors))
        return cls(path, manifest)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()


def validate_manifest(root: Path, manifest: dict) -> list[str]:
    required = ["schema_version", "city_uid", "name", "country", "timezone", "currency", "coordinate_reference_system", "data_date", "build_date", "sources", "files", "license"]
    errors = [f"manifest.{k} missing" for k in required if k not in manifest]
    errors += [f"missing {name}" for name in REQUIRED_FILES if not (root/name).is_file()]
    for item in manifest.get("files", []):
        rel = item.get("path")
        if not rel: errors.append("manifest.files entry without path"); continue
        p = root / rel
        if not p.is_file(): errors.append(f"missing {rel}"); continue
        expected = item.get("sha256")
        if expected and sha256_file(p) != expected: errors.append(f"checksum mismatch: {rel}")
    return errors
