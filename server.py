import socket
from libpts import *


class Socket(socket.socket):
    def __del__(self):
        super().__del__()
        self.close()


class Request:
    cmd: str|bytes
    path: str|bytes
    proto: str|bytes
    headers: str|bytes
    data: str|bytes
    extra: str|bytes
    def __init__(self, **k):
        self.__dict__.update(k)


s = Socket(socket.AF_INET6, socket.SOCK_STREAM)

s.bind(("", 8001))

def ParseInputs(ins: str):
    return ins.replace("%%i", "integers").\
        replace("%%f", "floats").\
        replace("%%s", "strings").\
        replace("%%l", "list of").\
        replace("*", " zero and more<br>").\
        replace("+", " one and more<br>").\
        replace(":}", " - &infin;<br>").\
        replace(":", " - ").\
        replace("{", " ").\
        replace("}", "<br>").\
        replace("?", " zero or one")

def ParseHttp(req: str|bytes):
    """GET / HTTP/1.1\r\nHost:www.example.com\r\n\r\n"""
    print(req)
    req = req.split(b"\r\n")
    cmd = req[0]
    path = req[1]
    proto = req[2]
    headers = req[3:][:-1]
    body = req[-1]
    cmd, path, proto = cmd.split()
    assert req[:4] != b"POST"
    return Request(cmd=cmd,
                   path=path,
                   proto=proto,
                   headers=headers,
                   data=body)

while True:
    s.listen(1)

    c, a = s.accept()

    try:
        req = ParseHttp(req:=c.recv(1024))
    except:
        pass
    
    if type(req) == bytes and req[:4] == b"POST":
        path = req.split()[1].split("/")
        
        while b"" in path:
            path.remove(b"")
        
        if path[0] == "check":
            task_id = eval(path[1])
        
        solution = req.split("&")[-1].decode()
        
        solution = eval("\""+solution.removeprefix("code=").replace("%", "\\x").replace("+", " ")+"\"")
        
        check = compile_task(task_id, solution)
        
        print()
        print("\t" + solution.replace("\n", "\n\t"))
        
        result = True
        
        ...
        
        c.sendall(b"HTTP/1.0 200 OK\r\nVary: Accept-Encoding\r"
                  b"\nContent-Type: text/plain; charset=utf-8\r\n"+(b"FAIL",b"OK")[result])
    
    elif req.cmd == b"GET":
        path = req.path.decode().split("/")
        
        while "" in path:
            path.remove("")
        
        if path[0] == "task":
            task_id = eval(path[1])
        
        default = fread("web/task.html")
        
        meta = fread("tasks/" + str(task_id) + "/meta.pyi")
        
        exec(meta)
        
        task_name = name
        task_problem = problem
        task_inputs = ParseInputs(inputs)
        task_example = " ".join(tuple(repr(i) for i in example))
        task_output = " ".join(tuple(repr(i) for i in run_task(task_id)(*example)))
        
        responce = default.replace("{task_name}", task_name).\
            replace("{task_problem}", task_problem).\
                replace("{task_inputs}", task_inputs).\
                    replace("{task_example}", task_example).\
                        replace("{task_output}", task_output).\
                            replace("{task_id}", repr(task_id))
        
        c.sendall(b"HTTP/1.0 200 OK\r\nVary: Accept-Encoding\r"
                  b"\nContent-Type: text/html; charset=utf-8\r\n"+responce.encode('utf-8'))
        
    del c
    
    print("DONE")