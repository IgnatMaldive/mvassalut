import openai
import streamlit as st
import time

assistant_id = "asst_AbMewO5VbfplaIO4wsX6M9KJ"
client = openai

# Initialize session state
st.session_state.setdefault("start_chat", False)
st.session_state.setdefault("thread_id", None)
st.session_state.setdefault("messages", [])
st.session_state.setdefault("openai_model", "gpt-4-1106-preview")

st.set_page_config(page_title="CatGPT", page_icon=":speech_balloon:")

openai.api_key = "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"

if st.sidebar.button("Start Chat"):
    st.session_state.start_chat = True
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

st.title("Mevasalut bot")
st.write("i make clinical hallucinations")

if st.button("Exit Chat"):
    st.session_state.messages = []  # Clear the chat history
    st.session_state.start_chat = False  # Reset the chat state
    st.session_state.thread_id = None

if st.session_state.get("start_chat", False):
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Escriu el teu missatge"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt
        )

        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            instructions="List the uploaded files and answer questions about them"
        )

        while run.status != 'completed':
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id
        )

        # Process and display assistant messages
        assistant_messages_for_run = [
            message for message in messages
            if message.run_id == run.id and message.role == "assistant"
        ]
        for message in assistant_messages_for_run:
            st.session_state.messages.append({"role": "assistant", "content": message.content[0].text.value})
            with st.chat_message("assistant"):
                st.markdown(message.content[0].text.value)

else:
    st.write("Click 'Start Chat' to begin.")
