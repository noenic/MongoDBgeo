import pymongo

# Connexion à la base de données
client = pymongo.MongoClient("mongodb://192.168.0.250:30017/")
oldcollection = client["iut"]["listings"]

# On drop la collection si elle existe déjà
client["iut"].drop_collection("listings_geojson")

# Pipeline d'agrégation
pipeline = [
    {
        "$addFields": {
            "geometry": {
                "$mergeObjects": [
                    "$localisation",
                    {
                        "coordinates": {"$reverseArray": "$localisation.coordinates"}
                    }
                ]
            }
        }
    },
    {
        "$project": {
            "_id": 1,
            "type": {"$literal": "Feature"},
            "geometry": 1,
            "properties": {
                "id": "$id",
                "name": "$name",
                "neighbourhood_cleansed": "$neighbourhood_cleansed",
            }
        }
    }
]


# Effectuer l'agrégation
result = oldcollection.aggregate(pipeline)

# Créer la nouvelle collection
newcollection = client["iut"]["listings_geojson"]

# Insérer les résultats dans la nouvelle collection
newcollection.insert_many(result)

# Créer un index géospatial sur la nouvelle collection
newcollection.create_index([("geometry", pymongo.GEOSPHERE)])
