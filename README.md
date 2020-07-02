# DSTools
 Docstring Tools - Generate and modify docstrings, easier than ever.

# Styling
 DSTools follows the Google Python Style Guide (https://google.github.io/styleguide/pyguide.html)


# How to use
 DSTools makes generating docstrings very easy.
 ```python
 import dstools
 tool = dstools() #initialize
 
 def func(x : int, y : str = 'test!') -> list:
    """Example function"""
    return [x, y]
     
  tool.generateDocstring(func, replace_function=True)
  
  #output:
  
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
