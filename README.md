# BingChatGPT-API

## How to run

`python api.py <cookies_U>`

## How to get cookies_U
Inspect -> Application -> Cookies -> Search "_U"

## bing API contracts

1. response body of https://www.bing.com/turing/conversation/create

```python
{
    "conversationId": None,
    "clientId": None,
    "conversationSignature": None,
    "result": 
        {
            "value": "Success", 
            "message": None
        }
}
```

2. request body of wss://sydney.bing.com/sydney/ChatHub

```python
{
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
            "isStartOfSession": {isStartOfSession},
            "message": {
                "author": "user",
                "inputMethod": "Keyboard",
                "text": {prompt},
                "messageType": "Chat",
            },
            "conversationSignature": {conversation_signature},
            "participant": {
                "id": {client_id},
            },
            "conversationId": {conversationId},
        },
    ],
    "invocationId": {invocationId},
    "target": "chat",
    "type": 4,
}
```

3. response body of wss://sydney.bing.com/sydney/ChatHub



## BingChatGPT-API contracts

### Create conversation
POST {host}/create_conversation

1. request body

```python
{
    "userId": "OlivierShi"
}
```

2. response body

```python
 {
    "conversationId": ,
    "clientId": ,
    "conversationSignature": ,
    "invocationId": 
}
```

- conversationId: to identify a conversation session
- clientId: to identify a user
- conversationSignature: to sign the data/message for this conversation session
- invocationId: to identify the invocation sequence. 0 stands for the first turn of a conversation.

### Chat with bing chatGPT
POST {host}/chatgpt

1. request body
```python
 {
    "prompt": "I love watching 'Three-Body'.",
    "conversationId": ,
    "clientId": ,
    "conversationSignature": ,
    "invocationId": 
}
```

2. response body

```python
 {
    "message": "",
    "conversationId": ,
    "invocationId": 
}
```

- message: is from Bing-ChatGPT
- conversationId: to identify a conversation session, is same with request conversationId
- invocationId: is one plus the request invocationId