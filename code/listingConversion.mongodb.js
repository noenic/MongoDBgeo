use ("data")

// On fait une agreagation sur la collection listings pour la transformer en geojson
db.getCollection("listings").aggregate([
    {
        // On crée un champ "type" qui contient la valeur "Feature"
        $addFields: {
            type: "Feature"
        }

    }, 
    // On remplace le champ "localisation" par "geometry"
    {
        $addFields: {
            geometry: "$localisation"
        }
    },
    // On inverse les coordonnées pour avoir la longitude en premier
    {
        $addFields: {
            "geometry.coordinates": {
                $reverseArray: "$geometry.coordinates"
            }
        }
    },

    // On supprime le champ "localisation"
    {
        $project: {
            localisation: 0
        }
    },
    // On crée un champ "properties" qui contient tous les autres champs de la collection sauf geometry et type et _id
    {
        $addFields: {
            properties: {
                $arrayToObject: {
                    $filter: {
                        input: {
                            $objectToArray: "$$ROOT"
                        },
                        cond: {
                            $not: {
                                $in: [
                                    "$$this.k", [
                                        "geometry",
                                        "type",
                                        "_id"
                                    ]
                                ]
                            }
                        }
                    }
                }
            }
        }
    },
    
    // On projette le champ "properties", "geometry" et "type" pour avoir un document geojson
    {
        $project: {
            properties: 1,
            geometry: 1,
            type: 1,
            _id: 1
        }
    },
    // On insère le document dans la collection "listings_geojson"
    {
        $out: "listings_geojson",
    }


    
    

])
