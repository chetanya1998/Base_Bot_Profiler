# scoring/threat_score.py
import numpy as np

def calculate_threat_score(row):
    """
    Threat score based on weighted features
    """
    score = (
        (row['hit_rate'] * 30) +
        (row['unique_paths'] * 20) +
        (row['ua_entropy'] * 25) +
        (row['avg_interval'] * -25)
    )
    return np.clip(score, 0, 100)
