from abc import ABC, abstractmethod
from datetime import datetime

"""
Module Documentation: Configurations

This module defines the Configurations abstract class, providing a configuration interface for profiling.

Classes:
    - Configurations: Abstract base class for configuration settings.

Attributes:
    - is_db_update_required (bool):[Not in USE] Flag indicating whether to update a database with profiling results.
    - file_type (str): File type for storing profiling data (default: "csv").
    - report_path (str): Path for storing profiling reports.
    - connection_string (str):[Not in USE] Database connection string.
    - master_table (str):[Not in USE] Name of the master table in the database.
    - network_table (str):[Not in USE] Name of the network table in the database.
    - console_table (str):[Not in USE] Name of the console table in the database.
    - scenario_name (str): Name of the web scenario being profiled.
    - prefix_file_name (str): Prefix for the profiling report file name.

Methods:
    - __init__(self, is_db_update_required=False, file_type="csv"): Constructor method.
    - with_report_file_name_prefix(self, prefix): Abstract method for setting the file name prefix.
    - build(self): Abstract method for building the configuration.
    - with_db_update_required(self, is_db_update_required=False): Sets the flag for database update.
    - with_file_type(self, file_type): Sets the file type for profiling data.
    - with_report_path(self, report_path): Sets the path for profiling reports.
    - with_db_details(self, connection_string): Sets the database connection string.
    - with_table_names(self, master_table_name, network_table_name, console_table_name):[Not in USE] Sets the database table names.
    - set_scenario_name(self, scenario_name): Sets the web scenario name.
    - get_scenario_name(self): Gets the web scenario name.
    - get_connection_string(self)[Not in USE]: Gets the database connection string.
    - get_report_file_relative_path(self): Gets the relative path for profiling reports.
    - get_file_type(self): Gets the file type for profiling data.
    - with_report_file_name_prefix(self, prefix): Sets the file name prefix.
    - get_report_file_name_prefix(self): Gets the file name prefix.
    - get_report_file_name(self, suffix): Generates a unique file name for the profiling report.

"""
class Configurations(ABC):
    def __init__(self, is_db_update_required=False, file_type="csv"):
        self.is_db_update_required = is_db_update_required
        self.file_type = file_type
        self.report_path = None
        self.connection_string = None

    @abstractmethod
    def with_report_file_name_prefix(self, prefix):
        pass

    @abstractmethod
    def build(self):
        pass

    def with_db_update_required(self, is_db_update_required=False):
        self.is_db_update_required = is_db_update_required
        return self

    def with_file_type(self, file_type):
        self.file_type = file_type
        return self

    def with_report_path(self, report_path):
        self.report_path = report_path
        return self

    def with_db_details(self, connection_string):
        self.connection_string = connection_string
        return self
    
    def with_table_names(self,master_table_name, network_table_name, console_table_name):
        self.master_table = master_table_name
        self.network_table = network_table_name
        self.console_table = console_table_name
        return self 
    
    def set_scenario_name(self,scenario_name):
        self.scenario_name = scenario_name
        
    def get_scenario_name(self):
        return self.scenario_name
    
    def get_connection_string(self):
        return self.connection_string

    def get_report_file_relative_path(self):
        return self.report_path

    def get_file_type(self):
        return self.file_type
    
    def with_report_file_name_prefix(self, prefix):
        self.prefix_file_name = prefix
        return self 

    def get_report_file_name_prefix(self):
        return self.prefix_file_name

    def get_report_file_name(self,suffix):
        if self.get_report_file_name_prefix() and self.file_type:
            return f'{self.report_path}/{self.get_report_file_name_prefix()}_{datetime.now().strftime("%d_%m_%y_%H_%M_%S")}_{suffix}.{self.file_type}'
        return None

