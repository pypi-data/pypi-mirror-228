# LCPDelta Python Package
This is the python wrapper to interact with all LCPDelta products through their API or DPS. To get started, install the latest version of the LCPDelta package. 

To find out more about LCPDelta's data products, click [**here**][LCPDelta_data_portal_link].
To find out more about Enact, click [**here**][Enact_Homepage].
## Enact API and DPS Instructions

Full instructions on how to utilise Enact's full API and DPS can be found [**here**][Enact_instructions_link]. Below are some examples to get you started. 

### API Example Code

```python
from LCPDelta import Enact
from datetime import date

username = "insert_username_here"
public_api_key = "insert_public_api_key_here"

apiHelper = Enact.APIHelper(username, public_api_key)

# Example dates
from_date= date(2022,4,1) 
to_date = date(2023,5,31)

response = apiHelper.get_series_data("tsdf", from_date, to_date)
print(response)
```

### DPS Example Code

```python
from LCPDelta import Enact

def handle_new_information(x):
    # A callback function that will be invoked with the received series updates.
    # The function should accept one argument, which will be the data received from the series updates.
    print(x)
    
username = "insert_username_here"
public_api_key = "insert_public_api_key_here"

dps_helper = Enact.DPSHelper(username, public_api_key)
# Input method to handle any update to the series, alongside the series ID, that can be found on Enact.
dps_helper.subscribe_to_series_updates(handle_new_information, "RealtimeDemand") 

message = None
while message != "exit()":
    message = input(">> ")

#Terminate the connection at the end 
dps_helper.terminate_hub_connection()
```


[Enact_instructions_link]: https://enact.lcp.energy/externalinstructions
[LCPDelta_data_portal_link]: https://portal.lcpdelta.com/
[Enact_Homepage]: https://enact.lcpdelta.com/