from sklearn.cluster import OPTICS, cluster_optics_dbscan
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import cluster, mixture, metrics
import cv2
from matplotlib import pyplot as plt

def get_coordinate_mask(img, threshold=255):
    h = img.shape[0]
    w = img.shape[1]
    res = []
    for y in range(0, h):
        for x in range(0, w):
            if img[y, x] >= threshold:
                res.append([x, y])
    return np.array(res)



def optic_segmentation_clustering(img):
    clust = OPTICS(min_samples=50)
    clust.fit(img)
    labels = cluster_optics_dbscan(
        reachability=clust.reachability_,
        core_distances=clust.core_distances_,
        ordering=clust.ordering_,
        eps=2,
    )
    return labels

def dbscan_segmentation_clustering(img):
    db = DBSCAN(eps=0.1, min_samples=50)
    db = db.fit(img)
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    n_noise_ = list(labels).count(-1)

    print("Estimated number of clusters: %d" % n_clusters_)
    print("Estimated number of noise points: %d" % n_noise_)


def gaussian_segmentation_clustering(img, min_clusters=1, max_clusters=10):
    bic_score = []
    aic_score = []
    clusters = []
    shape = img.shape
    n_range = np.linspace(min_clusters, max_clusters, num=max_clusters + 1 - min_clusters).astype(np.uint)
    X = get_coordinate_mask(img)
    for n in n_range:
        ag = mixture.GaussianMixture(
            n_components=n
        ).fit(X)
        pred = gm.predict(X)
        #pred = (pred / max(pred.max(),1)) * 255
        #cv2.imshow('pred', pred.astype(np.uint8))
        #cv2.waitKey(0)
        clusters.append(n)
        bic_score.append(gm.bic(X))
        aic_score.append(gm.aic(X))

        # Plot the BIC and AIC values together
    fig, ax = plt.subplots(figsize=(12,8),nrows=1)
    ax.plot(n_range, bic_score, '-o', color='orange')
    ax.plot(n_range, aic_score, '-o', color='green')
    ax.set(xlabel='Number of Clusters', ylabel='Score')
    ax.set_xticks(n_range)
    ax.set_title('BIC and AIC Scores Per Number Of Clusters')
    plt.show()
    return None
        
def agglomerative_clustering(img, min_clusters=2, max_clusters=10):
    sil = []
    clusters = []
    shape = img.shape
    n_range = np.linspace(min_clusters, max_clusters, num=max_clusters + 1 - min_clusters).astype(np.uint)
    X = get_coordinate_mask(img)
    for n in n_range:
        km = cluster.KMeans(
            n_clusters=n,
        ).fit(X)
        pred = km.predict(X)
        #pred = (pred / max(pred.max(),1)) * 255
        #cv2.imshow('pred', pred.astype(np.uint8))
        #cv2.waitKey(0)
        clusters.append(n)
        sil.append(metrics.silhouette_score(X, km.labels_, metric = 'euclidean'))

    fig, ax = plt.subplots(figsize=(12,8),nrows=1)
    ax.plot(n_range, sil, '-o', color='orange')
    ax.set(xlabel='Number of Clusters', ylabel='Score')
    ax.set_xticks(n_range)
    ax.set_title('SIL metric Per Number Of Clusters')
    plt.show()
    return None

