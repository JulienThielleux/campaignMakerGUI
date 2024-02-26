import json

def execute_function_call(message):
    function_name = message.tool_calls[0].function.name
    arguments = message.tool_calls[0].function.arguments

    match function_name:
        case "write_place":
            results = write_place(arguments)
        case "write_character":
            results = write_character(arguments)
        case "write_other":
            results = write_other(arguments)
        case _:
            results = f"Error: function {function_name} does not exist"

    return results

def write_place(content):
    """
    write the place asked by the user. Always use when you have to create or modify a place.

    Args:
        name (str): The name of the place.
        region (str): The region in which the place is located.
        population (int): The population of the place.
        summary (str): A summary of the place.
        detailed (str): A detailed description of the place.

    Returns:
        str: The json of the formatted place.
    """
    print("write_place")

    jsoncontent = json.loads(content)
    jsoncontent["type"] = "places"
    content = json.dumps(jsoncontent, indent=4)
    return content

def write_character(content):
    """
    Use this function each time you have to create or modify a character.

    Args:
        name (str): The name of the character.
        race (str): The race of the character.
        sex (str): The sex of the character.
        summary (str): A summary of the character.
        detailed (str): A detailed description of the character.

    Returns:
        str: The json of the formatted character.
    """
    print("write_character")

    jsoncontent = json.loads(content)
    jsoncontent["type"] = "characters"
    content = json.dumps(jsoncontent, indent=4)
    return content

def write_other(content):
    """
    Use this function each time you have to create something that has no other functions.

    Args:
        name (str): The name of the thing.
        summary (str): A summary of the thing.
        detailed (str): A detailed description of the thing.

    Returns:
        str: The json of the formatted thing.
    """
    print("write_other")

    jsoncontent = json.loads(content)
    jsoncontent["type"] = "others"
    content = json.dumps(jsoncontent, indent=4)
    return content

def set_custom_tools():
    custom_tools= []

    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'write_place',
             'description': 'write the place asked by the user. Always use when you have to create or modify a place. Always provide name, region, population, summary and detailed',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'name': {
                         'type': 'string',
                         'description': 'Name of the place, not a generic name like the mysterious forest or the small village but a specific name like New York or Rivendell.'
                     },
                     'region': {
                         'type': 'string',
                         'description': 'The region in which the place is located. Not a generic name like the north or the south but a specific name like the United States or Middle Earth.'
                     },
                     'population': {
                         'type': 'string',
                         'description': 'The population of the place. Not a generic number like a lot or a few but a specific number like 8,623,000 or 3,000.'
                     },
                     'summary': {
                         'type': 'string',
                         'description': 'summary of the description of the place'
                     },
                     'detailed': {
                         'type': 'string',
                         'description': 'A detailed description of the place. Do not add carriage returns at all in this'
                     }
                 }
             },
             "required": ["name", "region", "population", "summary", "detailed"],
         }
         }
    )
    
    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'write_character',
             'description': 'write the character asked by the user. Always use when you have to create or modify a character. Always provide name, race, sex, summary and detailed',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'name': {
                         'type': 'string',
                         'description': 'Name of the character. Not a generic name like the hero or the evil wizard but a specific name like Harry Potter or Frodo Baggins.'
                     },
                     'race': {
                         'type': 'string',
                         'description': 'The race of the character.'
                     },
                     'sex': {
                         'type': 'string',
                         'description': 'The sex of the character. Can be male, female or other'
                     },
                     'summary': {
                         'type': 'string',
                         'description': 'summary of the description of the character'
                     },
                     'detailed': {
                         'type': 'string',
                         'description': 'A detailed description of the character. Do not add carriage returns at all in this'
                     }
                 }
             },
             "required": ["name", "race", "sex", "summary", "detailed"],
         }
         }
    )
    
    """
    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'write_other',
             'description': 'write the thing asked by the user when there is no better function.',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'name': {
                         'type': 'string',
                         'description': 'Name of the thing. Not a generic name like the object or the item but a specific name like the ring or the sword.'
                     },
                     'summary': {
                         'type': 'string',
                         'description': 'summary of the description of the thing'
                     },
                     'detailed': {
                         'type': 'string',
                         'description': 'A detailed description of the thing. Do not add carriage returns at all in this'
                     }
                 }
             },
             "required": ["name", "summary", "detailed"],
         }
         }
    )
    """
    
    return custom_tools