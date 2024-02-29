import configparser
import tiktoken
import os
import json

# Load properties from settings.ini
def get_properties():
    config = configparser.ConfigParser()
    config.read('settings.ini')
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

def get_json_key(file_path, key):
    # Get the value of a key from a json file
    with open(file_path, 'r') as file:
        fileContent = file.read()
    jsonContent = json.loads(fileContent)
    return jsonContent[key]

def prune_messages(messages):
    # Remove the last message that is not a system message
    for i in range(len(messages)):
        if messages[i]["role"] != "system":
            del messages[i]
            break
    return messages

def list_files(path = ".\\campaign"):
    # List the files in the directory recursively
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    return files

def createDirectoriesFromFunctions():
    files = list_files('.\\campaign\\functions')

    # create a directory in the campaign folder for each file
    for file in files:
        file_name = file.split('\\')[-1].split('.')[0]
        if not os.path.isdir(f'.\\campaign\\{file_name}'):
            os.mkdir(f'.\\campaign/{file_name}')