import json

def get_interview_data(path):
    with open(path) as f:
        data = json.load(f)

    return data