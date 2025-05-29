from sklearn.cluster import KMeans
import pandas as pd

def estimate_clusters(data: pd.DataFrame, n_clusters: int = 3, features: list = None):
    if features is None:
        features = data.columns.tolist()

    try:
        model = KMeans(n_clusters=n_clusters, random_state=42)
        data["cluster"] = model.fit_predict(data[features])
        return data, model
    except Exception as e:
        print(f"[ClusterEstimator] Error: {e}")
        raise