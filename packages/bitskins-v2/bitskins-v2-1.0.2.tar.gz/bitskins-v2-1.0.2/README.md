# bitskins-v2-wrapper
An unofficial wrapper for the Bitskins V2 API in Python.

Quick Start
-----------
.. code:: bash
  
	pip install bitskins-v2


REST API example
----------------
.. code:: python

	from bitskins.client import Client

	client = Client(api_key)

	# get all available items on sale
	items = client.get_all_items_for_sale_list(app_id=730)

	# get account balance
	balance = client.get_account_balance()

Websockets example
------------------
.. code:: python

	import json
	from bitskins.streams import WebsocketClient

	def ws_callback(_, msg):
		data = json.loads(msg)
		print(data)

	ws_client = WebsocketClient(api_key, ws_callback)

	# subscrive to websocket channels
	ws_client.subscribe("listed")
	ws_client.subscribe("price_changed")
