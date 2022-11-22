import requests
import json

def get_feedback(q, user_id, state):
    res = requests.get('http://assignment-api.corca.ai:6000/feedback', params = {"user_id":user_id})
    feedback = json.loads(res.text)
    model_input = {}

    for item in feedback:
        del(item["CreatedAt"])
        del(item["UpdatedAt"])
        del(item["DeletedAt"])
        del(item["user"])
        
    model_input["state"] = state
    model_input["feedbacks"] = feedback
    
    if q.qsize()>1:
        return
    q.put([model_input, state])
    print('{0} 에 대한 피드백'.format(state))
    

def post_state(user_id, state):
    requests.post('http://assignment-api.corca.ai:6000/state', json = {"value": state,"user_id": user_id})
