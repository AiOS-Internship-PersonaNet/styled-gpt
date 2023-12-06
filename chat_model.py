from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatAnthropic
from apikey import apikey

def chat_model(input):
    llm = ChatOpenAI(openai_api_key=apikey)
    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(
                "You are a nice chatbot having a conversation with a human."
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
    conversation.predict(question="Hi there!")
    print(conversation.predict(question="what did I just say"))
    
   
    # for chunk in conversation.stream({"question": input}):
    #     print(chunk, end="", flush=True)
    # print("\n")
    # for ele in history:
    #     print("key: {}".format(history["text"]))
chat_model("hi")
