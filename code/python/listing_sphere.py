def trouver_listings_in_sphere(listing_collection, sphere):
    pipeline = [
        {
            "$match": {
                "geometry": {
                    "$geoWithin": {                                    # Utilisation de geoWithin pour trouver les listings dans une geometrie
                        "$centerSphere": [sphere[0], sphere[1]]        # Utilisation de centerSphere pour trouver les listings dans une sphère
                    }
                }
            }
        }
    ]
    resultats = list(listing_collection.aggregate(pipeline))
    return resultats





