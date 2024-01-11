import pymongo
from afficher_carte import afficher_carte
from listings_distance import trouver_listings_proches
# Connexion à la base de données MongoDB
client = pymongo.MongoClient("mongodb://192.168.0.250:30017/")
db = client["iut"]
commune_collection = db["communes"]
listing_collection = db["listings_geojson"]

# # Charger les données GeoJSON de MongoDB
# communes_data = list(commune_collection.find({}, {'_id': 0}))
# listing_data = list(listing_collection.find({}, {'_id': 0}))

# # Appeler la fonction avec les données de communes et de listings
# afficher_carte(communes_data, listing_data)


# # Trouver les listings proches de chaque commune
res=trouver_listings_proches(commune_collection,5000)
# afficher_carte(commune_collection, trouver_listings_proches(commune_collection,5000))