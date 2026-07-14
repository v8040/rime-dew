# SPDX-License-Identifier: GPL-3.0-only

import urllib.request
import zipfile
import shutil
import re
import subprocess
import sys
from pathlib import Path

ICE_ZIP_URL = "https://github.com/iDvel/rime-ice/archive/refs/heads/main.zip"
FROST_ZIP_URL = "https://github.com/gaboolic/rime-frost/archive/refs/heads/master.zip"
ICE_KEEP_FILES = {
    "rime_ice.schema.yaml",
    "t9.schema.yaml",
    "melt_eng.schema.yaml",
    "melt_eng.dict.yaml",
    "en_dicts",
    "default.yaml",
    "symbols_v.yaml",
    "radical_pinyin.schema.yaml",
    "radical_pinyin.dict.yaml",
    "lua",
    "opencc",
    "weasel.yaml",
    "squirrel.yaml",
    "custom_phrase.txt",
}
root_dir = Path(__file__).resolve().parent.parent.parent
temp_dir = root_dir / "temp_build"


def get_clean_whitelist():
    whitelist = {".git", "temp_build"}
    gitignore_path = root_dir / ".gitignore"
    if gitignore_path.exists():
        for line in gitignore_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("!/"):
                name = line[2:].rstrip("/")
                if name:
                    whitelist.add(name)
    generated_files = ICE_KEEP_FILES | {
        "recipe.yaml",
        "rime_ice.dict.yaml",
        "cn_dicts",
        "cn_dicts_cell",
    }
    whitelist -= generated_files
    return whitelist


def clean_root_directory():
    whitelist = get_clean_whitelist()
    for path in root_dir.iterdir():
        if path.name in whitelist:
            continue
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()


def download_and_extract(url, name, signature):
    extract_path = temp_dir / name
    extract_path.mkdir(parents=True, exist_ok=True)
    zip_path = temp_dir / f"{name}.zip"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(req) as resp:
        with open(zip_path, "wb") as f:
            shutil.copyfileobj(resp, f)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)
    zip_path.unlink()
    matches = list(extract_path.glob(f"**/{signature}"))
    if not matches:
        raise FileNotFoundError(
            f"Signature '{signature}' not found in extracted {name} zip"
        )
    return matches[0].parent


def normalize_line_endings():
    target_suffixes = {".lua", ".yaml", ".txt", ".dict", ".schema"}
    for path in root_dir.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_file() and path.suffix in target_suffixes:
            try:
                content = path.read_text(encoding="utf-8")
                path.write_text(content.replace("\r\n", "\n"), encoding="utf-8")
            except Exception as e:
                print(f"Warning: normalize {path.name}: {e}", file=sys.stderr)


def main():
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    ice_root = download_and_extract(ICE_ZIP_URL, "ice", "rime_ice.schema.yaml")
    frost_root = download_and_extract(FROST_ZIP_URL, "frost", "cn_dicts")
    clean_root_directory()
    for item in ICE_KEEP_FILES:
        src = ice_root / item
        dst = root_dir / item
        if src.exists():
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
    shutil.copytree(frost_root / "cn_dicts", root_dir / "cn_dicts")
    shutil.copytree(frost_root / "cn_dicts_cell", root_dir / "cn_dicts_cell")
    default_yaml_path = root_dir / "default.yaml"
    if default_yaml_path.exists():
        subprocess.run(
            [
                "yq", "-i",
                ".schema_list = [{\"schema\": \"rime_ice\"}, {\"schema\": \"t9\"}]",
                str(default_yaml_path),
            ],
            check=True,
        )
    custom_dict_src = root_dir / "others" / "presets" / "rime_frost.dict.yaml"
    dest_dict_path = root_dir / "rime_ice.dict.yaml"
    if custom_dict_src.exists():
        content = custom_dict_src.read_text(encoding="utf-8")
        content = re.sub(
            r"^name: rime_frost$", "name: rime_ice", content, flags=re.MULTILINE
        )
        dest_dict_path.write_text(content, encoding="utf-8")
    else:
        frost_dict_default = frost_root / "rime_frost.dict.yaml"
        if frost_dict_default.exists():
            content = frost_dict_default.read_text(encoding="utf-8")
            content = re.sub(
                r"^name: rime_frost$", "name: rime_ice", content, flags=re.MULTILINE
            )
            dest_dict_path.write_text(content, encoding="utf-8")
    full_recipe_path = root_dir / "others" / "recipes" / "full.recipe.yaml"
    dest_recipe_path = root_dir / "recipe.yaml"
    if full_recipe_path.exists():
        shutil.copy2(str(full_recipe_path), str(dest_recipe_path))
        subprocess.run(
            ["yq", "-i", ".recipe.Rx = \"all\"", str(dest_recipe_path)],
            check=True,
        )
    normalize_line_endings()
    shutil.rmtree(temp_dir)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(1)
