import requests, geopandas as gpd

url = "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/ArcGIS/rest/services/Veredas_Boyaca_2024/FeatureServer/0/query"
params = {
     "where": "COD_DPTO = 15",
    "outFields": "NOMB_MPIO,NOMBRE_VER,CODIGO_VER",
    "outSR": "4326",
    "f": "geojson",
}
r = requests.get(url, params=params, timeout=30)
r.raise_for_status()
gdf = gpd.GeoDataFrame.from_features(r.json()["features"], crs=4326)

# Listado de los 10 municipios con más veredas
conteo = (
    gdf.groupby("NOMB_MPIO")["NOMBRE_VER"]
    .count()
    .reset_index(name="Total_veredas")
    .sort_values("Total_veredas", ascending=False)
    .head(10)
)
# 1. Reproyectar a EPSG:9377 y calcular el área en hectáreas
gdf_area = gdf.to_crs(epsg=9377).copy()

gdf_area["AREA_HA"] = gdf_area.geometry.area / 10000

# 2. Identificar las 5 veredas con mayor área
top_5_veredas = gdf_area.nlargest(5, "AREA_HA")

# 3. Mostrar resultados
print("\n ************RESULTADOS************\n")
print("veredas en Boyaca : ",len(gdf))
print("\nListado de los 10 municipios con más veredas")
print(conteo.to_string(index=False))
print("\n\nTop 5 Veredas con mayor área (Hectareas)/n")
resultado = top_5_veredas[
    ["NOMB_MPIO", "NOMBRE_VER", "AREA_HA"]
].copy()
resultado["NOMBRE_VER"] = resultado["NOMBRE_VER"].str.rjust(
    resultado["NOMBRE_VER"].str.len().max()
)

print(
    resultado.to_string(
        index=False,
        formatters={"AREA_HA": "{:,.2f}".format}
    )
)