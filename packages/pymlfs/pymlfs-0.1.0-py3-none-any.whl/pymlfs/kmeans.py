import logging
import torch
from tqdm import tqdm


class Kmeans:
    """Implements a simplified version of the K-means algorithm."""

    def __init__(self, k: int, max_iters: int) -> None:
        """Constructor function.

        Init parameters.

        Parameters
        ----------
        k : int
            Number of clusters.
        max_iters : int
            Maximum number of iterations.
        """
        self.k = k
        self.max_iters = max_iters

        # logger
        self._logger_config()

    def fit(self, X: torch.Tensor) -> None:
        """
        This method is used to train the K-means algorithm.

        Parameters
        ----------
        X : torch.Tensor
            The training data (m x n) with m being the number of examples
            and n the number of features.
        """

        self.m, self.n = X.shape
        self.centroids = torch.rand(self.k, self.n)

        self.logger.info("Training K-means started")

        for iter in tqdm(range(self.max_iters + 1)):
            # Performing the Expectation step
            data_clusters = self._e_step(X)

            # Keeps in memory the last version of the centroids
            old_centroids = self.centroids.clone()

            # Performing the Maximization step
            self._m_step(X, data_clusters)

            # Convergence test
            if self._stopping_criterion(iter, old_centroids):
                break

        self.logger.info("Training K-means ended")

    def predict(self, X: torch.Tensor) -> torch.Tensor:
        """Performs cluster prediction

        This method is used to predict the cluster for a batch of examples.

        Parameters
        ----------
        X : torch.Tensor
            The test data (m x n) with m being the number of examples
            and n the number of features.

        Returns
        -------
        torch.Tensor
            returns pcluster predictions in a torch tensor.
        """
        return self._e_step(X)

    def _e_step(self, X: torch.Tensor) -> torch.Tensor:
        """Performs the expectation step.

        This method performs the expectation step of the EM algorithm.
        In other words, it assigns a cluster to every training point
        given the cluster's centroids.

        Parameters
        ----------
        X : torch.Tensor
            The training data (m x n) with m being the number
            of examples and n the number of features.

        Returns
        -------
            data_clusters : torch.Tensor
                Clusters of the input examples.
        """
        # Compute the distance between training points
        # and the current centroids
        distances = (X - self.centroids.reshape(self.k, 1, self.n)) ** 2
        distances = distances.sum(axis=2)

        # Assign the point to the closest centroid
        data_clusters = torch.argmin(distances, dim=0)

        return data_clusters

    def _m_step(self, X: torch.Tensor, data_clusters: torch.Tensor) -> None:
        """Performs the maximization step.

        This method performs the maximization step of the EM algorithm.
        In other words, given the clusters for each training point,
        it estimates the new centroids.

        Parameters
        ----------
        X : torch.Tensor
            The training data (m x n) with m being the number of examples
            and n the number of features.
        data_clusters : torch.Tensor
            Clusters of the input examples.
        """
        # The new centroid is the average over the examples assigned to it.
        for k in range(self.k):
            nb_samples = sum(data_clusters == k)
            if nb_samples != 0:
                self.centroids[k] = (1 / nb_samples) * X[data_clusters == k, :].sum(
                    axis=0
                )  # k x n

    def _stopping_criterion(self, iter: int, old_centroids: torch.Tensor) -> bool:
        """Stopping criterion definition.

        This method defines the stopping criterion for the K-means algorithm.

        Parameters
        ----------
        iter : int
            The curent iteration.
        old_centroids : torch.Tensor
            The previous version of clusters centroids.

        Returns
        -------
        bool
            returns True if the conditions of the stopping criterion are
            satisfied.
        """
        # Either the maxmimum number of iterations is reached
        # or the centroids do not move.
        return iter == self.max_iters or torch.equal(self.centroids, old_centroids)

    def _logger_config(self) -> None:
        """
        Logger configuration
        """
        self.logger = logging.getLogger("Kmeans")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)
