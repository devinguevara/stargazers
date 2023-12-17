# required / dependency
import numpy as np
import pandas as pd
import differint.differint as differint


class Augment:   # accept a processed pd dataframe
	''' Augment class provides encapsulated functions derive() and fractional_derive() for timeseries derivatives and 
	fractional derivatives, respectively. 
	
	As part of stargazers package, expected input to instantiate an instance of the class
	is the Pandas Dataframe output from the Query.get_df() function. However, both functions in this class will operate on any 
	Pandas Dataframe which provides column-wise timeseries data to return augmented Pandas Dataframes with columnwise-derivatives or 
	differintegrals. Missing data will potentially inhibit the ability of the gradient and differintegral (fractional derivative)
	functions to infer necessary values. ''' 

	def __init__(self, df_p):
		''' Data frame to create object of class Augment for attached methods must be a pandas df; it 
		should be formatted such that each column corresponds to a sequence of values for a given variable,
		and rows correspond to indices (time, etc.). '''

		if isinstance(df_p, pd.DataFrame) is False: 
			raise ValueError('Input must be a pandas dataframe')
		self.data = df_p   # ** assumes pd df, NOT numpy array

	def derive(self, run=None, notrun=None):
		''' Get derivative for timeseries provided in pre-processed Pandas dataframe; return an augmented Pandas Dataframe.

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
	
	def fractional_derive(self, frac, run=None, notrun=None, domain_start=0, domain_end=1):
		''' Get fractional differintegral (using 'improved' GL fractional derivative) for timeseries provided in pre-processed Pandas dataframe; 
		 return an augmented Pandas Dataframe. 
		
		 Required argument: frac, the order of the differintegral to be computed.

		 Takes optional arguments "run" and "notrun", which must be lists [or single values] of string columnames for 
		 columns which you do/do not want to calculate the differintegral for. By default, all columns will be differentiated.
         Also takes optional arguments "domain_start" and "domain_end" to diffint() GLI function; if not specified, defaults (0 and 1)
         match diffint() default values. Documentation: https://github.com/differint/differint/wiki/GLI

		 Returns dataframe with all of the columns in self.data + the differintegral (fractional derivative) columns
		 for each variable indicated with one value ("point") per row, i.e. an augmented df.
        '''
            
		df = self.data

		# in case not all derivates are desired: drop those not desired
		if run is not None:
			df = pd.DataFrame(df[run])  # run = list of column names for which to perform this
		if notrun is not None:
			df = df.drop(notrun, axis="columns")

		# provide interpretable colnames for output derivative columns
		der_names = "d_" + df.columns  # naming for derivative columns
		der_names = der_names.values.tolist()
        
		# calculate the fractional derivatives for each column
		# differint can only act on 1d arrays: iterate through all columns in df 
		diffint_list = []
		for col_ii in range(df.shape[1]):
			diffint_col = differint.GLI(frac, df.iloc[:,col_ii], num_points=df.shape[0], domain_start=domain_start, domain_end=domain_end) 
			diffint_list.append(diffint_col)
                  
		# return a df where each column corresponds to the fractional derivative, in order, of the columns in df
		der = pd.DataFrame(diffint_list).transpose()
		der.columns = der_names

		# concatenate i.e. augment pd df in self.data with derivatives & return pd df
		df_aug = pd.concat([self.data, der], ignore_index=False, axis=1)
		return df_aug