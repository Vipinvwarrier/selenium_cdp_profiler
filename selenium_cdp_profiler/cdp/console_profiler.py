class ConsoleProfiler:
    """
    ConsoleProfiler: Class for extracting console errors from a Selenium WebDriver Chrome instance.

    Attributes:
        - driver: Selenium WebDriver instance used for web automation.
        - scenario_name (str): Name of the web scenario associated with the profiling.

    Methods:
        - __init__(self, driver, scenario_name): Constructor method for initializing ConsoleProfiler.
        - get_console_errors(self): Retrieves console errors from the browser logs.

    Usage Example:
        profiler = ConsoleProfiler(driver, "SampleScenario")
        console_errors = profiler.get_console_errors()

    Returns:
        List[dict]: A list of dictionaries containing page titles and corresponding error messages.
                    Example: [{'page_title': 'SampleScenario', 'error_message': 'Sample error message'}]
    """
    def __init__(self, driver, scenario_name):
        """
        Constructor method for initializing ConsoleProfiler.

        Parameters:
            - driver: Selenium WebDriver instance.
            - scenario_name (str): Name of the web scenario for profiling.
        """
        self.driver = driver
        self.scenario_name = scenario_name

    def get_console_errors(self):
        """
        Retrieves console errors from the browser logs.

        Returns:
            List[dict]: A list of dictionaries containing page titles and corresponding error messages.
                        Example: [{'page_title': 'SampleScenario', 'error_message': 'Sample error message'}]
        """
        logs = self.driver.get_log('browser')
        console_errors = []
        for log in logs:
            if log['level'] == 'SEVERE' or log['level'] == 'WARNING':
                console_errors.append({
                    'page_title': self.scenario_name,
                    'error_message': log['message']
                })
        return console_errors
