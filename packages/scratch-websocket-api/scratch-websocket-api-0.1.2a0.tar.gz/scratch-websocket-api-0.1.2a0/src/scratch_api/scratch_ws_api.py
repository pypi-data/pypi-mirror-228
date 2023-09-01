import json
import re
import ssl

import requests
import websocket


class User:
    def __init__(self, username, session_id):
        self.username = username
        self.session_id = session_id

    def connect(self, project_id, max_connections, is_scratch=None):
        if project_id is str:
            project_id = int(project_id)
        connections = []
        if is_scratch is None or is_scratch is True:
            host = "wss://clouddata.scratch.mit.edu"

        elif isinstance(is_scratch, str) and is_scratch is not False:
            host = is_scratch
        else:
            host = "wss://clouddata.turbowarp.org/"

        for _ in range(max_connections):
            connection = websocket.WebSocket()
            if is_scratch is True or is_scratch is None:
                connection.connect(
                    "wss://clouddata.scratch.mit.edu",
                    cookie="scratchsessionsid=" + self.session_id + ";",
                    origin="https://scratch.mit.edu",
                    enable_multithread=True,
                )

            else:
                connection.connect(
                    host,
                    enable_multithread=True,
                )
                connection.send(
                    json.dumps({"method": "handshake", "user": self.username, "project_id": project_id}) + "\n")
            connections.append(connection)

        return Cloud(project_id, self.username, self.session_id, connections, host)


class Cloud:
    def __init__(self, project_id, username, session_id, conns: list[websocket.WebSocket], host):
        self.projectId = project_id
        self.username = username
        self.sessionId = session_id
        self.connections = conns
        self.hostUrl = host

    def send(self, var_name: list, value: list):
        if not isinstance(var_name, list): raise TypeError(
            "The argument 'var_name' can use only list.（型の不一致:引数var_nameにはlist型のみ使用できます）")
        if not isinstance(value, list): raise TypeError(
            "The argument 'value' can use only list. （型の不一致:引数valueにはlist型のみ使用できます）")
        length = len(var_name)
        if length > len(value):
            length = len(value)
        if length >= len(self.connections):
            length = len(self.connections)

        for index in range(length):
            data = json.dumps(
                {
                    "method": "set",
                    "name": "☁ " + var_name[index],
                    "value": str(value[index]),
                    "user": self.username,
                    "project_id": self.projectId,
                }
            )
            try:
                self.connections[index].send(data + "\n")
            except (websocket._exceptions.WebSocketBadStatusException, ssl.SSLEOFError):
                if self.hostUrl == "wss://clouddata.scratch.mit.edu":
                    self.connections[index].connect(
                        "wss://clouddata.scratch.mit.edu",
                        cookie="scratchsessionsid=" + self.sessionId + ";",
                        origin="https://scratch.mit.edu",
                        enable_multithread=True,
                    )
                else:
                    self.connections[index].connect(
                        self.hostUrl,
                        enable_multithread=True,
                    )

    def get(self, var_name: list[str], limit: str = "1000"):
        result = []

        for i in range(len(var_name)):
            result.append(None)

            var_name[i] = var_name[i].replace("☁ ", "")
            var_name[i] = var_name[i].replace("☁", "")
            var_name[i] = "☁ " + var_name[i]
        try:
            resp = requests.get("https://clouddata.scratch.mit.edu/logs?projectid=" +
                                str(self.projectId) + "&limit=" + str(limit) + "&offset=0").json()
            for i in resp:
                x: str = i['name']
                if (x in var_name) and (result[var_name.index(x)] is None):
                    result[var_name.index(x)] = i['value']
                if None not in result:
                    return result
        except Exception:
            raise Exception('Cloud variable could not be read.')
        return result

    def close(self):
        for index in range(len(self.connections)):
            self.connections[index].close()


def login(username, password):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        "x-csrftoken": "a",
        "x-requested-with": "XMLHttpRequest",
        "referer": "https://scratch.mit.edu",
    }
    data = json.dumps({"username": username, "password": password})
    headers["Cookie"] = "scratchcsrftoken=a;scratchlanguage=en;"
    request = requests.post(
        "https://scratch.mit.edu/login/", data=data, headers=headers
    )
    return User(username, str(re.search('"(.*)"', request.headers["Set-Cookie"]).group()))  # ユーザー名とセッションIDを返す
