const MAPS = {
  city: {
    id: "city",
    title: "静海市主舞台概念地图",
    image: "assets/maps/jinghai_city_placeholder.svg",
    width: 2400,
    height: 1600
  },
  oldNorthStation: {
    id: "oldNorthStation",
    title: "静海旧北站详细图",
    image: "assets/maps/old_north_station_placeholder.svg",
    width: 1600,
    height: 1000
  }
};

const state = {
  currentMap: "city",
  data: {
    locations: [],
    routes: [],
    areas: []
  },
  layers: {},
  baseOverlay: null
};

const map = L.map("map", {
  crs: L.CRS.Simple,
  minZoom: -2,
  maxZoom: 3,
  zoomSnap: 0.25,
  attributionControl: false
});

const layerGroups = {
  locations: L.layerGroup(),
  ep01: L.layerGroup(),
  ep02: L.layerGroup(),
  boundary: L.layerGroup(),
  danger: L.layerGroup(),
  future: L.layerGroup()
};

Object.values(layerGroups).forEach((group) => group.addTo(map));

const mapTitle = document.getElementById("mapTitle");
const zoomReadout = document.getElementById("zoomReadout");
const detailPanel = document.getElementById("detailPanel");
const backToCity = document.getElementById("backToCity");
const hotspotLayer = document.getElementById("hotspotLayer");

function xy(point) {
  return [point[1], point[0]];
}

async function loadJson(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(`${path} 加载失败`);
  }
  return response.json();
}

async function boot() {
  const [locations, routes, areas] = await Promise.all([
    loadJson("data/locations.json"),
    loadJson("data/routes.json"),
    loadJson("data/areas.json")
  ]);

  state.data = { locations, routes, areas };
  resetLayerControls();
  setBaseMap("city");
  renderLayers();
  wireControls();
  showEmptyPanel();
}

function resetLayerControls() {
  document.querySelectorAll("input[data-layer]").forEach((input) => {
    input.checked = input.defaultChecked;
  });
}

function setBaseMap(mapId) {
  state.currentMap = mapId;
  const config = MAPS[mapId];
  const bounds = [[0, 0], [config.height, config.width]];

  if (state.baseOverlay) {
    map.removeLayer(state.baseOverlay);
  }

  state.baseOverlay = L.imageOverlay(config.image, bounds).addTo(map);
  map.setMaxBounds(bounds);
  map.fitBounds(bounds);
  mapTitle.textContent = config.title;
  backToCity.disabled = mapId === "city";
}

function renderLayers() {
  Object.values(layerGroups).forEach((group) => group.clearLayers());
  renderLocations();
  renderRoutes();
  renderAreas();
  applyLayerVisibility();
}

function renderLocations() {
  hotspotLayer.innerHTML = "";

  state.data.locations
    .filter((location) => location.map === state.currentMap)
    .forEach((location) => {
      const marker = L.circleMarker(xy(location.position), {
        radius: 0,
        opacity: 0,
        fillOpacity: 0,
        interactive: false
      })
        .bindTooltip(location.name, {
          className: "place-label",
          direction: "top",
          offset: [0, -16]
        });

      const targetLayer = location.layer === "future" ? layerGroups.future : layerGroups.locations;
      targetLayer.addLayer(marker);

      const hotspot = document.createElement("button");
      hotspot.type = "button";
      hotspot.className = `map-hotspot ${location.layer === "future" ? "future" : ""}`;
      hotspot.dataset.locationId = location.id;
      hotspot.dataset.layer = location.layer === "future" ? "future" : "locations";
      hotspot.textContent = location.index;
      hotspot.setAttribute("aria-label", location.name);
      hotspot.addEventListener("click", () => openDetail(location));
      hotspotLayer.appendChild(hotspot);
    });

  updateHotspots();
}

function renderRoutes() {
  state.data.routes
    .filter((route) => route.map === state.currentMap)
    .forEach((route) => {
      const layer = L.polyline(route.points.map(xy), {
        color: route.color,
        weight: route.weight || 4,
        opacity: route.opacity || 0.92,
        dashArray: route.dashArray || null,
        lineCap: "round",
        lineJoin: "round"
      }).bindTooltip(route.name, {
        className: "place-label",
        sticky: true
      });

      layerGroups[route.layer].addLayer(layer);
    });
}

function renderAreas() {
  state.data.areas
    .filter((area) => area.map === state.currentMap)
    .forEach((area) => {
      const polygon = L.polygon(area.points.map(xy), {
        color: area.stroke,
        weight: area.weight || 2,
        opacity: area.opacity || 0.9,
        fillColor: area.fill,
        fillOpacity: area.fillOpacity || 0.18,
        dashArray: area.dashArray || null
      }).bindTooltip(area.name, {
        className: "place-label",
        sticky: true
      });

      layerGroups[area.layer].addLayer(polygon);
    });
}

function applyLayerVisibility() {
  document.querySelectorAll("input[data-layer]").forEach((input) => {
    const group = layerGroups[input.dataset.layer];
    const hotspots = hotspotLayer.querySelectorAll(`[data-layer="${input.dataset.layer}"]`);

    if (group && input.checked) {
      group.addTo(map);
    } else if (group) {
      map.removeLayer(group);
    }

    hotspots.forEach((hotspot) => {
      hotspot.hidden = !input.checked;
    });
  });
}

function wireControls() {
  document.querySelectorAll("[data-layer]").forEach((input) => {
    input.addEventListener("change", applyLayerVisibility);
  });

  document.addEventListener("click", (event) => {
    const markerElement = event.target.closest("[data-location-id]");
    if (!markerElement) return;

    const location = state.data.locations.find((item) => item.id === markerElement.dataset.locationId);
    if (location) {
      event.preventDefault();
      openDetail(location);
    }
  });

  backToCity.addEventListener("click", () => {
    setBaseMap("city");
    renderLayers();
    showEmptyPanel();
  });

  map.on("zoomend", () => {
    zoomReadout.textContent = `缩放 ${map.getZoom().toFixed(2)}`;
    updateHotspots();
  });

  map.on("move zoom resize", () => {
    updateHotspots();
  });
}

function updateHotspots() {
  hotspotLayer.querySelectorAll("[data-location-id]").forEach((hotspot) => {
    const location = state.data.locations.find((item) => item.id === hotspot.dataset.locationId);
    if (!location) return;

    const point = map.latLngToContainerPoint(xy(location.position));
    hotspot.style.left = `${point.x}px`;
    hotspot.style.top = `${point.y}px`;
  });
}

function openDetail(location) {
  const eventItems = location.events.map((event) => `<li>${event}</li>`).join("");
  const detailButton = location.detailMap
    ? `<button class="wide-button" id="enterDetailMap">进入详细图</button>`
    : `<button class="wide-button" disabled>等待详细图资产</button>`;

  detailPanel.innerHTML = `
    <h2 class="detail-title">${location.name}</h2>
    <p class="detail-type">${location.type}</p>
    <div class="info-row">
      <strong>所属集数</strong>
      <span>${location.episodes.join(" / ")}</span>
    </div>
    <div class="info-row">
      <strong>剧情作用</strong>
      <p>${location.storyRole}</p>
    </div>
    <img class="detail-image" src="${location.poster}" alt="${location.name}参考图">
    <div class="info-row">
      <strong>相关事件</strong>
      <ul class="event-list">${eventItems}</ul>
    </div>
    ${detailButton}
  `;

  if (location.detailMap) {
    document.getElementById("enterDetailMap").addEventListener("click", () => {
      setBaseMap(location.detailMap);
      renderLayers();
      showEmptyPanel();
    });
  }
}

function showEmptyPanel() {
  detailPanel.innerHTML = `
    <div class="empty-state">
      <p>选择一个地点</p>
      <span>地点名称、剧情作用、相关事件和详细图入口会显示在这里。</span>
    </div>
  `;
}

boot().catch((error) => {
  detailPanel.innerHTML = `
    <div class="empty-state">
      <p>地图加载失败</p>
      <span>${error.message}</span>
    </div>
  `;
});
