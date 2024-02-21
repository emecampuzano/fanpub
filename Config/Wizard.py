import os 
import tkinter as tk
from tkinter import filedialog, messagebox
import json


class Wizard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()
        self.configFile = r'Config/config.json'

    def setup_wizard(self):
        root = tk.Tk()
        root.withdraw()

        # Request user to select output folder
        messagebox.showinfo('Information', 'Select the output folder for the EPUB books.')

        # Select output folder
        output_folder = filedialog.askdirectory()
        if not output_folder:
            messagebox.showinfo('Information', 'No folder selected. Exiting...')
            exit()

        with open(self.configFile, 'r') as file:
            config = json.load(file)

        config['output'] = output_folder

        with open(self.configFile, 'w') as file:
            json.dump(config, file, indent=4)


        # Check if folders EPUB and Temp exist, if not, create them
        folders = ['EPUB', 'Temp', 'Temp/Content', 'Temp/Media']
        for folder in folders:
            try:
                os.makedirs(f'{output_folder}/{folder}')
            except FileExistsError:
                pass

    def doctor(self):
        '''
        Checks the configuration file for errors.
        '''
        with open(self.configFile, 'r') as file:
            config = json.load(file)
            output = config['output']

        if not os.path.exists(output):
            print('Configuration error: Output directory does not exist. Running setup wizard...')
            self.setup_wizard()
            
