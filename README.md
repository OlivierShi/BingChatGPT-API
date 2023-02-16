# BingChatGPT-API

## How to run

`python api.py <cookies_U>`

## How to get cookies_U
1. You should be in the whitelist of Bing/new
2. Log in Bing/new and search one time in BingChatGPT
3. Inspect -> Application -> Cookies -> Search "_U"

## API usage
1. call `POST {host}/create_conversation` with the body `{"userId": "OlivierShi"}`

The passed `userId` is a new-created concept in this PR, which is not the user account of Bing/new. This `userId` should be in the `whitelist.txt` and I write this simple logic to avoid too many uncontrollable requests.

It will return below information.
```python
 {
    "conversationId": ,
    "clientId": ,
    "conversationSignature": ,
    "invocationId": 
}
```

![image](https://user-images.githubusercontent.com/24621410/219033215-ef3cb61f-b909-4d8c-98bb-b0794d2e7eb3.png)
2. call `POST {host}/chatgpt` with the below body,
```python
{
  "prompt": "I love Three-Body.",
  "clientId": "",
  "conversationId": "",
  "conversationSignature": "",
  "invocationId": 0
}
```
where `clientId`, `conversationId`, `conversationSignature` and `invocationId` is the response from `create_conversation` API.

![image](https://user-images.githubusercontent.com/24621410/219032570-34f7d78b-6bf5-45a1-8262-b92c2c8c6f47.png)


## What is amazing
We can create multiple conversation sessions at the same time using **a single Bing account** with API `POST {host}/create_conversation`. In addition, those active sessions will not influence each other and multiple conversation can be processed independently within **a single Bing account**. 


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


# Reference 
https://github.com/acheong08/EdgeGPT
