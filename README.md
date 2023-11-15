# selenium_cdp_profiler

Overview
========

The Selenium Profiler is a repository designed to seamlessly integrate into your Selenium test cases, providing enhanced capabilities for profiling network tab details and capturing console errors during execution. By incorporating this repository into your Selenium automation framework, you can effortlessly generate valuable insights into the network activity and identify console errors that occur during the execution of your test cases.

Note: The feature for database updates is currently not active and is slated for inclusion in upcoming releases.


Key Features:
--------------
Network Tab Profiling: Automatically captures and records detailed information from the network tab, including API calls, response times, and status.

Console Error Tracking: Monitors and logs console errors that occur during the execution of Selenium test cases, aiding in the identification and resolution of issues.

Usage Benefits
--------------
Integrating this repository into your automation framework offers the following advantages:

Enhanced Profiling: Obtain comprehensive insights into network interactions and potential issues within the browser's console.

Automation Framework Improvement: Elevate the capabilities of your Selenium automation framework by effortlessly incorporating network and console profiling.

Getting Started
===============

To get started, follow the installation instructions in the Installation section. After installation, you can seamlessly integrate the profiler into your existing Selenium test cases.

Installation
============

You can add the Git repository as a dependency in your project's requirements.txt file:

git+https://github.com/Vipinvwarrier/selenium_cdp_profiler.git@v0.1.0

OR

pip install git+https://github.com/Vipinvwarrier/selenium_cdp_profiler.git@v0.1.0

Configuration
=============
Configure the profiler with the necessary parameters, such as the Selenium WebDriver instance and optional settings.

Note: The feature for database updates is currently not active and is slated for inclusion in upcoming releases.

This method needs to be added before starting a test

profiler = Profiler() \
    .with_report_path({absolute_path_to_csv_file_report}) \
    .with_report_file_name_prefix({prefix_name_for_csv_files}) \
    .build()

After the test completion:
---------------------------
profiler.run(driver,scenario_name)

Method to generate report by passing webdriver instance and scenario name. This needs to be called before browser is quit and after test case is executed

Sample:
-------

Note : Enable performance logging by 

    options = webdriver.ChromeOptions()
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    options.add_argument("--remote-debugging-port=8000")

profiler.run(driver,request.node.name) we pass the webdriver instance and the catgory name you want to show in console error csv file. In this sample code it will show class name and all console errors received.

As the build method doesnot require webdriver instance to be passed you can create instance of profiler as per your need. Ex: If you want only one file for each network and console details then you could initiate the profiler for the entire session.

```python
from selenium_cdp_profiler.profiler import Profiler
#Rest of imports
@pytest.fixture(scope="class")
def setup(request):
    options = webdriver.ChromeOptions()
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    options.add_argument("--remote-debugging-port=8000")

    driver = webdriver.Chrome(options=options)
    
    profiler = Profiler(is_db_update_required=False, file_type="csv") \
        .with_report_path({absolute_path_to_csv_file_report}) \
        .with_report_file_name_prefix({prefix_name_for_csv_files}) \
        .build()
    request.cls.driver = driver

    yield  
    profiler.run(driver,request.node.name)
    driver.quit()

@pytest.mark.usefixtures("setup")
class TestYourClass:

    def test_case_1(self):
        #your test case
        
    def test_case_2(self):
            #your test case
