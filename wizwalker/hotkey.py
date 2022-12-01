import asyncio
import win32con
from ctypes import windll,byref,c_int, POINTER, CFUNCTYPE
import ctypes
from ctypes.wintypes import WPARAM, LPARAM, MSG
from enum import Enum
from enum import IntFlag
from typing import Callable, Union
from icecream import ic

from wizwalker.constants import Keycode, ModifierKeys, user32

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 257
HC_ACTION = 0

LLKP_decl = CFUNCTYPE(c_int, c_int, WPARAM, POINTER(LPARAM))


class Hook:
    
    def __init__(self):
        """
        Constructor for the hook class.

        Responsible for allowing methods to call functions from
        user32.dll 
        """
        self.user32 = user32
        self.is_hooked = None
        

    def install_hook(self, ptr) -> bool:
        """
        Method for installing hook.

        Arguments
            ptr: pointer to the callback function
        """

        self.is_hooked = self.user32.SetWindowsHookExA(
            WH_KEYBOARD_LL,
            ptr,
            0,
            0
        )

        if not self.is_hooked:
            return False

        return True

    def uninstall_hook(self):
        """
        Method for uninstalling the hook.
        """

        if self.is_hooked is None:
            return
        
        self.user32.UnhookWindowsHookEx(self.is_hooked)
        self.is_hooked = None

class Hotkey:
    """
    A hotkey to be listened to

    Args:
        keycode: Keycode to listen for
        callback: Coroutine to run when the key is pressed
        modifiers: List of Key modifiers to apply
    """

    def __init__(
        self,
        keycode: Keycode,
        callback: Callable,
        *args: Union[ModifierKeys, int],
    ):
        self.keycode = keycode
        self.modifiers = args
        self.callback = callback


class KeyListener:
        def __init__(self, hotkey: list[Hotkey]):
            self.hotkeys = hotkey[0]
            self.user32 = user32
            self.modifiers = []
            self.key_pressed = []
            self.last_key_pressed = None
            self.mod_keycodes = [Keycode.Left_CONTROL, Keycode.Right_CONTROL, Keycode.Left_SHIFT, Keycode.Right_SHIFT, Keycode.ALT]
            self.hook = None

        def LowLevelKeyboardProc(self, nCode, wParam, lParam):
            """
            Hook procedure to monitor and log keyboard events.

            Arguments:
                nCode       = HC_ACTION code
                wParam      = Keyboard event message code
                lParam      = Address of keyboard input event

            """

            self.hotkey_match()

            if wParam == win32con.WM_SYSKEYDOWN:
                vkCode = lParam[0] >> 32
                self.handle_keydown(vkCode)
        
            if wParam == win32con.WM_SYSKEYUP:
                vkCode = lParam[0] >> 32
                self.handle_keyup(vkCode)

            if nCode == HC_ACTION and wParam == win32con.WM_KEYUP:
                vkCode = lParam[0] >> 32
                self.handle_keyup(vkCode)
                
            if nCode == HC_ACTION and wParam == WM_KEYDOWN:
                vkCode = lParam[0] >> 32
                self.handle_keydown(vkCode)
                
            return self.user32.CallNextHookEx(Hook().is_hooked , nCode, wParam, lParam)

        def handle_keyup(self, vkCode: int):
            self.nonrepeat_logic()
            keycode = self.key_type(Keycode(vkCode))
            if type(keycode) == Keycode:  # if keycode is a type Keycode
                if keycode in self.key_pressed:
                    self.key_pressed.remove(keycode) # remove the type Keycodejn to the list of keys_pressed
            else:
                if keycode in self.modifiers:
                    self.modifiers.remove(keycode) # else remove the ModifierKeys to the modifiers list


        def handle_keydown(self, vkCode: int):
            keycode = self.key_type(Keycode(vkCode))
            if type(keycode) == Keycode:  # if keycode is a type Keycode
                self.key_pressed.append(keycode) # add the type Keycode to the list of keys_pressed
            else:
                if keycode not in self.modifiers: # makes sure there isn't duplicates when holding down key
                    self.modifiers.append(keycode) # else add the ModifierKeys to the modifiers list
            self.last_key_pressed = keycode 


        def key_type(self, keycode: Keycode):

            """
            Finds if Keycode is a modifier key
            """

            if keycode in self.mod_keycodes:
                if keycode == Keycode.Left_CONTROL:
                    return ModifierKeys.CTRL
                elif keycode == Keycode.Right_CONTROL:
                    return ModifierKeys.CTRL
                elif keycode == Keycode.Left_SHIFT:
                    return ModifierKeys.SHIFT
                elif keycode == Keycode.Right_SHIFT:
                    return ModifierKeys.SHIFT
                elif keycode == Keycode.Alt:
                    return ModifierKeys.ALT             
            
            return keycode


        def run_callback(self, c: Callable):
            return c()


        def hotkey_match(self) -> None:
            """ 
            Finds if Listener has matched hotkey
            """
            #ic(self.key_pressed)
            #ic(self.last_key_pressed)
            #ic(self.modifiers)

            if self.key_pressed:
                hotkeys = [hotkey for hotkey in self.hotkeys if not ModifierKeys.NOREPEAT in hotkey.modifiers]
                for hotkey in hotkeys:
                    if hotkey.keycode == self.key_pressed[0] and list(hotkey.modifiers) == self.modifiers:
                        self.run_callback(hotkey.callback) 
                        self.last_key_pressed = None
                        self.key_pressed = []
                        return


        def nonrepeat_logic(self) -> None:
            if self.key_pressed:
                if len(set(self.key_pressed)) > 1: # makes it check if multiple key codes in key_pressed which is unwanted
                        self.key_pressed = [self.last_key_pressed]

                nonrepeat_hotkeys = [hotkey for hotkey in self.hotkeys if ModifierKeys.NOREPEAT in hotkey.modifiers]
                for hotkey in nonrepeat_hotkeys:
                    if ModifierKeys.NOREPEAT in hotkey.modifiers:
                        hotkey_modifiers = list(hotkey.modifiers)
                        hotkey_modifiers.remove(ModifierKeys.NOREPEAT)
                        if hotkey_modifiers == False:
                            #print("hi")
                            hotkey_modifiers = []
                        #print(hotkey_modifiers)
                        #print(self.modifiers)
                        if list(set(self.key_pressed))[0] == hotkey.keycode and hotkey_modifiers == self.modifiers:
                            if len(self.key_pressed) > 1 and self.key_pressed[0] == self.last_key_pressed:
                                ic("held down")
                                self.run_callback(hotkey.callback) 
                                self.key_pressed = []
                                return
                            self.run_callback(hotkey.callback)


        def install_keyhook(self):
            """
            Install hook
            """
            self.hook = Hook()
            callback = LLKP_decl((self.LowLevelKeyboardProc))
            self.hook.install_hook(callback)
            self.message()


        def uninstall_hook(self):
            """
            uninstall hook
            """
            self.hook.uninstall_hook()


        def message(self):
            # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-peekmessagew
            message = MSG()
            while True:
                is_message = self.user32.PeekMessageW(
                    ctypes.byref(message),
                    None,
                    0x311,
                    0x314,
                    1,
                )



class Listener():

    def __init__(self, *hotkey: Hotkey):
        self._loop = None
        self.hotkeys = list(hotkey)
        self.hook = None
        self.key_listener = None
        self.message_loop_task = None


    def message_loop(self):
        while True:
            self.key_listener.message()


    def start(self):
        """
        Start the listener
        """

        if self.message_loop_task:
            raise ValueError("This listener has already been started")
        
        self.key_listener = KeyListener(self.hotkeys)
        self.key_listener.install_keyhook()
        #self.message_loop()


    def stop(self):
        """
        Stop the listener
        """
        #TODO make it work
        if not self.message_loop_task:
            raise ValueError("This listener has already been stopped")

        self.key_listener.uninstall_hook()
        #self.key_listener = None

        #self.message_loop_task.cancel()
        #self.message_loop_task = None
        

def main():
    def callback2():
        print("notfaj was pressed")
    
    def callback1():
        print("a was pressed")
    
    def callback0():
        print("s was pressed")

    hotkey = [
            Hotkey(Keycode.A, callback1),
            Hotkey(Keycode.S, callback0, ModifierKeys.CTRL, ModifierKeys.NOREPEAT),
            Hotkey(Keycode.D, callback2, ModifierKeys.ALT, ModifierKeys.SHIFT )
            ]

    hotkey_L = Listener(hotkey)
    hotkey_L.start()

    
main()
