from openai import OpenAI
import os
from dotenv import load_dotenv
import utils
import custom_tools as ct
import json
from tenacity import retry, wait_random_exponential, stop_after_attempt

# Initiate the conversation
def initiate_conversation():
    GPT_MODEL = "gpt-3.5-turbo-0613"
    load_dotenv(override=True)
    client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))
    config = utils.get_properties()

    # Writing the system prompt
    systemPrompt = config.get('prompts','system.prompt')

    # Add the available functions to the system prompt
    function_files = utils.list_files('.\\campaign\\functions')
    available_functions_list = []
    for file in function_files:
        with open(file, 'r') as file:
            txtContent = file.read()
        jsonContent = json.loads(txtContent)
        available_functions_list.append(jsonContent["function"]["name"])
    available_functions = ', '.join(available_functions_list)

    systemPrompt += f" The only existing function are {available_functions}, always call one of those functions. "

    # Add the campaign setting to the system prompt
    settings = config.get('settings','campaign.setting')
    systemPrompt += f"The setting of the TTRPG is {settings}"

    print(systemPrompt)
    messages=[
            {"role": "system", "content": systemPrompt}
        ]
    
    return client, messages

# Handle the user input
def handle_input(user_text, client, messages):
    prompt = create_prompt(user_text)

    messages = call_model(prompt, client, messages)
    response = messages[-1]["content"]

    return messages, response

# Create the prompt for the model
def create_prompt(user_text):
    prompt = ""
    prompt += user_text

    # Check all the files to check if the user input contains a file
    contextContent = findMatchingFiles(user_text)


    if contextContent:
        prompt += '\n\nuse the following text as context:\n' + contextContent

    print(f"Prompt: {prompt}")
    return prompt

# Search recursively for the file in the campaign folder
def findMatchingFiles(user_text):
    contextContent = ""
    files = utils.list_files()
    for root, dirs, files in os.walk(".\\campaign"):
        for file in files:
            file_name = file.split('.')[0]  # Remove file extension
            file_name = file_name.replace('_', ' ')
            if file_name in user_text:
                with open(os.path.join(root, file), 'r') as file:
                    contextContent += file.read() + '\n\n'
    return contextContent

# Call the model
def call_model(prompt, client, messages):
    # Add the prompt to messages
    messages.append({"role": "user", "content": prompt})

    # Set up the custom tools
    custom_tools = ct.set_custom_tools()

    # Call the OpenAI API
    response = chat_completion_request(
        client, messages, tools=custom_tools, tool_choice='auto'
    )

    # Handle the response
    messages = handleAssistantResponse(response, messages, client)

    return messages

# Call the OpenAI API
@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(client, messages, tools=None, tool_choice=None):

    model = "gpt-3.5-turbo-0613"

    # Count the tokens of the conversation
    tokenNumber = utils.num_tokens_from_messages(messages, model)
    print(f"Number of tokens: {tokenNumber}")
    while tokenNumber > 2000:
        # Pruning the conversation
        print("Pruning the conversation")
        messages = utils.prune_messages(messages)
        tokenNumber = utils.num_tokens_from_messages(messages, model)
        print(f"Number of tokens: {tokenNumber}")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
            temperature=0,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

# Handle the assistant response 
def handleAssistantResponse(response, messages, client):
    assistant_message = response.choices[0].message
    if assistant_message.tool_calls:
        assistant_message.content = str(assistant_message.tool_calls[0].function)

    # Call a function if there is one
    messages.append({"role": assistant_message.role, "content": assistant_message.content})
    if assistant_message.tool_calls:
        results = ct.execute_function_call(assistant_message, client, messages)
        if results:
            messages.append({"role": "function", "tool_call_id": assistant_message.tool_calls[0].id, "name": assistant_message.tool_calls[0].function.name, "content": results})

    return messages

# Generate a picture
def generatePicture(client, file_path):
    
    # Get the description key from the file and use it to write the picture generation prompt
    prompt = utils.get_json_key(file_path, "representation")

    # Add the picture style to the prompt
    pictureStyle = utils.get_properties().get('prompts','picture.style.prompt')
    prompt += pictureStyle
    print(f"prompt:{prompt}")
    
    # Call the OpenAI API
    response = client.images.generate(
    model="dall-e-2",
    prompt=prompt,
    size="512x512",
    quality="standard",
    n=1,
    )

    image_url = response.data[0].url

    return image_url