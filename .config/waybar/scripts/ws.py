#!/usr/bin/env python3
import json
import subprocess
import sys


def run_json(cmd: str):
    try:
        out = subprocess.check_output(cmd, shell=True, text=True)
        return json.loads(out)
    except Exception:
        return None


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"text": "?", "class": "ws error", "tooltip": "missing arg"}))
        return

    target = sys.argv[1]
    try:
        target_id = int(target)
    except ValueError:
        target_id = None

    workspaces = run_json("hyprctl -j workspaces") or []
    active_ws = run_json("hyprctl -j activeworkspace") or {}
    clients = run_json("hyprctl -j clients") or []

    # Determine active
    active = False
    if active_ws:
        if target_id is not None and active_ws.get("id") == target_id:
            active = True
        elif str(active_ws.get("name")) == str(target):
            active = True

    # Find matching workspace info
    win_count = 0
    for ws in workspaces:
        if (target_id is not None and ws.get("id") == target_id) or str(ws.get("name")) == str(target):
            win_count = int(ws.get("windows", 0))
            break

    # Urgency detection (best-effort)
    urgent = False
    for c in clients:
        w = c.get("workspace") or {}
        if (target_id is not None and w.get("id") == target_id) or str(w.get("name")) == str(target):
            if c.get("urgent") or c.get("address") in (c.get("urgentWindows") or []):
                urgent = True
                break

    occupied = win_count > 0

    classes = ["ws"]
    classes.append("active" if active else "inactive")
    classes.append("occupied" if occupied else "empty")
    if urgent:
        classes.append("urgent")

    # Display number; could be roman/kanji if desired later
    text = str(target)
    tooltip = f"Workspace {target}: {'occupied' if occupied else 'empty'} | windows={win_count} | {'active' if active else 'inactive'}"

    print(json.dumps({
        "text": text,
        "class": " ".join(classes),
        "tooltip": tooltip
    }))


if __name__ == "__main__":
    main()

