import warnings
from typing import Dict, List, Optional, Tuple

import numpy as np
from ase import Atoms
from scipy.linalg import lstsq, qr

from agox.models.GPR.GPR import GPR
from agox.utils import candidate_list_comprehension
from agox.utils.sparsifiers import CUR, SparsifierBaseClass


class SparseGPR(GPR):
    name = "SparseGPR"

    supported_descriptor_types = ["global", "local"]

    implemented_properties = ["energy", "forces", "local_energy", "uncertainty"]

    dynamic_attributes = ["X", "Xm", "Kmm_inv", "alpha", "C_inv", "kernel", "mean_energy"]

    """
    Sparse GPR Class

    Attributes
    ----------
    Xn : np.ndarray
        Training data
    Xm : np.ndarray
        Inducing points
    K_mm : np.ndarray
        Kernel matrix between inducing points
    K_nm : np.ndarray
        Kernel matrix between training and inducing points
    Kmm_inv : np.ndarray
        Inverse of K_mm
    C_inv : np.ndarray
        Inverse of C = K_mm + K_nm.T @ sigma_inv @ K_nm
    L : np.ndarray
        Matrix of ones and zeros indicating which atoms are in which configuration
    sparsifier: SparsifierBaseClass
        Sparsifier object
    

    Methods
    -------
    predict_local_energy(atoms=None, X=None)
        Calculate the local energies in the model.
    
    """

    def __init__(
        self,
        noise: float = 0.01,
        centralize: bool = False,
        jitter: float = 1e-8,
        unc_jitter: float = 1e-5,
        filter=None,
        sparsifier: SparsifierBaseClass = CUR(),
        n_optimize=0,
        **kwargs
    ) -> None:
        """

        Parameters
        ----------
        noise : float
            Noise level per descriptor center ie. per atom for local descriptors and
            per configuration for global descriptors.
        sparsifier : SparsifierBaseClass
            Sparsifier object
        jitter : float
            Jitter level

        """
        super().__init__(
            centralize=centralize, filter=filter, n_optimize=n_optimize, **kwargs
        )

        self.jitter = jitter
        self.unc_jitter = unc_jitter
        self.noise = noise

        self.sparsifier = sparsifier

        self._transfer_data = []
        self._transfer_noise = np.array([])

        self.add_save_attributes(["Xn", "Xm", "K_mm", "K_nm", "Kmm_inv", "C_inv", "L"])
        self.Xn = None
        self.Xm = None
        self.K_mm = None
        self.K_nm = None
        self.Kmm_inv = None
        self.C_inv = None
        self.L = None

        if self.use_ray:
            self.actor_model_key = self.pool_add_module(self)
            self.self_synchronizing = True  # Defaults to False, inherited from Module.

    @candidate_list_comprehension
    def predict_local_energy(self, atoms: Atoms, **kwargs) -> np.ndarray:
        """
        Calculate the local energies in the model.

        Parameters
        ----------
        atoms : ase.Atoms
            ase.Atoms object
        X : np.ndarray
            Features for the ase.Atoms object

        Returns
        -------
        np.ndarray
            Local energies

        """
        X = self._get_features(atoms)
        k = self.kernel(self.Xm, X)
        return (k.T @ self.alpha).reshape(
            -1,
        ) + self.single_atom_energies[atoms.get_atomic_numbers()]

    @candidate_list_comprehension
    def predict_uncertainty(
        self, atoms: Atoms, k: np.ndarray = None, k0: np.ndarray = None, **kwargs
    ) -> float:
        """
        Predict uncertainty for a given atoms object

        Parameters
        ----------
        atoms : ase.Atoms
            Atoms object

        Returns
        -------
        float
            Uncertainty

        """
        if "uncertainty" not in self.implemented_properties or self.alpha is None:
            unc = 0
        else:
            unc = np.sqrt(np.sum(self.predict_variances(atoms, k=k, k0=k0)))
        return unc

    def predict_variances(
        self, atoms: Atoms, k: np.ndarray = None, k0: np.ndarray = None, **kwargs
    ) -> float:
        X = self._get_features(atoms)

        if k is None:
            k = self.kernel(self.Xm, X)

        k0 = self.kernel(X, X)
        local_var = (
            np.diagonal(k0)
            - np.diagonal(k.T @ self.Kmm_inv @ k)
            + np.diagonal(k.T @ self.C_inv @ k)
        )

        # ensure local var is positive
        local_var[local_var < 0] = 0

        unc = local_var

        return unc

    @candidate_list_comprehension
    def predict_uncertainty_forces(self, atoms, x=None, k=None, dk_dr=None, **kwargs):
        if k is None:
            if x is None:
                x = self._get_features(atoms)
            k = self.kernel(self.Xm, x)

        if dk_dr is None:
            dk_dr = self._get_kernel_derivative(atoms, x=x)

        var_force = np.zeros((len(atoms), 3))
        var = np.sum(self.predict_variances(atoms, k=k))

        # Subset of regressors part:
        result = np.einsum("qm,qn->nm", self.C_inv, k)
        result = np.einsum("nadq,nq->ad", dk_dr, result)
        var_force = 2 * result

        # Projected process part:
        result = np.einsum("qm,qn->nm", self.Kmm_inv, k)
        result = np.einsum("nadq,nq->ad", dk_dr, result)
        var_force -= 2 * result

        # Convert to standard deviation force.
        std_force = -var_force / (2 * np.sqrt(var))

        return std_force

    @property
    def noise(self) -> float:
        """
        Noise level

        Returns
        -------
        float
            Noise level

        """
        return self._noise

    @noise.setter
    def noise(self, s: float) -> None:
        """
        Noise level

        Parameters
        ----------
        s : float
            Noise level

        """
        self._noise = s

    @property
    def transfer_data(self) -> List[Atoms]:
        """
        List of ase.Atoms objects to transfer to the model

        Returns
        -------
        list of ase.Atoms
            List of ase.Atoms objects to transfer to the model

        """
        return self._transfer_data

    @transfer_data.setter
    def transfer_data(self, l: List[Atoms]) -> None:
        """
        List of ase.Atoms objects to transfer to the model

        Parameters
        ----------
        l : list of ase.Atoms
            ase.Atoms objects to transfer to the model

        """
        warnings.warn(
            "transfer_data should not be used. Use add_transfer_data instead."
        )
        self.add_transfer_data(l)

    @property
    def transfer_noise(self) -> np.ndarray:
        """
        Noise level for transfer data

        Returns
        -------
        np.ndarray
            Noise level for transfer data

        """
        return self._transfer_noise

    @transfer_noise.setter
    def transfer_noise(self, s: np.ndarray) -> None:
        """
        Noise level for transfer data

        Parameters
        ----------
        s : np.ndarray
            Noise level for transfer data

        """
        warnings.warn(
            "transfer_noise should not be used. Use add_transfer_data instead."
        )
        self._transfer_noise = s

    def add_transfer_data(self, data: List[Atoms], noise: float = None) -> None:
        """
        Add ase.Atoms objects to the transfer data

        Parameters
        ----------
        data : list of ase.Atoms
            List of ase.Atoms objects to add to the transfer data
        noise : float
            Noise level for the transfer data

        """
        if isinstance(data, list):
            self._transfer_data += data
            if noise is None:
                noise = self.noise

            self._transfer_noise = np.append(
                self._transfer_noise, np.ones(len(data)) * noise
            )

        else:
            self.add_transfer_data.append([data])

    def model_info(self, **kwargs) -> List[str]:
        """
        List of strings with model information
        """
        x = "    "

        filter_name = self.filter.name if self.filter is not None else "None"
        try:
            data_before_filter = self._data_before_filter
            data_after_filter = self._data_after_filter
            filter_removed_data = self._data_before_filter - self._data_after_filter
        except AttributeError:
            filter_removed_data = 0

        sparsifier_name = (
            self.sparsifier.name if self.sparsifier is not None else "None"
        )
        sparsifier_mpoints = (
            self.sparsifier.m_points if self.sparsifier is not None else "None"
        )

        out = [
            "------ Model Info ------",
            "Descriptor:",
            x + "{}".format(self.descriptor.name),
            "Kernel:",
            x + "{}".format(self.kernel),
            "Filter:",
            x + "{} removed {} structures".format(filter_name, filter_removed_data),
            x + "- Data before filter: {}".format(data_before_filter),
            x + "- Data after filter: {}".format(data_after_filter),
            "Sparsifier:",
            x
            + "{} selecting {} inducing points".format(
                sparsifier_name, sparsifier_mpoints
            ),
            "Noise:",
            x + "{}".format(self.noise),
            "------ Training Info ------",
            "Total training data size: {}".format(self.Y.shape[0]),
            "Transfer data size: {}".format(len(self.transfer_data)),
            "Number of local environments: {}".format(self.Xn.shape[0]),
            "Number of inducing points: {}".format(self.Xm.shape[0]),
            "Neg. log marginal likelihood.: {:.2f}".format(self._nlml),
        ]

        return out

    def _train_model(self, data: List[Atoms]) -> None:
        """
        Train the model

        """
        assert self.Xn is not None, "self.Xn must be set prior to call"
        assert self.L is not None, "self.L must be set prior to call"
        assert self.Y is not None, "self.Y must be set prior to call"

        if self.use_ray:
            self.pool_synchronize(
                attributes=["Xn", "Xm", "Y", "L", "sigma_inv"], writer=self.writer
            )
            self.hyperparameter_search_parallel(relax=False)
        else:
            self.monte_carlo_hyperparameter_search()

        self.K_mm = self.kernel(self.Xm)
        self.K_nm = self.kernel(self.Xn, self.Xm)

        LK_nm = self.L @ self.K_nm
        K = (
            self.K_mm
            + LK_nm.T @ self.sigma_inv @ LK_nm
            + self.jitter * np.eye(self.K_mm.shape[0])
        )
        K = self._symmetrize(K)

        self.alpha = self._solve(K, LK_nm.T @ self.sigma_inv @ self.Y)

        self.Kmm_inv = self._solve(
            self.K_mm + self.unc_jitter * np.eye(self.K_mm.shape[0])
        )

        local_sigma_inv = self._make_local_sigma(self.transfer_data + data)
        C = (
            self.K_mm
            + self.K_nm.T @ local_sigma_inv @ self.K_nm
            + self.unc_jitter * np.eye(self.K_mm.shape[0])
        )
        C = self._symmetrize(C)
        self.C_inv = self._solve(C)

        if self.use_ray:
            self.pool_synchronize(
                attributes=["X", "Kmm_inv", "alpha", "C_inv", "kernel", "mean_energy"],
                writer=self.writer,
            )

    def _log_marginal_likelihood(self, theta: Optional[np.ndarray] = None) -> float:
        """
        Marginal log likelihood

        Parameters
        ----------
        theta : np.ndarray
            Kernel parameters

        Returns
        -------
        float
            log Marginal likelihood

        """
        if theta is not None:
            t = self.kernel.theta.copy()
            self.kernel.theta = theta
            K_nm = self.kernel(self.Xn, self.Xm)
            Kmm_inv = self._solve(
                self.kernel(self.Xm) + self.unc_jitter * np.eye(self.Xm.shape[0])
            )
            self.kernel.theta = t
        else:
            K_nm = self.K_nm
            Kmm_inv = self.Kmm_inv

        LK_nm = self.L @ K_nm
        Ktilde = LK_nm @ Kmm_inv @ LK_nm.T + np.diag(1 / np.diagonal(self.sigma_inv)) 

        sign, logdet = np.linalg.slogdet(Ktilde)
        if sign <= 0:
            return np.inf
        
        lml = -0.5 * logdet
        a = self._solve(Ktilde, self.Y)
        lml -= 0.5 * self.Y.T @ a
        lml -= 0.5 * self.Y.shape[0] * np.log(2 * np.pi)

        return float(lml)

    def _preprocess(self, data: List[Atoms]) -> None:
        """
        Preprocess the training data for the model

        Parameters
        ----------
        data : list of ase.Atoms
            List of ase.Atoms objects

        Returns
        -------
        np.ndarray
            Features for the ase.Atoms objects
        np.ndarray
            Energies for the ase.Atoms objects

        """
        X, Y = super()._preprocess(self.transfer_data + data)
        self.Xn = X

        self.L = self._make_L(self.transfer_data + data, X.shape)
        self.sigma_inv = self._make_sigma(self.transfer_data + data)

        if self.sparsifier is not None:
            self.Xm, _ = self.sparsifier(self.Xn)
        else:
            self.Xm = self.Xn

        return self.Xm, Y

    def _make_L(self, atoms_list: List[Atoms], shape_X: Tuple[int, int]) -> np.ndarray:
        """
        Make the L matrix

        Parameters
        ----------
        atoms_list : list of ase.Atoms
            List of ase.Atoms objects

        Returns
        -------
        np.ndarray
            L matrix

        """
        if len(atoms_list) == shape_X[0]:
            return np.eye(shape_X[0])

        lengths = [self.descriptor.get_number_of_centers(atoms) for atoms in atoms_list]
        r = len(lengths)
        c = np.sum(lengths)

        col = 0
        L = np.zeros((r, c))
        for i, atoms in enumerate(atoms_list):
            L[i, col : col + len(atoms)] = 1.0
            col += len(atoms)
        return L

    def _make_sigma(self, atoms_list: List[Atoms]) -> np.ndarray:
        """
        Make the sigma matrix

        Parameters
        ----------
        atoms_list : list of ase.Atoms
            List of ase.Atoms objects

        Returns
        -------
        np.ndarray
            Sigma matrix

        """
        sigmas = np.array(
            [
                self.noise**2 * self.descriptor.get_number_of_centers(atoms)
                for atoms in atoms_list
            ]
        )
        sigmas[: len(self.transfer_data)] = self.transfer_noise**2 * np.array(
            [
                self.descriptor.get_number_of_centers(atoms)
                for atoms in self.transfer_data
            ]
        )

        sigma_inv = np.diag(1 / sigmas)

        return sigma_inv

    def _make_local_sigma(self, atoms_list: List[Atoms]) -> np.ndarray:
        """
        Make the local sigma matrix. This is the inverse of the local noise
        variance. 

        Parameters
        ----------
        atoms_list : list of ase.Atoms

        Returns
        -------
        np.ndarray
            Local sigma matrix
        """
        local_sigmas = self.noise**2 * np.ones(self.K_nm.shape[0])
        if len(self.transfer_data) > 0:
            idx = np.sum([len(atoms) for atoms in self.transfer_data])
            n_repeats = [self.descriptor.get_number_of_centers(atoms) for atoms in self.transfer_data]
            local_sigmas[:idx] = np.repeat(np.array(self.transfer_noise) ** 2, n_repeats)
        
        local_sigma_inv = np.diag(1 / local_sigmas)
        return local_sigma_inv


    def _solve(self, A: np.ndarray, Y: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Solve the linear system using QR decomposition and least squares

        Parameters
        ----------
        A : np.ndarray
            Matrix A
        Y : np.ndarray
            Matrix Y

        Returns
        -------
        np.ndarray
            Solution X

        """
        Q, R = qr(A)
        if Y is None:
            return lstsq(R, Q.T)[0]
        else:
            return lstsq(R, Q.T @ Y)[0]

    def _symmetrize(self, A: np.ndarray) -> np.ndarray:
        """
        Symmetrize a matrix

        Parameters
        ----------
        A : np.ndarray
            Matrix to symmetrize

        Returns
        -------
        np.ndarray
            Symmetrized matrix

        """
        return (A + A.T) / 2
