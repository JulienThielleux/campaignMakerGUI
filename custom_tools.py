import json
import model
from utils import list_files

# Execute the function call
def execute_function_call(message, client, messages):
    function_name = message.tool_calls[0].function.name
    arguments = message.tool_calls[0].function.arguments

    # get the allowed functions from the content of the campaign/functions folder
    files = list_files('.\\campaign\\functions')
    allowed_functions = []
    for file in files:
        # open the file and load into a json object
        with open(file, 'r') as file:
            txtContent = file.read()
        jsonContent = json.loads(txtContent)
        allowed_functions.append(jsonContent["function"]["name"])

    
    if function_name in allowed_functions:
        print(f"{function_name}")
        # Verify that all the arguments are present
        # List all the arguments received
        arguments_list = []
        jsonArguments = json.loads(arguments)
        for key in jsonArguments:
            arguments_list.append(key)

        # List all the required arguments
        function_file_path = f'.\\campaign\\functions\\{function_name.split("_")[1]}.txt'
        with open(function_file_path, 'r') as file:
            txtContent = file.read()
        jsonContent = json.loads(txtContent)
        required_arguments = jsonContent["function"]["required"]

        # Check if all the required arguments are present
        missing_arguments = []
        for required_argument in required_arguments:
            if required_argument not in arguments_list:
                missing_arguments.append(required_argument)

        # If there are missing arguments, call the model back with a message to ask for the missing arguments, else call the function.
        if missing_arguments:
            print(f"Missing arguments: {missing_arguments}")
            messages = model.call_model(f"Please complete with the following arguments too: {', '.join(missing_arguments)}", client, messages)
            return None
        else:
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