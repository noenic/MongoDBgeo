import folium
from folium.plugins import MarkerCluster
import geopandas as gpd

def afficher_carte(communes_data, listing_data):
    # Créer une GeoDataFrame à partir des données MongoDB
    communes = gpd.GeoDataFrame(communes_data)
    listing = gpd.GeoDataFrame(listing_data)

    # Créer une carte centrée sur la France
    m = folium.Map(location=[46.6031, 1.8883], zoom_start=6, tiles='CartoDB positron')

    # Ajouter les données GeoJSON à la carte (communes en bleu et mairies en rouge)
    marker_cluster = MarkerCluster(maxClusterRadius=50).add_to(m)
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
                        popup=f"<b>Mairie de :</b> {properties['commune']}",
                        icon=folium.Icon(color=marker_color)
                    ).add_to(marker_cluster)
                else:
                    folium.GeoJson(
                        geom,
                        style_function=lambda x: {'color': 'blue', 'fillColor': 'blue', 'weight': 1.5, 'fillOpacity': 0.2}
                    ).add_to(m)

    # Ajouter des marqueurs avec des propriétés personnalisées (listing en orange)
    for idx, row in listing.iterrows():
        popup_text = f"<b>ID:</b> {row['properties']['id']}<br><b>Name:</b> {row['properties']['name']}<br><b>Ville:</b> {row['properties']['neighbourhood_cleansed']}"
        folium.Marker(
            location=[row['geometry']['coordinates'][1], row['geometry']['coordinates'][0]],
            popup=popup_text,
            icon=folium.Icon(color='orange', icon='home', prefix='fa')
        ).add_to(marker_cluster)

    # Afficher la carte
    return m

