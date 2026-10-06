"""P0.5 .wkrt save format, checksum and migration primitives."""
from pathlib import Path
import hashlib, json, os
from .model import MODEL_VERSION, SCHEMA_VERSION

FORMAT_VERSION = 1

def _checksum(payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",",":")).encode()
    return hashlib.sha256(raw).hexdigest()


def save(path: str | Path, state: dict) -> None:
    target = Path(path); payload = {"format_version": FORMAT_VERSION, "model_version": MODEL_VERSION, "schema_version": SCHEMA_VERSION, "state": state}
    document = {"payload": payload, "checksum": _checksum(payload)}
    tmp = target.with_name(target.name + ".tmp")
    tmp.write_text(json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2), encoding="utf-8")
    with tmp.open("rb") as f: os.fsync(f.fileno())
    os.replace(tmp, target)


def load(path: str | Path) -> dict:
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    payload = document.get("payload")
    if not isinstance(payload, dict) or document.get("checksum") != _checksum(payload): raise ValueError("SAVE-CHECKSUM-001: checksum mismatch")
    if payload.get("format_version") != FORMAT_VERSION: raise ValueError("SAVE-VERSION-001: unsupported save format")
    return payload
