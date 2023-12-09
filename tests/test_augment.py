
#alright make the correct imports 
import numpy as np
import pandas as pd
import pytest 
from unittest.mock import patch
from _pytest.monkeypatch import MonkeyPatch
import sys
import os


sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)
from src.augment import Augment 


#make a function called test Augment

def test_Augment(): 

    my_array = np.array([[11, 22, 33], [44, 55, 66], [77, 88, 99], [111, 122, 133]])
    df = pd.DataFrame(my_array, columns=['indexA', 'B', 'C'])

    # 1. Augment.derive() with unitary increase (default)
    testinggg = Augment(df)
    assert isinstance(testinggg.data, pd.DataFrame)

    #making sure nothing happens to testing data 
    before_col = len(testinggg.data.columns)
    geddit = testinggg.derive()
    assert(len(testinggg.data.columns)  == before_col)
    #making sure that the new object has 1 new derive columns for every original column
    assert(len(geddit.columns) == 6)

    #make sure you can choose to not derive a certain column
    geddit = testinggg.derive(notrun="B")
    assert(len(geddit.columns) == 5)
    #also make sure the number of rows hasn't changed 
    assert(len(testinggg.data) == len(geddit))
   
    #Make sure the run argument works too, this should now have 5 columns since 2 derivative ones where added for columns B and c
    geddit = testinggg.derive(run=["B","C"])
    assert(len(geddit.columns) == 5)

    # the one-column case -- trickiest
    geddit = testinggg.derive(run=["B"])
    assert(len(geddit.columns) == 4)

    #check to see that it an error happens if the wrong kind of argument is taken
    with pytest.raises(ValueError):
        test = Augment([1, 2, 3])




#Pandas data frame check 
#Double columns check 
#No row number chance check 
#Class augment: 
#derive()
#fractional_derive()


