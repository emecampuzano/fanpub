import json, os

# Yes, I'm aware we could just read the dictionary and pass it through , but this 
# this way we can add more functionality to it later on. 

class Configurator:
    def __init__(self):
        self.path = 'Config/config.json'
        with open(self.path, 'r') as file:
            self.config = json.load(file)
            self.output : str = self.config['output']
            self.temp = os.path.join(self.output, 'Temp')
            self.content = os.path.join(self.temp, 'Content')
            self.media = os.path.join(self.temp, 'Media')
            self.epub = os.path.join(self.output, 'EPUB')


