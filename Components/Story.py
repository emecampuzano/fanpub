import os


class Story:
    '''
    Main story class. \n
    Args:
        -title (str): The title of the story.
        -author (str): The author of the story.
        -cover (str): The cover of the story.
    '''

    def __init__(self, title, author, cover=None, configurator=None):
        self.title = self.sanitiseTitle(title)
        self.author = author
        self.chapters = []
        self.cover = cover
        self.config = configurator

    def sanitiseTitle(self, title):
        # Remove special characters from title
        title = title.replace('/', '-')
        return title

    def addChapter(self, title, content):
        chapter = Chapter(title, content)
        self.chapters.append(chapter)
        self.writeChapter(chapter)

    def sanitiseChapter(self, chapter):
        # Check paragraphs in chapter (the chapter is a list of paragraphs) for paragraphs without text, and remove them,
        # It's safe to remove by the first character because the sanitiseParagraph function removes the first character if it's a space or tab
        for paragraph in chapter:
            if paragraph[0] == ' ' or paragraph[0] == '\t':
                chapter.remove(paragraph)

    def writeChapter(self, chapter):
        # get chapter number
        chapterNumber = self.chapters.index(chapter) + 1
        # Add trailing zeros to chapter number
        chapterNumber = str(chapterNumber).zfill(3)
        chapterTitle = f'{chapterNumber} - {chapter.title}'
        # if chapter title ends with a dot (.), remove it
        if chapterTitle[-1] == '.':
            chapterTitle = chapterTitle[:-1]
        # if file exists, delete it
        chapterPath = os.path.join(self.config.content, f'{chapterTitle}.md')
        if os.path.exists(chapterPath):
            os.remove(chapterPath)

        with open(chapterPath, 'a', encoding="utf-8", newline='\n') as cd:
            cd.write(
                f'<h1 style="text-align: center;">{chapter.title.strip()}</h1>\n')
            for paragraph in chapter.content:
                # remove the last character of the paragraph
                paragraph = paragraph[:-1]
                if paragraph.strip():
                    cd.write(paragraph + '\n\n')

    def __addWithoutWriting(self, chapter):
        self.chapters.append(chapter)

    def addBaseChapters(self):
        pass


class Chapter:
    '''
    A book chapter. \n
    Args:
        -title (str): The title of the chapter.
        -text (str): The text of the chapter.
    '''

    def __init__(self, title, content, release=None):
        self.title = title
        ''' 
        The title of the chapter.
        '''
        self.content = content
