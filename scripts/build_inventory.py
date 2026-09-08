from __future__ import annotations

import csv
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
TARGET_DIRS = [ROOT / "标准规范", ROOT / "法律法规"]
OUT_CSV = ROOT / "catalog_auto.csv"
OUT_MD = ROOT / "文件清单_自动生成.md"

ALLOWED_SUFFIXES = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".md"}


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
    print(f"Generated {OUT_CSV.name} and {OUT_MD.name}: {len(rows)} files")


if __name__ == "__main__":
    main()
