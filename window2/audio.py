import pygame
from threading import Thread
from time import sleep


class Audio:
    AppliID: int = 0
    MAX_CHANNELS: int = 1024
    APPLI: dict = {}
    DEBUG: bool = False
    MUTE: bool = False

    @classmethod
    def init(self, debug=False):
        self.DEBUG = debug
        if self.DEBUG:
            print("Total Audio channel number =", self.MAX_CHANNELS)
        pygame.mixer.set_num_channels(self.MAX_CHANNELS)

    @classmethod
    def get_reserved_channels_number(self):
        nombre = 0
        for application in self.APPLI:
            nombre += self.APPLI[application]["max_channels"]
        return nombre

    @classmethod
    def new_application(self):
        self.AppliID += 1
        return f"APP{self.AppliID}"

    @classmethod
    def init_application(self, application, max_channels=1):
        if application not in self.APPLI:
            max_channels = max(0, min(max_channels, self.MAX_CHANNELS-self.get_reserved_channels_number()))
            self.APPLI[application] = {}
            self.APPLI[application]["max_channels"] = max_channels
            self.APPLI[application]["sound_index"] = 1
            self.APPLI[application]["SOUNDS"] = {}
            self.APPLI[application]["CHANNELS"] = {}
            self.APPLI[application]["SNDMUTE"] = {}
            if self.DEBUG:
                print(f"Init Audio pour ({application}) avec {max_channels} canaux")

    @classmethod
    def close(self):
        while self.APPLI:
            application, contenu = self.APPLI.popitem()
            while contenu["CHANNELS"]:
                idx, channel = contenu["CHANNELS"].popitem()
                channel.stop()
            if self.DEBUG:
                print(f"Audio clos pour application '{application}'")

    @classmethod
    def close_application(self, application):
        for idx, channel in self.APPLI[application]["CHANNELS"].items():
            if self.DEBUG:
                print("stop channel", idx, "pour :", application)
            channel.stop()
        self.APPLI.pop(application)
        if self.DEBUG:
            print(f"Audio clos pour application '{application}'")

    @classmethod
    def stop_all_channels_application(self, application):
        for idx, channel in self.APPLI[application]["CHANNELS"].items():
            if self.DEBUG:
                print("stop channel", idx, "pour :", application)
            channel.stop()

    @classmethod
    def remove_all_unused_sound_channels(self):
        for application in self.APPLI:
            self.remove_appli_unused_sound_channels(application)

    @classmethod
    def remove_appli_unused_sound_channels(self, application):
        channels_to_del = []
        for idx, channel in self.APPLI[application]["CHANNELS"].items():
            if not channel.get_busy():
                channel.stop()
                channels_to_del.append(idx)
                if self.DEBUG:
                    print("stop & remove channel", idx, "pour", application)

        for idx in channels_to_del:
            self.APPLI[application]["CHANNELS"].pop(idx)

    @classmethod
    def set_channel_volume(self, application, idx, volume):
        if application in self.APPLI:
            if idx in self.APPLI[application]["CHANNELS"]:
                self.APPLI[application]["CHANNELS"][idx].set_volume(volume)

    @classmethod
    def set_sound_volume(self, application, idx, volume):
        if application in self.APPLI:
            if idx in self.APPLI[application]["SOUNDS"]:
                self.APPLI[application]["SOUNDS"][idx].set_volume(volume)

    @classmethod
    def get_channel_volume(self, application, idx):
        if application in self.APPLI:
            if idx in self.APPLI[application]["CHANNELS"]:
                return self.APPLI[application]["CHANNELS"][idx].get_volume()
        return 0

    @classmethod
    def get_sound_volume(self, application, idx):
        if application in self.APPLI:
            if idx in self.APPLI[application]["SOUNDS"]:
                return self.APPLI[application]["SOUNDS"][idx].get_volume()
        return 0

    @classmethod
    def channel_fadeout(self, application, idx, time):
        if application in self.APPLI:
            if idx in self.APPLI[application]["CHANNELS"]:
                self.APPLI[application]["CHANNELS"][idx].fadeout(time)

    @classmethod
    def mute_all_applications(self):
        self.MUTE = True
        for application in self.APPLI:
            self.mute_application(application)

    @classmethod
    def unmute_all_applications(self):
        self.MUTE = False
        for application in self.APPLI:
            self.unmute_application(application)

    @classmethod
    def mute_application(self, application):
        if application in self.APPLI:
            if len(self.APPLI[application]["SNDMUTE"]) == 0:
                for snd_idx in self.APPLI[application]["SOUNDS"]:
                    snd_volume = self.APPLI[application]["SOUNDS"][snd_idx].get_volume()
                    self.APPLI[application]["SNDMUTE"][snd_idx] = snd_volume
                    self.APPLI[application]["SOUNDS"][snd_idx].set_volume(0)

    @classmethod
    def unmute_application(self, application):
        if application in self.APPLI:
            for snd_idx in self.APPLI[application]["SNDMUTE"]:
                snd_volume = self.APPLI[application]["SOUNDS"][snd_idx].get_volume()
                if snd_volume == 0:
                    self.APPLI[application]["SOUNDS"][snd_idx].set_volume(
                        self.APPLI[application]["SNDMUTE"].get(snd_idx, 1))
            self.APPLI[application]["SNDMUTE"].clear()

    @classmethod
    def sound_fadeout(self, application, idx, time):
        if application in self.APPLI:
            if idx in self.APPLI[application]["SOUNDS"]:
                self.APPLI[application]["SOUNDS"][idx].fadeout(time)

    @classmethod
    def unload_sound(self, application, idx):
        if application in self.APPLI:
            if idx in self.APPLI[application]["SOUNDS"]:
                if self.DEBUG:
                    print("Unloading Sound", idx, "pour", application)
                self.APPLI[application]["SOUNDS"].pop(idx)

    @classmethod
    def load_sound(self, application, sound_file, volume=1):
        if application in self.APPLI:
            idx = self.APPLI[application]["sound_index"]
            if self.DEBUG:
                print("Loading Sound", idx, "pour", application)
            try:
                sound = pygame.mixer.Sound(sound_file)
                sound.set_volume(volume)
                self.APPLI[application]["SOUNDS"][idx] = sound
                if self.MUTE:
                    snd_volume = sound.get_volume()
                    self.APPLI[application]["SNDMUTE"][idx] = snd_volume
                    sound.set_volume(0)

            except Exception as e:
                print("SoundEffect Error:", e)
                return False

            self.APPLI[application]["sound_index"] += 1
            return idx
        return False

    @classmethod
    def wait_channel(self, channel, callback):
        while channel.get_busy():
            sleep(0.5)
        callback()

    @classmethod
    def play_sound(self, application, idx, callback=None):
        if application in self.APPLI:
            if idx in self.APPLI[application]["SOUNDS"] and (
              len(self.APPLI[application]["CHANNELS"]) < self.APPLI[application]["max_channels"]):
                self.remove_appli_unused_sound_channels(application)
                channel = self.APPLI[application]["SOUNDS"][idx].play()
                if channel:
                    channel_index = min(
                        [x for x in range(1, 1+self.APPLI[application]["max_channels"]) if x not in self.APPLI[application]["CHANNELS"]])
                    if self.DEBUG:
                        print("Play Sound", idx, "pour", application, "sur channel", channel_index)
                    self.APPLI[application]["CHANNELS"][channel_index] = channel
                    if callback:
                        Thread(target=self.wait_channel, args=(channel, callback)).start()
                    return channel_index

        if callback:
            callback()
                        
    @classmethod
    def channel_action(self, action, application, idx):
        if application in self.APPLI:
            if idx in self.APPLI[application]["CHANNELS"]:
                if action.upper() == "STOP":
                    self.APPLI[application]["CHANNELS"][idx].stop()
                    del self.APPLI[application]["CHANNELS"][idx]
                elif action.upper() == "PLAY":
                    self.APPLI[application]["CHANNELS"][idx].play()
                elif action.upper() == "PAUSE":
                    self.APPLI[application]["CHANNELS"][idx].pause()
                elif action.upper() == "UNPAUSE":
                    self.APPLI[application]["CHANNELS"][idx].unpause()
                else:
                    return False
                return True
        return False


def set_true(variable):
    variable[0] = True
    return lambda: True


close_app_id = ""


def fin():
    assert len(Audio.APPLI) == 3
    Audio.close_application(close_app_id)
    assert len(Audio.APPLI) == 2

    Audio.remove_all_unused_sound_channels()
    assert len(Audio.APPLI[application]["SOUNDS"]) == 2

    Audio.close()
    assert len(Audio.APPLI) == 0
    print("Nettoyage: OK !")


if __name__ == "__main__":
    print("Compilation: OK")
    import os

    pygame.mixer.init()
    Audio.init(debug=True)

    app_id = Audio.new_application()
    Audio.init_application(app_id, 510)
    assert len(Audio.APPLI[app_id]) == 5

    close_app_id = Audio.new_application()
    Audio.init_application(close_app_id, 510)
    assert len(Audio.APPLI) == 2

    application = Audio.new_application()
    Audio.init_application(application, 10)
    assert len(Audio.APPLI) == 3

    sound_file = os.path.join("sounds", "fusee1.mp3")
    sidx = Audio.load_sound(application, sound_file)
    assert len(Audio.APPLI[application]["SOUNDS"]) == 1

    cidx = Audio.play_sound(application, sidx)
    sleep(0.3)
    cidx = Audio.play_sound(application, sidx)
    assert len(Audio.APPLI[application]["CHANNELS"]) == 2
    sleep(1.5)

    sound_file = os.path.join("sounds", "petard1.mp3")
    sidx = Audio.load_sound(application, sound_file)
    assert len(Audio.APPLI[application]["SOUNDS"]) == 2

    sound_file = os.path.join("sounds", "petard3.mp3")
    sidx2 = Audio.load_sound(application, sound_file)
    assert len(Audio.APPLI[application]["SOUNDS"]) == 3

    Audio.unload_sound(application, sidx)
    assert len(Audio.APPLI[application]["SOUNDS"]) == 2

    cidx = Audio.play_sound(application, sidx2)
    sleep(0.25)
    if True:
        cidx = Audio.play_sound(application, sidx2, fin)
    else:
        suite = [False]
        cidx = Audio.play_sound(application, sidx2, set_true(suite))
        while not suite[0]:
            sleep(0.25)
        fin()
