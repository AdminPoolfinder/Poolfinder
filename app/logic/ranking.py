def rank_data(scores, alternatives):

    result = []

    for alt in alternatives:
        result.append({
            "name": alt["name"],
            "harga": alt["harga"],
            "fasilitas": alt["fasilitas"],
            "kedalaman": alt["kedalaman"],
            "rating": alt["rating"],
            "score": scores.get(alt["name"], 0)
        })

    return sorted(result, key=lambda x: x["score"], reverse=True)