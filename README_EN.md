<h1 align="center">Natural Resources Standards & Specifications</h1>

<p align="center">
  <strong>Technical standards · specifications · regulations · reference documents</strong><br/>
  for natural resources survey and monitoring, spatial planning, registration, surveying & mapping, remote sensing and GIS.
</p>

<p align="center">
  <a href="./README.md">🇨🇳 中文</a> · <a href="./README_EN.md"><b>🇺🇸 English</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Natural_Resources-Technical_Standards-2E7D32?style=flat-square" />
  <img src="https://img.shields.io/badge/Survey_%26_Monitoring-Registration-1565C0?style=flat-square" />
  <img src="https://img.shields.io/badge/Surveying_%26_Mapping-Remote_Sensing_GIS-00838F?style=flat-square" />
  <img src="https://img.shields.io/badge/Spatial_Planning-Ecological_Restoration-6A1B9A?style=flat-square" />
  <img src="https://img.shields.io/badge/Standards_System-2022-C77800?style=flat-square" />
</p>

---

## 📚 About

This repository collects and maintains **technical standards, specifications, regulations, policies and reference documents** in the natural resources domain for classification, retrieval, version management and long-term maintenance.

The repository is organized according to the **Natural Resources Standards System issued by the Ministry of Natural Resources of China in May 2022**. The top-level folders follow the official classification framework, while lower-level folders are further divided according to the professional scope of the collected standards.

## 🗂️ Classification

All classified documents are stored under [`标准规范`](./标准规范/). The top-level categories follow the 2022 Natural Resources Standards System:

- `TY1-00 基础通用`
- `DJ2-00 自然资源调查监测`
- `GH2-00 国土空间规划`
- `ZC2-00 自然资源确权登记与权益`
- `LY2-00 自然资源开发利用`
- `DC2-00 用途管制与督察执法`
- `ST2-00 国土空间生态保护与修复`
- `TD2-00 土地资源`
- `DZ2-00 地质与矿产资源`
- `HY2-00 海洋`
- `XX2-00 自然资源信息化`
- `CH2-00 测绘地理信息`

The folder codes retain the official classification codes and hierarchy used by the Natural Resources Standards System. Categories with a large number of standards, such as surveying and mapping, are further divided into professional subfolders for easier browsing and management.

## 🔎 Catalog

The master index is maintained in [`catalog.csv`](./catalog.csv), including standard number, title, primary and secondary category, status, supersession relationship, file path, source and notes.

As the library grows, `catalog.csv` should be used as the primary search index before browsing the corresponding PDF folders.

## 📥 Incoming Documents

Newly uploaded files that have not yet been classified can be placed in [`待整理`](./待整理/). After checking the official standard number, title and professional category, they can be moved into the formal classification structure.

## 📝 File Naming

Use the following format:

```text
StandardNo StandardTitle.pdf
```

Example:

```text
TDT 1015.2-2024 地籍数据库 第2部分：自然资源.pdf
```

Keep the official standard number and official title whenever possible. Avoid download-site names, timestamps, redundant prefixes and other unrelated text.

## ✅ Maintenance Rules

- One standard/document per PDF whenever possible.
- Keep standard numbers and titles consistent with the officially published text.
- Classification should primarily follow the 2022 Natural Resources Standards System, with further subdivision where necessary.
- Revised, abolished or superseded standards should not be silently deleted; their status and relationships should be retained in `catalog.csv`.
- Uncertain documents should remain in `待整理` until their classification is verified.
- Prefer authoritative sources such as the Ministry of Natural Resources, official national standard services and relevant standards publishers.

## ⚠️ Copyright & Disclaimer

This repository is intended for **technical reference, learning and document indexing**. Copyright and distribution rights of individual standards and documents remain with their respective publishers or rights holders.

Public accessibility does not automatically imply unrestricted redistribution rights. When redistribution rights are unclear, only metadata and official source links should be maintained instead of the full PDF.

---

<p align="center">Maintained by <a href="https://github.com/zhangyhrs">Zhang Y.H.</a></p>
