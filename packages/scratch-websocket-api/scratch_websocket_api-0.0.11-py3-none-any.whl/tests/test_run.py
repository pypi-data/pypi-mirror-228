import random
import time

from src.scratch_api.scratch_ws_api import *
conn = login("yosshi---_Cloudvar", ".Cloudsession").connect(885712843, 2, True)  # https://scratch.mit.edu/projects/557792234
for _ in range(10):
    conn.send(["Sound1", "Subtitle"], [random.randint(1, 10), random.randint(1, 10)])
    time.sleep(0.1)