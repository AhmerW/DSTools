from dstools import dstools
import sys

tool = dstools()

def func(x : int, y : str = "some")  -> int:
    """test
    ai
    """
    try:
        1+1
    except IndexError:
        pass
    
    try:
        return x + y
    except ValueError:
        print("INvalid value!")



result = tool.generateDocstrings()

#print(result)

print(tool.getDocstring(func))


#print(result)