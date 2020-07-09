# DSTools
 Docstring Tools - Generate and modify docstrings

# Styling
 DSTools follows the Google Python Style Guide (https://google.github.io/styleguide/pyguide.html)


# How to use
 DSTools makes generating docstrings very easy.
 ```python
 import dstools
 tool = dstools.dstools() #initialize
  
  #Original function:
  def func(x : int, y : str = 'test!') -> list:
    """Example function"""
    return [x, y]
     
  result = tool.generateDocstring(func, replace_function=True) #generate a single docstring
  print(result)
  
  #Function after generating a docstring 
  def func(x : int, y : str = 'test!') -> list:
    """
    Function func

    Args:
        x (int):
        y (str, optional): Defaults to test!


    Returns:
        list:

    Raises:
        None
    """
    return [x, y]
   
 ```
 
 You can also replace all the functions in a file.
 By default the file will be the current file, if you wish to change it you need to pass in a filename argument in the constructor method.
 
 ```python
 #Generating multiple docstrings 
 from dstools import dstools
 
 tool = dstools(filename="test.py") #by default the filename will be the current file.
 tool.generateDocstrings(to_file="output.py") #saves the output to a file called output.py
 
 #boom, it's that easy!
 ```
