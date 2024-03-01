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
        settingsIni.write('#gpt-3.5-turbo-0613, gpt-3.5-turbo-0125, gpt-4-1106-preview, gpt-4-0125-preview, gpt-4-turbo-preview\n')
        settingsIni.write('campaign.language.model = gpt-3.5-turbo-0613\n\n')
        settingsIni.write('#dall-e-2, dall-e-3\n')
        settingsIni.write('campaign.image.model = dall-e-2\n\n')
