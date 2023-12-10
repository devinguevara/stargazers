"""
Query gaia to extract information for an object inputted by the user. 


This module contains the GaiaPipeline class, which is used to query the Gaia.
Object must be a denomination in the Gaia data table. A flag can be set to
print a plot of the epoch vs g_mag for the object.
"""
import pandas as pd 
from astroquery.sdss import SDSS

#alright create the query class 
class Query(): 

    def __init__(self, ADQL_string : str): 
        self.ADQL_string = ADQL_string
        try:
            from astroquery.sdss import SDSS
            import pandas as pd
            self.SDSS = SDSS
            self.pandas = pd
        except ImportError:
            print("Please install the required libraries using:")
            print("pip install astroquery pandas")
            # You may exit the program or take appropriate action based on your use case
            exit(1)        

    
    def get_df(self): 
        try:
            # Query SDSS using the provided ADQL query
            result = SDSS.query_sql(self.ADQL_string)           
            df = result.to_pandas()
            return df
        
        except Exception as e:
            print(f"An error occurred. Make sure you have a valid ADQL query.")

    def get_table(self): 
        try:
            # Query SDSS using the provided ADQL query
            result = SDSS.query_sql(self.ADQL_string)          
            return result
        
        except Exception as e:
            print(f"An error occurred. Make sure you have a valid ADQL query.")

    def print(self): 
        try:
            # Query SDSS using the provided ADQL query
            result = SDSS.query_sql(self.ADQL_string)          
            print(result)
        
        except Exception as e:
            print(f"An error occurred. Make sure you have a valid ADQL query.")



if __name__ == "__main__":
    # Example ADQL query (you can replace this with your own query)
    sample_query = """
    SELECT
        TOP 10
        p.objID, p.ra, p.dec, p.u, p.g, p.r, p.i, p.z
    FROM
        PhotoObj AS p
    WHERE
        p.u BETWEEN 0 AND 19.6
    """
    query = Query(sample_query)
    df = query.get_df()
    if isinstance(df, pd.DataFrame): 
        print(df)
    else: 
        print('ok df method failed')

