# 边界回声图片瓦片地图系统

这个目录是《边界回声》的正式网页版地图系统雏形。它使用 Leaflet 和 `L.CRS.Simple`，按“高精度图片底图 + 独立数据图层”的方式搭建，不再用 HTML/CSS 从零画粗糙城市。

## 当前状态

- `index.html`：地图入口页。
- `src/app.js`：Leaflet 地图逻辑、图层开关、地点点击、详细图切换。
- `src/styles.css`：界面样式。
- `data/locations.json`：地点数据。
- `data/routes.json`：EP01 / EP02 路线数据。
- `data/areas.json`：异常边界、危险区域数据。
- `assets/maps/`：当前使用占位图片底图。
- `assets/tiles/`：预留给后续高精度瓦片。

## 等待美术地图资产

当前底图是占位图，只用于跑通交互功能。建筑、废墟、道路、车站、海岸线、区域质感等精细内容必须来自高精度地图图片素材，不能由 CSS、Canvas 或简单方块线条假画成最终图。

建议后续美术资产：

- `jinghai_city_final.png` 或切片瓦片：静海市主舞台总图。
- `old_north_station_final.png` 或切片瓦片：静海旧北站详细图。
- 各重点区域海报图：用于右侧详情面板。

## 替换方式

如果先使用单张高精度图片，在 `src/app.js` 的 `MAPS` 中替换 `image / width / height`。

如果后续切成瓦片，可在 `assets/tiles/` 下按 `{z}/{x}/{y}.png` 放置，并把当前 `L.imageOverlay` 方案升级为 `L.tileLayer`。地点、路线、区域数据可以继续沿用，只需要按最终地图像素坐标校准位置。
