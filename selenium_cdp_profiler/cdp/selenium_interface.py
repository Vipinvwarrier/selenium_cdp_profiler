class SeleniumInterface:
    def __init__(self, driver):
        self.driver = driver
        self.driver.execute_cdp_cmd('Network.enable', {})
        self.driver.execute_cdp_cmd('Page.enable', {})
        self.driver.execute_cdp_cmd('Runtime.enable', {})
        
    def get_driver(self):
        return self.driver

    
