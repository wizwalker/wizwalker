import ctypes
from enum import Enum, IntFlag

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
gdi32 = ctypes.windll.gdi32
ntdll = ctypes.windll.ntdll


# Number of units covered in 1 second
WIZARD_SPEED = 580


type_format_dict = {
    "char": "<c",
    "signed char": "<b",
    "unsigned char": "<B",
    "bool": "?",
    "short": "<h",
    "unsigned short": "<H",
    "int": "<i",
    "unsigned int": "<I",
    "long": "<l",
    "unsigned long": "<L",
    "long long": "<q",
    "unsigned long long": "<Q",
    "float": "<f",
    "double": "<d",
}


class Keycode(Enum):
    PAGE_DOWN = 347892351010
    PAGE_UP = 313532612641
    BACKSPACE = 60129542152
    TAB = 64424509449
    ENTER = 120259084301
    CAPS_LOCK = 249108103188
    Escape = 4294967323
    SPACEBAR = 244813135904
    END = 339302416419
    HOME = 304942678052
    LEFT_ARROW = 322122547237
    UP_ARROW = 309237645350
    RIGHT_ARROW = 330712481831
    DOWN_ARROW = 343597383720
    PRINT_SCREEN = 352187318317
    DEL = 356482285614
    ZERO = 47244640304
    ONE = 8589934641
    TWO = 12884901938
    THREE = 17179869235
    FOUR = 21474836532
    FIVE = 25769803829
    SIX = 30064771126
    SEVEN = 34359738423
    EIGHT = 38654705720
    NINE = 42949673017
    A = 128849018945
    B = 206158430274
    C = 197568495683
    D = 137438953540
    E = 77309411397
    F = 141733920838
    G = 146028888135
    H = 150323855432
    I = 98784247881
    J = 154618822730
    K = 158913790027
    L = 163208757324
    M = 214748364877
    N = 210453397582
    O = 103079215183
    P = 107374182480
    Q = 68719476817
    R = 81604378706
    S = 133143986259
    T = 85899346004
    U = 94489280597
    V = 201863462998
    W = 73014444119
    X = 193273528408
    Y = 90194313305
    Z = 188978561114
    Left_Windows = 390842024027
    Right_Windows = 395136991324
    Numeric_pad_0 = 352187318368
    Numeric_pad_1 = 339302416481
    Numeric_pad_2 = 343597383778
    Numeric_pad_3 = 347892351075
    Numeric_pad_4 = 322122547300
    Numeric_pad_5 = 326417514597
    Numeric_pad_6 = 330712481894
    Numeric_pad_7 = 304942678119
    Numeric_pad_8 = 309237645416
    Numeric_pad_9 = 313532612713
    Multiply = 236223201386
    Add = 335007449195
    Subtract = 317827580013
    Decimal = 356482285678
    Divide = 227633266799
    F1 = 253403070576
    F2 = 257698037873
    F3 = 261993005170
    F4 = 266287972467
    F5 = 270582939764
    F6 = 274877907061
    F7 = 279172874358
    F8 = 283467841655
    F9 = 287762808952
    F10 = 292057776249
    F11 = 373662154874
    F12 = 377957122171
    NUM_LOCK = 296352743568
    Left_SHIFT = 180388626592
    Right_SHIFT = 231928234145
    Left_CONTROL = 124554051746
    Right_CONTROL = 124554051747
    Ctrl = 124554051746
    Alt = 240518168740
    Shift = 180388626592
    Win = 390842024027

class ModifierKeys(IntFlag):
    """
    Key modifiers
    """

    ALT = 0x12
    CTRL = 0x11
    SHIFT = 0x10
    NOREPEAT = 0x4000
