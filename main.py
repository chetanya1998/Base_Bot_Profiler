# main.py
from data_ingestion.parse_logs import load_logs
from feature_engineering.extract_features import compute_features
from clustering.cluster_profiles import cluster_behaviors
from scoring.threat_score import calculate_threat_score
import joblib

if __name__ == "__main__":
    logs = load_logs('logs/access.csv')
    feature_df = compute_features(logs)
    feature_df, model = cluster_behaviors(feature_df)
    feature_df['threat_score'] = feature_df.apply(calculate_threat_score, axis=1)
    
    joblib.dump(model, 'models/clustering_model.pkl')
    feature_df.to_csv('outputs/profiles.csv', index=False)
    
    print("[INFO] Bot profiling complete!")
