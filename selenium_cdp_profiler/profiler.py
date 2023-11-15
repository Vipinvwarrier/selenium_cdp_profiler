from selenium_cdp_profiler.cdp.console_profiler import ConsoleProfiler
from selenium_cdp_profiler.cdp.network_profiler import NetworkProfiler
from selenium_cdp_profiler.cdp.selenium_interface import SeleniumInterface
from selenium_cdp_profiler.configs.interface_configurations import Configurations
from selenium_cdp_profiler.utils.db_handler import DataBaseHandler
from selenium_cdp_profiler.utils.file_handler import FileHandler
import concurrent.futures

"""
Module Documentation: selenium_cdp_profiler.Profiler

This module defines the Profiler class, which facilitates devtools profiling using Chrome Dev Protocol:
    - Profiler: Main class for cdp profiling.

Usage Example:
    profiler = Profiler() \
        .with_report_path({absolute_path_to_csv_file_report}) \
        .with_report_file_name_prefix({prefix_name_for_csv_files}) \
        .build()

Note: Ensure that you have the required dependencies installed and configured before using this module.

Attributes:
    - is_db_update_required (bool): Flag indicating whether to update a database with profiling results.[Not in USE]
    - file_type (str): File type for storing profiling data (default: "csv").

Methods:
    - __init__(self, is_db_update_required=False, file_type="csv"): Constructor method.
    - build(self): Builds the Profiler instance, checking for mandatory configurations.
    - _get_data(self, network_profiler, console_profiler): Retrieves network and console error data.
    - _write_csv(self, data, headers, filename): Writes data to a CSV file.
    - _write_data_to_db(self, network_data, console_errors): Writes data to a database if required.[Not in USE]
    - run(self, driver, scenario_name): Executes the profiling for a given Selenium WebDriver and scenario.

Exceptions:
    - ValueError: Raised for missing mandatory configurations.

"""

class Profiler(Configurations, SeleniumInterface):

    def __init__(self,is_db_update_required=False, file_type="csv"):
        super().__init__(is_db_update_required, file_type)

    def build(self):
        if self.report_path is None:
            raise ValueError("Report path is mandatory.")
        elif self.is_db_update_required and not all([self.connection_string, self.master_table_name, self.network_table_name, self.console_table_name]):
            raise ValueError("If database update is required, a valid connection string and all table names are mandatory.")
        return self
    
    def _get_data(self, network_profiler, console_profiler):
        network_data = network_profiler.get_network_tab_performance_matrix()
        console_errors = console_profiler.get_console_errors()
        return network_data, console_errors

    def _write_csv(self, data, headers, filename):
            csv_handler = FileHandler()
            csv_handler.write_data_to_csv(data, headers,filename)

    def _write_data_to_db(self, network_data, console_errors):
        db_handler = DataBaseHandler()
        db_handler.write_data_to_DB(network_data)
        db_handler.write_console_errors_to_db(console_errors)

    def run(self,driver,scenario_name):
        SeleniumInterface.__init__(self, driver)
        self.set_scenario_name(scenario_name)
        network_profiler = NetworkProfiler(self.get_driver())
        console_profiler = ConsoleProfiler(self.get_driver(), self.get_scenario_name())

        network_csv_filename = self.get_report_file_name("_Network")
        console_csv_filename = self.get_report_file_name("_Console_errors")
        network_headers = ['API', 'CALL', 'TIME', 'STATUS', 'RESPONSE', 'TYPE']
        console_headers = ['Test Name', 'Error']

        with concurrent.futures.ThreadPoolExecutor() as executor:
            network_data, console_errors = executor.submit(self._get_data, network_profiler, console_profiler).result()

            network_fut=executor.submit(self._write_csv, network_data, network_headers, network_csv_filename)
            console_fut=executor.submit(self._write_csv, console_errors, console_headers, console_csv_filename)
            network_fut.result()
            console_fut.result()

        if self.is_db_update_required:
            self._write_data_to_db(network_data, console_errors)

