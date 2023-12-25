def fread(fp, mode="rt") -> str:
    with open(fp, mode) as f:
        return f.read()


def compile_task(task_id, solution: str):
    code1 = fread(f"tasks/{task_id}/solution.py"). \
           replace("from pts2 import *", fread("pts2.py"))
    code2 = solution.\
           replace("from pts2 import *", fread("pts2.py"))

    goin = [code1, code2]
    
    def _test_ok(*inputs):
        outputs = []
        code = goin[0]
        code = code.replace('"{IN}"', repr(list(inputs))[1:][:-1])
        exec(code)
        return outputs
    
    def _test_no(*inputs):
        outputs = []
        code = goin[1]
        code = code.replace('"{IN}"', repr(list(inputs))[1:][:-1])
        exec(code)
        return outputs
    
    return lambda inputs: _test_ok(*inputs) == _test_no(*inputs)


def run_task(task_id):
    code1 = fread(f"tasks/{task_id}/solution.py"). \
           replace("from pts2 import *", fread("pts2.py"))

    goin = [code1]
    
    def _test_ok(*inputs):
        outputs = []
        code = goin[0]
        code = code.replace('"{IN}"', repr(list(inputs))[1:][:-1])
        l = {}
        exec(code, l)
        return l["outputs"]
    
    return _test_ok
