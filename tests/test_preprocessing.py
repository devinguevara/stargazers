import sys
import os
import pytest
import pandas as pd 

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from cs107stargazers.preprocessing import Preprocessing


data = {
    'objID': [1237678537416376475, 1237679321774096394, 1237679321774293108, 1237679321774293159, 1237679321776914474, 1237679321777242131, 1237679321777373209, 1237679321778683924, 1237679321779339268, 1237679321780715603],
    'ra': [319.855107, 3.990128, 4.476100, 4.576460, 10.457250, 11.304236, 11.567794, 14.594269, 16.036018, 19.278764],
    'dec': [8.710008, -6.116578, -6.126685, -6.071747, -6.062639, -6.220873, -6.060652, -6.010121, -5.958546, -5.903059],
    'u': [18.35033, 18.59702, 19.03942, 19.45110, 18.18036, 19.23810, 18.69356, 18.47187, 17.60519, 18.81682],
    'g': [17.13285, 17.47490, 18.30472, 17.53095, 16.13855, 18.04356, 17.48123, 17.18467, 16.43019, 17.72914],
    'r': [16.66923, 17.07987, 17.93391, 16.80655, 15.30769, 17.51633, 17.03138, 16.72974, 15.99243, 17.35243],
    'i': [16.56604, 16.92422, 17.82319, 16.50827, 14.99698, 17.31822, 16.87575, 16.57353, 15.80109, 17.21273],
    'z': [16.40493, 16.88132, 17.79516, 16.34224, 14.80965, 17.25550, 16.81628, 16.50560, 15.75423, 17.14535]
}

df = pd.DataFrame(data)


@pytest.fixture
def pp_fixture(): 
    return Preprocessing(df)

#create your test_normalize 
class TestNormalize:

    def test_no_replace(self, pp_fixture):
    
        #make sure that the pp_fixture.data hasnt changed 
        n_df = pp_fixture.normalize()
        assert pp_fixture.data.equals(df)
        assert(n_df['u'].max() <= 1)    

    #def test replace
    def test_replace(self, pp_fixture): 

        pp_fixture.normalize(replace = True)
        assert not pp_fixture.data.equals(df) 




#class TestRmOutlier: 
class TestRmOutlier: 

    def test_no_replace(self, pp_fixture):
        n_df = pp_fixture.rm_outlier()
        #make sure the new df doesn't equal original 
        assert not n_df.equals(df)
        assert pp_fixture.data.equals(df)

    def test_replace(self, pp_fixture): 
        pp_fixture.rm_outlier(replace = True)
        assert not pp_fixture.data.equals(df) 






    



#class TestInterpolate 
class TestInterpolate: 

    def test_no_replace(self, pp_fixture):
        n_df = pp_fixture.interpolate([13, 14, 15], y_col = 'z', x_col='ra', replace =False)
        assert len(n_df.columns) is 2

    def test_replace(self, pp_fixture): 
        pp_fixture.interpolate([13, 14, 15], y_col = 'z', x_col='ra', replace =True)
        assert not pp_fixture.data.equals(df)







 



