import os
from flask_restful import Resource, reqparse, Api
from flask import Flask, request, jsonify, session, stream_with_context, render_template, Response

from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.callbacks import StdOutCallbackHandler
from langchain.schema import SystemMessage

from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def hello_world():
    return render_template('index.html')

template = """You are a chatbot having a conversation with a human.

{chat_history}
Human: {human_input}
Chatbot:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"], template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")

handler = StdOutCallbackHandler()
llm = OpenAI(openai_api_key="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", streaming=True, max_tokens=-1)
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    callbacks=[handler],
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
            yield chunk
    return Response(generate(), mimetype='text/event-stream')
    # return stream_with_context(generate())


@app.route('/stream', methods=['POST'])
def stream_data():
    args = parser.parse_args()
    user_input = args['query']
    def generate():
        for chunk in llm.stream(user_input):
            yield chunk
    return Response(generate(), mimetype='text/event-stream')

@socketio.on('start_stream')
def handle_start_stream():
    for chunk in stream_data():
        emit('stream_data', {'data': chunk})

if __name__ == '__main__':
    app.run(debug=True)
