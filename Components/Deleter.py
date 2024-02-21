'''Yes, there was no need for a separate Deleter file,
but I had an Archiver function I won't ship, cause I know 
y'all be using it for piracy if I did. So instead you get this.'''

import os

class Deleter:

    def __init__(self, config):
        self.config = config

    def delete(self):
        try:
            chapters = os.listdir(self.config.content)
            cover = os.listdir(self.config.media)
            for chapter in chapters:
                os.remove(os.path.join(self.config.content, chapter))
            for file in cover:
                os.remove(os.path.join(self.config.media, file))
        except:
            pass