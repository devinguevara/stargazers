# build augmentation module for final project

# for normal derivatives: use numpy.gradient

# for fractional derivatives: numpy.fracdiff

# input: a pd df with each colaumn being a timeseries [i.e.columns correspond to variables, rows correspond to timepoints

# output: a pd df with (default) 2n - 1 columns, assuming that there is one column which gives the time references/index for the values in each row

# required / dependency
import numpy as np
import pandas as pd
#from fracdiff.sklearn import Fracdiff


class Augment:   # accept a processed pd dataframe
	''' doc string to explain'''  # note required input (cols must be, rows must be, etc.)

	def __init__(self, df_p):
		''' Data frame to create object of class Augment for attached methods must be a pandas df; it 
		should be formatted such that each column corresponds to a sequence of values for a given variable,
		and rows correspond to indices (time, etc.). '''

		if isinstance(df_p, pd.DataFrame) is False: 
			raise ValueError('Input must be a pandas dataframe')
		self.data = df_p   # ** assumes pd df, NOT numpy array

	def derive(self, run=None, notrun=None):
		''' Get derivative for timeseries provided in pre-processed dataframe.
		 Takes optional arguments "run" and "notrun", which must be lists of string columnames for 
		 columns which you do/do not want to calculate the derivative for. By default, all columns will be differentiated.
		 Returns dataframe with all of the columns in self.data + the derivative columns
		 for each variable indicated (default=all i.e. all columns), i.e. an augmented df.  '''
		
		df = self.data

		# in case not all derivates are desired: drop those not desired
		if run is not None:
			df = pd.DataFrame(df[run])  # run = list of column names for which to perform this
		if notrun is not None:
			df = df.drop(notrun, axis="columns")

		# convert df to numpy array & apply np.gradient
		if df.shape[1] == 1:   # np.gradient acts up for the single column case, needs to be formatted like this
			df_ = np.array(df.iloc[:,0])
			grad = np.gradient(df_)
		else:
			df_ = df.to_numpy(dtype=float)
			grad = np.gradient(df_, axis=1)   # default for varargs: assumes unitary increase  

		# provide interpretable colnames for output derivative columns
		der_names = "d_" + df.columns  # naming for derivative columns
		der_names = der_names.values.tolist()
		der = pd.DataFrame(grad, columns=der_names)

		# concatenate i.e. augment pd df in self.data with derivatives & return pd df
		df_aug = pd.concat([self.data, der], ignore_index=False, axis=1)
		return df_aug
	
	'''
	def fractional_derive(self, run=None, notrun=None, d=1.0, window=10, mode="same", window_policy="fixed"):
		
		df = self.data

		# in case not all derivates are desired: drop those not desired
		if run is not None:
			df = pd.DataFrame(df[run])  # run = list of column names for which to perform this
		if notrun is not None:
			df = df.drop(notrun, axis="columns")

		# convert df to numpy array & apply fractdiff
		if df.shape[1] == 1:   # np.gradient acts up for the single column case, needs to be formatted like this
			df_ = np.array(df.iloc[:,0])
		else:
			df_ = df.to_numpy(dtype=float)
		fracdiff = Fracdiff(d, window=window, mode=mode, window_policy=window_policy)
		out_ = fracdiff.fit_transform(df_)  # returns an array of the same dim

		# concatenate i.e. augment pd df in self.data with derivatives & return pd df
		out = pd.DataFrame(out)
		df_aug = pd.concat([self.data, out], ignore_index=False, axis=1)
		return df_aug

	'''








# 2. Augment.fractional_derive()



'''

# ------------------------------------------------------------------------------------
# fracdiff (?????)

my_array = np.array([[11, 22, 33], [44, 55, 66], [77, 88, 99], [111, 122, 133]])
df = pd.DataFrame(my_array, columns=['indexA', 'B', 'C'])
df


X = numpy.arange(10).reshape(5, 2)

fracdiff = Fracdiff(0.5, window=3)


np.array(df)
fracdiff.fit_transform(X)


fracdiff.fit_transform(X)
array([[0.   , 1.   ],
       [2.   , 2.5  ],
       [3.   , 3.375],
       [3.75 , 4.125],
       [4.5  , 4.875]])


'''
# np.arange(10)








# ------------------------------------------------------------------------------------

# work for derive()

# # # note: I will ignore this case bc varargs is being veryyyy annoying
# # df1 = pd.DataFrame(my_array, columns=['A', 'B', 'C'])
# # df1

# # test = np.gradient(df_npforgrad, index_grad, axis=1)    # df_index = varargs, axis=1 == columns

# test1 = np.gradient(np.array([1,2,3]))
# test1    # returns an array of the same size
# test1_names = "d_" + df1.columns
# test1_names = test1_names.values.tolist()
# test11 = pd.DataFrame(test1)
# test11
# test111 = pd.concat([df,test11], ignore_index=True, axis=1)
# test111

# pd.DataFrame(df["B"]).shape
# np.array(pd.DataFrame(df["B"])).transpose()

# np.gradient(np.array(pd.DataFrame(df["B"])).transpose())


# df["B"]
# np.gradient(np.array(df.iloc[:,0]))
