import os
from dotenv import load_dotenv
import streamlit as st
from ai_api import query_to_llm
from forvo_api import get_pronounciation
from tests import is_japanese

#Load .env
load_dotenv()

# Load API Key 
openai_api_key = os.environ['OPENAI_API_KEY']

# Load forvo api key
forvo_api_key = os.environ['FORVO_API_KEY']

# <-- DO NOT PLACE ANY STREAMLIT APPS BEFORE THIS LINE -->

st.set_page_config(page_title="日本語　例文 - Japanese Example Generator",
                   page_icon="🎌",
                   layout="wide")

headerbox = st.container()
querybox = st.container()
responsebox = st.container()
forvobox = st.empty()

headerbox.title("日本語　例文 - Japanese Example Sentence Generator")
headerbox.header("ようこそ　- Welcome to the Japanese Example Sentence Generator")
headerbox.write("Directions: Lorem ipsum dolor sit amet, ea cibo novum debitis per. Eam munere ancillae iracundia at. Quodsi fabulas duo an. Eu cum noluisse periculis erroribus, pro no essent maiorum, an appetere petentium imperdiet mei. Probo omittantur appellantur ea sit, mea iusto ceteros delicata an, ut vulputate repudiandae necessitatibus nec.")

with querybox:
    with st.form('Sentence Form', clear_on_submit=True):
        st.subheader(":red[Please enter the word or phrase for the desired example sentence:]")
        look_up_word = st.text_input(":red[Word or Phrase]")
        qty = st.selectbox(":red[Return # of examples]", options=list(range(1,6)), index=1)
        temperature = st.slider(":red[LLM Temperature (How deterministic or creative)]",0.0,1.0,.70,.10)
        submitted = st.form_submit_button(label="Submit")
    st.divider()

if submitted:
    try:
        is_japanese(look_up_word)
    except Exception as e:
        st.error(e)
        st.stop()
    with st.spinner("Query In Progress... 「待ってください。」"):
        query = query_to_llm(look_up_word,str(qty),temperature,openai_api_key)
        pronounciation = get_pronounciation(look_up_word)
    responsebox.header(f"Example Sentence Results for \"{look_up_word}\"")
    responsebox.markdown(query)
    responsebox.divider()
    forvobox.write(pronounciation, unsafe_allow_html=True)

