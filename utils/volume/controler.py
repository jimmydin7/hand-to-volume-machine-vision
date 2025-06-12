from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from utils.logs import logs as lg

def set_volume(new_volume):
    try:
        # Get the default audio device
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        volume.SetMasterVolumeLevelScalar(new_volume, None)
        lg.logInfo(f"Volume set to: {round((new_volume*100), 1)}%")
        
    except Exception as e:
        volumeval = 100
        lg.logInfo(f"Volume set to: {volumeval}%")

def get_current_volume():
    try:
        # Get the default audio device
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        current_volume = volume.GetMasterVolumeLevelScalar()
        return current_volume #0.0 - 1.0
        
    except Exception as e:
        lg.logError(f"Failed to get current volume: {str(e)}")
        return None