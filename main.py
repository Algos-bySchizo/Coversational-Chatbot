import os 
from typing import Literal
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START,END
from state import State
from listener import record_audio
from history import save_history, load_history
from speaker import speak
from transcriber import transcribe
from llm import generate

load_dotenv()

def get_input(state: State):

    if not state.get("messages"):
        messages = load_history()
        if not messages:
            messages = [{"role": "system", "content": "You are a helpful assistant. Be conversational and remember the chat history."}]
    else:
        messages = state["messages"]

    get_mode = input("how would you like to talk to the agent? Speech or Text (s/t), 'exit' to quit, 'clear' to reset history: ").lower()

    if get_mode=='exit':
        print("Goodbye...")
        return {"input_mode":"exit"}
    
    if get_mode == "clear":
        messages = [{"role": "system", "content": "You are a helpful assistant. Be conversational and remember the chat history."}]
        save_history(messages)
        print('History cleared!')
        return {"messages": messages, "input_mode": "clear"}

    input_mode = "speech" if get_mode =="s" else "text"
    return {"messages": messages, "input_mode": input_mode}

def handle_input(state: State):

    if state['input_mode']=="speech":
        path = record_audio()
        return {'audio_path':path}
    else:
        typed = input("You: ").strip()
        return {"transcription":typed}

def handle_transcribe(state: State):
    
    if state["input_mode"] == "speech":
        get_transcription = transcribe(state["audio_path"])
        return {"transcription":get_transcription}
    else:
        return {}
    
def handle_generate(state: State):

    transcription = state["transcription"]
    
    messages = load_history()
    if not messages:
        messages.append({"role":"assistant", "content":"you are a helpful assistant. Be conversational and remember the chat history."})
    
    messages.append({"role":"user", "content":transcription})

    response = generate(messages=messages)
    messages.append({"role":"assistant", "content":response})
    
    save_history(messages)
    
    return {"response": response}

def handle_output(state: State):
    
    response = state["response"]
    output_mode = input('\nDo you want me to type or speak the response for you?(s/t)').lower()

    if output_mode == "s":
        print(f"\n Assistant: {response}\n")    
        speak(response)
    else:
        print(f"\n Assistant: {response}\n")

    return {"output_mode":output_mode}

def should_continue(state: State) -> Literal["get_input", END]:

    if state['input_mode']=="exit":
        return END
    
    if state['input_mode']=="clear":
        return "get_input"

    return "handle_input"



workflow = StateGraph(State)

# Add nodes
workflow.add_node("get_input", get_input)
workflow.add_node("handle_input", handle_input)
workflow.add_node("handle_transcribe", handle_transcribe)
workflow.add_node("handle_generate", handle_generate)
workflow.add_node("handle_output", handle_output)

# add edges
workflow.add_edge(START, "get_input")

workflow.add_conditional_edges("get_input", should_continue, {
    "handle_input": "handle_input",  # normal flow
    "get_input": "get_input",        # clear — loop back
    END: END                         # exit — stop
})

# these four are simple — always go A to B, no conditions
workflow.add_edge("handle_input", "handle_transcribe")
workflow.add_edge("handle_transcribe", "handle_generate")
workflow.add_edge("handle_generate", "handle_output")
workflow.add_edge("handle_output", "get_input")

# Compile the graph
app = workflow.compile()

# Run the agent
if __name__ == "__main__":
    print("🎙️  SpeechAgent Started - Type 'exit' to quit, 'clear' to reset history\n")
    config = {"configurable": {"thread_id": "1"}}
    
    for event in app.stream({
        "messages": [],
        "input_mode" : "",
        "output_mode": "",
        "transcription":"",
        "response":"",
        "audio_path":"",
    }, config):
        pass

