# CampaignMakerGUI
The CampaignMakerGUI is a small RAG project with the primary goal of aiding Game Masters.

The project is currently a proof of concept and will undergo significant development in the coming weeks.
The user will be prompted to provide an OpenAI API key when running the program for the first time.

## Current Features:
- Currently supports systematic character and places creation.
- Other requests are categorized as “others”.
- Possibility to add different kind of generatable lore by adding files in the campaign/functions directory
  
## Interface Components:
- Current File Window: Displays the content of existing files and allows editing.
    The “save” button enables users to save files in the working directory.
    The file name will correspond to the name key of the model response.
  
- Model Generation Window: Contains the response generated by the language model.
    The “send to current” button transfers the response to the current file window for further editing and saving.

- User Input Window: Where users communicate with the model.
    Prompts should look like this:
      “Write me a small human village at the end of the Perimon village.”
      “Create a dark and mysterious forest said to be home to a nymph.”
    The “send to model” button calls the model with the user input.

- Context Inclusion:
  When the model is called, it should recognize references to previous pieces of lore in the user input.
  For instance, if King Bronn already exists in the ‘characters’ lore, typing “Write a big castle where King Bronn lives” should provide context about King Bronn to the model.


## Installation:
- Put the CMGUI.exe file in a directory.
- Launch CMGUI.exe.
- The 'Campaign' directory will be created containing everything that will be generated by the program.
- Give a valid openai API key when prompted.

## Roadmap:
- Give the possibility to choose which language model and which image generation model to use