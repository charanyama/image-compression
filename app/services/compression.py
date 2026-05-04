import numpy as np
from sklearn.cluster import KMeans


def compress_kmeans(img: np.ndarray, clusters: int = 5, max_iter: int = 100, random_state: int = 42):
    height, width, colors = img.shape
    points = img.reshape(-1, colors)

    kmeans = KMeans(
        n_clusters=clusters, max_iter=max_iter, n_init=10, random_state=random_state
    )

    kmeans.fit(points)

    centroids = kmeans.cluster_centers_
    lables = kmeans.labels_

    compressed_points = centroids[lables]

    compressed_img = compressed_points.reshape(height, width, colors)

    return compressed_img, centroids, lables


def compute_compression_stats(img: np.ndarray, centroids: np.ndarray, labels: np.ndarray):
    original_size = img.size
    compressed_size = centroids.nbytes + labels.size
    compression_ratio = original_size / compressed_size
    saved_percent = (1 - compressed_size / original_size) * 100

    return {
        "original_size": int(original_size),
        "compressed_size": int(compressed_size),
        "compression_ratio": round(compression_ratio, 2),
        "saved_percent": round(saved_percent, 2),
    }
