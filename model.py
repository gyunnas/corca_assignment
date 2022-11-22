import requests
from call_api import post_state
import json

def post_model(data, current_process, user_id):
    model_input = data[0]
    state = data[1]
    
    print(f"{state} state 모델링 시작/PID:", current_process.pid)
    res = requests.post('http://localhost:54468/model', json = model_input)
    model_output = json.loads(res.text)
    new_state = model_output['state']
    post_state(user_id, new_state)
    print(f"{state} state 모델링 끝/PID:", current_process.pid)
    return new_state