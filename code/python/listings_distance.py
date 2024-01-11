def trouver_listings_proches(commune_collection,distance):
    # Agrégation pour trouver les listings proches du centre de chaque commune
    pipeline = [
    { '$unwind': '$geometry.geometries' },  # Étape 1: Dérouler (unwind) le tableau 'geometry.geometries'
    { '$match': { 'geometry.geometries.type': 'Point' } },  # Étape 2: Filtrer les documents avec le type 'Point'
    {
        '$project': {
            '_id': 0,
            'commune': '$properties.commune',
            'mairie_coords': '$geometry.geometries.coordinates'
        }
    },  # Étape 3: Projeter les champs nécessaires et renommer certains champs
    {
        '$lookup': {
            'from': 'listings_geojson',
            'let': { 'mairie_coords': '$mairie_coords' },
            'pipeline': [
                {
                    '$geoNear': {
                        'near': { 'type': 'Point', 'coordinates': '$$mairie_coords' },
                        'distanceField': 'distance',
                        'maxDistance': distance,
                        'spherical': True
                    }
                },
                { '$project': { '_id': 0, 'properties': 1, 'geometry': 1, 'distance': 1 } }
            ],
            'as': 'Features'
        }
    },  # Étape 4: Effectuer une jointure avec la collection 'listings_geojson' en utilisant l'opérateur $geoNear
    { '$unwind': '$Features' },  # Étape 5: Dérouler (unwind) le tableau 'Features' créé par la jointure
    {
        '$project': {
            'type': 'Feature',
            'geometry': { 'type': 'Point', 'coordinates': '$Features.geometry.coordinates' },
            'properties': {
                'id': '$Features.properties.id',
                'name': '$Features.properties.name',
                'neighbourhood_cleansed': '$Features.properties.neighbourhood_cleansed'
            }
        }
    },  # Étape 6: Projeter les champs nécessaires pour créer des features GeoJSON
    {
        '$group': {
            '_id': { 'commune': '$commune', 'name': '$properties.name' },
            'Features': { '$first': '$$ROOT' }
        }
    },  # Étape 7: Regrouper les documents par 'commune' et 'name', en conservant le premier document de chaque groupe
    {
        '$replaceRoot': {
            'newRoot': { '$mergeObjects': ['$Features'] }
        }
    }  # Étape 8: Remplacer le document racine par le document fusionné (Features)
]



    # Exécuter l'agrégation
    resultats_agregation = list(commune_collection.aggregate(pipeline))
    
    return resultats_agregation


