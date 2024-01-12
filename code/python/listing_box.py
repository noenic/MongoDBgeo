def trouver_listings_in_box(listing_collection,box):
    pipeline = [
    {
        "$match": {
            "geometry": {
                "$geoWithin": {                                             # Utilisation de geoWithin pour trouver les listings dans une geometrie
                    "$box": [ [ box[0], box[1] ], [ box[2], box[3] ] ]      # Utilisation de box pour trouver les listings dans une boîte
                }
            }
        }
    }
]
    resultats = list(listing_collection.aggregate(pipeline))
    return resultats
