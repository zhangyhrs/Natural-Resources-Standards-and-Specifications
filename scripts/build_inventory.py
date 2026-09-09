from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
TARGET_DIRS = [ROOT / "标准规范", ROOT / "法律法规"]
OUT_CSV = ROOT / "catalog_auto.csv"
OUT_MD = ROOT / "文件清单_自动生成.md"
OUT_JSON = ROOT / "docs" / "standards.json"

ALLOWED_SUFFIXES = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".md"}
STANDARD_SUFFIXES = {".pdf", ".doc", ".docx"}

PREFIX_MAP = {
    "GBT": "GB/T",
    "GBZ": "GB/Z",
    "GB": "GB",
    "CHT": "CH/T",
    "CHZ": "CH/Z",
    "CJJT": "CJJ/T",
    "DZT": "DZ/T",
    "TDT": "TD/T",
    "LYT": "LY/T",
    "NYT": "NY/T",
    "HYT": "HY/T",
}


def iter_files():
    for base in TARGET_DIRS:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*"), key=lambda p: p.as_posix().lower()):
            if path.is_file() and path.suffix.lower() in ALLOWED_SUFFIXES:
                yield path


def classify(path: Path):
    rel = path.relative_to(ROOT)
    parts = rel.parts
    source_type = parts[0]
    level1 = parts[1] if len(parts) > 2 else ""
    level2 = parts[2] if len(parts) > 3 else ""
    level3 = parts[3] if len(parts) > 4 else ""
    return source_type, level1, level2, level3, rel


def github_link(rel: Path) -> str:
    return "./" + "/".join(quote(part) for part in rel.parts)


def parse_standard_name(filename: str) -> dict[str, str]:
    stem = Path(filename).stem.strip()
    stem = re.sub(r"\s+", " ", stem)
    m = re.match(r"^(GB_T|GBT|GBZ|GB|CHT|CHZ|CJJT|DZT|TDT|LYT|NYT|HYT)\s*([0-9]+(?:\.[0-9]+)?)-([0-9]{4})\s*(.*)$", stem, re.I)
    if not m:
        return {"标准号": "", "标准名称": stem, "年份": "", "标准层级": "其他", "标准性质": "其他"}

    raw_prefix = m.group(1).upper().replace("_", "")
    number = m.group(2)
    year = m.group(3)
    title = m.group(4).strip(" -_")
    formal_prefix = PREFIX_MAP.get(raw_prefix, raw_prefix)
    std_no = f"{formal_prefix} {number}-{year}"

    if raw_prefix in {"GB", "GBT", "GBZ"}:
        level = "国家标准"
    elif raw_prefix in {"CHT", "CHZ", "CJJT", "DZT", "TDT", "LYT", "NYT", "HYT"}:
        level = "行业标准"
    else:
        level = "其他"

    if raw_prefix == "GB":
        nature = "强制性"
    elif raw_prefix in {"GBZ", "CHZ"}:
        nature = "指导性技术文件"
    elif raw_prefix.endswith("T"):
        nature = "推荐性"
    else:
        nature = "其他"

    return {"标准号": std_no, "标准名称": title or stem, "年份": year, "标准层级": level, "标准性质": nature}


def build_standards_json() -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    standards_root = ROOT / "标准规范"
    if not standards_root.exists():
        return items

    for path in sorted(standards_root.rglob("*"), key=lambda p: p.as_posix().lower()):
        if not path.is_file() or path.suffix.lower() not in STANDARD_SUFFIXES:
            continue
        rel = path.relative_to(ROOT)
        parts = rel.parts
        system = parts[1] if len(parts) > 2 else "未分类"
        domain_parts = [p for p in parts[2:-1] if p]
        domain = " / ".join(domain_parts) if domain_parts else "未分类"
        parsed = parse_standard_name(path.name)
        repo_url = "https://github.com/zhangyhrs/Natural-Resources-Standards-and-Specifications/blob/main/" + "/".join(quote(p) for p in rel.parts)
        items.append(
            {
                **parsed,
                "标准体系": system,
                "专业分类": domain,
                "文件名": path.name,
                "文件路径": rel.as_posix(),
                "链接": repo_url,
            }
        )
    return items


def main():
    rows = []
    for path in iter_files():
        source_type, level1, level2, level3, rel = classify(path)
        rows.append(
            {
                "资料类型": source_type,
                "一级分类": level1,
                "二级分类": level2,
                "三级分类": level3,
                "文件名": path.name,
                "扩展名": path.suffix.lower(),
                "相对路径": rel.as_posix(),
            }
        )

    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["资料类型", "一级分类", "二级分类", "三级分类", "文件名", "扩展名", "相对路径"],
        )
        writer.writeheader()
        writer.writerows(rows)

    groups: dict[str, list[dict]] = {}
    for row in rows:
        groups.setdefault(row["资料类型"], []).append(row)

    lines = [
        "# 📦 自动文件清单",
        "",
        "> 本文件由 `scripts/build_inventory.py` 自动生成，仅反映仓库当前文件结构，不替代人工维护的标准目录和法律法规目录。",
        "",
        f"当前共扫描到 **{len(rows)}** 个资料文件。",
        "",
    ]

    for source_type in ["标准规范", "法律法规"]:
        items = groups.get(source_type, [])
        lines += [f"## {source_type}", ""]
        if not items:
            lines += ["暂无文件。", ""]
            continue
        by_level1: dict[str, list[dict]] = {}
        for row in items:
            by_level1.setdefault(row["一级分类"] or "未分类", []).append(row)
        for level1, level_items in sorted(by_level1.items()):
            lines += [f"### {level1}", ""]
            for row in level_items:
                rel = Path(row["相对路径"])
                lines.append(f"- [{row['文件名']}]({github_link(rel)})")
            lines.append("")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    standards = build_standards_json()
    OUT_JSON.write_text(json.dumps(standards, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Generated {OUT_CSV.name}, {OUT_MD.name} and {OUT_JSON.relative_to(ROOT)}: {len(rows)} files / {len(standards)} standards")


if __name__ == "__main__":
    main()
