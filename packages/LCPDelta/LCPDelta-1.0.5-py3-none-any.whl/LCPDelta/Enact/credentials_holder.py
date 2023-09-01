from LCPDelta import requests
from LCPDelta import json

class CredentialsHolder:
    
    MAX_RETRIES = 3
    
    def __init__(self, username, public_api_key):
        self.username = username
        self.public_api_key = public_api_key
        self.bearer_token = self.get_bearer_token(username, public_api_key)
        
    def get_bearer_token(self, enact_username, public_api_key):
        
        """Get the bearer token for authentication.

        This method sends a request to obtain a bearer token for authentication
        using the Enact API. It takes an Enact username and public API key as 
        input parameters.

        Args:
            enact_username (str): The username for Enact authentication.
            public_api_key (str): The public API key for Enact authentication.

        Returns:
            str: The bearer token obtained from the Enact API.
        """
        
        headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache'}
        data = {
            "Username": enact_username,
            "ApiKey": public_api_key
        }
        response = requests.post('https://enactapifd.lcp.uk.com/auth/token', headers=headers, data=json.dumps(data))
        
        if response.status_code == 401 or response.status_code == 500:
            response = self.retry_request(headers, data)
        
        bearer_token = response.text
        return bearer_token
    
    def retry_request(self, headers, data):
        """Retry the request to obtain a valid bearer token.

        This method retries the request to obtain a valid bearer token for authentication. It takes the request headers and data as input parameters.

        Args:
            headers (dict): The headers for the request.
            data (dict): The data to be sent with the request.

        Raises:
            Exception: If a valid bearer token cannot be obtained after
                    multiple attempts.

        Returns:
            Response: The response object containing the bearer token.
        """
        retry_count = 0
        while retry_count < self.MAX_RETRIES:
            response = requests.post('https://enactapifd.lcp.uk.com/auth/token', headers=headers, data=json.dumps(data))
            if response.status_code != 401 and response.status_code != 500:
                    # Successful response, no need to retry
                break   
            retry_count += 1
                
        if retry_count == self.MAX_RETRIES:
            raise Exception("Failed to obtain a valid bearer token after multiple attempts.")
        
        return response
    
    def get_remaining_token_count(self):
        """Get the remaining token count for API calls.

        This method sends a request to obtain the remaining token count for API calls. It retrieves the count based on the Enact username and public API key associated with the instance.

        Returns:
            str: The remaining token count for API calls.
        """
        headers = {'Content-Type': 'application/json', 'cache-control': 'no-cache'}
        data = {
            "Username": self.enact_username,
            "ApiKey": self.public_api_key
        }
        response = requests.post('https://enactapifd.lcp.uk.com/auth/usage', headers=headers, data=json.dumps(data))
        
        if response.status_code == 401 or response.status_code == 500:
            response = self.retry_request(headers, data)
            
        remaining_calls = response.text    
        print(f"You have {remaining_calls} API calls remaining") 
        return remaining_calls