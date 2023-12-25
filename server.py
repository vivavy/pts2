import socket
import sys

from libpts import *


class Socket(socket.socket):
    def __del__(self):
        super().__del__()
        self.close()

    def sendall(self, __data, __flags=...):
        super().sendall(__data, __flags)
        print(">>>", __data)
        print()


class Request:
    cmd: str | bytes
    path: str | bytes
    proto: str | bytes
    headers: str | bytes
    data: str | bytes
    extra: str | bytes

    def __init__(self, **k):
        self.__dict__.update(k)


s = Socket(socket.AF_INET6, socket.SOCK_STREAM)

s.bind(("", 8001))


def parse_http(req_src: str | bytes):
    """GET / HTTP/1.1\r\nHost:www.example.com\r\n\r\n"""
    print(req_src)
    req_src = req_src.split(b"\r\n")
    cmd = req_src[0]
    req_path = req_src[1]
    proto = req_src[2]
    headers = req_src[3:][:-1]
    body = req_src[-1]
    cmd, req_path, proto = cmd.split()
    assert req_src[:4] != b"POST"
    return Request(cmd=cmd,
                   path=req_path,
                   proto=proto,
                   headers=headers,
                   data=body)

print("http://localhost:8001/task/0")

while True:
    s.listen(1)

    c, a = s.accept()

    req = c.recv(1024)
    
    if not req:
        continue

    if req.split()[0] == b"POST":
        print("POST", file=sys.stderr)
        path = list(req.split()[1].decode().split("/"))

        while "" in path:
            path.remove("")

        if path[0] == "check":
            task_id = eval(path[1])

        solution = req.split(b"&")[-1].decode()

        solution = eval("\"" + solution.removeprefix("code=").replace("%", "\\x").replace("+", " ") + "\"")

        check = compile_task(task_id, solution)

        print()
        print("\t" + solution.replace("\n", "\n\t"))

        result = True

        response = b"HTTP/1.0 200 OK\r\nVary: Accept-Encoding\r" + \
                   b"\nContent-Type: application/x-www-form-urlencoded; charset=utf-8\r\n\r\n" + (b"FAIL",
                                                                                                  b"OK")[result]

        print("   ", response, file=sys.stderr)

        c.sendall(response)

    elif req.split()[0] == b"GET":
        req = parse_http(req)

        path = req.path.decode().split("/")

        while "" in path:
            path.remove("")

        if path[0] == "task":
            task_id = eval(path[1])

        default = fread("web/task.html")

        meta = fread("tasks/" + str(task_id) + "/meta.pyi")
        
        name: str
        problem: str
        inputs: str
        example: list[object]

        exec(meta)

        task_name = name
        task_problem = problem
        task_inputs = inputs
        task_example = " ".join(tuple(repr(i) for i in example))
        task_output = " ".join(tuple(repr(i) for i in run_task(task_id)(*example)))

        response = default.replace("{task_name}", task_name). \
            replace("{task_problem}", task_problem). \
            replace("{task_inputs}", task_inputs). \
            replace("{task_example}", task_example). \
            replace("{task_output}", task_output). \
            replace("{task_id}", repr(task_id))

        c.sendall(b"HTTP/1.0 200 OK\r\nVary: Accept-Encoding\r"
                  b"\nContent-Type: text/html; charset=utf-8\r\n" + response.encode('utf-8'))

    del c

    print("DONE")
