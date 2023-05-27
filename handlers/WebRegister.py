from typing import Union

WebStore = {}

def WebRegister(Path):
    def wrapper(f): 
        WebStore[Path] = f
        return f
    return wrapper