COMPARATIVA: WMS, WFS, FeatureServer y OGC API - Features

Servicio | Qué entrega | Cómo se filtra | Cómo se pagina
---------|-------------|----------------|----------------
WMS | Mapa renderizado mediante GetMap, normalmente PNG/JPEG; no una colección de entidades vectoriales. | LAYERS selecciona capas; BBOX delimita la extensión; TIME/ELEVATION si están disponibles. CQL_FILTER en GeoServer es una extensión, no una capacidad universal de WMS. | No pagina entidades: cada petición genera un mapa para una extensión y tamaño. Cambiar BBOX no equivale a paginar registros.
WFS | Entidades con geometría y atributos mediante GetFeature; GML como formato estándar y GeoJSON si el servidor lo ofrece. | BBOX para selección espacial; OGC Filter/FES para condiciones espaciales y de atributos. GeoServer también admite CQL_FILTER como extensión. | WFS 2.0: startIndex (desde 0) y count. WFS 1.x: maxFeatures limita resultados, pero no garantiza paginación estándar; algunos servidores añaden startIndex.
FeatureServer (ArcGIS REST) | Entidades con atributos y, si se solicita, geometría mediante /FeatureServer/{layerId}/query; normalmente Esri JSON, con otros formatos según el servicio. | where para atributos; geometry + geometryType + spatialRel para selección espacial; objectIds y time según las capacidades de la capa. | resultOffset (desde 0) y resultRecordCount si supportsPagination=true. El tamaño de página está sujeto a maxRecordCount.
OGC API - Features | Colecciones y entidades como recursos HTTP; /collections/{collectionId}/items devuelve entidades, por ejemplo en GeoJSON si se ofrece esa codificación. | Core: bbox, datetime y filtros simples por propiedades cuando se anuncien. Expresiones avanzadas: filter y filter-lang, por ejemplo CQL2, si implementa Part 3 y las conformidades correspondientes. | limit fija el máximo de entidades de la página; seguir el enlace rel="next" de la respuesta. Core no establece un parámetro universal offset ni page.

DISTINCIÓN CLAVE
WMS entrega una representación visual; los otros tres permiten obtener entidades para procesar geometría y atributos.
