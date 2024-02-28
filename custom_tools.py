import json
import sys
from utils import list_files

# this contains all the custom tools that the user can use. For now only characters, places, items and quests can be created. 

"""def execute_function_call(message):
    function_name = message.tool_calls[0].function.name
    arguments = message.tool_calls[0].function.arguments

    match function_name:
        case "write_place":
            results = write_place(arguments)
        case "write_character":
            results = write_character(arguments)
        case "write_item":
            results = write_item(arguments)
        case "write_quest":
            results = write_quest(arguments)
        case "write_other":
            results = write_other(arguments)
        case _:
            results = f"Error: function {function_name} does not exist"

    return results"""

def execute_function_call(message):
    function_name = message.tool_calls[0].function.name
    arguments = message.tool_calls[0].function.arguments

    # get the allowed functions from the content of the campaign/functions folder
    files = list_files('.\\campaign\\functions')
    allowed_functions = ['write_others']
    for file in files:
        # open the file and load into a json object
        with open(file, 'r') as file:
            txtContent = file.read()
        jsonContent = json.loads(txtContent)
        allowed_functions.append(jsonContent["function"]["name"])

    if function_name in allowed_functions:
        print(f"{function_name}")
        jsoncontent = json.loads(arguments)
        jsoncontent["type"] = f"{function_name.split('_')[1]}"
        results = json.dumps(jsoncontent, indent=4)

    else:
        results = f"Error: function {function_name} is not allowed"

    return results

def set_custom_tools():
    custom_tools= []

    # For each function, add a dictionary to the custom_tools list
    for file in list_files('.\\campaign\\functions'):
        # open the file and load into a json object
        with open(file, 'r') as file:
            txtContent = file.read()
        jsonContent = json.loads(txtContent)
        custom_tools.append(jsonContent)
    
    return custom_tools