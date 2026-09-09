from __future__ import annotations

import re
from pathlib import Path

REGIONS=("北京市","天津市","河北省","山西省","内蒙古自治区","辽宁省","吉林省","黑龙江省","上海市","江苏省","浙江省","安徽省","福建省","江西省","山东省","河南省","湖北省","湖南省","广东省","广西壮族自治区","海南省","重庆市","四川省","贵州省","云南省","西藏自治区","陕西省","甘肃省","青海省","宁夏回族自治区","新疆维吾尔自治区")
DB_REGION={"11":"北京市","12":"天津市","13":"河北省","14":"山西省","15":"内蒙古自治区","21":"辽宁省","22":"吉林省","23":"黑龙江省","31":"上海市","32":"江苏省","33":"浙江省","34":"安徽省","35":"福建省","36":"江西省","37":"山东省","41":"河南省","42":"湖北省","43":"湖南省","44":"广东省","45":"广西壮族自治区","46":"海南省","50":"重庆市","51":"四川省","52":"贵州省","53":"云南省","54":"西藏自治区","61":"陕西省","62":"甘肃省","63":"青海省","64":"宁夏回族自治区","65":"新疆维吾尔自治区"}

def anyw(text,*words): return any(w in text for w in words)
def code(system):
    m=re.match(r"([A-Z]{2}\d?-\d{2})",system)
    return m.group(1) if m else system.split()[0]

def professional_domain(path:Path,title:str,system:str)->str:
    text=" / ".join(path.parts[2:-1])+" / "+title
    c=code(system)
    if c.startswith("CH2"):
        rules=[
            (("导航电子地图",),"导航电子地图"),(("互联网地理信息","互联网地图","在线地图"),"互联网地理信息服务"),
            (("行政区域界线","界线测绘","行政界线"),"行政区域界线测绘"),(("房产测绘","房产面积","房屋面积"),"房产测绘"),
            (("地籍测绘","土地勘测定界","勘测定界"),"地籍测绘"),(("海洋测绘","海道测量","海图"),"海洋测绘"),
            (("测绘航空摄影","航空摄影","航摄"),"测绘航空摄影"),(("摄影测量","遥感","正射影像","影像测图"),"摄影测量与遥感"),
            (("地图制图","地图编制","地图图式","分幅和编号","分幅编号"),"地图制图"),(("地理信息系统","GIS","地理空间数据","空间数据库"),"地理信息系统"),
            (("工程测量","工程测绘"),"工程测量"),(("大地测量","GNSS","卫星导航","水准","坐标转换","坐标系","控制测量","控制点"),"大地测量")]
        for words,label in rules:
            if anyw(text,*words): return label
        return "测绘综合"
    if c.startswith("DJ2"):
        if "冰川" in text:return "冰川调查"
        if anyw(text,"森林","林地"):return "森林资源调查"
        if "草原" in text:return "草原资源调查"
        if "湿地" in text:return "湿地资源调查"
        if anyw(text,"河湖","水资源"):return "水资源调查"
        if anyw(text,"土地调查","土地利用现状","地类调查"):return "土地调查"
        if anyw(text,"地理国情","国情监测"):return "地理国情监测"
        return "自然资源调查监测"
    if c.startswith("ZC2"):
        if anyw(text,"自然资源确权登记","自然资源登记单元","自然资源登记","自然资源统一确权"):return "自然资源确权登记"
        if anyw(text,"不动产登记","不动产单元"):return "不动产登记"
        if anyw(text,"地籍调查","集体土地所有权","农村土地承包经营权"):return "地籍调查"
        return "确权登记与权益"
    if c.startswith("GH2"):
        if "详细规划" in text:return "详细规划"
        if "村庄规划" in text:return "村庄规划"
        if "专项规划" in text:return "专项规划"
        if "总体规划" in text:return "总体规划"
        return "国土空间规划"
    if c.startswith("DC2"):
        if anyw(text,"永久基本农田","耕地保护"):return "耕地保护"
        if anyw(text,"执法","督察","卫片"):return "执法督察"
        return "用途管制"
    if c.startswith("ST2"):
        if "自然保护地" in text:return "自然保护地"
        if "生态保护红线" in text:return "生态保护红线"
        if "矿山" in text and "修复" in text:return "矿山生态修复"
        return "生态保护修复"
    if c.startswith("LY2"):
        if anyw(text,"分等定级","评价"):return "资源评价与分等定级"
        if anyw(text,"节约集约","集约利用"):return "节约集约利用"
        if anyw(text,"资产","权益"):return "资源资产管理"
        return "自然资源开发利用"
    if c.startswith("TD2"):
        if "土地整治" in text:return "土地整治"
        if anyw(text,"土地评价","土地分等"):return "土地评价"
        if "土地利用" in text:return "土地利用"
        return "土地资源"
    if c.startswith("DZ2"):
        if "地质灾害" in text:return "地质灾害"
        if "地下水" in text:return "地下水"
        if anyw(text,"矿产","矿业"):return "矿产资源"
        return "地质调查"
    if c.startswith("HY2"):
        if anyw(text,"冰川","极地"):return "极地与冰川"
        if "海域" in text:return "海域使用"
        if anyw(text,"海岸带","海岸线"):return "海岸带"
        if "海洋测绘" in text:return "海洋测绘"
        return "海洋调查"
    if c.startswith("XX2"):
        if "元数据" in text:return "元数据"
        if anyw(text,"数据交换","数据共享"):return "数据交换与共享"
        if anyw(text,"数据库","数据资源"):return "数据库"
        if anyw(text,"平台","系统建设"):return "信息平台"
        return "自然资源信息化"
    if c.startswith("TY1"):
        if anyw(text,"分类","代码","编码"):return "分类与代码"
        if "术语" in text:return "术语"
        return "基础通用"
    return system.split(" ",1)[-1] if " " in system else "其他"

def detect_region(path:Path,prefix:str|None)->str:
    text=path.as_posix()
    for r in REGIONS:
        if r in text:return r
    if prefix:
        p=re.sub(r"[._-]","",prefix.upper());m=re.match(r"DB(\d{2})",p)
        if m and m.group(1) in DB_REGION:return DB_REGION[m.group(1)]
    return "全国"

def keyword_tags(path:Path,title:str)->str:
    text=path.as_posix()+" "+title
    words=("GNSS","水准测量","坐标转换","控制测量","土地勘测定界","界址点","界址线","地籍数据库","登记单元","集体土地所有权","农村土地承包经营权","永久基本农田","河湖管理范围","冰川厚度","冰川监测","实景三维","基础地理实体","自然保护地","生态保护红线","地图图式","分幅编号","成果检验","数据库","遥感","航空摄影")
    return "、".join(w for w in words if w in text)
