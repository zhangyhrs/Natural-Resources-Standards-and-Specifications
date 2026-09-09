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
DOCS_DIR = ROOT / "docs"
STANDARDS_JSON = DOCS_DIR / "standards.json"
LAWS_JSON = DOCS_DIR / "laws.json"
LEGAL_INDEX = ROOT / "法律法规索引.md"

ALLOWED_SUFFIXES = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".txt", ".md"}
STANDARD_RE = re.compile(r"^(?P<prefix>[A-Z]+(?:\.?[A-Z]+)?)\s*(?P<number>\d+(?:\.\d+)?)\s*[-—]\s*(?P<year>\d{4})\s*(?P<title>.*)$")
LEGAL_ITEM_RE = re.compile(
    r"^- \[(?P<title>.+?)\]\((?P<path>.+?)\)\s*·\s*`(?P<date>[^`]*)`\s*·\s*`(?P<issuer>[^`]*)`\s*·\s*`(?P<tag>[^`]*)`"
)
SUMMARY_RE = re.compile(r"<summary><b>(?P<level>\d{2}\s+[^<]+)</b></summary>")


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


def repo_blob_url(rel: Path) -> str:
    encoded = "/".join(quote(part) for part in rel.parts)
    return f"https://github.com/zhangyhrs/Natural-Resources-Standards-and-Specifications/blob/main/{encoded}"


def standard_level(prefix: str) -> str:
    p = prefix.replace("_", "").upper()
    if p.startswith("GB"):
        return "国家标准"
    return "行业标准"


def standard_nature(prefix: str) -> str:
    p = prefix.replace("_", "").upper()
    if p in {"GB", "GBT"}:
        return "强制性" if p == "GB" else "推荐性"
    if p.endswith("Z"):
        return "指导性技术文件"
    return "推荐性"


def parse_standard(path: Path) -> dict | None:
    stem = path.stem.strip().replace("  ", " ")
    m = STANDARD_RE.match(stem)
    if not m:
        return None
    prefix = m.group("prefix").replace("_", "")
    title = m.group("title").strip()
    official_prefix = prefix
    replacements = {"GBT": "GB/T", "CHT": "CH/T", "CHZ": "CH/Z", "DZT": "DZ/T", "TDT": "TD/T", "LYT": "LY/T", "NYT": "NY/T", "CJJT": "CJJ/T"}
    official_prefix = replacements.get(prefix, prefix)
    std_no = f"{official_prefix} {m.group('number')}-{m.group('year')}"
    rel = path.relative_to(ROOT)
    parts = rel.parts
    system = parts[1] if len(parts) > 2 else "未分类"
    domain = " / ".join(parts[2:-1]) if len(parts) > 3 else "未分类"
    return {
        "标准号": std_no,
        "标准名称": title or stem,
        "标准层级": standard_level(prefix),
        "标准性质": standard_nature(prefix),
        "标准体系": system,
        "专业分类": domain or "未分类",
        "年份": m.group("year"),
        "文件名": path.name,
        "链接": repo_blob_url(rel),
    }


def build_laws() -> list[dict]:
    if not LEGAL_INDEX.exists():
        return []
    laws = []
    current_level = "未分类"
    current_domain = "未分类"
    for raw in LEGAL_INDEX.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        m = SUMMARY_RE.search(line)
        if m:
            current_level = m.group("level").strip()
            current_domain = "未分类"
            continue
        if line.startswith("### "):
            current_domain = line[4:].strip()
            continue
        m = LEGAL_ITEM_RE.match(line)
        if not m:
            continue
        path_text = m.group("path").replace("%20", " ")
        if path_text.startswith("./"):
            path_text = path_text[2:]
        rel = Path(path_text)
        laws.append({
            "名称": m.group("title").strip(),
            "效力层级": current_level,
            "业务领域或地区": current_domain,
            "日期": m.group("date").strip(),
            "发布机关": m.group("issuer").strip(),
            "标签": m.group("tag").strip(),
            "链接": repo_blob_url(rel),
        })
    return laws


def main():
    rows = []
    standards = []
    for path in iter_files():
        source_type, level1, level2, level3, rel = classify(path)
        rows.append({
            "资料类型": source_type,
            "一级分类": level1,
            "二级分类": level2,
            "三级分类": level3,
            "文件名": path.name,
            "扩展名": path.suffix.lower(),
            "相对路径": rel.as_posix(),
        })
        if source_type == "标准规范":
            item = parse_standard(path)
            if item:
                standards.append(item)

    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["资料类型", "一级分类", "二级分类", "三级分类", "文件名", "扩展名", "相对路径"])
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
    DOCS_DIR.mkdir(exist_ok=True)
    STANDARDS_JSON.write_text(json.dumps(standards, ensure_ascii=False, indent=2), encoding="utf-8")
    laws = build_laws()
    LAWS_JSON.write_text(json.dumps(laws, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {OUT_CSV.name}, {OUT_MD.name}, docs/standards.json and docs/laws.json: {len(rows)} files / {len(standards)} standards / {len(laws)} laws")


if __name__ == "__main__":
    main()
