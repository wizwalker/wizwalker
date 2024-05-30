import win32gui
from ctypes import byref, c_int, CFUNCTYPE, Structure
from ctypes.wintypes import WPARAM, MSG, DWORD
from typing import Callable, Union
import asyncio
from wizwalker.constants import Keycode, user32, ModifierKeys

WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 257
WM_SYSKEYDOWN = 260
WM_SYSKEYUP = 261
HC_ACTION = 0


class KBDLLHOOKSTRUCT(Structure):_fields_=[
	('vkCode', DWORD),
	('scanCode', DWORD),
	('flags', DWORD),
	('dwExtraInfo', DWORD)
]

LLKP_decl = CFUNCTYPE(c_int, c_int, WPARAM, KBDLLHOOKSTRUCT)

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
		self.modifiers = set()
		self.current_pressed_key = None
		self.last_pressed_key = None
		self.mod_keycodes = (Keycode.Left_CONTROL, Keycode.Right_CONTROL, Keycode.Left_SHIFT, Keycode.Right_SHIFT, Keycode.Left_MENU, Keycode.Right_MENU)
		self.hook = None
		self.message_loop = None
		self._message_loop_delay = 0


	def LowLevelKeyboardProc(self, nCode, wParam, lParam):
		"""
		Hook procedure to monitor and log keyboard events.
		Arguments:
			nCode       = HC_ACTION code
			wParam      = Keyboard event message code
			lParam      = Address of keyboard input event
		"""

		if wParam == WM_SYSKEYDOWN:
			kb = KBDLLHOOKSTRUCT.from_param(lParam)
			vkCode = kb.vkCode
			self.handle_keydown(vkCode)
	
		if wParam == WM_SYSKEYUP:
			kb = KBDLLHOOKSTRUCT.from_param(lParam)
			vkCode = kb.vkCode
			self.handle_keyup(vkCode)

		if nCode == HC_ACTION and wParam == WM_KEYUP:
			kb = KBDLLHOOKSTRUCT.from_param(lParam)
			vkCode = kb.vkCode
			self.handle_keyup(vkCode)
			
		if nCode == HC_ACTION and wParam == WM_KEYDOWN:
			kb = KBDLLHOOKSTRUCT.from_param(lParam)
			vkCode = kb.vkCode
			self.handle_keydown(vkCode)
			
		return self.user32.CallNextHookEx(Hook().is_hooked , nCode, wParam, lParam)


	def handle_keyup(self, vkCode: int):
		try:
			keycode = self.key_type(Keycode(vkCode))
		except:
			keycode = None

		if keycode:
			if type(keycode) == ModifierKeys:
				if keycode in self.modifiers:
					self.modifiers.remove(keycode)

		if self.current_pressed_key == keycode:
			self.current_pressed_key = None
			self.last_pressed_key = None


	def handle_keydown(self, vkCode: int):
		try:
			keycode = self.key_type(Keycode(vkCode))
		except:
			keycode = None

		if keycode:
			if type(keycode) == ModifierKeys:
				self.modifiers.add(keycode)
			else:
				self.current_pressed_key = keycode

				self.hotkey_match()

		self.last_pressed_key = keycode 


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
			elif keycode == Keycode.Left_MENU:
				return ModifierKeys.ALT         
			elif keycode == Keycode.Right_MENU:
				return ModifierKeys.ALT
		
		return keycode


	def run_callback(self, c: Callable):
		return asyncio.create_task(c())


	def hotkey_match(self) -> None:
		""" 
		Finds if Listener has matched hotkey
		"""

		if self.current_pressed_key:
			hotkeys = [hotkey for hotkey in self.hotkeys if not ModifierKeys.NOREPEAT in hotkey.modifiers and self.current_pressed_key == hotkey.keycode]
			for hotkey in hotkeys:
				if set(hotkey.modifiers) == self.modifiers:
					self.run_callback(hotkey.callback)
					return 

		if not self.current_pressed_key == self.last_pressed_key:
			no_repeat_hotkeys = [hotkey for hotkey in self.hotkeys if ModifierKeys.NOREPEAT in hotkey.modifiers and self.current_pressed_key == hotkey.keycode]
			for hotkey in no_repeat_hotkeys:
				hotkey_modifiers = set(hotkey.modifiers)
				hotkey_modifiers.remove(ModifierKeys.NOREPEAT)
				if hotkey_modifiers == self.modifiers:
						self.run_callback(hotkey.callback)
						return


	async def install_keyhook(self):
		"""
		Install hook
		"""

		if self.hook is None:
			self.hook = Hook()

		callback = LLKP_decl((self.LowLevelKeyboardProc))
		self.hook.install_hook(callback)

		if self.message_loop is None:
			self.message_loop = asyncio.create_task(self.message())
			await self.message_loop


	def uninstall_hook(self):
		"""
		uninstall hook
		"""
		if self.hook is not None:
			self.hook.uninstall_hook()
			self.hook = None

		if self.message_loop is not None:
			self.message_loop.cancel()
			self.message_loop = None


	async def message(self):
		message = MSG()
		while True:
			msg = self.user32.PeekMessageW(
				byref(message),
				None,
				0x311,
				0x314,
				1,
				)

			if msg:
				self.user32.DispatchMessageW(byref(message))

			await asyncio.sleep(self._message_loop_delay)
			


class Listener():
	"""
    Hotkey listener
    Args:
        hotkeys: list of Hotkeys to be listened for
        loop: The event loop to use; defaults to current
    Examples:
        .. code-block:: py
			import asyncio
			from wizwalker import Hotkey, Keycode, Listener, ModifierKeys
			async def main():
				async def callback():
					print("a was pressed")
				hotkeys = [Hotkey(Keycode.A, callback, ModifierKeys.CTRL)] 
				listener = Listener(hotkeys)
				listener.listen_forever()
				# your program here
				while True:
					await asyncio.sleep(1)
			if __name__ == "__main__":
				asyncio.run(main())
    """

	def __init__(self, *hotkey: Hotkey):
		self._loop = asyncio.get_event_loop()
		self.hotkeys = list(hotkey)
		self.hook = None
		self.key_listener = None
		self.listen_task = None


	def listen_forever(self) -> asyncio.Task:
		"""
		return a task listening to events
		"""

		self.key_listener = KeyListener(self.hotkeys)
		self.listen_task = asyncio.create_task(self.key_listener.install_keyhook())

		return self.listen_task


	def close(self):
		"""
		Stop the listener
		"""

		if self.listen_task is None:
			raise ValueError("This listener has already been stopped or not started")

		self.key_listener.uninstall_hook()
		self.listen_task.cancel()
		self.listen_task = None
