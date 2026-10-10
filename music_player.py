
import time
import vlc
import yt_dlp


class MusicPlayer:

    def __init__(self):

        self.instance = vlc.Instance(
            "--no-video",
            "--quiet"
        )

        self.player = self.instance.media_player_new()

        self.media = None
        self.current_song = ""
        self.volume = 80

    # =====================================================
    # PLAY
    # =====================================================

    def play(self, song):

        song = song.strip()

        if not song:
            return "Tell me which song you want me to play, boss."

        try:

            print(
                f"MUSIC: Searching for {song}..."
            )

            search_options = {
                "quiet": True,
                "no_warnings": True,
                "extract_flat": True,
                "noplaylist": True
            }

            with yt_dlp.YoutubeDL(
                search_options
            ) as ydl:

                result = ydl.extract_info(
                    "ytsearch1:" + song,
                    download=False
                )

            entries = result.get(
                "entries",
                []
            )

            if not entries:

                return (
                    f"I couldn't find {song}, boss."
                )

            video = entries[0]

            video_id = video.get("id")

            if not video_id:

                return (
                    f"I couldn't find {song}, boss."
                )

            print(
                "MUSIC: Found video:",
                video_id
            )

            video_url = (
                "https://www.youtube.com/watch?v="
                + video_id
            )

            # =================================================
            # GET AUDIO STREAM
            # =================================================

            stream_options = {

                "quiet": True,

                "no_warnings": True,

                "format": "bestaudio/best",

                "noplaylist": True

            }

            with yt_dlp.YoutubeDL(
                stream_options
            ) as ydl:

                info = ydl.extract_info(
                    video_url,
                    download=False
                )

            stream_url = info.get("url")

            if not stream_url:

                return (
                    "I couldn't get the audio stream, boss."
                )

            print(
                "MUSIC: Audio stream found."
            )

            # =================================================
            # STOP PREVIOUS SONG
            # =================================================

            self.player.stop()

            # =================================================
            # CREATE MEDIA
            # =================================================

            self.media = (
                self.instance.media_new(
                    stream_url
                )
            )

            self.player.set_media(
                self.media
            )

            # =================================================
            # SET VOLUME
            # =================================================

            self.player.audio_set_volume(
                self.volume
            )

            # =================================================
            # PLAY
            # =================================================

            result = self.player.play()

            if result == -1:

                return (
                    "VLC couldn't start the music, boss."
                )

            # =================================================
            # WAIT FOR VLC
            # =================================================

            for _ in range(20):

                time.sleep(0.25)

                state = self.player.get_state()

                if state == vlc.State.Playing:

                    break

                if state == vlc.State.Error:

                    return (
                        "VLC reported an error while "
                        "starting the music, boss."
                    )

            self.current_song = song

            print(
                "MUSIC STATE:",
                self.player.get_state()
            )

            return (
                f"Playing {song}, boss."
            )

        except Exception as error:

            print(
                "MUSIC ERROR:",
                error
            )

            return (
                "I couldn't play that song, boss."
            )

    # =====================================================
    # PAUSE
    # =====================================================

    def pause(self):

        try:

            self.player.pause()

            return (
                "Music paused, boss."
            )

        except Exception:

            return (
                "I couldn't pause the music, boss."
            )

    # =====================================================
    # RESUME
    # =====================================================

    def resume(self):

        try:

            self.player.play()

            return (
                "Music resumed, boss."
            )

        except Exception:

            return (
                "I couldn't resume the music, boss."
            )

    # =====================================================
    # STOP
    # =====================================================

    def stop(self):

        try:

            self.player.stop()

            self.current_song = ""
            self.media = None

            return (
                "Music stopped, boss."
            )

        except Exception:

            return (
                "I couldn't stop the music, boss."
            )

    # =====================================================
    # VOLUME UP
    # =====================================================

    def volume_up(self):

        try:

            self.volume = min(
                100,
                self.volume + 10
            )

            self.player.audio_set_volume(
                self.volume
            )

            return (
                f"Volume is now "
                f"{self.volume} percent, boss."
            )

        except Exception:

            return (
                "I couldn't change the volume, boss."
            )

    # =====================================================
    # VOLUME DOWN
    # =====================================================

    def volume_down(self):

        try:

            self.volume = max(
                0,
                self.volume - 10
            )

            self.player.audio_set_volume(
                self.volume
            )

            return (
                f"Volume is now "
                f"{self.volume} percent, boss."
            )

        except Exception:

            return (
                "I couldn't change the volume, boss."
            )

    # =====================================================
    # MUTE
    # =====================================================

    def mute(self):

        try:

            self.player.audio_toggle_mute()

            return (
                "Music muted, boss."
            )

        except Exception:

            return (
                "I couldn't mute the music, boss."
            )

    # =====================================================
    # STATUS
    # =====================================================

    def is_playing(self):

        try:

            return bool(
                self.player.is_playing()
            )

        except Exception:

            return False

