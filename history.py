import os, json

FILE_PATH = "convo_history.json"

def load_history():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, 'r') as f:
        content = f.read()
        if not content.strip():
            return []
    return json.loads(content)

def save_history(messages):

    with open(FILE_PATH, "w") as f:
        json.dump(messages, f, indent=2)