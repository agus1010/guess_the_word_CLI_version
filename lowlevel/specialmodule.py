import importlib
import sys
import types



class SpecialModule(types.ModuleType):
    """ Customization of a module that is able to dynamically loads submodules.
    
    It is expected to be a plain package (and to be declared in the __init__.py)
    The special attribute is a dictionary attribute name -> relative module name.
    The first time a name is requested, the corresponding module is loaded, and 
    the attribute is binded into the package
    """

    special = {"SpecialModule":".specialmodule.SpecialModule", "import_names":".specialmodule.import_names"}

    def __getattr__(self, name):
        if name in self.special:
            m = importlib.import_module(self.special[name], __name__) # import submodule
            o = getattr(m, name)                      # find the required member
            setattr(sys.modules[__name__], name, o)   # bind it into the package
            return o
        else:
            raise AttributeError(f'module {__name__} has no attribute {name}')



def import_names(special_module:type):
    sys.modules[__name__].__class__ = special_module       # customize the class of the package
