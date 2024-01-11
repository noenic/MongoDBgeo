import pymongo

# Connexion à la base de données
client = pymongo.MongoClient("mongodb://192.168.0.250:30017/")
oldcollection = client["iut"]["contour-des-communes-capbgeojsonNew"]

# On drop la collection si elle existe déjà
client["iut"].drop_collection("communes")

# Pipeline d'agrégation pour transformer les données
pipeline = [
    {
        "$project": {
            "_id": 1,
            "type": {"$literal": "Feature"},
            "properties": {
                "code_insee": "$properties.code_insee",
                "commune": "$properties.commune",
                "surf_ha": "$properties.surf_ha",
                "nom_epci": "$properties.nom_epci",
                "pole_territoriaux": "$properties.pole_territoriaux"
            },
            "geometry": {
                "type": {"$literal": "GeometryCollection"},
                "geometries": [
                    {
                        "type": {"$literal": "MultiPolygon"},
                        "coordinates": "$geometry.coordinates"
                    },
                    {
                        "type": {"$literal": "Point"},
                        "coordinates": [
                            "$properties.geo_point.lon",
                            "$properties.geo_point.lat"
                        ]
                    }
                ]
            }
        }
    },
    {
        "$unset": ["properties.geo_point"]
    }
]

# Exécutez le pipeline d'agrégation
result = oldcollection.aggregate(pipeline)

# Enregistrez les résultats dans la nouvelle collection "communes"
client["iut"]["communes"].insert_many(result)

# Créer un index géospatial sur la nouvelle collection
client["iut"]["communes"].create_index([("geometry", pymongo.GEOSPHERE)])

