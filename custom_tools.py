import json

# this contains all the custom tools that the user can use. For now only characters, places, items and quests can be created. 

def execute_function_call(message):
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

    return results

def write_place(content):
    """
    write the place asked by the user. Always use when you have to create or modify a place.

    Args:
        name (str): The name of the place.
        region (str): The region in which the place is located.
        population (int): The population of the place.
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
        personality (str): The outward personality of the character. The way he speaks, acts, etc.
        appearance (str): The appearance of the character.
        goals (str): The goals of the character.
        detailed (str): A detailed description of the character in 5 lines or less.

    Returns:
        str: The json of the formatted character.
    """
    print("write_character")

    jsoncontent = json.loads(content)
    jsoncontent["type"] = "characters"
    content = json.dumps(jsoncontent, indent=4)
    return content

def write_item(content):
    """
    Use this function each time you have to create or modify an item.

    Args:
        name (str): The name of the item.
        kind (str): The kind item.
        owner (str): The owner of the item.
        detailed (str): A detailed description of the item.

    Returns:
        str: The json of the formatted item.
    """
    print("write_item")

    jsoncontent = json.loads(content)
    jsoncontent["type"] = "items"
    content = json.dumps(jsoncontent, indent=4)
    return content

def write_quest(content):
    """
    Use this function each time you have to create or modify a quest.

    Args:
        name (str): The name of the quest.
        steps (str): The steps of the quest.
        detailed (str): A detailed description of the quest.

    Returns:
        str: The json of the formatted quest.
    """
    print("write_quest")

    jsoncontent = json.loads(content)
    jsoncontent["type"] = "quests"
    content = json.dumps(jsoncontent, indent=4)
    return content

def write_other(content):
    """
    Use this function each time you have to create something that has no other functions.

    Args:
        name (str): The name of the thing.
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
             'description': 'write the place asked by the user. Always use when you have to create or modify a place. Always provide name, region, population and detailed',
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
                     'detailed': {
                         'type': 'string',
                         'description': 'A detailed description of the place. Do not add carriage returns at all in this'
                     }
                 }
             },
             "required": ["name", "region", "population", "detailed"],
         }
         }
    )
    
    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'write_character',
             'description': 'write the character asked by the user. Always use when you have to create or modify a character. Always provide name, race, sex and detailed',
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
                     'personality': {
                            'type': 'string',
                            'description': 'The outward personality of the character. The way he speaks, acts, etc.'
                     },
                        'appearance': {
                            'type': 'string',
                            'description': 'The appearance of the character.'
                     },
                        'goals': {
                            'type': 'string',
                            'description': 'The goals of the character.'
                     },
                     'detailed': {
                         'type': 'string',
                         'description': 'A detailed description of the character. Do not add carriage returns at all in this'
                     }
                 }
             },
             "required": ["name", "race", "sex", "personality", "appearance", "goals", "detailed"],
         }
         }
    )
    
    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'write_item',
             'description': 'write the item asked by the user. Always use when you have to create or modify an item. Always provide name, kind, owner and detailed',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'name': {
                         'type': 'string',
                         'description': 'Name of the item. Not a generic name like the object or the item but a specific name like the ring of armor or the flaming sword.'
                     },
                     'kind': {
                         'type': 'string',
                         'description': 'The kind of item like a weapon, an armor, a chest.'
                     },
                        'owner': {
                            'type': 'string',
                            'description': 'The owner of the item.'
                     },
                     'detailed': {
                         'type': 'string',
                         'description': 'A detailed description of the item. Do not add carriage returns at all in this'
                     }
                 }
             },
             "required": ["name", "kind", "owner", "detailed"],
         }
         }
    )

    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'write_quest',
             'description': 'write the quest asked by the user. Always use when you have to create or modify a quest. Always provide name, steps and detailed',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'name': {
                         'type': 'string',
                         'description': 'Name of the quest.'
                     },
                     'steps': {
                         'type': 'string',
                         'description': 'The steps of the quest. No more than 5 steps in one line each.'
                     },
                     'detailed': {
                         'type': 'string',
                         'description': 'A detailed description of the quest in 5 lines. Do not add carriage returns at all in this'
                     }
                 }
             },
             "required": ["name", "steps", "detailed"],
         }
         }
    )


    custom_tools.append(
        {"type": "function",
         "function": {
             'name': 'write_other',
             'description': 'write the thing asked by the user when there is no better function. Use as a last resort. Always provide name and detailed.',
             'parameters': {
                 'type': 'object',
                 'properties': {
                     'name': {
                         'type': 'string',
                         'description': 'Name of the thing.'
                     },
                     'detailed': {
                         'type': 'string',
                         'description': 'A detailed description of the thing. Do not add carriage returns at all in this'
                     }
                 }
             },
             "required": ["name", "detailed"],
         }
         }
    )

    
    return custom_tools