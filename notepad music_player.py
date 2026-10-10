import threading
import vlc
import yt_dlp


class MusicPlayer:

    def __init__(self):

        self.instance = vlc.Instance(
            "--no-video",
            "--quiet"
        )

        self.player = self.instance.media_player_new()

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

            print(f"MUSIC: Searching for {song}...")

            options = {
                "quiet": True,
                "no_warnings": True,
                "extract_flat": True,
                "noplaylist": True
            }

            with yt_dlp.YoutubeDL(options) as ydl:

                result = ydl.extract_info(
                    "ytsearch1:" + song,
                    download=False
                )

            entries = result.get("entries", [])

            if not entries:

                return f"I couldn't find {song}, boss."

            video = entries[0]

            video_id = video.get("id")

            if not video_id:

                return f"I couldn't find {song}, boss."

            print("MUSIC: Found video:", video_id)

            # Get actual audio stream
            stream_options = {
                "quiet": True,
                "no_warnings": True,
                "format": "bestaudio/best"
            }

            with yt_dlp.YoutubeDL(stream_options) as ydl:

                info = ydl.extract_info(
                    "https://www.youtube.com/watch?v=" + video_id,
                    download=False
                )

            stream_url = info.get("url")

            if not stream_url:

                return "I couldn't get the audio stream, boss."

            media = self.instance.media_new(stream_url)

            self.player.set_media(media)

            self.player.audio_set_volume(
                self.volume
            )

            self.player.play()

            self.current_song = song

            return f"Playing {song}, boss."

        except Exception as error:

            print(
                "MUSIC ERROR:",
                error
            )

            return "I couldn't play that song, boss."

    # =====================================================
    # PAUSE
    # =====================================================

    def pause(self):

        try:

            self.player.pause()

            return "Music paused, boss."

        except Exception:

            return "I couldn't pause the music, boss."

    # =====================================================
    # RESUME
    # =====================================================

    def resume(self):

        try:

            self.player.play()

            return "Music resumed, boss."

        except Exception:

            return "I couldn't resume the music, boss."

    # =====================================================
    # STOP
    # =====================================================

    def stop(self):

        try:

            self.player.stop()

            self.current_song = ""

            return "Music stopped, boss."

        except Exception:

            return "I couldn't stop the music, boss."

    # =====================================================
    # VOLUME UP
    # =====================================================

    def volume_up(self):

        self.volume = min(
            100,
            self.volume + 10
        )

        self.player.audio_set_volume(
            self.volume
        )

        return f"Volume is now {self.volume} percent, boss."

    # =====================================================
    # VOLUME DOWN
    # =====================================================

    def volume_down(self):

        self.volume = max(
            0,
            self.volume - 10
        )

        self.player.audio_set_volume(
            self.volume
        )

        return f"Volume is now {self.volume} percent, boss."

    # =====================================================
    # MUTE
    # =====================================================

    def mute(self):

        self.player.audio_toggle_mute()

        return "Music muted, boss."

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