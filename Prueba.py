import requests

url = "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/ArcGIS/rest/services/Veredas_Boyaca_2024/FeatureServer/0/query"
base = {"where": "1=1", "outFields": "NOMB_MPIO,NOMBRE_VER", "outSR": "4326", "f": "geojson"}

features, offset, bloque = [], 0, 1000
while True:
    p = {**base, "resultOffset": offset, "resultRecordCount": bloque}
    datos = requests.get(url, params=p, timeout=30).json()
    nuevos = datos.get("features", [])
    features += nuevos
    print(f"offset {offset}: +{len(nuevos)} (total {len(features)})")
    if len(nuevos) < bloque:          # último bloque
        break
    offset += bloque

print("TOTAL:", len(features))        # debe acercarse a 1.713