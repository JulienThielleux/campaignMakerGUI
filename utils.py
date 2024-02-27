import configparser
import tiktoken
import os

# Load properties from prompt.ini
def get_properties():
    config = configparser.ConfigParser()
    config.read('prompt.ini')
    return config

def num_tokens_from_messages(messages, model):
    # Return the number of tokens used by a list of messages.
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    tokens_per_message = 3
    tokens_per_name = 1

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def prune_messages(messages):
    # Remove the last message that is not a system message
    for i in range(len(messages)):
        if messages[i]["role"] != "system":
            del messages[i]
            break
    return messages

def list_files():
    # List the files in the campaign directory recursively

    path = "./campaign"
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    print(files)
    return files