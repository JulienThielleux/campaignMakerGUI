import os

def createSettingsIni():
    # Verifiy if the file exists
    if os.path.isfile('settings.ini'):
        return
    
    # Create the file
    with open('settings.ini', 'w') as settingsIni:
        settingsIni.write('[prompts]\n')
        settingsIni.write('system.prompt = You are a DM helper. You help dungeon master to create or modify interesting pieces of lore. You have access to several functions to create or modify differents pieces of lore. You decide which function is the most useful to answer the user request. You always use a function. You never greet the user. You never have a conversation with the user. You must always answer by calling a function.\n')
        settingsIni.write('picture.style.prompt = realistic art\n')
        settingsIni.write('\n')
        settingsIni.write('[settings]\n')
        settingsIni.write('campaign.setting = generic TTRPG\n')

