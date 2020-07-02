import inspect
import sys
import typing
import ast
import astunparse
import re
from collections.abc import Iterable


class dstools(object):
    def __init__(self, filename: str = None):
        if filename is None:
            filename = sys.argv[0]

        self.filename = filename
        self.callables = []

    def __str__(self) -> str:
        """Returns a string representation of -self-"""
        return "{}".format(self)

    def __repr__(self) -> str:
        """Returns a redirect to __str__"""
        return self.__str__()



    def getFuncs(self):
        try:
            with open(self.filename, 'rt') as file_data:
                return ast.parse(file_data.read(), filename=self.filename)
        except FileNotFoundError as e:
            raise FileNotFoundError("<File {0} was not found! Error while getting the docstrings of {0}>".format(self.filename)) \
                from e

    def getDocstrings(self, funcs : typing.Sequence[typing.Callable] = None) -> dict:

        if funcs is None:
            self.funcs = self.getFuncs()
            self.callables = [
                func for func in self.funcs.body if isinstance(func, ast.FunctionDef)]

            return {func.name: ast.get_docstring(func) for func in self.callables}
        

        if isinstance(funcs, Iterable) and all([callable(func) for func in funcs]):
            return {func.__name__:func.__doc__ for func in funcs if hasattr(func, '__name__') and hasattr(func, '__doc__')}
        
    def getDocstring(self, func : typing.Callable) -> dict:
        if callable(func):
            if hasattr(func, '__name__') and hasattr(func, '__doc__'):
                return {func.__name__:func.__doc__}

    def generateDocstring(self, func, replace_function = False):
        if not callable(func):
            raise ValueError("Invalid callable. Please pass in a function or method.")
        rtype= None
        raises= []


        previous_doc = func.__doc__

        # inspection
        signature= inspect.signature(func)
        src= inspect.getsource(func)
        details= inspect.getfullargspec(func)

        args= details.args
        annotations= details.annotations

        defaults=  {
            k: v.default
            for k, v in signature.parameters.items()
            if v.default is not inspect.Parameter.empty
        }

        # paramters
        all_param = ""
        

        
        raises = self.get_exceptions(src)
        
        
        # get all arguments
        for i in range(len(args)):
            arg = args[i]
            if arg in annotations:
                obj_type = annotations[arg]
            else:
                obj_type = type(arg)
                
                
            cleaned_type = str(obj_type).split()[-1][1:-2]
            if i == 0:
                final = f"{arg} ({cleaned_type}): \n"
            else:
                final =  f"        {arg} ({cleaned_type}): \n"
                
            if arg in defaults:
                final = final.replace('):', f', optional): Defaults to {defaults[arg]}')
            all_param += final

        _rypte_split = src.split('\n')[0]
        if('->' in _rypte_split):
            rtype = _rypte_split.split('->')[1].replace(':', '').strip()
        else:
            pass

        

        new_doc = \
        f""" 
    Function {func.__name__}

    Args:
        {all_param} 

    Returns:
        {rtype}:
        
    Raises:
        {raises}
    """
        

        if replace_function:    
            return src.replace(previous_doc, new_doc)
        return f"    \"\"\"{new_doc}\"\"\""
  
    def get_exceptions(self, text):
        _found = []
        raises = ""
        for line in text.split('\n'):
            if 'except' in (line):
                to_add = line.strip().replace('except', '')+"\n"
                if to_add in _found:
                    continue
                if not _found:
                    raises += to_add
                else:
                    raises += f"        {to_add}"
                _found.append(to_add)    
        if raises == "":
            raises = None
        return raises

    def _get_args(self, text):
        """
        Function get_args -> returns a list with all the 
        necessary information about the function's parameters

        args
            text -> text to inspect
        returns:
            list (dict, return_type) -> The information
        raises:
            None

        Example of return:
        input: 'def test(x : str, y : int = 5) -> list'
        returns: [{'x': ['str', None], 'y': ['int', 5]}, 'list']
        """
        result = {}
        line = str(text).split('(')[1].split(',')
        if '->' in line[-1]:
            splitted = line[-1].split('->')
            return_type = splitted[-1].strip()
            line[-1] = splitted[0].replace(')', '').strip()
        else:
            return_type = None
        for arg in line:
            arg_splitted = arg.split()
            _list = [None, None]
            if '=' in arg:
                arg_eq = arg.split('=')
                
                _list[1] = arg_eq[-1].replace("'", "").strip()
            if len(arg_splitted) == 2:
                _type = arg_splitted[1].split("=")[0]
            else:
                _type = 'str'
            _list[0] = _type
            if len(arg_splitted) == 3:
                _list[0] = arg_splitted[-1]
            elif len(arg_splitted) == 5:
                _list[0] = arg_splitted[2]
            arg = arg_splitted[0].replace(':', '').split('=')[0]

            if _list[0] != None:
                if '=' in _list[0]:
                    _list[0] = _list[0].split('=')[0]
                
            if ':' in return_type:
                return_type = return_type.split(':')[0]
                
            result[arg] = _list
        return (result, return_type)
    
    def generateDocstrings(self, replace_function=False, to_file=False):
        self.funcs = self.getFuncs()
        final = ""


        for func in self.funcs.body:
            if isinstance(func, ast.FunctionDef):
                previous_doc = ast.get_docstring(func)
                src = astunparse.unparse(ast.parse(func))
                
                data, return_type = self._get_args(src)
                raises = self.get_exceptions(src)

                
                i = 0
                all_param = ""
                f = ""
                
                for arg, _type in data.items():
                    _rtype = _type[0]
                    optional = _type[1]
                    if i == 0:
                        f = f"{arg} ({_rtype}): \n"
                    else:
                        f =  f"        {arg} ({_rtype}): \n"
                    if optional != None:
                        f = f.replace('):', f', optional): Defaults to {optional}')
                    
                    all_param += f
                    i = 1
                if all_param == '':
                    all_param = None
                new_doc = \
                f""" 
    Function {func.name}

    Args:
        {all_param}

    Returns:
        {return_type}:
            
    Raises:
        {raises}
    """
                if replace_function:
                    final += src.replace(previous_doc, new_doc)
        
                final += f"    \"\"\"{new_doc}\"\"\""
        if to_file:
            try:
                with open(to_file, "a") as f:
                    f.write(to_file)
            except FileNotFoundError:
                raise FileNotFoundError(f"File {to_file} was not found!")
        return final

