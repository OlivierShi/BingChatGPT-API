import json
import websockets.client as websockets

from utils import append_identifier, DELIMITER

class ChatHubRequest:
    """
    Request object for ChatHub
    """

    def __init__(
        self,
        conversation_signature: str,
        client_id: str,
    ) -> None:
        self.struct: dict

        self.client_id: str = client_id
        self.conversation_id: str = ""
        self.conversation_signature: str = conversation_signature
        self.invocation_id: int = 0

    def update(
        self,
        prompt: str,
        conversationId: str,
        invocationId: int
    ) -> None:
        """
        Updates request object
        """
        self.struct = {
            "arguments": [
                {
                    "source": "cib",
                    "optionsSets": [
                        "nlu_direct_response_filter",
                        "deepleo",
                        "enable_debug_commands",
                        "disable_emoji_spoken_text",
                        "responsible_ai_policy_235",
                        "enablemm",
                    ],
                    "isStartOfSession": invocationId == 0,
                    "message": {
                        "author": "user",
                        "inputMethod": "Keyboard",
                        "text": prompt,
                        "messageType": "Chat",
                    },
                    "conversationSignature": self.conversation_signature,
                    "participant": {
                        "id": self.client_id,
                    },
                    "conversationId": conversationId,
                },
            ],
            "invocationId": str(invocationId),
            "target": "chat",
            "type": 4,
        }


class ChatHub:
    """
    Chat Hub API
    """
    def __init__(self) -> None:
        self.wss_link = "wss://sydney.bing.com/sydney/ChatHub"
        self.wss : websockets.WebSocketClientProtocol = None
        self.negotiate_hub_request = append_identifier({"protocol": "json", "version": 1})

    async def connect(self,):
        self.wss = await websockets.connect(self.wss_link)
        await self.__initial_handshake()

    async def ask_stream(self, hub_request: ChatHubRequest) -> str:
        """
        Ask a question to the bot
        """
        # Check if websocket is closed
        if self.wss:
            if self.wss.closed:
                self.connect()
        else:
            print("=========")
            await self.connect()

        # Send request
        await self.wss.send(append_identifier(hub_request.struct))
        final = False
        while not final:
            objects = str(await self.wss.recv()).split(DELIMITER)
            for obj in objects:
                if obj is None or obj == "":
                    continue
                response = json.loads(obj)
                if response.get("type") == 1:
                    yield False, response["arguments"][0]["messages"][0][
                        "adaptiveCards"
                    ][0]["body"][0]["text"]
                elif response.get("type") == 2:
                    final = True
                    yield True, response

    async def __initial_handshake(self):
        await self.wss.send(self.negotiate_hub_request)
        await self.wss.recv()

    async def close(self):
        """
        Close the connection
        """
        if self.wss:
            if not self.wss.closed:
                await self.wss.close()

