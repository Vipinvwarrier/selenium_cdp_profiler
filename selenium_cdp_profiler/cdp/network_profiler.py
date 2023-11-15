
import json
"""
    NetworkProfiler: Class for profiling network requests and responses using the Chrome DevTools Protocol (CDP).

    Attributes:
        - network_requests (list): List to store network request log messages.
        - request_details (dict): Dictionary to store details of network requests by request ID.
        - network_data (list): List to store formatted network performance matrix.
        - driver: Selenium WebDriver instance with Chrome DevTools enabled.

    Methods:
        - __init__(self, driver): Constructor method for initializing NetworkProfiler.
        - get_response_body(self, request_id): Retrieves the response body for a given request ID.
        - get_browser_logs(self): Retrieves browser logs related to network performance.
        - request_will_be_sent(self, params, log_message): Handles 'Network.requestWillBeSent' events.
        - response_received(self, params): Handles 'Network.responseReceived' events.
        - get_network_tab_performance_matrix(self): Extracts network performance matrix from browser logs.

    Usage Example:
        profiler = NetworkProfiler(driver)
        network_data = profiler.get_network_tab_performance_matrix()

    Returns:
        List[dict]: A list of dictionaries containing network request details and response information.
                    Example: [{'API': 'https://example.com', 'CALL': 'GET', 'TIME': 120, 'STATUS': 200, 'TYPE': 'XHR', 'RESPONSE': {...}}]
"""

class NetworkProfiler():
    def __init__(self,driver):
        self.network_requests = []
        self.request_details = {}
        self.network_data = []
        self.driver = driver
    
    def get_response_body(self, request_id):
        response_body = self.driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': request_id})
        return response_body.get('body', '')

    def get_browser_logs(self):
        return self.driver.get_log('performance')

    def request_will_be_sent(self,params,log_message):
        request_id = params.get('requestId')
        wall_time = params.get('wallTime')
        request_url = params.get('request', {}).get('url')
        request_method = params.get('request', {}).get('method')
        request_type = params.get('type')

        if request_id and wall_time:
            self.request_details[request_id] = {
                'url': request_url,
                'method': request_method,
                'type': request_type,
                'start_time': wall_time
            }
            self.network_requests.append(log_message)

    def response_received(self,params):
        request_id = params.get('requestId')
        if request_id in self.request_details:
            request_data = self.request_details[request_id]
            request_url = request_data['url']
            request_method = request_data['method']
            request_type = request_data['type']

            response = params.get('response', {})
            response_status = response.get('status')

            timing = response.get('timing')
            if timing is not None:
                time_taken = timing['receiveHeadersEnd'] - timing['sendStart']

            network_entry = {
                'API': request_url,
                'CALL': request_method,
                'TIME': time_taken,
                'STATUS': response_status,
                'TYPE': request_type
            }
            if request_type == 'XHR' and response.get(
                    'mimeType') == 'application/json':
                response_body = self.get_response_body(request_id)
                network_entry['RESPONSE'] = response_body
            else:
                network_entry['RESPONSE'] = response
            self.network_data.append(network_entry)
  
    def get_network_tab_performance_matrix(self):
        browser_logs = self.get_browser_logs()
        for entry in browser_logs:
            log_message = json.loads(entry['message'])
            message = log_message.get('message', {})
            method = message.get('method', '')
            params = message.get('params', {})
            if method == 'Network.requestWillBeSent':
                self.request_will_be_sent(params,log_message)
            elif method == 'Network.responseReceived':
               self.response_received(params)

        return self.network_data
