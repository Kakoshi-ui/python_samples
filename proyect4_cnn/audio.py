from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from networkx import volume
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
import pyautogui

vol_chng = 0

class AudioController():
    
    def __init__(self):
        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = self.interface.QueryInterface(IAudioEndpointVolume)
        self.vol_range = self.volume.GetVolumeRange()
        self.min_vol = self.vol_range[0]
        self.max_vol = self.vol_range[1]
        self.stp_vol = 0.2
        self.vol_ac = -48.0

    def vol_control(self, option):
        if option == 0:
            pyautogui.press("playpause")

        elif option == 1:
            pyautogui.press("playpause")
        elif option == 2:
            current_vol = float(self.volume.GetMasterVolumeLevel())
            if current_vol < self.max_vol:
                vol_chng = current_vol + 0.2
                self.volume.SetMasterVolumeLevel(vol_chng, None)
                print(self.volume.GetMasterVolumeLevel())
            else:
                self.volume.SetMasterVolumeLevel(self.max_vol, None)
        elif option == 3:
            current_vol = float(self.volume.GetMasterVolumeLevel())
            if current_vol > self.min_vol:
                vol_chng = current_vol - 0.2
                self.volume.SetMasterVolumeLevel(vol_chng, None)
            else:
                self.volume.SetMasterVolumeLevel(self.min_vol, None)