from chathub import ChatHub, ChatHubRequest

class Chatbot:
    """
    Combines everything to make it seamless
            self.client_id: str = client_id
        self.conversation_id: str = ""
        self.conversation_signature: str = conversation_signature
        self.invocation_id: int = 0
    """

    def __init__(self) -> None:
        self.chat_hub: ChatHub = ChatHub()

    async def ask(self, 
                prompt: str, 
                conversationId: str,
                clientId: str,
                conversationSignature: str,
                invocationId: int
            ) -> dict:
        """
        Ask a question to the bot
        """
        # construct ChatHubRequest
        hub_request = ChatHubRequest(conversation_signature=conversationSignature, client_id=clientId)
        hub_request.update(prompt=prompt, conversationId=conversationId, invocationId=invocationId)
        async for final, response in self.chat_hub.ask_stream(hub_request):
            if final:
                return response

    # async def ask_stream(self, prompt: str, conversationId: str) -> str:
    #     """
    #     Ask a question to the bot
    #     """
    #     async for response in self.chat_hub.ask_stream(prompt=prompt, conversationId=conversationId):
    #         yield response

    async def close(self):
        """
        Close the connection
        """
        await self.chat_hub.close()

    async def reset(self):
        """
        Reset the conversation
        """
        await self.close()
        self.chat_hub = ChatHub()