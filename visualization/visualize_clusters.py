# visualization/visualize_clusters.py
import matplotlib.pyplot as plt
import seaborn as sns
import umap

def plot_clusters(features_df):
    reducer = umap.UMAP()
    embedding = reducer.fit_transform(features_df.drop(columns=['ip', 'cluster']))
    
    plt.figure(figsize=(10,8))
    sns.scatterplot(x=embedding[:,0], y=embedding[:,1], hue=features_df['cluster'], palette='tab10')
    plt.title('Bot Behavior Clusters')
    plt.show()
