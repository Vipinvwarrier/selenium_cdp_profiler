import pandas as pd
import os

class FileHandler:
   
    def write_data_to_csv(self, data,headers, filename):
        """
        Writes data to a CSV file.

        Parameters:
            - data (list): List of dictionaries representing the data to be written to the CSV file.
            - headers (list): List of column headers for the CSV file.
            - filename (str): Name of the CSV file.

        Returns:
            None
        """
        df = pd.DataFrame(data)
        if os.path.isfile(filename):
            df.to_csv(filename, mode='a', header=False, index=False)
        else:
            df.to_csv(filename, header=headers, index=False, mode='w')