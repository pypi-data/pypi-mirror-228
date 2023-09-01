from ase.io import write

from agox.writer import agox_writer
from .ABC_sampler import SamplerBaseClass
import numpy as np
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist


class KMeansSampler(SamplerBaseClass):
    name = "SamplerKMeans"
    parameters = {}

    """
    Parameters
    ----------
    descriptor : agox.models.descriptor.ABC_descriptor.DescriptorBaseClass
        Descriptor object that inherits from DescriptorBaseClass.
    model : agox.models.model.ABC_model.ModelBaseClass
        Model object that inherits from ModelBaseClass.
    sample_size : int
        The number of sample members, or population size. 
    max_energy : float
        The maximum energy difference, compared to the lowest energy structure, 
        for a structure to be considered for sampling.
    """

    def __init__(
        self, descriptor=None, model=None, sample_size=10, max_energy=5, **kwargs
    ):
        super().__init__(**kwargs)
        self.descriptor = descriptor
        self.sample_size = sample_size
        self.max_energy = max_energy
        self.sample = []
        self.sample_features = []
        self.model = model
        self.debug = False

    def setup(self, all_finished_structures):
        """
        Setup up the KMeans Sampler.

        Parameters
        ----------
        all_finished_structures : list of ase.Atoms or agox.candidates.candidate.Candidate
        """

        # Check if there are any finished structures
        if len(all_finished_structures) < 1:
            self.sample = []
            return

        # Sort the structures according to energy:
        structures, energies = self.energy_filter_structures(all_finished_structures)

        # Calculate features:
        X = self.get_features(structures)

        # Determine the number of clusters:
        # TODO: Why is this necessary?
        n_clusters = 1 + min(self.sample_size - 1, int(np.floor(len(energies) / 5)))

        # Perform KMeans clustering:
        kmeans = KMeans(n_clusters=n_clusters, init="k-means++", n_init=10, 
                        random_state=np.random.randint(0, 10e6)).fit(X)
        labels = kmeans.labels_

        # For each cluster find the lowest energy member:
        sample_indices = self.select_from_clusters(energies, n_clusters, labels)
        sample = [structures[i] for i in sample_indices]
        sample_features = [X[i] for i in sample_indices]
        cluster_centers = [kmeans.cluster_centers_[i] for i in labels[sample_indices]]

        # Sort the sample mmebers according to energy.
        # This is only important for the output.
        sample_energies = [t.get_potential_energy() for t in sample]
        sorting_indices = np.argsort(sample_energies)
        self.sample = [sample[i] for i in sorting_indices]
        self.sample_features = [sample_features[i] for i in sorting_indices]
        self.cluster_centers = [cluster_centers[i] for i in sorting_indices]

        # Print information about the sample:
        self.print_output(all_finished_structures, structures)

    def energy_filter_structures(self, all_structures):
        """
        Filter out structures with energies higher than e_min + max_energy

        Parameters
        ----------
        all_structures : list of ase.Atoms or agox.candidates.candidate.Candidate

        Returns
        -------
        structures : list of ase.Atoms or agox.candidates.candidate.Candidate
            List of structures that are within the energy range.
        e : list of float
            List of energies of the structures.
        """
        # Get energies of all structures:
        e_all = np.array([s.get_potential_energy() for s in all_structures])
        e_min = min(e_all)

        for i in range(5):
            filt = e_all <= e_min + self.max_energy * 2**i
            if np.sum(filt) >= 2 * self.sample_size:
                break
        else:
            filt = np.ones(len(e_all), dtype=bool)
            index_sort = np.argsort(e_all)
            filt[index_sort[2 * self.sample_size :]] = False

        # The final set of structures to consider:
        structures = [all_structures[i] for i in range(len(all_structures)) if filt[i]]
        e = e_all[filt]
        return structures, e

    def select_from_clusters(self, energies, n_clusters, labels):
        """
        Select the lowest energy member from each cluster.

        Parameters
        ----------
        energies : list of float
            List of energies of the structures.
        n_clusters : int
            Number of clusters.
        labels : list of int
            List of cluster labels for each structure.

        Returns
        -------
        sample_indices : list of int
            List of indices of the lowest energy member of each cluster.
        """
        indices = np.arange(len(energies))
        sample_indices = []
        for n in range(n_clusters):
            filt_cluster = labels == n
            cluster_indices = indices[filt_cluster]
            if len(cluster_indices) == 0:
                continue
            min_e_index = np.argmin(energies[filt_cluster])
            index_best_in_cluster = cluster_indices[min_e_index]
            sample_indices.append(index_best_in_cluster)
        return sample_indices

    def get_label(self, candidate):
        """
        Get the label of a candidate.

        Parameters
        ----------
        candidate : ase.Atoms or agox.candidates.candidate.Candidate
            Object to get the label of.

        Returns
        -------
        label : int
            The label of the candidate.
        """

        if len(self.sample) == 0:
            return None

        # find out what cluster we belong to
        f_this = np.array(self.descriptor.get_global_features([candidate]))
        distances = cdist(f_this, self.cluster_centers, metric="euclidean").reshape(-1)

        label = int(np.argmin(distances))
        return label

    def get_closest_sample_member(self, candidate):
        """
        Get the sample member that the candidate belongs to.

        Parameters
        ----------
        """
        label = self.get_label(candidate)
        cluster_center = self.sample[label]
        return cluster_center

    def get_features(self, structures):
        features = np.array(self.descriptor.get_features(structures)).sum(axis=1)
        return features

    def print_output(self, all_finished_structures, structures):
        sample_energies = [t.get_potential_energy() for t in self.sample]
        for i, sample_energy in enumerate(sample_energies):
            self.writer(f"{i}: Sample DFT Energy {sample_energy:8.3f}")

        if self.model is not None and self.model.ready_state:
            for s in self.sample:
                t = s.copy()
                t.set_calculator(self.model)
                E = t.get_potential_energy()
                sigma = self.model.get_property("uncertainty")
                s.add_meta_information("model_energy", E)
                s.add_meta_information("uncertainty", sigma)
            self.writer(
                "SAMPLE_MODEL_ENERGY",
                "[",
                ",".join(
                    [
                        "{:8.3f}".format(t.get_meta_information("model_energy"))
                        for t in self.sample
                    ]
                ),
                "]",
            )
            self.writer(
                "SAMPLE_MODEL_SIGMA",
                "[",
                ",".join(
                    [
                        "{:8.3f}".format(t.get_meta_information("uncertainty"))
                        for t in self.sample
                    ]
                ),
                "]",
            )

        if self.debug:
            write(
                f"all_strucs_iteration_{self.get_iteration_counter()}.traj",
                all_finished_structures,
            )
            write(
                f"filtered_strucs_iteration_{self.get_iteration_counter()}.traj",
                structures,
            )
            write(f"sample_iteration_{self.get_iteration_counter()}.traj", self.sample)
