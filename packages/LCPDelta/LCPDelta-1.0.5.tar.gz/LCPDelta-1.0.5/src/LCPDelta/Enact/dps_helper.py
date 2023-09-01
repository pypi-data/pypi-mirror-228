from LCPDelta import HubConnectionBuilder
from LCPDelta import pytime
from LCPDelta import partial
from .credentials_holder import CredentialsHolder
from LCPDelta import global_helper_methods

class DPSHelper:
    def __init__(self, username, public_api_key): 
        self.enact_credentials = CredentialsHolder(username, public_api_key)
        access_token_factory = partial(self.fetch_bearer_token)
        self.hub_connection = HubConnectionBuilder().with_url("https://enact-signalrhub.azurewebsites.net/dataHub",
            options={
                "access_token_factory" : access_token_factory
                }
            ).with_automatic_reconnect({
                "type": "raw",
                "keep_alive_interval": 10,
                "reconnect_interval": 5,
                "max_attempts": 5
            }).build()
        
        self.hub_connection.on_open(lambda: print("connection opened and handshake received ready to send messages"))
        self.hub_connection.on_close(lambda: print("connection closed"))
        
        success = self.hub_connection.start()
        pytime.sleep(5)
        
        if not success:
            raise ValueError("connection failed")        
    def fetch_bearer_token (self):
        return self.enact_credentials.bearer_token
              
    def add_subscription(self, request_object, handle_data):
        pytime.sleep(3)
        enact_push_response = self.hub_connection.send("JoinEnactPush", request_object, lambda m: self.callback_received(m.result, handle_data))
    
    def callback_received(self, m, handle_data):
        self.hub_connection.on(m['data']['pushName'], handle_data)
    
    def terminate_hub_connection(self): 
        self.hub_connection.stop()
        
    def subscribe_to_epex_trade_updates(self, handle_data_method):
        """
        Subscribe to EPEX trade updates and specify a callback function to handle the received data.

        Parameters:
            handle_data_method (callable): A callback function that will be invoked with the received EPEX trade updates.
                The function should accept one argument, which will be the data received from the EPEX trade updates.
        """
        # Create the Enact request object for EPEX trade updates
        enact_request_object_epex = [{ "Type" : "EPEX", "Group" : "Trades"}]
        # Add the subscription for EPEX trade updates with the specified callback function
        self.add_subscription(enact_request_object_epex, handle_data_method)


    def subscribe_to_series_updates(self, handle_data_method, series_id, option_id = None, country_id = "Gb"):
        """
        Subscribe to series updates with the specified SeriesId and optional parameters.

        Parameters:
            handle_data_method (callable): A callback function that will be invoked with the received series updates.
                The function should accept one argument, which will be the data received from the series updates.

            series_id (str): This is the Enact ID for the requested Series, as defined in the query generator on the 'General' tab.

            option_id (List of strings, optional): If the selected Series has options, then this is the Enact ID for the requested Option,
                                       as defined in the query generator on the 'General' tab.
                                       If this is not sent, but is required, you will receive back an error.

            country_id (str, optional): This is the Enact ID for the requested Country, as defined in the query generator on the 'General' tab. Defaults to 'Gb'. 
        """
        request_details = {
            "SeriesId" : series_id,
            "CountryId" : country_id
        }
        
        if option_id is not None:
            if not global_helper_methods.is_list_of_strings(option_id):
                raise Exception("Option ID input must be a list of strings")
            request_details["OptionId"] = option_id
        
        enact_request_object_series = [ request_details ]
        self.add_subscription(enact_request_object_series, handle_data_method)    

        