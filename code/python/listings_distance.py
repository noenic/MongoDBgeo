def trouver_listings_proches(commune_collection,distance):
    # Agrégation pour trouver les listings proches de chaque commune
    pipeline = [
    {
        '$unwind': '$geometry.geometries'
    }, {
        '$match': {
            'geometry.geometries.type': 'Point'
        }
    }, {
        '$project': {
            '_id': 0, 
            'commune': '$properties.commune', 
            'mairie_coords': '$geometry.geometries.coordinates'
        }
    }, {
        '$lookup': {
            'from': 'listings_geojson', 
            'let': {
                'mairie_coords': '$mairie_coords'
            }, 
            'pipeline': [
                {
                    '$geoNear': {
                        'near': {
                            'type': 'Point', 
                            'coordinates': '$$mairie_coords'
                        }, 
                        'distanceField': 'distance', 
                        'maxDistance': 5000, 
                        'spherical': True
                    }
                }, {
                    '$project': {
                        '_id': 0
                    }
                }
            ], 
            'as': 'Features'
        }
    }, {
        '$unwind': '$Features'
    }, {
        '$project': {
            'Features': 1
        }
    }
]

    # Exécuter l'agrégation
    resultats_agregation = list(commune_collection.aggregate(pipeline))
    
    return resultats_agregation


