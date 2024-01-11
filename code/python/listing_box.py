def trouver_listings_in_box(listing_collection,box):
    pipeline = [
    {
        "$match": {
            "geometry": {
                "$geoWithin": {
                    "$box": [ [ box[0], box[1] ], [ box[2], box[3] ] ]
                }
            }
        }
    }
]
    resultats = list(listing_collection.aggregate(pipeline))
    return resultats
