from flask import Flask, request, jsonify
from chat_model import *
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from flask_sqlalchemy import SQLAlchemy
from apikey import apikey

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/chat', methods=['POST'])
def chat():
    input = request.json['message']
    llm = ChatOpenAI(openai_api_key=apikey)
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                "You are a nice chatbot having a conversation with a human.{chat_history}"
                
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
    )
    # m = langchain_memory._create_chat_memory()
    memory = ConversationBufferMemory(
        # chat_memory=m, 
        memory_key="chat_history", 
        return_messages=True
    )

    conversation = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        memory=memory
    )
    answer = conversation.predict(question=input)
    memory.load_memory_variables({})
    return jsonify({"message": answer})


# @app.route('/add')
# def add():
#     chroma = langchain_memory._create_chroma_vector_store()
#     chroma.add_texts(texts=["doc1", "doc2", "doc3"])
#     return "Added texts"

# @app.route('/count')
# def count():
#     chroma = langchain_memory._create_chroma_vector_store()
#     return str(chroma._collection.count())
    
if __name__ == '__main__':

    app.run(debug=True)
