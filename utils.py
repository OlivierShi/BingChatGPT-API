import json

DELIMITER = "\x1e"

def append_identifier(msg: dict) -> str:
    """
    Appends special character to end of message to identify end of message
    """
    # Convert dict to json string
    request_body = json.dumps(msg) + DELIMITER
    return request_body

def get_whitelist_users():
    with open("whitelist.txt", 'r') as fr:
        users = fr.readlines()
        return [line.strip() for line in users]

