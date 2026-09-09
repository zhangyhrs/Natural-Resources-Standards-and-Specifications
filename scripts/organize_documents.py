from __future__ import annotations

import argparse
import hashlib
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "待整理"
STANDARDS = ROOT / "标准规范"
LAWS = ROOT / "法律法规"
REVIEW = INBOX / "待人工确认"
DUPLICATES = INBOX / "重复文件"
REPORT_DIR = ROOT / "整理报告"

DOC_SUFFIXES = {".pdf", ".doc", ".docx"}
SKIP_DIRS = {"疑似重复", "待人工确认", "重复文件"}

STANDARD_PREFIX_RE = re.compile(
    r"^(?P<prefix>(?:GB|CH|TD|DZ|HY|SL|LY|NY|CJJ|JGJ|JTG|NB|HJ|MH|WS|AQ|JC|DB|T|Q)[A-Z0-9._-]*)\s*(?P<number>\d+(?:\.\d+)?)\s*[-—]\s*(?P<year>\d{4})\b",
    re.I,
)

LEGAL_HINTS = (
    "中华人民共和国", "条例", "办法", "规定", "决定", "司法解释", "实施细则",
    "通知", "意见", "令", "批复",
)
TECH_HINTS = (
    "规范", "规程", "标准", "技术指南", "技术要求", "技术大纲", "技术文件", "工作细则",
    "数据库", "图式", "测量", "测绘", "调查", "监测", "确权登记", "勘测定界",
)


@dataclass
class Decision:
    category: str
    destination: Path | None
    confidence: int
    reason: str


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_filename(name: str) -> str:
    p = Path(name)
    stem = p.stem.strip()
    stem = re.sub(r"^\s*\d+\s*[-_.、]+\s*", "", stem)
    stem = stem.replace("GB_T", "GBT").replace("CH_T", "CHT").replace("TD_T", "TDT")
    stem = stem.replace("DZ_T", "DZT").replace("HY_T", "HYT").replace("SL_T", "SLT")
    stem = re.sub(r"[《》]", "", stem)
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem + p.suffix.lower()


def text_has(text: str, *keywords: str) -> bool:
    return any(k in text for k in keywords)


def classify_standard(filename: str) -> Decision | None:
    text = Path(filename).stem
    upper = text.upper().replace("_", "").replace("/", "")

    # 测绘地理信息
    if text_has(text, "2000国家大地坐标系", "坐标转换"):
        return Decision("技术标准", STANDARDS / "CH2-00 测绘地理信息" / "获取与处理" / "大地测量" / "坐标转换", 98, "坐标转换关键词")
    if text_has(text, "国家基本比例尺地图图式", "地图图式"):
        return Decision("技术标准", STANDARDS / "CH2-00 测绘地理信息" / "获取与处理" / "地图编制与印刷", 98, "地图图式关键词")
    if text_has(text, "新型基础测绘", "实景三维", "基础地理实体"):
        return Decision("技术资料", STANDARDS / "CH2-00 测绘地理信息" / "获取与处理" / "新型基础测绘与实景三维", 98, "新型基础测绘/实景三维关键词")
    if text_has(text, "土地勘测定界", "勘测定界"):
        dest = STANDARDS / "CH2-00 测绘地理信息" / "获取与处理" / "地籍测绘" / "土地勘测定界"
        if "西藏自治区" in text:
            dest = dest / "西藏自治区"
        return Decision("技术资料", dest, 97, "土地勘测定界关键词")
    if text_has(text, "测绘技术设计", "测绘技术总结"):
        return Decision("技术标准", STANDARDS / "CH2-00 测绘地理信息" / "管理" / "项目管理", 97, "测绘项目管理关键词")
    if text_has(text, "RTK", "GNSS", "卫星导航", "水准", "大地测量", "控制点坐标"):
        return Decision("技术标准", STANDARDS / "CH2-00 测绘地理信息" / "获取与处理" / "大地测量", 92, "大地测量关键词")

    # 确权登记与权益
    if "农村土地承包经营权" in text:
        return Decision("技术标准", STANDARDS / "ZC2-00 自然资源确权登记与权益" / "自然资源和不动产确权登记" / "农村土地承包经营权", 98, "农村土地承包经营权关键词")
    if "集体土地所有权" in text:
        return Decision("技术资料", STANDARDS / "ZC2-00 自然资源确权登记与权益" / "自然资源和不动产确权登记" / "业务指南" / "集体土地所有权", 98, "集体土地所有权关键词")
    if text_has(text, "自然资源确权登记", "自然资源登记单元", "不动产登记", "地籍数据库"):
        sub = "业务指南" if text_has(text, "指南", "操作指南") else "地籍数据库" if "数据库" in text else "登记规程"
        return Decision("技术资料", STANDARDS / "ZC2-00 自然资源确权登记与权益" / "自然资源和不动产确权登记" / sub, 94, "确权登记/地籍关键词")

    # 调查监测、用途管制、生态修复、开发利用
    if "冰川" in text:
        if upper.startswith("HYT"):
            return Decision("技术标准", STANDARDS / "HY2-00 海洋" / "极地与冰川", 96, "HY/T 冰川标准")
        region = None
        if upper.startswith("DB63"):
            region = "青海省"
        elif upper.startswith("DB65"):
            region = "新疆维吾尔自治区"
        dest = STANDARDS / "DJ2-00 自然资源调查监测" / "冰川资源调查监测"
        if region:
            dest = dest / "地方标准" / region
        return Decision("技术标准", dest, 94, "冰川调查监测关键词")
    if "森林资源规划设计调查" in text:
        return Decision("技术标准", STANDARDS / "DJ2-00 自然资源调查监测" / "森林资源调查监测", 96, "森林资源调查关键词")
    if text_has(text, "河湖管理范围", "水资源调查"):
        return Decision("技术标准", STANDARDS / "DJ2-00 自然资源调查监测" / "水资源调查监测" / "河湖管理范围", 96, "河湖管理范围关键词")
    if "永久基本农田" in text:
        return Decision("技术资料", STANDARDS / "DC2-00 用途管制与督察执法" / "耕地用途管制" / "永久基本农田", 98, "永久基本农田关键词")
    if "自然资源分等定级" in text:
        return Decision("技术标准", STANDARDS / "LY2-00 自然资源开发利用" / "自然资源分等定级", 98, "自然资源分等定级关键词")
    if "自然保护地" in text and text_has(text, "勘界", "立标"):
        return Decision("技术标准", STANDARDS / "ST2-00 国土空间生态保护与修复" / "自然保护地" / "勘界立标", 98, "自然保护地勘界立标关键词")

    # 基础通用
    if text_has(text, "行政区划代码", "国民经济行业分类"):
        return Decision("技术标准", STANDARDS / "TY1-00 基础通用" / "分类代码", 98, "分类代码关键词")

    # 有明确标准号，但暂时无法准确落到专业目录时，不强行归档
    if STANDARD_PREFIX_RE.search(Path(filename).stem):
        return Decision("待确认", None, 65, "识别到标准号，但专业目录判断不足")
    return None


def looks_legal(filename: str) -> bool:
    stem = Path(filename).stem
    if STANDARD_PREFIX_RE.search(stem):
        return False
    core = re.sub(r"[_\-\s]?\d{8}$", "", stem).strip()
    # 明确的法律法规名称优先于专业关键词，避免“冰川保护条例”等误归技术标准。
    if core.endswith("法") or core.endswith("条例"):
        return True
    if "实施" in core and "办法" in core and "法" in core:
        return True
    legal_hits = sum(1 for k in LEGAL_HINTS if k in core)
    tech_hits = sum(1 for k in TECH_HINTS if k in core)
    return legal_hits >= 2 and legal_hits > tech_hits


def decide(filename: str) -> Decision:
    # 法律法规识别必须先于专业技术关键词分类。
    if looks_legal(filename):
        return Decision("法律法规待确认", None, 90, "明确法律法规名称；优先进入人工确认，避免误归技术标准")
    std = classify_standard(filename)
    if std:
        return std
    return Decision("待确认", None, 50, "缺少足够明确的自动分类依据")


def unique_path(dest_dir: Path, filename: str, source_hash: str) -> tuple[Path, bool]:
    dest = dest_dir / filename
    if not dest.exists():
        return dest, False
    if sha256(dest) == source_hash:
        return dest, True
    stem, suffix = Path(filename).stem, Path(filename).suffix
    i = 2
    while True:
        candidate = dest_dir / f"{stem}（版本{i}）{suffix}"
        if not candidate.exists():
            return candidate, False
        i += 1


def build_existing_hashes() -> dict[str, Path]:
    result: dict[str, Path] = {}
    for base in (STANDARDS, LAWS):
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and p.suffix.lower() in DOC_SUFFIXES:
                try:
                    result.setdefault(sha256(p), p)
                except OSError:
                    pass
    return result


def inbox_files() -> list[Path]:
    files = []
    if not INBOX.exists():
        return files
    for p in INBOX.iterdir():
        if p.is_file() and p.suffix.lower() in DOC_SUFFIXES:
            files.append(p)
    return sorted(files, key=lambda p: p.name.lower())


def move_file(src: Path, dest: Path, dry_run: bool) -> None:
    if dry_run:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest))


def main() -> None:
    parser = argparse.ArgumentParser(description="整理待整理目录中的 PDF/DOC/DOCX")
    parser.add_argument("--dry-run", action="store_true", help="仅生成整理报告，不移动文件")
    args = parser.parse_args()

    existing_hashes = build_existing_hashes()
    rows = []

    for src in inbox_files():
        original_name = src.name
        clean_name = normalize_filename(original_name)
        digest = sha256(src)

        if digest in existing_hashes:
            matched = existing_hashes[digest]
            dest = DUPLICATES / clean_name
            action = "重复文件"
            reason = f"与 {matched.relative_to(ROOT).as_posix()} 内容完全一致"
            move_file(src, dest, args.dry_run)
            rows.append((original_name, action, dest.relative_to(ROOT).as_posix(), 100, reason))
            continue

        decision = decide(clean_name)
        if decision.destination is not None and decision.confidence >= 90:
            dest, same = unique_path(decision.destination, clean_name, digest)
            if same:
                dest = DUPLICATES / clean_name
                action = "重复文件"
                reason = "目标目录已存在完全相同文件"
            else:
                action = "自动归档"
                reason = decision.reason
            move_file(src, dest, args.dry_run)
            if action == "自动归档":
                existing_hashes[digest] = dest
            rows.append((original_name, action, dest.relative_to(ROOT).as_posix(), decision.confidence, reason))
        else:
            dest = REVIEW / clean_name
            move_file(src, dest, args.dry_run)
            rows.append((original_name, "待人工确认", dest.relative_to(ROOT).as_posix(), decision.confidence, decision.reason))

    now = datetime.now(ZoneInfo("Asia/Shanghai"))
    REPORT_DIR.mkdir(exist_ok=True)
    report = REPORT_DIR / f"{now:%Y-%m-%d_%H%M%S}{'_预览' if args.dry_run else ''}.md"
    summary = {
        "自动归档": sum(1 for r in rows if r[1] == "自动归档"),
        "重复文件": sum(1 for r in rows if r[1] == "重复文件"),
        "待人工确认": sum(1 for r in rows if r[1] == "待人工确认"),
    }
    lines = [
        "# 自动整理报告",
        "",
        f"- 时间：{now:%Y-%m-%d %H:%M:%S}（北京时间）",
        f"- 模式：{'仅预览' if args.dry_run else '正式整理'}",
        f"- 扫描文件：{len(rows)} 个",
        f"- 自动归档：{summary['自动归档']} 个",
        f"- 重复文件：{summary['重复文件']} 个",
        f"- 待人工确认：{summary['待人工确认']} 个",
        "",
        "| 原文件 | 处理结果 | 目标位置 | 置信度 | 判断依据 |",
        "|---|---|---|---:|---|",
    ]
    if rows:
        for name, action, dest, confidence, reason in rows:
            lines.append(f"| {name.replace('|','／')} | {action} | `{dest}` | {confidence}% | {reason.replace('|','／')} |")
    else:
        lines.append("| — | 无待处理文件 | — | — | — |")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Processed {len(rows)} files: {summary}; report={report.relative_to(ROOT)}")


if __name__ == "__main__":
    main()