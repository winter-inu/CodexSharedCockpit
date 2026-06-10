# 边界回声 / 静海市双地图交互原型

## 当前版本

当前版本是 `v0.4：双地图模式交互原型`。

本项目只负责网页交互系统，不重新绘制地图，不替换地图，不使用 SVG/CSS/Canvas 画城市。

## 已采纳地图资产

断层影响区地图：

- 临时 8K 无字底图：`assets/maps/jinghai_fault_zone_base_8k.webp`
- 临时 8K 标注参考图：`assets/maps/jinghai_fault_zone_annotated_8k.webp`
- 原始母版备份：`assets/maps/jinghai_fault_zone_base.png`、`assets/maps/jinghai_fault_zone_annotated.png`

断层影响区以用户确认的母版标注图为唯一基准。方向、地名和相对位置锁定在 `data/map_locks.json` 中，除非用户明确要求，不得自动更改。

静海市全域结构图：

- 全域结构图：`assets/maps/jinghai_city_regional_structure.png`

全域结构图用于外围扩展、核心异常区、缓冲残留区、外环安全区、外围交通和生活区结构参考。

## 文件结构

- `index.html`
- `src/main.js`
- `src/styles.css`
- `data/locations_fault_zone.json`
- `data/locations_regional.json`
- `data/routes_fault_zone.json`
- `data/routes_regional.json`
- `data/layers.json`
- `data/map_locks.json`
- `assets/maps/jinghai_fault_zone_base_8k.webp`
- `assets/maps/jinghai_fault_zone_annotated_8k.webp`
- `assets/maps/jinghai_fault_zone_base.png`
- `assets/maps/jinghai_fault_zone_annotated.png`
- `assets/maps/jinghai_city_regional_structure.png`
- `README.md`

## 地图模式

模式 1：断层影响区地图

- 默认主地图
- 使用 `jinghai_fault_zone_base_8k.webp`
- `jinghai_fault_zone_annotated_8k.webp` 只作为“标注参考图”图层查看，不作为默认底图
- 显示旧北站、断层核心区、旧城街区、派出所、档案室、地下轨道、异常区边缘、黑市维修点、海堤与港区等地点

模式 2：静海市全域结构图

- 点击左侧“切换到全域结构图”进入
- 使用 `jinghai_city_regional_structure.png`
- 显示核心异常区、缓冲残留区、外环安全区、新城区、安置区、医疗救援区、物流补给区、对外交通线等信息

## 图层规则

默认只开启：

- 无字底图
- 地点标记

默认关闭：

- EP01 路线
- EP02 路线
- 异常区边界
- 危险区域
- 未来事件位
- 标注参考图

每一类图层都使用独立 Leaflet `LayerGroup`。checkbox 关闭后，该图层所有元素必须完全隐藏。地点标记关闭时，地点圆点、编号、名称、tooltip、divIcon 都必须隐藏。

## 坐标规则

页面使用 Leaflet + `L.CRS.Simple`。断层影响区地点 JSON 中统一优先保存归一化坐标：

- `normalizedX`
- `normalizedY`

左上角为 `[0, 0]`，右下角为 `[1, 1]`。Leaflet 当前坐标轴需要把图片 Y 转成 `imageHeight - y` 后显示：

```js
const x = normalizedX * imageWidth;
const y = normalizedY * imageHeight;
return [imageHeight - y, x];
```

校准模式开启后，点击地图任意位置，右下角显示图片坐标 `[x, y]`，控制台输出当前地图模式、x、y 和 zoom。

## 打开方式

不要直接双击 `index.html`。地图需要读取 JSON、脚本和图片资源，浏览器在 `file://` 模式下会拦截部分本地读取。

推荐双击：

- `打开地图网页.bat`

它会启动本地预览服务并打开 `http://127.0.0.1:8787/production/online/boundary_echo_map/index.html`。

## 方向锁

静海市断层影响区方向锁：

- 画面上方 = 北
- 画面右侧 = 东
- 画面下方 = 南
- 画面左侧 = 西

地点方位固定在 `data/map_locks.json` 中，除非用户明确要求，不得自动改变方向、地名和相对位置。

## 详细图

已为后续预留：

- 静海旧北站详细图
- 候车区 / 连廊 / 隔离门详细图
- 静海断层核心区详细图
- 地下轨道枢纽详细图
- 静海档案室详细图
- 静海派出所周边图
- 黑市维修点 / 港区详细图
- 外环安全区详细图

当前没有详细图资产时，不生成粗糙替代图，只显示“等待该区域详细地图资产”。

## 后续

后续深度缩放需要 `4096 / 8192` 高清底图，或升级为 `assets/tiles/` 瓦片地图。
