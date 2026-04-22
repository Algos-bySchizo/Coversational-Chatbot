from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    
    messages: Annotated[list, add_messages]

    input_mode: str

    output_mode: str

    transcription: str

    response: str

    audio_path: str
