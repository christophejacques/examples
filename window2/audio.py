import pygame
from threading import Thread
from time import sleep


def fprint(*args, **kwargs):
    print(*args, **kwargs, flush=True)


class Audio:
    AppliID: int = 0
    MAX_CHANNELS: int = 1024
    APPLI: dict = {}
    DEBUG: bool = False
    MUTE: bool = False

    @classmethod
    def init(cls, debug=False):
        cls.DEBUG = debug
        if cls.DEBUG:
            fprint("Total Audio channel number =", cls.MAX_CHANNELS)

        if not pygame.mixer.get_init():
            pygame.mixer.init()
            if cls.DEBUG:
                fprint("Sound initialized:", pygame.mixer.get_init())
            
        pygame.mixer.set_num_channels(cls.MAX_CHANNELS)

    @classmethod
    def get_reserved_channels_number(cls):
        nombre = 0
        for application in cls.APPLI:
            nombre += cls.APPLI[application]["max_channels"]
        return nombre

    @classmethod
    def new_application(cls):
        cls.AppliID += 1
        return f"APP{cls.AppliID}"

    @classmethod
    def init_application(cls, application, max_channels=1):
        if application not in cls.APPLI:
            max_channels = max(0, min(max_channels, cls.MAX_CHANNELS-cls.get_reserved_channels_number()))
            cls.APPLI[application] = {}
            cls.APPLI[application]["max_channels"] = max_channels
            cls.APPLI[application]["sound_index"] = 1
            cls.APPLI[application]["SOUNDS"] = {}
            cls.APPLI[application]["CHANNELS"] = {}
            cls.APPLI[application]["SNDMUTE"] = {}
            if cls.DEBUG:
                fprint(f"Init Audio pour ({application}) avec {max_channels} canaux")

    @classmethod
    def close(cls):
        while cls.APPLI:
            application, contenu = cls.APPLI.popitem()
            while contenu["CHANNELS"]:
                idx, channel = contenu["CHANNELS"].popitem()
                channel.stop()
            if cls.DEBUG:
                fprint(f"Audio clos pour application '{application}'")

    @classmethod
    def close_application(cls, application):
        for idx, channel in cls.APPLI[application]["CHANNELS"].items():
            if cls.DEBUG:
                fprint("stop channel", idx, "pour :", application)
            channel.stop()
        cls.APPLI.pop(application)
        if cls.DEBUG:
            fprint(f"Audio clos pour application '{application}'")

    @classmethod
    def stop_all_channels_application(cls, application):
        for idx, channel in cls.APPLI[application]["CHANNELS"].items():
            if cls.DEBUG:
                fprint("stop channel", idx, "pour :", application)
            channel.stop()

    @classmethod
    def remove_all_unused_sound_channels(cls):
        for application in cls.APPLI:
            cls.remove_appli_unused_sound_channels(application)

    @classmethod
    def remove_appli_unused_sound_channels(cls, application):
        channels_to_del = []
        for idx, channel in cls.APPLI[application]["CHANNELS"].items():
            if not channel.get_busy():
                channel.stop()
                channels_to_del.append(idx)
                if cls.DEBUG:
                    fprint("stop & remove channel", idx, "pour", application)

        for idx in channels_to_del:
            cls.APPLI[application]["CHANNELS"].pop(idx)

    @classmethod
    def set_channel_volume(cls, application, idx, volume):
        if application in cls.APPLI:
            if idx in cls.APPLI[application]["CHANNELS"]:
                cls.APPLI[application]["CHANNELS"][idx].set_volume(volume)

    @classmethod
    def set_sound_volume(cls, application, idx, volume):
        if application in cls.APPLI:
            if idx in cls.APPLI[application]["SOUNDS"]:
                cls.APPLI[application]["SOUNDS"][idx].set_volume(volume)

    @classmethod
    def get_channel_volume(cls, application, idx):
        if application in cls.APPLI:
            if idx in cls.APPLI[application]["CHANNELS"]:
                return cls.APPLI[application]["CHANNELS"][idx].get_volume()
        return 0

    @classmethod
    def get_sound_volume(cls, application, idx):
        if application in cls.APPLI:
            if idx in cls.APPLI[application]["SOUNDS"]:
                return cls.APPLI[application]["SOUNDS"][idx].get_volume()
        return 0

    @classmethod
    def channel_fadeout(cls, application, idx, time):
        if application in cls.APPLI:
            if idx in cls.APPLI[application]["CHANNELS"]:
                cls.APPLI[application]["CHANNELS"][idx].fadeout(time)

    @classmethod
    def mute_all_applications(cls):
        cls.MUTE = True
        for application in cls.APPLI:
            cls.mute_application(application)

    @classmethod
    def unmute_all_applications(cls):
        cls.MUTE = False
        for application in cls.APPLI:
            cls.unmute_application(application)

    @classmethod
    def mute_application(cls, application):
        if application in cls.APPLI:
            if len(cls.APPLI[application]["SNDMUTE"]) == 0:
                for snd_idx in cls.APPLI[application]["SOUNDS"]:
                    snd_volume = cls.APPLI[application]["SOUNDS"][snd_idx].get_volume()
                    cls.APPLI[application]["SNDMUTE"][snd_idx] = snd_volume
                    cls.APPLI[application]["SOUNDS"][snd_idx].set_volume(0)

    @classmethod
    def unmute_application(cls, application):
        if application in cls.APPLI:
            for snd_idx in cls.APPLI[application]["SNDMUTE"]:
                snd_volume = cls.APPLI[application]["SOUNDS"][snd_idx].get_volume()
                if snd_volume == 0:
                    cls.APPLI[application]["SOUNDS"][snd_idx].set_volume(
                        cls.APPLI[application]["SNDMUTE"].get(snd_idx, 1))
            cls.APPLI[application]["SNDMUTE"].clear()

    @classmethod
    def sound_fadeout(cls, application, idx, time):
        if application in cls.APPLI:
            if idx in cls.APPLI[application]["SOUNDS"]:
                cls.APPLI[application]["SOUNDS"][idx].fadeout(time)

    @classmethod
    def unload_sound(cls, application, idx):
        if application in cls.APPLI:
            if idx in cls.APPLI[application]["SOUNDS"]:
                if cls.DEBUG:
                    fprint("Unloading Sound", idx, "pour", application)
                cls.APPLI[application]["SOUNDS"].pop(idx)

    @classmethod
    def load_sound(cls, application, sound_file, volume=1):
        if application in cls.APPLI:
            idx = cls.APPLI[application]["sound_index"]
            if cls.DEBUG:
                fprint("Loading Sound", idx, "pour", application)
            try:
                sound = pygame.mixer.Sound(sound_file)
                sound.set_volume(volume)
                cls.APPLI[application]["SOUNDS"][idx] = sound
                if cls.MUTE:
                    snd_volume = sound.get_volume()
                    cls.APPLI[application]["SNDMUTE"][idx] = snd_volume
                    sound.set_volume(0)

            except Exception as e:
                fprint("SoundEffect Error:", e)
                return False

            cls.APPLI[application]["sound_index"] += 1
            return idx
        return False

    @classmethod
    def wait_channel(cls, channel, callback):
        while channel.get_busy():
            sleep(0.5)
        callback()

    @classmethod
    def play_sound(cls, application, idx, callback=None):
        if application in cls.APPLI:
            if idx in cls.APPLI[application]["SOUNDS"] and (
              len(cls.APPLI[application]["CHANNELS"]) < cls.APPLI[application]["max_channels"]):
                cls.remove_appli_unused_sound_channels(application)
                channel = cls.APPLI[application]["SOUNDS"][idx].play()
                if channel:
                    channel_index = min(
                        [x for x in range(1, 1+cls.APPLI[application]["max_channels"]) if x not in cls.APPLI[application]["CHANNELS"]])
                    if cls.DEBUG:
                        fprint("Play Sound", idx, "pour", application, "sur channel", channel_index)
                    cls.APPLI[application]["CHANNELS"][channel_index] = channel
                    if callback:
                        Thread(target=cls.wait_channel, args=(channel, callback)).start()
                    return channel_index

        if callback:
            callback()
                        
    @classmethod
    def channel_action(cls, action, application, idx):
        if application in cls.APPLI:
            if idx in cls.APPLI[application]["CHANNELS"]:
                if action.upper() == "STOP":
                    cls.APPLI[application]["CHANNELS"][idx].stop()
                    del cls.APPLI[application]["CHANNELS"][idx]
                elif action.upper() == "PLAY":
                    cls.APPLI[application]["CHANNELS"][idx].play()
                elif action.upper() == "PAUSE":
                    cls.APPLI[application]["CHANNELS"][idx].pause()
                elif action.upper() == "UNPAUSE":
                    cls.APPLI[application]["CHANNELS"][idx].unpause()
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
    fprint("Nettoyage: OK !")


if __name__ == "__main__":
    fprint("Compilation: OK")
    import os

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
