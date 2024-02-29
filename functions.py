import os
import json

def createFunctionsIni():

    if not os.path.isfile('.\\campaign\\functions\\characters.txt'):
        write_character = '{"type":"function","function":{"name":"write_characters","description":"write the character asked by the user. Always use when you have to create or modify a character. Always provide name, race, sex, personality, goals, detailed and representation","parameters":{"type":"object","properties":{"name":{"type":"string","description":"Name of the character. Not a generic name like the hero or the evil wizard but a specific name like Harry Potter or Frodo Baggins."},"race":{"type":"string","description":"The race of the character."},"sex":{"type":"string","description":"The sex of the character. Can be male, female or other"},"personality":{"type":"string","description":"The outward personality of the character. The way he speaks, acts, etc."},"goals":{"type":"string","description":"The goals of the character."},"detailed":{"type":"string","description":"A detailed description of the character."},"representation":{"type":"string","description":"The appearance of the character. Do nott say the name. Uses as few words as possible"}}},"required":["name","race","sex","personality","goals","detailed","representation"]}}'
        jsoncharacter = json.loads(write_character)
        write_character = json.dumps(jsoncharacter, indent=4)
        with open('.\\campaign\\functions\\characters.txt', 'w') as writeCharacter:
            writeCharacter.write(write_character)

    if not os.path.isfile('.\\campaign\\functions\\places.txt'):
        write_place = '{"type":"function","function":{"name":"write_places","description":"write the place asked by the user. Always use when you have to create or modify a place. Always provide name, region, population detailed and representation","parameters":{"type":"object","properties":{"name":{"type":"string","description":"Name of the place, not a generic name like the mysterious forest or the small village but a specific name like New York or Rivendell."},"region":{"type":"string","description":"The region in which the place is located. Not a generic name like the north or the south but a specific name like the United States or Middle Earth."},"population":{"type":"string","description":"The population of the place. Not a generic number like a lot or a few but a specific number like 8,623,000 or 3,000."},"detailed":{"type":"string","description":"A detailed description of the place."},"representation":{"type":"string","description":"A one sentence physical description of the place, this will be used to make a prompt for automatic picture generation.Include the region in which this place exist."}}},"required":["name","region","population","detailed","representation"]}}'
        jsonplace = json.loads(write_place)
        write_place = json.dumps(jsonplace, indent=4)
        with open('.\\campaign\\functions\\places.txt', 'w') as writePlace:
            writePlace.write(write_place)

    if not os.path.isfile('.\\campaign\\functions\\others.txt'):
        write_other = '{"type":"function","function":{"name":"write_others","description":"write the thing asked by the user when there is no better function. Use as a last resort. Always provide name and detailed.","parameters":{"type":"object","properties":{"name":{"type":"string","description":"Name of the thing."},"detailed":{"type":"string","description":"A detailed description of the thing."}}},"required":["name","detailed"]}}'
        jsonother = json.loads(write_other)
        write_other = json.dumps(jsonother, indent=4)
        with open('.\\campaign\\functions\\others.txt', 'w') as writeOther:
            writeOther.write(write_other)