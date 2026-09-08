<h1 align="center">自然资源技术标准规范库</h1>

<p align="center">
  <strong>技术标准 · 规范规程 · 政策法规 · 参考资料</strong><br/>
  面向自然资源、测绘地理信息、遥感、GIS、地籍调查与确权登记等业务领域。
</p>

<p align="center">
  <a href="./README.md">🇺🇸 English</a> · <a href="./README_CN.md"><b>🇨🇳 中文</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/自然资源-技术标准-2E7D32?style=flat-square" />
  <img src="https://img.shields.io/badge/测绘地理信息-规范规程-1565C0?style=flat-square" />
  <img src="https://img.shields.io/badge/遥感-GIS-00838F?style=flat-square" />
  <img src="https://img.shields.io/badge/地籍调查-确权登记-6A1B9A?style=flat-square" />
  <img src="https://img.shields.io/badge/政策法规-技术标准-C77800?style=flat-square" />
</p>

---

## 📚 仓库简介

本仓库用于整理和维护 **自然资源领域技术标准、规范规程、政策法规及相关参考资料**，重点服务自然资源调查监测、地籍调查、不动产与自然资源确权登记、测绘地理信息、遥感、GIS 等业务场景。

仓库按照专业领域进行分类，而不是简单按照标准发布部门划分，便于将不同来源、不同结构和不同标准体系的文件统一纳入管理，并长期维护标准版本、现行状态及替代关系。

## 🗂️ 分类体系

| 分类 | 主要内容 | 目录 |
|---|---|---|
| 综合通用 | 基础性、通用性、跨专业标准 | [`standards/01-General`](./standards/01-General/) |
| 调查监测 | 自然资源调查、监测、调查评价 | [`standards/02-Survey-Monitoring`](./standards/02-Survey-Monitoring/) |
| 地籍与确权登记 | 地籍调查、不动产登记、自然资源确权登记 | [`standards/03-Cadastral-Registration`](./standards/03-Cadastral-Registration/) |
| 测绘地理信息 | 大地测量、摄影测量、工程测量、制图等 | [`standards/04-Surveying-Mapping`](./standards/04-Surveying-Mapping/) |
| 遥感与 GIS | 遥感、GIS、空间数据、数据库等 | [`standards/05-Remote-Sensing-GIS`](./standards/05-Remote-Sensing-GIS/) |
| 国土空间规划与用途管制 | 土地利用、耕地保护、国土空间规划、用途管制 | [`standards/06-Land-Spatial-Planning`](./standards/06-Land-Spatial-Planning/) |
| 生态与自然资源资产 | 森林、草原、湿地、生态、自然资源资产等 | [`standards/07-Ecology-Natural-Assets`](./standards/07-Ecology-Natural-Assets/) |
| 地质与矿产 | 地质调查、矿产资源及相关技术标准 | [`standards/08-Geology-Minerals`](./standards/08-Geology-Minerals/) |
| 其他 | 暂未归入上述类别的文件 | [`standards/99-Other`](./standards/99-Other/) |

## 🔎 标准目录

仓库总目录统一维护在 [`catalog.csv`](./catalog.csv) 中，建议记录标准号、标准名称、分类、现行状态、发布日期、实施日期、替代关系、文件路径、来源链接及备注等信息。

当标准数量较多时，应优先通过 `catalog.csv` 检索，而不是仅依靠文件夹浏览。

## 📝 文件命名

建议统一采用：

```text
标准号 标准名称.pdf
```

例如：

```text
TDT 1015.2-2024 地籍数据库 第2部分：自然资源.pdf
```

原则上尽量保留 **正式标准号 + 正式标准名称**，不附加下载网站名称、无关时间戳、重复前缀等信息。

## ✅ 维护规则

- 原则上一份标准对应一个 PDF 文件。
- 标准号、名称尽量保持官方正式写法。
- 对修订、废止、被替代的标准，不直接删除历史记录，应在 `catalog.csv` 中标记状态和替代关系。
- 暂时无法准确判断分类的文件可先放入 `99-Other`，核实后再调整。
- 来源链接优先使用政府部门、标准发布机构或其他权威来源。
- 批量上传前建议检查重复文件、命名不统一、版本冲突等问题。

## ⚠️ 版权与免责声明

本仓库主要用于 **技术学习、资料索引和标准规范整理**。各标准、规范及相关文件的著作权和传播权归原发布机构或权利人所有。

文件能够公开获取并不当然意味着可以自由转载或再次分发。对于传播权限不明确的文件，建议仅维护标准元数据和官方来源链接，不直接上传完整 PDF。

如仓库中的有关资料存在版权、有效性或其他问题，可通过 Issue 提交说明并进行核查处理。

---

<p align="center">Maintained by <a href="https://github.com/zhangyhrs">Zhang Y.H.</a></p>
