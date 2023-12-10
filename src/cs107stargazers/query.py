
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




