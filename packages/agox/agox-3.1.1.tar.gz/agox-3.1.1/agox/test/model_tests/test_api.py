import os
import pytest 

@pytest.mark.ray
def test():
    import agox.test.model_tests.descriptors_api
    import agox.test.model_tests.gpr_api
    import agox.test.model_tests.sgpr_api
    import agox.test.model_tests.load_api
    os.remove('gpr.h5')
    os.remove('sgpr.h5')
    
    
