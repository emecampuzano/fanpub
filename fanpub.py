import argparse
from Components.Sailor import Sailor
from playwright.sync_api import sync_playwright
from Config.Wizard import Wizard

def main(story_link):
    # Make sure everything's ready to run, baby
    Wizard().doctor()
    # Use story_link here
    with sync_playwright() as playwright:
        thief = Sailor(playwright)
        thief.port(story_link)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Your description here')
    parser.add_argument('story_link', type=str, help='The wattpad story link')
    args = parser.parse_args()
    main(args.story_link)