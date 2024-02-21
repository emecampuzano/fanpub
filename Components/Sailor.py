# from playwright.async_api import async_playwright
from .Story import Story
from time import sleep as wait
from .Gutenberg import Press
from .Human import randomWait
# from .Archiver import Archiver, Deleter
from .Deleter import Deleter
from undetected_playwright import stealth_sync
# from undetected_playwright import stealth_async
from .Configurator import Configurator

# You might be asking why I (comment) imported async versions of playwright and stealth.
# I wanted to make this service asynchronous to use as a Telegram bot, but it's
# a pain in the ass and I kinda don't want to rewrite the whole thing.
# Also, I didn't include the Archive module, you can make one, but I won't
# want to deal with people missusing it to make a piracy library.
# Again, this is for personal use ONLY.


class Sailor:
    '''
    It's called sailor because it ports, get it?

    '''

    def __init__(self, playwright, admin=False):
        self.playwright = playwright
        self.browser = playwright.chromium.launch(headless=True)
        self.context = self.browser.new_context()
        stealth_sync(self.context)
        self.config = Configurator()

    def warmup(self, url):
        self.page = self.context.new_page()
        self.page.goto(url)
        return self

    def getDetails(self):
        self.title = self.page.locator('.story-info__title').text_content()
        self.author = self.page.locator(
            '.author-info__username a').first.text_content()
        self.cover = self.page.locator('.story-cover img').get_attribute('src')
        self.chapters = self.page.query_selector_all(
            '.story-parts >> ul >> li >> a')
        return self

    def createStory(self):
        self.story = Story(self.title, self.author,
                           self.cover, configurator=self.config)
        return self

    def getChapters(self):
        self.chapterLinks = []
        self.chapterNames = []
        for chapter in self.chapters:
            link = 'https://www.wattpad.com' + chapter.get_attribute('href')
            name = chapter.query_selector('.part-title').text_content()
            if link not in self.chapterLinks:
                self.chapterLinks.append(link)
                self.chapterNames.append(name)
        return self

    def getParagraphs(self):
        content = []
        paragraphs = self.page.query_selector_all('pre >> p')
        # TESTING
        for paragraph in paragraphs:
            # TESTING
            comment = paragraph.query_selector('.num-comment')
            if comment:
                self.page.evaluate("(element) => element.remove()", comment)
            paragraph_text = paragraph.text_content()
            paragraph_text = self.sanitiseParagraph(paragraph_text)
            content.append(paragraph_text)
        return content

    def extractChapters(self):
        for chapter in self.chapterLinks:
            randomWait()
            self.page.goto(chapter)
            self.simulateRead()
            self.story.addChapter(
                self.chapterNames[self.chapterLinks.index(chapter)], self.getParagraphs())

    def simulateRead(self):
        for i in range(0, 8):
            self.page.evaluate(
                'window.scrollTo(0, document.body.scrollHeight)')
            wait(.2)

    def sanitiseParagraph(self, text):
        # remove the ' +' from the end of the string
        text = text.replace('  +', '')
        # remove the last character of the string
        text = text[:-1]
        # if the first character is a space or a tab, remove it
        try:
            if text[0] == ' ' or text[0] == '\t':
                text = text[1:]
        except:
            pass
        return text

    def port(self, url):
        self.warmup(url)
        self.getDetails()
        self.createStory()
        self.getChapters()
        self.extractChapters()
        press = Press(self.story, url, self.config)
        deliverable = press.deliverable
        # if self.admin:
        #     Archiver(self.story.title, self.story.author).archive()
        # # else:
        #     Deleter().delete()
        Deleter(config=self.config).delete()

        return deliverable
