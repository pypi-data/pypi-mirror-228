import random
import time

from src.scratch_api.scratch_ws_api import login
conn = login("yosshi---_Cloudvar", ".Cloudsession").connect(846708650, 2, True)  # https://scratch.mit.edu/projects/846708650
conn.send(["1", "2"], [random.randint(1, 10), random.randint(1, 10)])
print(conn.get(["1","2"]))