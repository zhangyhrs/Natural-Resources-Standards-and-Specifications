<h1 align="center">Natural Resources Standards & Specifications</h1>

<p align="center">
  <strong>Technical standards · specifications · regulations · reference documents</strong><br/>
  for natural resources, surveying & mapping, remote sensing, GIS, cadastral surveying and registration.
</p>

<p align="center">
  <a href="./README.md"><b>🇺🇸 English</b></a> · <a href="./README_CN.md">🇨🇳 中文</a>
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

This repository is a curated library of **technical standards, specifications, regulations and reference documents** related to the natural resources sector. It is intended for convenient classification, retrieval and long-term maintenance of documents used in surveying, mapping, cadastral work, registration, remote sensing, GIS and related engineering workflows.

Documents are organized by professional field rather than by source organization, so standards from different systems and structures can be maintained in one consistent library.

## 🗂️ Categories

| Category | Scope | Folder |
|---|---|---|
| General | Basic, common and cross-domain standards | [`standards/01-General`](./standards/01-General/) |
| Survey & Monitoring | Natural resources survey, monitoring and investigation | [`standards/02-Survey-Monitoring`](./standards/02-Survey-Monitoring/) |
| Cadastral & Registration | Cadastral surveying, real estate and natural resources registration | [`standards/03-Cadastral-Registration`](./standards/03-Cadastral-Registration/) |
| Surveying & Mapping | Geodesy, photogrammetry, engineering surveying and mapping | [`standards/04-Surveying-Mapping`](./standards/04-Surveying-Mapping/) |
| Remote Sensing & GIS | Remote sensing, GIS, spatial data and databases | [`standards/05-Remote-Sensing-GIS`](./standards/05-Remote-Sensing-GIS/) |
| Land & Spatial Planning | Land use, cultivated land, spatial planning and use control | [`standards/06-Land-Spatial-Planning`](./standards/06-Land-Spatial-Planning/) |
| Ecology & Natural Assets | Forest, grassland, wetland, ecology and natural-resource assets | [`standards/07-Ecology-Natural-Assets`](./standards/07-Ecology-Natural-Assets/) |
| Geology & Minerals | Geology, mineral resources and related technical standards | [`standards/08-Geology-Minerals`](./standards/08-Geology-Minerals/) |
| Other | Documents not yet assigned to the categories above | [`standards/99-Other`](./standards/99-Other/) |

## 🔎 Catalog

The master catalog is maintained in [`catalog.csv`](./catalog.csv). It records the standard number, title, category, status, dates, replacement relationship, file path and source information.

When the library grows, the catalog should be treated as the primary index rather than relying only on folder browsing.

## 📝 File Naming

Recommended naming format:

```text
StandardNo StandardTitle.pdf
```

Example:

```text
TDT 1015.2-2024 地籍数据库 第2部分：自然资源.pdf
```

Keep the **official standard number and official title** whenever possible. Avoid adding unrelated download-site names, timestamps or redundant prefixes to filenames.

## ✅ Maintenance Rules

- One standard/document per PDF file whenever possible.
- Keep official titles and standard numbers unchanged.
- Record revised, abolished or replaced standards in `catalog.csv` instead of silently deleting historical records.
- Put uncertain documents in `99-Other` first, then reclassify them after verification.
- Prefer authoritative or official source links in the catalog.
- Large batches of PDFs should be checked for duplicate files, inconsistent names and version conflicts before merging.

## ⚠️ Copyright & Disclaimer

This repository is intended for **technical reference, learning and document indexing**. Copyright and distribution rights of individual standards and documents remain with their respective publishers or rights holders.

A document being publicly accessible does not necessarily mean it may be freely redistributed. When redistribution rights are unclear, maintain only the document metadata and official source link rather than uploading the full PDF.

If any material should not be included here, please open an issue for review and removal.

---

<p align="center">Maintained by <a href="https://github.com/zhangyhrs">Zhang Y.H.</a></p>
