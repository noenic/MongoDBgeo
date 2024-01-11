import pymongo
import numpy as np
import geopandas as gpd
from random import randint
from afficher_carte import afficher_carte
from listings_distance import trouver_listings_proches
from listing_box import trouver_listings_in_box
from listing_sphere import trouver_listings_in_sphere

# Utilisation de GeoNear, box et geoWithin




# Connexion à la base de données MongoDB
client = pymongo.MongoClient("mongodb://192.168.0.250:30017/")
db = client["iut"]
commune_collection = db["communes"]
listing_collection = db["listings_geojson"]
choice = input("Vous pouvez choisir 3 opérations : \n 1) Afficher les habitations proches du centre d'une commune \n 2) Afficher toutes les habitions qui sont dans une box \n 3) Afficher toutes les habitions qui sont dans une sphère \n Votre choix : ")

if choice == "1":
    # Pour afficher les habitations proches du centre d'une commune
    communes = gpd.GeoDataFrame(list(commune_collection.find({}, {'_id': 0})))
    distance=int(input("Entrez la distance en mètres : "))
    listing = gpd.GeoDataFrame(trouver_listings_proches(commune_collection,distance))

    layer1= communes
    layer2= listing


if choice == "2":

    # Coordonnées de la boîte
    ran=randint(0, 2)
    if ran == 0:
        box = [-1.540232, 43.472231, -1.458864, 43.510775]    # Biarritz
    if ran == 1:
        box = [-1.568301,43.323245,-1.319730,43.503810]       # Zone large autour de Bayonne
    if ran == 2:
        box = [-1.481137,43.485746,-1.460881,43.499601]       # Centre de Bayonne
    # Créer une GeoDataFrame pour la boîte
    box_gdf = gpd.GeoDataFrame([{"geometry": {"type": "Polygon","coordinates": [[[box[0], box[1]],[box[2], box[1]],[box[2], box[3]],[box[0], box[3]],[box[0], box[1]]]]}, "properties": {"Box": "Box"}}])
    # Créer une GeoDataFrame pour les listings dans la boîte
    listing_box = gpd.GeoDataFrame(trouver_listings_in_box(listing_collection, box))

    layer1= box_gdf
    layer2= listing_box

if choice == "3":
    # Coordonnées du centre de la sphère
    def create_circle(center, radius, num_points=100):
        angles = np.linspace(0, 2*np.pi, num_points)
        circle_points = np.array([[center[0] + radius * np.cos(angle), center[1] + radius * np.sin(angle)] for angle in angles])
        return circle_points
    ran=randint(0, 2)
    if ran == 0:
        sphere = [ -1.540232,43.472231 ]
        radius = 1.875/3963.2
    if ran == 1:
        sphere = [ -1.568301,43.323245 ]
        radius = 5/3963.2
    if ran == 2:
        sphere = [ -1.481137,43.485746 ]
        radius = 0.125/3963.2

    # Il y a une certaine approximation dans la création de la sphère a cause de la projection de Mercator
    circle_points = create_circle(sphere, radius*80)
    circle_gdf = gpd.GeoDataFrame([{"type" : "feature", "geometry": {"type": "Polygon", "coordinates": [circle_points.tolist()]},"properties": {"Circle": "Circle"}}])


    # Créer une GeoDataFrame pour les listings dans la sphère
    listing_sphere = gpd.GeoDataFrame(trouver_listings_in_sphere(listing_collection, [sphere, radius]))

    layer1= circle_gdf
    layer2= listing_sphere


afficher_carte(layer1,layer2)
