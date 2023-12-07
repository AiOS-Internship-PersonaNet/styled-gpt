import os
from flask_restful import Resource, reqparse, Api
from flask import Flask, request, jsonify, session, stream_with_context, request, Response

from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

from langchain.schema import SystemMessage
from apikey import apikey

app = Flask(__name__)

@app.route('/')
def hello_world():
    
    return "<p>Hello, World!</p>"

template = """You are a chatbot having a conversation with a human.

{chat_history}
Human: {human_input}
Chatbot:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"], template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")
llm = OpenAI(openai_api_key=apikey)
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
    memory=memory,
)
parser = reqparse.RequestParser()
parser.add_argument('query', type=str, required=True, location='json', help="Input cannot be blank!")

@app.route('/chain', methods=['POST'])
def chain_route():
    args = parser.parse_args()
    user_input = args['query']
    
    def generate():
        for chunk in llm_chain.run(user_input):
            yield (chunk)
    #return stream_with_context(llm_chain.run(user_input))
    return stream_with_context(generate())


if __name__ == '__main__':
    app.run(debug=True)
