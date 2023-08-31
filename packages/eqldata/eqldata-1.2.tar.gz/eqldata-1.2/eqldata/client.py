import asyncio
import websockets
import json

class DataClient:
    def __init__(self, auth_token, topics, max_size=10 * 1024 * 1024, auto_reconnect=True, reconnect_interval=5):
        self.uri = 'wss://live.equalsolution.com'
        self.headers = {"token": auth_token}
        self.topics = topics
        self.max_size = max_size
        self.websocket = None
        self.auto_reconnect = auto_reconnect
        self.reconnect_interval = reconnect_interval
        self.is_listening = False

        asyncio.create_task(self._start())

    async def _start(self):
        await self.connect()
        await self.subscribe_to_topics(self.topics)
        await self.listen()

    async def connect(self):
        self.websocket = await websockets.connect(self.uri, extra_headers=self.headers, max_size=self.max_size)
        login_response = await self.websocket.recv()
        print(login_response)
        login_data = json.loads(login_response)
        if login_data.get("status") == "Successfully Login!":
            return True
        return False

    async def subscribe_to_topics(self, topics):
        if self.websocket is not None:
            subscribe_request = {
                "action": "subscribe",
                "topics": topics
            }
            await self.websocket.send(json.dumps(subscribe_request))
        else:
            raise ValueError("WebSocket connection is not established.")

    async def listen(self):
        while True:
            try:
                response = await self.websocket.recv()
                return response  # Return the received data
            except websockets.exceptions.ConnectionClosed:
                if self.auto_reconnect:
                    print("Connection closed. Reconnecting...")
                    await asyncio.sleep(self.reconnect_interval)
                    await self.connect()
                    await self.subscribe_to_topics(self.topics)
                else:
                    break

    def stop_listening(self):
        self.is_listening = False

    def disconnect(self):
        if self.websocket:
            asyncio.get_event_loop().run_until_complete(self.websocket.close())
