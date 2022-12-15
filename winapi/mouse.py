import win32api 


def getPos():
    return win32api.GetCursorPos()


def press(pos:tuple[int, int]):
    win32api.mouse_event(0x2, pos[0], pos[1], 0, 0)


def release(pos:tuple[int, int]):
    win32api.mouse_event(0x4, pos[0], pos[1], 0, 0)


def click(pos:tuple[int, int]):
    win32api.SetCursorPos(pos)
    press(pos)
    release(pos)


def mouse_move(pos:tuple[int, int]):
    win32api.SetCursorPos(pos)

    