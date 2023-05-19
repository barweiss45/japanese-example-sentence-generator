#!/usr/bin/env python3

from requests import get
from dotenv import  get_key
from jinja2 import Environment, FileSystemLoader, select_autoescape
import argparse

def get_pronounciation(word_to_search):
    environment = Environment(
        loader=FileSystemLoader('templates'),
        autoescape=select_autoescape(enabled_extensions='html',
                                    default_for_string=True),
        lstrip_blocks=True,
        trim_blocks=True
        )
    template = environment.get_template('output.j2')
    forvo_api_key = get_key('../.env', 'forvo_api_key')

    country = 'Japan'

    FORMAT = 'json'
    LANGUAGE = 'ja'
    ACTION = 'word-pronunciations'
    ORDER = 'rate-desc'  # pronunciations order by rate, high rated first
    HEADERS = {'Accept':'application/json'}

    URL = f'https://apifree.forvo.com/key/{forvo_api_key}/format/{FORMAT}/word/{word_to_search}/language/{LANGUAGE}/action/{ACTION}/order{ORDER}'

    response = get(URL, headers=HEADERS)

    # print(f"HTTP Response Code: {response.status_code} {response.reason}\n")
    output = response.json()['items']

    items_list = [index for index in output if country == index['country']]
    content = template.render({"word_to_search": word_to_search, "items_list":items_list})
    
    # creat json file for tshoot purposes.
    # with open(f'forvo_{word_to_search}.json', 'w', encoding='UTF-8') as file:
    #     print(json.dumps(items_list, indent=4), file=file)

    with open(f'output.html', 'w', encoding='UTF-8') as file:
        print(content, file=file)

def main(args):
    get_pronounciation(args.word_to_search)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve MP3 file from forvo.com")
    parser.add_argument('word_to_search', help='The word or phrase that you want to check to see if forvo has the MP3 for.')
    args = parser.parse_args()
    main(args)
