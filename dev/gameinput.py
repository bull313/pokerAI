"""
GameInput:
    Gets input from the user (prompts commands and listens for hotkeys)
"""

"""
Imports
"""
from os                 import name                     as os_name
from os                 import system                   as os_system
from pynput.keyboard    import Key, KeyCode, Listener

class GameInput:

    """
    Constants
    """
    HOT_KEY_DEBUG       = False
    OS_WINDOWS_NAME     = "nt"

    """
    Hotkey Constants
    """
    GAME_SAVE = None

    """
    Select hot key values based on OS
    """
    if os_name == OS_WINDOWS_NAME:
        """
        WINDOWS HOTKEYS

        ---------------------------------------------------------------------------------------------------------------
        | Contstant name |      Description      | Key Combo String |                     Key Combo                   |
        ---------------------------------------------------------------------------------------------------------------
        """
        GAME_SAVE = ( "Ctrl+7",     "Save the game progress",           ( Key.ctrl.value.vk,    int("0x37", 0) ) )
    else:
        """
        MAC HOTKEYS

        ---------------------------------------------------------------------------------------------------------------
        | Contstant name |      Description      | Key Combo String |                     Key Combo                   |
        ---------------------------------------------------------------------------------------------------------------
        """
        GAME_SAVE = ( "Cmd+7",      "Save the game progress",           ( Key.cmd.value.vk,     int("0x1A", 0) ) )

    """
    Constructor
    """
    def __init__(self):
        self._installed_hot_keys = dict()
        self._pressed_keys = set()

    """
    Private Methods
    """
    def _convert_key_to_vk(self, key):
        """
        Local Variables
        """
        vk = 0

        """
        Convert left and right keys into the general key (ctrl, cmd)
        Use the type of key parameter to find the virtual key (vk)
        """
        if key in { Key.ctrl_l, Key.ctrl_r }:
            vk = Key.ctrl.value.vk
        elif key in { Key.cmd_l, Key.cmd_r }:
            vk = Key.cmd.value.vk
        elif isinstance(key, Key):
            vk = key.value.vk
        elif isinstance(key, KeyCode):
            vk = key.vk

        """
        Return Result
        """
        return vk

    def _check_for_hot_keys(self):
        """
        Check the list of pressed keys to detect if a hot key is pressed
        """
        for hot_key in self._installed_hot_keys:
            """
            Get the hot key key combo
            Get the corresponding callback function
            And initially assume that the hot key key is pressed
            """
            _, _, key_code          = hot_key
            exec_hot_key_function   = self._installed_hot_keys[hot_key]
            hot_key_pressed         = True

            """
            If a key in the hot key is not in the pressed keys set, the hot key is not pressed
            (contradicts the assumption)
            """
            for key_atom in key_code:
                
                if key_atom not in self._pressed_keys:
                    hot_key_pressed = False
                    break

            """
            If a hot key is pressed, invoke the callback function
            """
            if hot_key_pressed:
                exec_hot_key_function()

    """
    Event Methods
    """
    def _handle_key_press(self, key):
        """
        Add the virtual key to the pressed keys list and check if any hot key combos are pressed
        """
        vk = self._convert_key_to_vk(key)

        """
        If debug mode is on, display the virtual key code
        """
        if GameInput.HOT_KEY_DEBUG:
            print("Virtual Key Code Pressed: %s" % vk)

        self._pressed_keys.add(vk)
        self._check_for_hot_keys()

    def _handle_key_release(self, key):
        """
        Get the virutal key of the key parameter
        """
        vk = self._convert_key_to_vk(key)

        """
        Remove this virtual key from the pressed keys set if it exists
        """
        if vk in self._pressed_keys:
            self._pressed_keys.remove(vk)

    """
    Public Methods
    """
    def get_input(self, input_msg):
        """
        Wrapper for the input() function:
            This is done to easily switch between Python 2.7 (raw_input) and 3.x (input) if/when necessary
        """
        return input(input_msg)

    def pair_hot_key_to_command(self, hot_key, command):
        """
        Add a key combo and callback function (executed on the press of the hot key) to the hot key list
        """
        self._installed_hot_keys.update({ hot_key : command })

    def get_installed_hotkey_strings(self):
        """
        Convert installed hot keys to a list of string tuples
        first value is a readable key combo string
        second value is a description of the hot key's callback function
        Local Variables
        """
        hot_keys = list()

        """
        Get the name and description of each hotkey
        """
        for hot_key in self._installed_hot_keys:
            hotkey_name, description, _ = hot_key
            hot_keys.append((hotkey_name, description))

        """
        Return Result
        """
        return hot_keys

    def listen_for_hot_keys(self):
        """
        Create and start a hot key listener thread and have it die when the main thread is finished (daemon)
        """
        listener = Listener(on_press=self._handle_key_press, on_release=self._handle_key_release)
        listener.setDaemon(True)
        listener.start()
