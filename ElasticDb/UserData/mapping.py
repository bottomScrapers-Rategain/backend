userDataMapping = {
    "properties": {
        "id": {"type": "keyword"},
        "ipAddress": {"type": "ip"},
        "browserData": {"type": "text"},
        "searchTerms": {"type": "text", "similarity": "jaccard_similarity"},
        "interactedAds": {"type": "keyword", "similarity": "jaccard_similarity"},
        "interests": {"type": "text", "similarity": "jaccard_similarity"}
    }
}

userDataSetting = {
    "index": {
        "similarity": {
            "jaccard_similarity": {
                "type": "DFR",
                "basic_model": "g",
                "after_effect": "b",
                "normalization": "h2",
                "background_corpus": 0.5
            }
        }
    }
}