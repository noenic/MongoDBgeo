import folium
from folium.plugins import MarkerCluster
import geopandas as gpd

def afficher_carte(communes, listing):
    # Créer une carte centrée sur la France
    m = folium.Map(location=[46.6031, 1.8883], zoom_start=6, tiles='CartoDB positron')

    # Ajouter les données GeoJSON à la carte (communes en bleu et mairies en rouge)
    marker_cluster = MarkerCluster(maxClusterRadius=50).add_to(m)
    
    # Afficher les communes sur la carte
    for idx, row in communes.iterrows():
        properties = row['properties']
        geometry = row['geometry']

        # Vérifier si la géométrie est une collection
        if geometry['type'] == 'GeometryCollection':
            for geom in geometry['geometries']:
                # Personnaliser la couleur en fonction du type de géométrie
                if geom['type'] == 'Point':
                    marker_color = 'red'
                    # Ajouter le marqueur avec la couleur personnalisée
                    folium.Marker(
                        location=[geom['coordinates'][1], geom['coordinates'][0]],
                        popup=f"<b>Centre de :</b> {properties['commune']}",
                        icon=folium.Icon(color=marker_color),
                    ).add_to(m)
                else:
                    folium.GeoJson(
                        geom,
                        style_function=lambda x: {'color': 'blue', 'fillColor': 'blue', 'weight': 1.5, 'fillOpacity': 0.2}
                    ).add_to(m)
        elif geometry['type'] == 'Polygon':
            folium.GeoJson(
                geometry,
                style_function=lambda x: {'color': 'blue', 'fillColor': 'blue', 'weight': 1.5, 'fillOpacity': 0.2}
            ).add_to(m)

    # Ajouter des marqueurs avec des propriétés personnalisées (listing en orange)
    for idx, row in listing.iterrows():
        folium.Marker(
            # On affiche toutes les propriétés du listing dans le popup
            popup='<br>'.join([f"<b>{k}</b>: {v}" for k, v in row['properties'].items()]),
            location=[row['geometry']['coordinates'][1], row['geometry']['coordinates'][0]],
            icon=folium.Icon(color='orange', icon='home', prefix='fa')
        ).add_to(marker_cluster)

    # Afficher la carte
    return m
