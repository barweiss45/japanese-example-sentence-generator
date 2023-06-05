#!/usr/bin/env python3

import os
from requests import get
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
import argparse
from streamlit.logger import get_logger

logger = get_logger(__name__)

load_dotenv()

# Load forvo api key
forvo_api_key = os.environ['FORVO_API_KEY']

def get_pronounciation(word_to_search):
    
    # Retrieve Jinja2 template to build HTML
    environment = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(enabled_extensions='html',
                                    default_for_string=True),
        lstrip_blocks=True,
        trim_blocks=True
        )
    template = environment.get_template('output.j2')

    country = 'Japan'
    
    # Values for Forvo API. See https://api.forvo.com/
    FORMAT = 'json'
    LANGUAGE = 'ja'
    ACTION = 'word-pronunciations'
    ORDER = 'rate-desc'  # pronunciations order by rate, high rated first
    HEADERS = {'Accept':'application/json'}

    try:
        URL = f'https://apifree.forvo.com/key/{forvo_api_key}/format/{FORMAT}/word/{word_to_search}/language/{LANGUAGE}/action/{ACTION}/order{ORDER}'
        response = get(URL, headers=HEADERS)
        logger.debug(f"Forvo HTTP Response Code: {response.status_code} {response.reason}\n")
    except Exception as e:
        logger.warning(e)
        return e

    output = response.json()['items']
    items_list = [index for index in output if country == index['country']]
    content = template.render({"word_to_search": word_to_search, "items_list":items_list})
    logger.debug(f"forvo_api.py content: {content}")    
    return content

def main(args):
    get_pronounciation(args.word_to_search)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve MP3 file from forvo.com")
    parser.add_argument('word_to_search', help='The word or phrase that you want to check to see if forvo has the MP3 for.')
    args = parser.parse_args()
    main(args)
