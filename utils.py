import json
import os


def read_json(file_path):
    """Doc du lieu tu file JSON, tra ve list rong neu loi."""
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def write_json(file_path, data):
    """Ghi du lieu xuong file JSON."""
    folder = os.path.dirname(file_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
