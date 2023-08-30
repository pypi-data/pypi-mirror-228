from MyOverlay.funcs import myfunctions


def InnitOverlay():
    screen = myfunctions.StartOverlay()
    print(screen)
    return screen


def settext(screen, text: str, PosX: int, PosY: int, font: str = 'Segoe UI Semibold', size: int = 30, opx: int = 2):
    myfunctions.settext(screen, text, PosX, PosY, font, size, opx)


def KillOverlay():
    myfunctions.KillOverlay()


def StatusOverlay():
    return myfunctions.StatusOverlay()


def GetJobDirectory(JobName: str):
    return myfunctions.GetJobDirectory(JobName)


def GetJob(JobName: str):
    return myfunctions.GetJob(JobName)