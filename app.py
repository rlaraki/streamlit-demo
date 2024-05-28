import os
import streamlit as st
#from IPython.display import Image, display
import autogen
from autogen.coding import LocalCommandLineCodeExecutor
from dotenv import load_dotenv

st.title("💻 Multi-Agent Code Assistant")
st.write("""Let’s see how to use agents to write a python script and execute the script. 
This process involves the collaboration of:
* An AssistantAgent to serve as the assistant: It is an LLM-based agent that can write Python code (in a Python coding block) for a user to execute for a given task. UserProxyAgent 
* A UserProxyAgent that acts as a proxy for the human user. It is thus an agent which serves to execute the code written by AssistantAgent, or automatically execute the code""")
load_dotenv('/Users/rayanelaraki/Desktop/Demo AI LEAD/credentials.env')


base_url = os.getenv("BASE_URL")
# When using a single openai endpoint, you can use the following:
config_list = [{"model": "gpt-4-32k-deployment", "api_key": os.getenv("OPENAI_API_KEY"), "base_url": base_url,
        "api_type": "azure", 'api_version': '2024-02-15-preview'}]

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "cache_seed": 41,  # seed for caching and reproducibility
        "config_list": config_list,  # a list of OpenAI API configurations
        "temperature": 0,  # temperature for sampling
    },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        # the executor to run the generated code
        "executor": LocalCommandLineCodeExecutor(work_dir="coding"),
    },
)
# the assistant receives a message from the user_proxy, which contains the task description

user_input = st.text_input("Enter your prompt:")

dict_conv = {'assistant': 'User Proxy -> Assistant', 'user': 'Assistant -> User Proxy'}
first_session_chat = 0

if st.button("Generate Text"):
    # Use AutoGen agent to generate text based on user input
    
    chat_res = user_proxy.initiate_chat(
    assistant,
    message=user_input,
    summary_method="reflection_with_llm",
)
    first_session_chat = len(chat_res.chat_history)
    #st.write("Generated Text")
    for i in range(first_session_chat):
        st.write(f"Direction: {dict_conv[chat_res.chat_history[i]['role']]}")
        st.write(f"Response: {chat_res.chat_history[i]['content']}")



