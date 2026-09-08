<h1 align="center">Natural Resources Standards & Specifications</h1>

<p align="center">
  <strong>Technical standards · specifications · regulations · reference documents</strong><br/>
  for natural resources, surveying & mapping, remote sensing, GIS, cadastral surveying and registration.
</p>

<p align="center">
  <a href="./README.md">🇨🇳 中文</a> · <a href="./README_EN.md"><b>🇺🇸 English</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Natural_Resources-Standards-2E7D32?style=flat-square" />
  <img src="https://img.shields.io/badge/Surveying_%26_Mapping-Specifications-1565C0?style=flat-square" />
  <img src="https://img.shields.io/badge/Remote_Sensing-GIS-00838F?style=flat-square" />
  <img src="https://img.shields.io/badge/Cadastral-Registration-6A1B9A?style=flat-square" />
  <img src="https://img.shields.io/badge/Policies-Technical_Standards-C77800?style=flat-square" />
</p>

---

## 📚 About

This repository maintains **technical standards, specifications, regulations, policies and reference documents** for the natural resources sector, with a focus on natural resources survey and monitoring, cadastral work, real estate and natural resources registration, surveying and mapping, remote sensing and GIS.

The classification follows the **Natural Resources Standards System (2022)** as the main framework, while surveying and mapping standards are further organized with reference to the **Surveying and Mapping Standards System**.

## 🗂️ Classification

Standards are primarily organized according to natural resources business domains. Surveying and mapping documents are further subdivided into categories such as definition & description, acquisition & processing, inspection & testing, products & services, and management.

Processed standards are stored under [`standards`](./standards/), while newly uploaded and unclassified files may first be placed in [`incoming`](./incoming/).

## 🔎 Catalog

The master index is maintained in [`catalog.csv`](./catalog.csv), including the standard number, title, primary and secondary category, status, replacement relationship, file path and source information.

As the library grows, `catalog.csv` should be treated as the primary search and management index.

## 📝 File Naming

Use the following format:

```text
StandardNo StandardTitle.pdf
```

Example:

```text
TDT 1015.2-2024 地籍数据库 第2部分：自然资源.pdf
```

Keep the **official standard number and official title** whenever possible, and remove download-site names, timestamps, repeated spaces and other redundant text.

## ✅ Maintenance Rules

- One standard/document per PDF whenever possible.
- Keep official titles and standard numbers unchanged.
- Do not silently delete revised, abolished or superseded standards; record their status and relationships in `catalog.csv`.
- Newly uploaded files that have not yet been classified should be placed in `incoming` first.
- When multiple versions of the same standard exist, preserve their version relationships and identify current, abolished or superseded status.
- Prefer authoritative official source links whenever available.

## ⚠️ Copyright & Disclaimer

This repository is intended for **technical reference, learning and document indexing**. Copyright and distribution rights of individual standards and documents remain with their respective publishers or rights holders.

Public accessibility does not automatically imply unrestricted redistribution rights. When redistribution rights are unclear, only metadata and official source links should be maintained instead of the full PDF.

If any material should not be included here, please open an Issue for review.

---

<p align="center">Maintained by <a href="https://github.com/zhangyhrs">Zhang Y.H.</a></p>
