#!/usr/bin/env python3
"""
Exporta sessões do Cline (VS Code) para prompts/sessoes/.

Uso:
    python scripts/exportar_sessoes.py
    python scripts/exportar_sessoes.py --dry-run

Caminho das tasks do Cline:
    Linux  : ~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/
    macOS  : ~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/
    Windows: %APPDATA%/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/

Override com env var: CLINE_TASKS_DIR
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEST_DIR = REPO_ROOT / "prompts" / "sessoes"
DEST_DIR.mkdir(parents=True, exist_ok=True)

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"gsk_[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"AIza[0-9A-Za-z\-_]{35}"),
    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    re.compile(r"-----BEGIN [A-Z ]+PRIVATE KEY-----"),
    re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"][^'\"]{12,}['\"]"),
]

MAX_SIZE_MB = 50


def find_cline_tasks_dir() -> Path | None:
    env = os.environ.get("CLINE_TASKS_DIR")
    if env:
        p = Path(env).expanduser()
        return p if p.is_dir() else None

    home = Path.home()
    if sys.platform.startswith("linux"):
        base = home / ".config" / "Code" / "User" / "globalStorage"
    elif sys.platform == "darwin":
        base = home / "Library" / "Application Support" / "Code" / "User" / "globalStorage"
    elif sys.platform.startswith("win"):
        appdata = os.environ.get("APPDATA")
        if not appdata:
            return None
        base = Path(appdata) / "Code" / "User" / "globalStorage"
    else:
        return None

    for slug in ("saoudrizwan.claude-dev", "cline.cline"):
        candidate = base / slug / "tasks"
        if candidate.is_dir():
            return candidate
    return None


def contains_secret(text: str) -> str | None:
    for pat in SECRET_PATTERNS:
        m = pat.search(text)
        if m:
            return m.group(0)[:40]
    return None


def already_exported(task_id: str) -> bool:
    for _ in DEST_DIR.glob(f"*-{task_id}*"):
        return True
    return False


def export_task(task_dir: Path, dry_run: bool) -> None:
    task_id = task_dir.name
    if already_exported(task_id):
        print(f"  [skip] {task_id} já exportado")
        return

    metadata = {}
    ui_messages = None
    api_history = None

    for fname in ("task_metadata.json", "ui_messages.json", "api_conversation_history.json"):
        f = task_dir / fname
        if not f.is_file():
            continue
        raw = f.read_text(encoding="utf-8", errors="replace")
        secret = contains_secret(raw)
        if secret:
            print(f"  [ERRO] segredo detectado em {task_id}/{fname}: {secret!r}")
            print("         Revogue a chave ANTES de exportar. Pulando task.")
            return
        if fname == "task_metadata.json":
            try:
                metadata = json.loads(raw)
            except Exception:
                metadata = {}
        elif fname == "ui_messages.json":
            try:
                ui_messages = json.loads(raw)
            except Exception:
                ui_messages = raw
        elif fname == "api_conversation_history.json":
            try:
                api_history = json.loads(raw)
            except Exception:
                api_history = raw

    if ui_messages is None and api_history is None:
        print(f"  [skip] {task_id} sem conteúdo reconhecível")
        return

    ts = metadata.get("created_at") or metadata.get("ts")
    if ts:
        try:
            dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        except Exception:
            dt = datetime.fromtimestamp(task_dir.stat().st_mtime)
    else:
        dt = datetime.fromtimestamp(task_dir.stat().st_mtime)

    stamp = dt.strftime("%Y-%m-%d-%H%M")
    out_name = f"{stamp}-cline-{task_id}.json"
    out_path = DEST_DIR / out_name

    payload = {
        "task_id": task_id,
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "task_metadata": metadata,
        "ui_messages": ui_messages,
        "api_conversation_history": api_history,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2)

    size_mb = len(text.encode("utf-8")) / (1024 * 1024)
    gzip_it = size_mb > MAX_SIZE_MB

    if dry_run:
        print(f"  [dry] exportaria {out_name} ({size_mb:.1f} MB{' → gz' if gzip_it else ''})")
        return

    if gzip_it:
        out_path = out_path.with_suffix(".json.gz")
        with gzip.open(out_path, "wt", encoding="utf-8") as f:
            f.write(text)
        print(f"  [ok]   {out_path.name} ({size_mb:.1f} MB gz)")
    else:
        out_path.write_text(text, encoding="utf-8")
        print(f"  [ok]   {out_path.name} ({size_mb:.1f} MB)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--tool", default="cline", choices=["cline"])
    args = parser.parse_args()

    src = find_cline_tasks_dir()
    if not src:
        print("Não encontrei a pasta de tasks do Cline.")
        print("Defina CLINE_TASKS_DIR=/caminho/para/tasks")
        return 1

    print(f"Lendo de: {src}")
    print(f"Gravando em: {DEST_DIR}")

    tasks = sorted([p for p in src.iterdir() if p.is_dir()])
    print(f"Encontradas {len(tasks)} tasks.\n")

    for t in tasks:
        export_task(t, args.dry_run)

    print("\nPronto. Revise os arquivos antes do commit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())