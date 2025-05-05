# clustering/cluster_profiles.py
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

def cluster_behaviors(features_df):
    """
    Cluster behaviors using DBSCAN
    """
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features_df.drop(columns=['ip']))
    
    db = DBSCAN(eps=0.5, min_samples=5)
    labels = db.fit_predict(scaled_features)
    
    features_df['cluster'] = labels
    return features_df, db
