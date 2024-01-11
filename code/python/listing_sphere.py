def trouver_listings_in_sphere(listing_collection, sphere):
    pipeline = [
        {
            "$match": {
                "geometry": {
                    "$geoWithin": {
                        "$centerSphere": [sphere[0], sphere[1]]
                    }
                }
            }
        }
    ]
    resultats = list(listing_collection.aggregate(pipeline))
    return resultats