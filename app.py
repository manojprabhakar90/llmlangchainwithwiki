import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain,SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

def get_api_key():
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

st.title('🦜🔗 Youtube GPT Creator')
prompt = st.text_input('Plug in your prompt here')

titletemplate = PromptTemplate(
	input_variables = ['topic'],
	template = 'Write me a Youtube video title about {topic}')


scripttemplate = PromptTemplate(
	input_variables = ['title','wikipedia_research'],
	template = 'Write me a Youtube script title based on this TITLE: {title} while leveraging this wikipedia research: {wikipedia_research}')

titlememory = ConversationBufferMemory(input_key='topic',memory_key='chat_history')
scriptmemory = ConversationBufferMemory(input_key='title',memory_key='chat_history')

llm=OpenAI(temperature = 0.9)
title_chain = LLMchain(llm = llm, prompt = titletemplate,verbose=True,output_key='title',memory=titlememory)
script_chain = LLMchain(llm = llm, prompt = scripttemplate,verbose=True,output_key='script',memory=scriptmemory)

wiki = WikipediaAPIWrapper()

if prompt:
	title = title_chain.run(prompt)
	wiki_research = wiki.run(prompt)
	script = script_chain.run(title=title,wikipedia_research=wiki_research)

	st.write(response['title'])
	st.write(response['script'])
	with st.expander('Title History'):
		st.info(titlememory.buffer)
	with st.expander('Title History'):
		st.info(scriptmemory.buffer)
	with st.expander('Wikipedia Research'):
		st.info(wiki_research)
