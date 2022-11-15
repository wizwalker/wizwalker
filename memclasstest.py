
def get_repr_code(basename, params: list[str]):
    txt = f"def __repr_{basename}__(self) -> str:\n\treturn f'{basename}("
    paramstrs = []
    for name in params:
        paramstrs.append("{repr(self." + name + ")}")
    txt += f"{', '.join(paramstrs)})'\n"
    return txt

def get_init_code(basename, params: list[str], defaults: dict[int, object]) -> str:
    paramstrs = []
    for i in range(len(params)):
        if i in defaults:
            paramstrs.append(f" {params[i]}={repr(defaults[i])}")
        else:
            paramstrs.append(f" {params[i]}=None")

    txt = f"def __init_{basename}__(self,{','.join(paramstrs)}):\n"
    for name in params:
        txt += f"\tself.{name}={name}\n"
    return txt


def memclass(cls):
    defaults = {}
    known_params = set([])
    params = []
    for x in cls.__mro__[-2::-1]: # last is 'object'
        if not hasattr(x, "__memdeletedattrs"):
            x.__memdeletedattrs = {}
        cls_annotations = x.__dict__.get('__annotations__', {})
        for n in cls_annotations.keys():
            if n not in known_params:
                known_params.add(n)
                curval = None
                try:
                    curval = getattr(cls, n)
                    defaults[len(params)] = curval
                except AttributeError:
                    try:
                        curval = x.__memdeletedattrs[n]
                        defaults[len(params)] = curval
                    except KeyError:
                        pass
                params.append(n)
                try:
                    delattr(x, n)
                    if curval != None:
                        x.__memdeletedattrs[n] = curval
                except AttributeError:
                    pass

    # TODO: Repurpose this for untyped params
    # for i in range(len(params)):
    #     for x in cls.__mro__[0:-1]:
    #         for name, member in inspect.getmembers(x):
    #             print(name, repr(member))

    txt = get_repr_code(cls.__name__, params)
    txt += f"setattr(cls, '__repr__', __repr_{cls.__name__}__)"
    exec(txt, None, {'cls': cls})

    # TODO: Make this work with intellisense
    # TODO: Support __post_init__ 
    txt = get_init_code(cls.__name__, params, defaults)
    txt += f"setattr(cls, '__init__', __init_{cls.__name__}__)"
    print(txt)
    exec(txt, None, {'cls': cls})
    
    return cls


@memclass
class Base:
    offset: ... = 1
    x_field: ... = None

@memclass
class YBase(Base):
    base: ... = Base(99)
    teststr: ... = "coolstr"

@memclass 
class ZBase():
    ybase: ... = YBase()
    teststr2: ... = "coolerstr"

b = ZBase()
print(repr(b))
