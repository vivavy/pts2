inputs: list[object] = ["{IN}"]
outputs: list[object] = []

inputs.reverse()

def put(data) -> None: outputs.append(data)
def get() -> object: return inputs.pop()
