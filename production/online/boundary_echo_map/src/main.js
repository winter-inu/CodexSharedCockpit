const DATA_VERSION = "20260610-v04-fault-map-8k-temp";

const state = {
  mode: "fault",
  config: null,
  locations: [],
  routes: [],
  layers: null,
  locks: null,
  baseOverlay: null,
  referenceOverlay: null,
  calibrationMode: false
};

const map = L.map("map", {
  crs: L.CRS.Simple,
  minZoom: -3,
  maxZoom: 3,
  zoomSnap: 0.25,
  attributionControl: false
});

const groups = {
  locations: L.layerGroup(),
  ep01: L.layerGroup(),
  ep02: L.layerGroup(),
  boundary: L.layerGroup(),
  danger: L.layerGroup(),
  future: L.layerGroup(),
  reference: L.layerGroup()
};

const groupNames = new Map(Object.entries(groups).map(([name, group]) => [group, name]));

const layerControl = L.control.layers(null, {
  "地点标记": groups.locations,
  "EP01 路线": groups.ep01,
  "EP02 路线": groups.ep02,
  "异常区边界": groups.boundary,
  "危险区域": groups.danger,
  "未来事件位": groups.future,
  "标注参考图": groups.reference
}, { collapsed: true }).addTo(map);

const mapWrap = document.getElementById("mapWrap");
const mapTitle = document.getElementById("mapTitle");
const zoomReadout = document.getElementById("zoomReadout");
const detailPanel = document.getElementById("detailPanel");
const hotspotLayer = document.getElementById("hotspotLayer");
const calibrationToggle = document.getElementById("calibrationToggle");
const calibrationReadout = document.getElementById("calibrationReadout");

function toLeafletPoint(location, imageWidth = state.config?.width || 1254, imageHeight = state.config?.height || 1254) {
  if (typeof location.normalizedX === "number" && typeof location.normalizedY === "number") {
    const x = location.normalizedX * imageWidth;
    const y = location.normalizedY * imageHeight;
    return [imageHeight - y, x];
  }
  const x = location.imageX ?? location[0];
  const y = location.imageY ?? location[1];
  return [imageHeight - y, x];
}

function toPoint(latlng) {
  const imageHeight = state.config?.height || 1254;
  return [Number(latlng.lng.toFixed(2)), Number((imageHeight - latlng.lat).toFixed(2))];
}

async function loadJson(path) {
  const response = await fetch(`${path}?v=${DATA_VERSION}`, { cache: "no-store" });
  if (!response.ok) throw new Error(`${path} 加载失败`);
  return response.json();
}

async function boot() {
  const [layers, locks] = await Promise.all([
    loadJson("data/layers.json"),
    loadJson("data/map_locks.json")
  ]);
  state.layers = layers;
  state.locks = locks;
  bindControls();
  await switchMode("fault");
}

async function switchMode(mode) {
  state.mode = mode;
  state.config = state.layers.maps[mode];
  const [locations, routes] = await Promise.all([
    loadJson(state.config.locations),
    loadJson(state.config.routes)
  ]);
  state.locations = locations;
  state.routes = routes;
  setModeButtons();
  renderMap();
  showEmptyPanel();
}

function setModeButtons() {
  document.querySelectorAll(".mode-button").forEach((button) => {
    const active = button.dataset.mode === state.mode;
    button.classList.toggle("active", active);
    button.textContent = button.dataset.mode === "fault"
      ? "断层影响区地图"
      : "切换到全域结构图";
  });
}

function resetCheckboxes() {
  document.querySelectorAll("input[data-layer]").forEach((input) => {
    input.checked = input.dataset.layer === "locations";
    if (state.mode === "regional" && ["ep01", "ep02", "reference"].includes(input.dataset.layer)) {
      input.checked = false;
      input.disabled = true;
    } else {
      input.disabled = false;
    }
  });
}

function clearGroups() {
  Object.values(groups).forEach((group) => {
    group.clearLayers();
    if (map.hasLayer(group)) map.removeLayer(group);
  });
  hotspotLayer.innerHTML = "";
}

function renderMap() {
  clearGroups();
  const bounds = [[0, 0], [state.config.height, state.config.width]];
  if (state.baseOverlay) map.removeLayer(state.baseOverlay);
  state.baseOverlay = L.imageOverlay(`${state.config.baseImage}?v=${DATA_VERSION}`, bounds).addTo(map);
  map.setMaxBounds(bounds);
  map.fitBounds(bounds);
  mapTitle.textContent = state.config.title;

  if (state.mode === "fault" && state.config.annotatedImage) {
    state.referenceOverlay = L.imageOverlay(`${state.config.annotatedImage}?v=${DATA_VERSION}`, bounds, { opacity: 1 });
    groups.reference.addLayer(state.referenceOverlay);
    verifyReferenceMaster();
  }

  renderLocations();
  renderRoutes();
  renderAreas();
  resetCheckboxes();
  applyLayerVisibility();
  updateZoomTier();
  updateHotspots();
}

function loadImageSize(src) {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => resolve({ width: image.naturalWidth, height: image.naturalHeight });
    image.onerror = reject;
    image.src = `${src}?v=${DATA_VERSION}`;
  });
}

async function verifyReferenceMaster() {
  try {
    const [base, reference] = await Promise.all([
      loadImageSize(state.config.baseImage),
      loadImageSize(state.config.annotatedImage)
    ]);
    if (base.width !== reference.width || base.height !== reference.height) {
      const message = "底图与标注参考图不是同一母版，无法精确对齐。";
      calibrationReadout.textContent = message;
      detailPanel.innerHTML = `<div class="empty-state"><p>${message}</p><span>请先替换为同一母版导出的无字底图和标注参考图。</span></div>`;
    }
  } catch (error) {
    console.warn("参考图母版检查失败", error);
  }
}

function renderLocations() {
  state.locations.forEach((location) => {
    const groupName = location.layer === "future" ? "future" : "locations";
    const hotspot = document.createElement("button");
    hotspot.type = "button";
    hotspot.className = `map-hotspot ${location.layer === "future" ? "future" : ""}`;
    hotspot.dataset.locationId = location.id;
    hotspot.dataset.layer = groupName;
    hotspot.dataset.priority = location.priority || "secondary";
    hotspot.setAttribute("aria-label", location.name);
    const [labelX, labelY] = location.labelOffset || [16, -28];
    hotspot.style.setProperty("--label-x", `${labelX}px`);
    hotspot.style.setProperty("--label-y", `${labelY}px`);
    hotspot.innerHTML = `
      <span class="region-label">${location.regionName || location.name}</span>
      <span class="hotspot-dot">${location.index}</span>
      <span class="hotspot-label">${location.name}</span>
    `;
    hotspot.addEventListener("click", (event) => {
      event.stopPropagation();
      openLocationDetail(location);
    });
    hotspotLayer.appendChild(hotspot);
  });
}

function renderRoutes() {
  state.routes.forEach((route) => {
    const target = groups[route.layer];
    if (!target) return;
    const points = route.points.map((point) => toLeafletPoint(point));
    const glow = L.polyline(points, {
      color: route.color,
      weight: (route.weight || 3) + 6,
      opacity: 0.08,
      dashArray: route.dashArray || null,
      lineCap: "round",
      lineJoin: "round",
      className: "route-glow"
    });
    const core = L.polyline(points, {
      color: route.color,
      weight: route.weight || 3,
      opacity: route.opacity || 0.36,
      dashArray: route.dashArray || null,
      lineCap: "round",
      lineJoin: "round",
      className: "route-core"
    });
    [glow, core].forEach((layer) => {
      layer.options.routeId = route.id;
      layer.on("mouseover", () => setRouteFocus(route.id, true));
      layer.on("mouseout", () => setRouteFocus(route.id, false));
      layer.on("click", () => openRouteDetail(route));
      target.addLayer(layer);
    });
  });
}

function renderAreas() {
  (state.config.areas || []).forEach((area) => {
    const target = groups[area.layer];
    if (!target) return;
    const polygon = L.polygon(area.points.map((point) => toLeafletPoint(point)), {
      color: area.stroke,
      fillColor: area.fill,
      fillOpacity: Math.min(area.fillOpacity || 0.08, 0.12),
      opacity: 0.72,
      weight: area.weight || 2,
      dashArray: area.dashArray || null,
      className: area.layer === "boundary" ? "boundary-area" : "danger-area"
    });
    polygon.options.areaId = area.id;
    polygon.on("mouseover", () => setAreaFocus(area.id, true));
    polygon.on("mouseout", () => setAreaFocus(area.id, false));
    polygon.on("click", () => openAreaDetail(area));
    target.addLayer(polygon);
  });
}

function applyLayerVisibility() {
  document.querySelectorAll("input[data-layer]").forEach((input) => {
    const layerName = input.dataset.layer;
    const visible = input.checked && !input.disabled;
    const group = groups[layerName];
    if (group) visible ? group.addTo(map) : map.removeLayer(group);
    hotspotLayer.querySelectorAll(`[data-layer="${layerName}"]`).forEach((hotspot) => {
      hotspot.hidden = !visible;
    });
  });
}

function bindControls() {
  document.querySelectorAll(".mode-button").forEach((button) => {
    button.addEventListener("click", () => switchMode(button.dataset.mode));
  });
  document.querySelectorAll("input[data-layer]").forEach((input) => {
    input.addEventListener("change", applyLayerVisibility);
  });
  map.on("overlayadd overlayremove", (event) => {
    const layerName = groupNames.get(event.layer);
    if (!layerName) return;
    const checked = event.type === "overlayadd";
    const input = document.querySelector(`input[data-layer="${layerName}"]`);
    if (input && input.checked !== checked) input.checked = checked;
    updateDomLayerVisibility(layerName, checked);
    updateReferenceView(layerName, checked);
  });
  calibrationToggle.addEventListener("change", () => {
    state.calibrationMode = calibrationToggle.checked;
    calibrationReadout.textContent = state.calibrationMode ? "校准模式开启：点击地图取坐标" : "校准模式关闭";
  });
  map.on("click", (event) => {
    if (!state.calibrationMode) return;
    reportCalibrationPoint(event.latlng);
  });
  map.getContainer().addEventListener("click", (event) => {
    if (!state.calibrationMode) return;
    reportCalibrationPoint(map.mouseEventToLatLng(event));
  });
  map.on("zoomend", () => {
    updateZoomTier();
    updateHotspots();
  });
  map.on("move zoom resize", updateHotspots);
}

function updateReferenceView(layerName, visible) {
  if (layerName !== "reference" || !state.baseOverlay) return;
  state.baseOverlay.setOpacity(visible ? 0 : 1);
}

function updateDomLayerVisibility(layerName, visible) {
  hotspotLayer.querySelectorAll(`[data-layer="${layerName}"]`).forEach((hotspot) => {
    hotspot.hidden = !visible;
  });
}

function reportCalibrationPoint(latlng) {
  const [x, y] = toPoint(latlng);
  calibrationReadout.textContent = `坐标 [${x}, ${y}]`;
  console.log("地图校准", { mode: state.mode, x, y, zoom: map.getZoom() });
}

function updateZoomTier() {
  const zoom = map.getZoom();
  zoomReadout.textContent = `缩放 ${zoom.toFixed(2)}`;
  mapWrap.dataset.zoomTier = zoom < -1.2 ? "low" : zoom < 0.4 ? "mid" : "high";
}

function updateHotspots() {
  hotspotLayer.querySelectorAll("[data-location-id]").forEach((hotspot) => {
    const location = state.locations.find((item) => item.id === hotspot.dataset.locationId);
    if (!location) return;
    const point = map.latLngToContainerPoint(toLeafletPoint(location));
    hotspot.style.left = `${point.x}px`;
    hotspot.style.top = `${point.y}px`;
  });
}

function setRouteFocus(routeId, focused) {
  Object.values(groups).forEach((group) => {
    group.eachLayer((layer) => {
      if (layer.options?.routeId !== routeId || !layer.setStyle) return;
      layer.setStyle({ opacity: focused ? 0.9 : (layer.options.className === "route-glow" ? 0.08 : 0.36) });
    });
  });
}

function setAreaFocus(areaId, focused) {
  Object.values(groups).forEach((group) => {
    group.eachLayer((layer) => {
      if (layer.options?.areaId !== areaId || !layer.setStyle) return;
      layer.setStyle({ fillOpacity: focused ? 0.18 : 0.08, opacity: focused ? 0.95 : 0.72 });
    });
  });
}

function openLocationDetail(location) {
  const events = (location.events || []).map((item) => `<li>${item}</li>`).join("");
  const people = (location.people || []).join(" / ") || "待定";
  const detailButton = location.detailMap
    ? `<button class="wide-button" id="enterDetailMap">进入详细地图</button>`
    : `<button class="wide-button" disabled>等待该区域详细地图资产</button>`;

  detailPanel.innerHTML = `
    <h2 class="detail-title">${location.name}</h2>
    <p class="detail-type">${location.type}</p>
    <div class="info-row"><strong>所属区域</strong><span>${location.area || "未分区"}</span></div>
    <div class="info-row"><strong>所属集数</strong><span>${(location.episodes || []).join(" / ") || "后续"}</span></div>
    <div class="info-row"><strong>剧情作用</strong><p>${location.storyRole || "待补充"}</p></div>
    <div class="info-row"><strong>相关人物</strong><span>${people}</span></div>
    <div class="info-row"><strong>相关事件 / 镜头</strong><ul class="event-list">${events}</ul></div>
    <div class="info-row"><strong>危险等级</strong><span>${location.dangerLevel || "未知"}</span></div>
    <div class="info-row"><strong>详细地图</strong><span>${location.detailMap ? "已预留入口" : "暂未开放"}</span></div>
    ${detailButton}
  `;
  if (location.detailMap) {
    document.getElementById("enterDetailMap").addEventListener("click", () => {
      detailPanel.innerHTML = `<div class="empty-state"><p>等待该区域详细地图资产</p><span>${location.name} 的详细地图入口已预留，后续放入无字局部地图后接入。</span></div>`;
    });
  }
}

function openRouteDetail(route) {
  detailPanel.innerHTML = `
    <h2 class="detail-title">${route.name}</h2>
    <p class="detail-type">路线图层</p>
    <div class="info-row"><strong>说明</strong><p>${route.description || "占位路线，后续继续按道路和轨道精修。"}</p></div>
  `;
}

function openAreaDetail(area) {
  detailPanel.innerHTML = `
    <h2 class="detail-title">${area.name}</h2>
    <p class="detail-type">${area.type || "区域图层"}</p>
    <div class="info-row"><strong>说明</strong><p>${area.description || "默认隐藏，开启图层后可查看。"}</p></div>
  `;
}

function showEmptyPanel() {
  detailPanel.innerHTML = `
    <div class="empty-state">
      <p>选择一个地点或区域</p>
      <span>地点名称、剧情作用、相关事件和详细图入口会显示在这里。</span>
    </div>
  `;
}

boot().catch((error) => {
  detailPanel.innerHTML = `<div class="empty-state"><p>地图加载失败</p><span>${error.message}</span></div>`;
});
