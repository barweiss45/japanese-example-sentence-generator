import os
from textwrap import dedent
from dotenv import load_dotenv
import streamlit as st
from streamlit.logger import get_logger
from ai_api import query_to_chat
from forvo_api import get_pronounciation
from tests import is_japanese

logger = get_logger(__name__)

#Load .env
load_dotenv()

# Load API Key 
openai_api_key = os.environ['OPENAI_API_KEY']

# Load forvo api key
forvo_api_key = os.environ['FORVO_API_KEY']

# <-- DO NOT PLACE ANY STREAMLIT APPS BEFORE THIS LINE -->

st.set_page_config(page_title="日本語 例文 - Japanese Example Generator",
                   page_icon="🎌",
                   layout="wide")

headerbox = st.container()
querybox = st.container()
responseheader = st.container()
responsebox = st.empty()
forvodivider = st.container()
forvobox = st.empty()

headerbox.title("日本語の例文 - Japanese Example Sentence Generator")
headerbox.header("ようこそ - Welcome to the Japanese Example Sentence Generator")
headerbox.write(dedent("""\
Welcome to your Japanese Example Sentence Generator. This app is designed to assist you in crafting sentences
that fit within various everyday situations set in modern Japan:\n\n

1. Input your desired word or phrase in Kanji(漢字), Katakana(カタカナ), or Hiragana(ひらがな).\n
2. Choose to generate up to five sentences.\n
3. Adjust the temperature slider (scale: 0.1 - 1.0) to control creativity. Lower values (0.1) result in less creativity, and higher values (1.0) result in more.\n
4. Note that the generated sentences may contain inaccuracies in grammar, word choice, and etc. Remember this is AI generated so be sure to check the sentences before using.\n\n
\n\n
Enjoy!"""))

with querybox:
    with st.form('Sentence Form', clear_on_submit=True):
        st.subheader(":red[Please enter the word or phrase for the desired example sentence:]\n例文のための単語やフレーズを入力してください。")
        look_up_word = st.text_input(":red[Word or Phrase]")
        qty = st.selectbox(":red[Return # of examples]", options=list(range(1,6)), index=1)
        temperature = st.slider(":red[LLM Temperature (How deterministic or creative)]",0.0,1.0,.70,.10)
        submitted = st.form_submit_button(label="Submit")
    st.divider()

if submitted:
    responseheader.header(f"Example Sentence Results for \"{look_up_word}\"")

    # Validate that word is a in Japanese Characters
    try:
        is_japanese(look_up_word)
    except Exception as e:
        st.error(e)
        logger.warn(e)
        st.stop()
    
    #Start Query
    with st.spinner(f"ChatGPT is working on creating an example sentence for {look_up_word}. Please be patient... 「待ってください。」"):
        query = query_to_chat(look_up_word,
                              str(qty),
                              temperature,
                              openai_api_key
                              )
        pronounciation = get_pronounciation(look_up_word)
    responsebox.markdown(query)
    forvodivider.divider()
    forvobox.write(pronounciation, unsafe_allow_html=True)
