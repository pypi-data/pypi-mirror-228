# Eql Rt Data Client - v1.3

The official Python client for subscribing to 1 minutes Data.

Equal Solution is a India-based professional Setup providing realtime and historical data services to stock market traders – to help them take correct trading decisions. Founded in 2007 , we aim to revolutionize delivery of Financial Data in Indian and international exchanges.

We distribute low latency, realtime data of various Stock Exchanges . The data is disseminated in multiple charting and technical analysis platforms which support desktop, server, mobile and web editions.We employs reliable, proven and sophisticated techniques to deliver direct exchange datafeeds into multiple Charting and Technical Analysis platforms. We are  focused to deliver authentic and accurate live data of Stock Market to their clients – at affordable price.

We also provide  Historical EOD and IEOD data for Amibroker™ , MetaStock™ , Advance Get™ & many others.


[Equalsolution] (https://equalsolution.com/) (c) 2023. Licensed under the MIT License.

## Documentation

Installing the client
>pip install eqldata

Usage
Subscribing to Instruments
You can subscribe to Instruments from server using the provided client.

>from eqldata import DataClient


List of topics to subscribe to
>instrument_list = ["CRUDEOILM_I", "CRUDEOILM_II"]


Subscribe to Instruments data
>DataClient(auth_token, topics_to_subscribe)

Start listening for messages
>client.listen()


Use Example

```python
from eqldata import DataClient  # Import the DataClient class from your package


auth_token = 'your_auth_token'
instrument_list = ["CRUDEOILM_I", "SILVERM_I"]

# Create a DataClient instance
client = DataClient(auth_token, instrument_list)

try:
    while True:
        response = client.listen()
        if response is not None:
            print("Received:", response)
except KeyboardInterrupt:
    client.stop_listening()
    client.disconnect()
```