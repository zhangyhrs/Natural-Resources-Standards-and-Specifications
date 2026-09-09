<h1 align="center">自然资源标准规范与法律法规库</h1>

<p align="center"><strong>Natural Resources Standards, Specifications, Laws & Regulations Library</strong></p>

<p align="center">面向自然资源、测绘地理信息及相关业务的标准规范与法律法规资料库</p>

<p align="center">
  <a href="./README.md"><b>🇨🇳 中文</b></a> ·
  <a href="./README_EN.md">🇺🇸 English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/技术标准-自然资源标准体系2022-2F6B3B" alt="技术标准">
  <img src="https://img.shields.io/badge/法律法规-效力层级分类-2F5597" alt="法律法规">
  <img src="https://img.shields.io/badge/资料库-持续更新-00897B" alt="持续更新">
</p>

<p align="center">
  <a href="https://zhangyhrs.github.io/Natural-Resources-Standards-and-Specifications/"><b>🔎 标准检索</b></a> ·
  <a href="https://zhangyhrs.github.io/Natural-Resources-Standards-and-Specifications/laws.html"><b>⚖️ 法规检索</b></a> ·
  <a href="./标准目录.md"><b>📋 标准目录</b></a> ·
  <a href="./法律法规索引.md"><b>📖 法律法规目录</b></a> ·
  <a href="./常用资料速查.md"><b>⭐ 常用速查</b></a> ·
  <a href="./总索引.md"><b>📚 总索引</b></a> ·
  <a href="./CHANGELOG.md"><b>🕒 更新日志</b></a> ·
  <a href="./待整理/"><b>📥 待整理</b></a>
</p>

---

## 📚 仓库简介

本仓库用于集中整理自然资源领域常用的**技术标准、规范规程、法律法规、部门规章、规范性文件及政策文件**，便于日常学习、项目实施和资料查阅。技术标准按照自然资源部2022年《自然资源标准体系》组织，法律法规按照“**法律效力层级 → 业务领域或地区**”分类，资料后续持续补充更新。

| 资料类型 | 组织方式 | 快速入口 |
|---|---|---|
| **技术标准规范** | 自然资源部2022年《自然资源标准体系》 | [标准检索](https://zhangyhrs.github.io/Natural-Resources-Standards-and-Specifications/) · [标准目录](./标准目录.md) |
| **法律法规** | 法律效力层级 → 业务领域或地区 | [法规检索](https://zhangyhrs.github.io/Natural-Resources-Standards-and-Specifications/laws.html) · [法律法规目录](./法律法规索引.md) |
| **常用资料** | 高频标准和常用业务资料 | [常用资料速查](./常用资料速查.md) |
| **全部资料** | 总索引与自动文件清单 | [总索引](./总索引.md) |

## 🔎 在线检索

标准检索页支持按**标准名称、标准号、标准层级、标准性质、标准体系、专业分类**筛选，并可直接下载仓库已收录文档。

法律法规检索页支持按**法规名称、法律效力层级、业务领域或地区、发布机关**筛选，并可直接下载对应文档。两个页面采用统一界面，可相互切换。

## 🗂️ 技术标准体系

技术标准统一存放在 [`标准规范`](./标准规范/) 目录，按照自然资源部《自然资源标准体系（2022）》组织：

| 代码 | 子体系 | 代码 | 子体系 |
|---|---|---|---|
| TY1-00 | 基础通用 | DJ2-00 | 自然资源调查监测 |
| GH2-00 | 国土空间规划 | ZC2-00 | 自然资源确权登记与权益 |
| LY2-00 | 自然资源开发利用 | DC2-00 | 用途管制与督察执法 |
| ST2-00 | 国土空间生态保护与修复 | TD2-00 | 土地资源 |
| DZ2-00 | 地质与矿产资源 | HY2-00 | 海洋 |
| XX2-00 | 自然资源信息化 | CH2-00 | 测绘地理信息 |

## ⚖️ 法律法规体系

法律法规通过 [`法律法规目录`](./法律法规索引.md) 浏览，采用“**法律效力层级 → 业务领域或地区**”的双重分类：

`01 宪法` → `02 法律` → `03 行政法规` → `04 部门规章` → `05 地方性法规` → `06 地方政府规章` → `07 司法解释` → `08 规范性文件与政策文件`

同一层级内再按业务领域或地区细分，并保留时间、发布机关、业务领域或地区等辅助信息。

## 🔄 自动索引与更新

仓库通过 `scripts/build_inventory.py` 扫描标准规范和法律法规资料，并生成检索数据。GitHub Pages 会随仓库更新自动重新部署，人工维护的 [标准目录](./标准目录.md) 和 [法律法规目录](./法律法规索引.md) 继续作为主要业务分类依据。

新上传但尚未校核的资料可先放入 [`待整理`](./待整理/)；重要结构调整和批量更新记录在 [CHANGELOG.md](./CHANGELOG.md)。

## ⚠️ 版权与免责声明

本仓库主要用于技术学习、资料索引和行业资料整理。各标准、规范、法律法规及相关文件的著作权和传播权归原发布机构或权利人所有；具体法律效力、现行状态和适用范围应以官方发布文本为准。

---

<p align="center">Maintained by <a href="https://github.com/zhangyhrs">Zhang Y.H.</a></p>
