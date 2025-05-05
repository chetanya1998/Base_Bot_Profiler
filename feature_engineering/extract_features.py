# feature_engineering/extract_features.py
import pandas as pd
import numpy as np
from scipy.stats import entropy

def compute_features(df):
    """
    Feature extraction per IP/session
    """
    features = []
    
    for ip, group in df.groupby('ip'):
        hit_rate = group.shape[0] / ((group['timestamp'].max() - group['timestamp'].min()).total_seconds() + 1)
        unique_paths = group['path'].nunique()
        avg_interval = (group['timestamp'].sort_values().diff().mean()).total_seconds()
        ua_entropy = entropy(group['user_agent'].value_counts(normalize=True))
        
        features.append({
            'ip': ip,
            'hit_rate': hit_rate,
            'unique_paths': unique_paths,
            'avg_interval': avg_interval,
            'ua_entropy': ua_entropy,
        })
    
    feature_df = pd.DataFrame(features)
    return feature_df
