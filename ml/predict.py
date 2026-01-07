from ml.features import event_to_features


def ml_ddos_score(model, event) -> float:
    
    features = event_to_features(event)
    return model.predict_proba([features])[0][1]
