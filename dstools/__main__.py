from dstools import dstools

"""
Example of dstools
"""

tool = dstools()

def test_func(x : int, y : str = "some")  -> int:
    """
    test
    """
    try:
        1+1
    except IndexError:
        pass
    
    try:
        return x + y
    except ValueError:
        print("INvalid value!")



result = tool.generateDocstring(test_func, replace_function=True)

