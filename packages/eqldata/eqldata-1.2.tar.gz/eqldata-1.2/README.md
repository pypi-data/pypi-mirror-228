# WebSocket Client Package

A Python package for subscribing to 1 minutes Data.

Usage
Subscribing to Instruments
You can subscribe to Instruments from server using the provided client.

>from eqldata import DataClient


# List of topics to subscribe to
>instrument_list = ["CRUDEOILM_I", "CRUDEOILM_II"]


# Subscribe to Instruments data
>DataClient(auth_token, topics_to_subscribe)

# Start listening for messages
>client.listen()


# Example

> from eqldata import DataClient
> 
> #your authentication token
>
>auth_token = '1mJcvAAsJ5E3X2s'
> 
> #Instrument_list to subscribe to
> 
>instrument_list = ["CRUDEOILM_I"]
> 
>client = DataClient(auth_token, instrument_list)
> 
> #Wait for a response
> 
>response = client.listen()
> 
>print("Received:", response)
