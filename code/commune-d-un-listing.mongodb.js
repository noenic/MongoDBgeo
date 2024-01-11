use("data")
// On fait une aggregation qui nous permetde recuperer le nom de la commune de chaque listing 
// en utilisant le champs geometry du document geojson listings_geojson et la collection communes 
// en utilisant l'operateur $geoIntersects qui permet de savoir si un point est dans un polygone
// On utilise l'operateur $lookup pour faire une jointure entre les deux collections

db.getCollection("listings_geojson").aggregate([
    {
        $lookup: {
            from: "communes",
            let: {
                geometry: "$geometry"
            },
            pipeline: [
                {
                    $match: {
                        geometry: {
                            $geoIntersects: {
                                $geometry: "$$geometry"
                            }
                        }
                    }
                },
                {
                    $project: {
                        _id: 0,
                        nom: 1
                    }
                }
            ],
            as: "commune"
        }
    },
    {
        $unwind: "$commune"
    }
])
