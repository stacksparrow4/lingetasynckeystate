# LinGetAsyncKeyState

Windows API has a useful function called GetAsyncKeyState which can be used to find out if a key is currently being held down.
To achieve such functionality on Linux, you instead must connect to an X display and use XQueryKeymap to find out which keys are being held down.

(As such this library only provides if the given key is being held, not the additional information that GetAsyncKeyState provides)

However, the keycodes used in these apis differ. To solve this issue, I downloaded the keycodes described in [on the microsoft docs](https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes), as well as the [xorg key symbols](https://www.cl.cam.ac.uk/~mgk25/ucs/keysymdef.h).

**Because of this, not all key presses will work with this library. If you find the keypress you desire does not work, refer to "adding new keys".**

## Usage
### C#

Normally in C# you could create a IsKeyDown function like this:

```cs
[DllImport("User32.dll")]
private static extern short GetAsyncKeyState(Keys key);

public static bool IsKeyDown(Keys keys) {
    return (GetAsyncKeyState(keys) & 0x8000) == 0x8000;
}
```

However this will not work with Mono on linux. To get this to work, first build the shared object
on linux by running `build.sh` (You may be able to use WSL).
You can replace then write something as follows

```cs
[DllImport("User32.dll")]
private static extern short GetAsyncKeyState(Keys key);

[DllImport("./libkeystate.so")]
private static extern bool LinGetAsyncKeyState(Keys key);

public static bool IsKeyDown(Keys keys) {
    if(Environment.OSVersion.Platform == PlatformID.Unix){
        // Use the compiled linux version of GetAsyncKeyState
        return LinGetAsyncKeyState(keys);
    }

    return (GetAsyncKeyState(keys) & 0x8000) == 0x8000;
}
```

### C, C++
You can copy paste the contents of keystate.c, or link the shared object file.

### Other languages
Figure out how to call a native function and use that to call LinGetAsyncKeyState

## Adding New Keys

1. Find the windows key code (you can look in win_keycodes.txt)
2. Find the X symbol name (look in x_syms.txt)
3. Add a new elif in `createmapping.py` using a similar structure which connects the windows to the X symbol
4. Run `create_mapping.py` and copy the last line into line 8 of `keystate.c`
5. Recompile the shared object
