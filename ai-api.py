import os
from dotenv import load_dotenv
from forvo_api import get_pronounciation
from langchain.llms import OpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate

load_dotenv('.env')

openai_api_key = os.getenv('openai_api_key')

llm = OpenAI(model_name="text-davinci-003", openai_api_key=openai_api_key)

template = """
Please create two sentences in modern conversational Japanese that include the word/phrase 「{look_up_word}」 based on the following instructions:

I will provide a word or phrase, and you will create two realistic example sentences that may include verbs in either polite or dictionary forms. The sentences will be set in various everyday situations in modern Japan, such as at home, school, the store, a party, a restaurant, work between co-workers, on a date, a park, a train station, etc. Each sentence will be written in a way that can be understood by a student with proficiency at an N4 or N3 level and may include a proper Japanese first name or surname where appropriate. The sentences may be in a different tense, such as present, past, potential, te-form, subjective, or causative verb forms, and may be in either positive or negative form. The honorific or humble tense will not be used. The explanation will include an English translation and a very brief note about the tense and grammar points used. Absolutely do not include any Romanji transliteration.

{format_instructions}

The tone will be realistic and appropriate for a general audience. Thank you.
"""

response_schemas = [
    ResponseSchema(name="sentence_1", description="This is the first example sentence."),
    ResponseSchema(name="sentence_1_explanation", description="This is the first example sentence explanation."),
    ResponseSchema(name="sentence_2", description="This is the second example sentence."),
    ResponseSchema(name="sentence_2_explanation", description="This is the second example sentence explanation.")
]

# How you would like to parse your output
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# See the prompt template you created for formatting
format_instructions = output_parser.get_format_instructions()
print (format_instructions)

# %%
prompt = PromptTemplate(
    input_variables=["look_up_word"],
    partial_variables={"format_instructions": format_instructions},
    template=template,
)

get_pronounciation(word)

promptValue = prompt.format(look_up_word=word) # keyword is 'word' which is defined in PromptTemplate Class

print (f"Final Prompt: {promptValue}")
print ("-----------")
llm_output = llm(promptValue)
print (f"LLM Output: {llm_output}")


# %%
import re
import json

cleaned_output = re.sub(r'```json|```|\n|\t', '', llm_output)

response_dict = json.loads(cleaned_output)

for key, value in response_dict.items():
    print(f"This is {key} -> {value}.")

# %% [markdown]
# ## Output of Forvo of Pronounciation

# %%
from IPython.display import display, HTML

with open('output.html', 'r') as f:
    html_string = f.read()

display(HTML(html_string))

# %%



