import ast
import inspect
import sys
from collections import namedtuple


class ParamType:
    pass


def get_repr_code(basename, params: list[str]):
    txt = f"def __repr_{basename}__(self) -> str:\n\treturn f'{basename}("
    paramstrs = []
    for name in params:
        paramstrs.append("{repr(self." + name + ")}")
    txt += f"{', '.join(paramstrs)})'\n"
    return txt

def get_init_code(params: list[str], initfields: list[str], defaults: dict[str, str]) -> str:
    paramstrs = []
    for name in params:
        if name in defaults:
            paramstrs.append(f" {name}={defaults[name]}")
        else:
            paramstrs.append(f" {name}=None")

    if len(paramstrs) > 0:
        txt = f"def __init__(self,{','.join(paramstrs)}):\n"
    else:
        txt = f"def __init__(self):\n"
    for name in params:
        txt += f"\tself.{name}={name}\n"
    
    for name in initfields:
        if name in defaults:
            txt += f"\tself.{name}={defaults[name]}\n"
        else:
            txt += f"\tself.{name}=None\n"    
    # TODO: Maybe generate super().__init__() call    
    return txt


ClsFieldTuple = namedtuple("ClsFieldTuple", "seen_vars, defaults, params, initfields")
def lift_fields(tree) -> ClsFieldTuple:
    seen_vars = set([])
    defaults = {}
    params = []
    initfields = []

    # (TODO: Handle stuff like a = b (inject self.))
    for b in tree.body:
        for bod in b.body:
            match type(bod):
                case ast.Assign:
                    seen_vars.add(bod.targets[0].id)
                    if hasattr(bod, "value") and bod.value is not None:
                        defaults[bod.targets[0].id] = ast.unparse(bod.value)
                    initfields.append(bod.targets[0].id)
                case ast.AnnAssign:
                    seen_vars.add(bod.target.id)
                    if hasattr(bod, "value") and bod.value is not None:
                        defaults[bod.target.id] = ast.unparse(bod.value)

                    tnames = [x.strip() for x in ast.unparse(bod.annotation).split("|")]
                    if "ParamType" in tnames:
                        params.append(bod.target.id)
                    else:
                        initfields.append(bod.target.id)
                case _:
                    pass
    return ClsFieldTuple(seen_vars, defaults, params, initfields)

def memclass(cls):
    globals = sys.modules[cls.__module__].__dict__

    class_source = inspect.getsource(cls)
    class_source = class_source.replace("@memclass", "").strip()
    class_ast = ast.parse(class_source)

    # grab all the fields
    fielddata = lift_fields(class_ast)
    
    # handle inheritance, inject params from parents into constructor
    parent_params = []
    parent_param_defaults = {}
    parent_initfields = []
    for x in cls.__mro__[-2:0:-1]:
        if not hasattr(x, "__memdeletedattrs__") or id(x) not in x.__memdeletedattrs__:
            # the type was not processed by memclass, so nothing to extract
            continue
        for p in x.__memdeletedattrs__[id(x)]["params"]:
            if p not in fielddata.seen_vars:
                parent_params.append(p)
                if p in x.__memdeletedattrs__[id(x)]["defaults"]:
                    parent_param_defaults[p] = x.__memdeletedattrs__[id(x)]["defaults"][p]
        for p in x.__memdeletedattrs__[id(x)]["initfields"]:
            if p not in fielddata.seen_vars:
                parent_initfields.append(p)
                if p in x.__memdeletedattrs__[id(x)]["defaults"]:
                        parent_param_defaults[p] = x.__memdeletedattrs__[id(x)]["defaults"][p]

    full_params = parent_params + fielddata.params
    full_defaults = parent_param_defaults | fielddata.defaults # order is important, right side replaces left in case of conflict
    full_initfields = parent_initfields + fielddata.initfields
    
    initcode = get_init_code(
        full_params,
        full_initfields,
        full_defaults
    )
    #print(cls.__name__)
    #print(initcode)
    ls = {}
    exec(
        initcode,
        globals,
        ls
    )
    cls.__init__ = ls["__init__"]
    
    # {"defaults": {}, "params": [], "initfields": []}
    # allows filling in all the defaults
    if not hasattr(cls, "__memdeletedattrs__"):
        cls.__memdeletedattrs__ = { }
    if id(cls) not in cls.__memdeletedattrs__:
        cls.__memdeletedattrs__[id(cls)] = {}

    for p in fielddata.params + fielddata.initfields:
        try:
            delattr(cls, p)
        except AttributeError:
            pass

    # use deletedattrs to pass along to derived classes
    cls.__memdeletedattrs__[id(cls)]["defaults"] = fielddata.defaults
    cls.__memdeletedattrs__[id(cls)]["params"] = fielddata.params
    cls.__memdeletedattrs__[id(cls)]["initfields"] = fielddata.initfields
    
    return cls



if __name__ == "__main__":
    @memclass
    class Base:
        a: ParamType | int = 99
        b = None
        c: int = "test"
        d: ParamType = 1.0
        e = 99.00

    @memclass
    class Child(Base):
        cool_str = "Childstr"

    @memclass
    class OtherBase:
        a = Base()
        b: Child | None
        c: "OtherObj"

    @memclass
    class OtherObj:
        a: ParamType | int

        def test(self):
            if self.a is None:
                print(self.a.x) # cause issue intentionally
            print("gaming")

    x = OtherObj()
    print(x.a)
