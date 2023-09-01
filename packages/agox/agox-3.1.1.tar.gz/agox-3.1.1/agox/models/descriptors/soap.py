import numpy as np
from copy import copy
from agox.models.descriptors import DescriptorBaseClass

class SOAP(DescriptorBaseClass):

    feature_types = ['local', 'global', 'local_gradient']

    name = 'SOAP'
    descriptor_type = 'local'

    def __init__(self, r_cut=4, nmax=3, lmax=2, sigma=1.0,
                 weight=True, periodic=True, dtype='float64', normalize=False, crossover=True, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        from dscribe.descriptors import SOAP as dscribeSOAP

        self.normalize = normalize
        self.feature_types = self.feature_types.copy()
        self.r_cut = r_cut
        
        if periodic:
            self.feature_types.remove('local_gradient')
        
        if weight is True:
            weighting = {'function':'poly', 'r0':r_cut, 'm':2, 'c':1}
        elif weight is None:
            weighting = None
        elif weight is False:
            weighting = None
        else:
            weighting = weight
            

        self.soap = dscribeSOAP(
            species=self.environment.get_species(),
            periodic=periodic,
            r_cut=r_cut,
            n_max=nmax,
            l_max=lmax,
            sigma=sigma,
            weighting=weighting,
            dtype=dtype,
            crossover=crossover,
            sparse=False)

        self.lenght = self.soap.get_number_of_features()

    def create_features(self, atoms):
        """Returns soap descriptor for "atoms".
        Dimension of output is [n_centers, n_features]
        """
        return self.soap.create(atoms)
            
    def create_feature_gradient(self, atoms):
        """Returns derivative of soap descriptor for "atoms" with
        respect to atomic coordinates.
        Dimension of output is [n_centers, 3*n_atoms, n_features]
        """
        f_deriv = self.soap.derivatives(atoms, return_descriptor=False, attach=True, method='numerical')
        return f_deriv

    def get_number_of_centers(self, atoms):
        return len(atoms)

    @classmethod
    def from_species(cls, species, **kwargs):
        from ase import Atoms
        from agox.environments import Environment
        environment = Environment(template=Atoms(''), symbols=''.join(species), use_box_constraint=False,
                                  print_report=False)
        return cls(environment=environment, **kwargs)
