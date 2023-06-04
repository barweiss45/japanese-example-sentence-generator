import os
from dotenv import load_dotenv
from langchain.llms.loading import load_llm
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate

load_dotenv()

# Load API Key 
openai_api_key = os.environ['OPENAI_API_KEY']

# Load LLM from 'llm_config.jso' see 
# https://python.langchain.com/en/latest/modules/models/llms/examples/llm_serialization.html

llm = load_llm('llm_config.json')
llm.openai_api_key = openai_api_key

def prompt_template():
# Create Prompt Template --->>>
    template = """
    Please create {qty} sentences in modern conversational Japanese that include the word/phrase 「{look_up_word}」 based on the following instructions:

    I will provide a word or phrase, and you will create two realistic example sentences that may include verbs in either polite or dictionary forms. The sentences will be set in various everyday situations in modern Japan, such as at home, school, the store, a party, a restaurant, work between co-workers, on a date, a park, a train station, etc. Each sentence will be written in a way that can be understood by a student with proficiency at an N4 or N3 level and may include a proper Japanese first name or surname where appropriate. The sentences may be in a different tense, such as present, past, potential, te-form, subjective, or causative verb forms, and may be in either positive or negative form. The honorific or humble tense will not be used. The explanation will include an English translation and a very brief note about the tense and grammar points used. Absolutely do not include any Romanji transliteration.

    {format_instructions}

    The tone will be realistic and appropriate for a general audience. Thank you.
    """
    return template

def output_template():
    # Output Template --->>>

    # Schema for Output
    response_schemas = [
        ResponseSchema(name="sentence_1", description="This is the first example sentence."),
        ResponseSchema(name="sentence_1_explanation", description="This is the first example sentence explanation."),
        ResponseSchema(name="sentence_2", description="This is the second example sentence."),
        ResponseSchema(name="sentence_2_explanation", description="This is the second example sentence explanation.")
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas) # Build structure from schema
    # Build instructions for LLM
    format_instructions = output_parser.get_format_instructions()
    return format_instructions

def build_prompt():
    format_instructions = output_template()
    template = prompt_template()
    prompt = PromptTemplate(
        input_variables=["look_up_word","qty"],
        partial_variables={"format_instructions": format_instructions},
        template=template,
    )
    return prompt

def query_to_llm(word: str,quantity: str|int =2, temp: float =0.7, openai_api_key: str =openai_api_key) -> str: 
    prompt = build_prompt()
    prompt_value = prompt.format(look_up_word=word, qty=quantity) # keyword is 'word' which is defined in build_prompt()
    llm.openai_api_key = openai_api_key
    llm.temperature = temp
    llm_output = llm(prompt_value)
    return llm_output

def main():
    word = input('Welcome to the Example sentence creator\nPleae enter a word that you want for an example sentence: ')
    return print(query_to_llm(word,quantity=2,temp=0.7, openai_api_key=openai_api_key))

if __name__ == "__main__":
    main()
