import time, ctypes
from call_api import get_feedback
from model import post_model
from multiprocessing import Process, Manager, freeze_support
import multiprocessing as mp

user_id = "test-user"

def repeat_get_feedback(q, state):
    while True:
        if not q.full():
            get_feedback(q, user_id, state[0])
            time.sleep(10)

def repeat_modeling(q, state):
    current_process = mp.current_process()
    
    while True:
        if not q.empty():
            new_state = post_model(q.get(), current_process, user_id)
            state[0] = new_state
        else:
            time.sleep(1)

if __name__ == '__main__':
    freeze_support()
    q = Manager().Queue()
    state = Manager().list()
    state.append(0) # 초기 state -> state[0]
    p1 = Process(target=repeat_get_feedback, args=(q,state))
    p1.start()
    
    procs = []
    for i in range(4):
        proc = Process(target=repeat_modeling, args=(q, state))
        procs.append(proc)
        proc.start()
    
    p1.join()
    for proc in procs:
        proc.join()
    
    