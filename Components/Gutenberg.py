from ebooklib import epub
import markdown2
from .CoverArt import CoverArt
import datetime
import os
import re
import time
import warnings
warnings.filterwarnings("ignore")


class Press:

    def __init__(self, story, url, configurator):
        """
        Initializes a Press object.

        Parameters:
        - story: A Story object representing the story to be converted to an EPUB book.

        This method creates an EPUB book using the provided story's title and author.
        It adds chapters to the book and creates the spine for navigation.
        """
        # Create the book
        self.url = url
        self.book = epub.EpubBook()
        self.author = story.author
        self.title = story.title
        self.story = story
        self.book.set_title(story.title)
        self.book.add_author(story.author)
        self.config = configurator
        self.sanitise()

        self.insertDisclaimer()
        self.insertTitlePage()
        self.addMetadata()

        # Add chapters and create spline
        self.chapters = story.chapters
        self.addChapters()

        # Add cover
        self.cover = story.cover
        self.addCover()
        self.insertCover()

        # add table of contents
        # Add table of contents
        self.book.toc = ([epub.Link('Table of Contents.xhtml',
                         'Table of Contents', 'Table of Contents')] + self.book.toc)
        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())
        self.book.spine = ['nav'] + self.book.spine
        self.save()
        print(f'EPUB book created for {story.title} by {story.author}')

    def addChapters(self):
        try:
            chapters = os.listdir(self.config.content)
            chapters = sorted(chapters)
            for chapter in chapters:
                self.processChapter(chapter)
        except Exception as e:
            print(f"Exception in addChapters: {e}")
        return self

    def processChapter(self, chapter):
        try:
            with open(os.path.join(self.config.content, chapter), 'r', encoding='utf-8') as f:
                content = f.read()
                title = re.sub(r'.* - ', '', chapter)
                title = title.replace('.md', '')
                html = markdown2.markdown(content)
                chapter_number = re.search(r'\d+', chapter).group()
                chapter = epub.EpubHtml(
                    title=title, file_name=f'{chapter_number}_{title}.xhtml', lang='en')
                chapter.content = html
                self.book.add_item(chapter)
                self.book.spine.append(chapter)
                self.book.toc.append(chapter)
        except Exception as e:
            print(f"Exception in processChapter: {e}")

    def addCover(self):
        CoverArt(self.cover, self.config).fetch()
        time.sleep(1)
        self.book.set_cover('cover.jpg', open(os.path.join(
            self.config.media, 'cover.jpg'), 'rb').read())

    def insertCover(self):
        cover_page = epub.EpubImage()
        cover_page.file_name = 'cover.jpg'
        cover_page.media_type = 'image/jpeg'
        cover_page.content = open(os.path.join(
            self.config.media, 'cover.jpg'), 'rb').read()
        self.book.add_item(cover_page)
        self.book.spine.insert(0, cover_page)  # Insert after the intro

    def insertTitlePage(self):
        title_page = epub.EpubHtml(
            title='Title', file_name='title.xhtml', lang='en')
        title_page.content = f'<h1 style="text-align: center;">{self.book.title}</h1><h2 style="text-align: center;">{self.author}</h2>'
        self.book.add_item(title_page)
        self.book.spine.insert(1, title_page)  # Insert after the cover

    def insertDisclaimer(self):
        goodreadsLink = f'https://www.goodreads.com/search?q={self.story.title}'
        disclaimer_page = epub.EpubHtml(
            title='Disclaimer', file_name='disclaimer.xhtml', lang='en')
        with open('Resources/disclaimer.md', 'r', encoding='utf-8') as f:
            md_content = f.read().format(storyLink=self.url, Goodreads=goodreadsLink)
            html_content = markdown2.markdown(md_content)
            html_content = '<div style="text-align: center;">' + html_content + '</div>'
            disclaimer_page.content = html_content
        self.book.add_item(disclaimer_page)
        # Insert after the title pagee
        self.book.spine.insert(2, disclaimer_page)

    def addMetadata(self):
        idRegex = r'(\d*)-'
        id = re.search(idRegex, self.url).group(1)
        if id:
            self.book.set_identifier(f'wttpdthf{str(id)}')
        else:
            self.book.set_identifier(f'wttpdthf{str(time.time())}')

        self.book.set_language('en')
        from ebooklib import epub
        # Set publication date
        self.book.set_unique_metadata('DC', 'date', str(
            datetime.datetime.now()), {'event': 'publication'})

        # Set publisher
        self.book.set_unique_metadata(
            'DC', 'publisher', 'FANPUB', {})

    def sanitise(self):
        for file in os.listdir(self.config.content):
            filePath = os.path.join(self.config.content, file)
            if file.endswith('.md'):
                with open(filePath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                with open(filePath, 'w', encoding='utf-8') as f:
                    for line in lines:
                        if line.strip():
                            if line.strip()[-1].isdigit():
                                line = line[:-1]
                            f.write(line + '\n')

    def save(self):
        filename = self.story.title.replace(' ', '_')
        # if the name ends with a dot (.), remove it
        if filename[-1] == '.':
            filename = filename[:-1]
        exportPath = os.path.join(self.config.epub, f'{filename}.epub')
        epub.write_epub(exportPath, self.book)

        with open(exportPath, 'rb') as file:
            self.deliverable = file.read()

        return self
