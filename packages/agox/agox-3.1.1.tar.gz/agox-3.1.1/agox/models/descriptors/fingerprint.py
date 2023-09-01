from agox.models.descriptors import DescriptorBaseClass
from agox.models.descriptors.fingerprint_cython.angular_fingerprintFeature_cy import \
    Angular_Fingerprint


class Fingerprint(DescriptorBaseClass):

    name = "Fingerprint"
    descriptor_type = 'global'

    def __init__(
        self,
        rc1=6,
        rc2=4,
        binwidth=0.2,
        Nbins=30,
        sigma1=0.2,
        sigma2=0.2,
        gamma=2,
        eta=20,
        use_angular=True,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.cython_module = Angular_Fingerprint(
            self.environment.get_atoms(),
            Rc1=rc1,
            Rc2=rc2,
            binwidth1=binwidth,
            Nbins2=Nbins,
            sigma1=sigma1,
            sigma2=sigma2,
            gamma=gamma,
            eta=eta,
            use_angular=use_angular,
        )

    def create_features(self, atoms):
        return self.cython_module.get_feature(atoms).reshape(1, -1)

    def create_feature_gradient(self, atoms):
        return self.cython_module.get_featureGradient(atoms).reshape(1, len(atoms), 3, -1)

    def get_number_of_centers(self, atoms):
        return 1

    @classmethod
    def from_atoms(cls, atoms, **kwargs):
        from agox.environments import Environment

        environment = Environment(
            template=atoms, symbols="", use_box_constraint=False, print_report=False
        )
        return cls(environment=environment, **kwargs)

    