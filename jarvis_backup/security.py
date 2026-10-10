import os
import numpy as np
import sounddevice as sd
from scipy.io import wavfile


# ============================================================
# JARVIS VOICE SECURITY
# Python 3.13 compatible
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECURITY_DIR = os.path.join(
    BASE_DIR,
    "security"
)

VOICE_PROFILE = os.path.join(
    SECURITY_DIR,
    "enrolled_voice.wav"
)

SAMPLE_RATE = 16000


def record_voice(seconds=5):

    print()
    print("🎙️ LISTENING...")
    print("Speak naturally.")

    try:

        audio = sd.rec(
            int(seconds * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32"
        )

        sd.wait()

        audio = audio.flatten()

        print("✅ Recording complete.")

        return audio

    except Exception as error:

        print()
        print("MICROPHONE ERROR:")
        print(error)

        return None


def normalize_audio(audio):

    if audio is None or len(audio) == 0:
        return None

    audio = np.asarray(
        audio,
        dtype=np.float32
    )

    audio = audio - np.mean(audio)

    maximum = np.max(
        np.abs(audio)
    )

    if maximum > 0:
        audio = audio / maximum

    return audio


def extract_features(audio):

    audio = normalize_audio(audio)

    if audio is None:
        return None

    # Remove very quiet parts
    threshold = 0.02

    mask = np.abs(audio) > threshold

    if np.sum(mask) > 1000:
        audio = audio[mask]

    if len(audio) < 2000:
        return None

    # Divide audio into small frames
    frame_length = int(
        0.025 * SAMPLE_RATE
    )

    frame_step = int(
        0.010 * SAMPLE_RATE
    )

    frames = []

    for start in range(
        0,
        len(audio) - frame_length,
        frame_step
    ):

        frame = audio[
            start:start + frame_length
        ]

        # Hamming window
        frame = frame * np.hamming(
            len(frame)
        )

        # FFT
        spectrum = np.abs(
            np.fft.rfft(frame)
        )

        spectrum += 1e-10

        log_spectrum = np.log(
            spectrum
        )

        features = [

            np.mean(log_spectrum),

            np.std(log_spectrum),

            np.mean(
                log_spectrum[:20]
            ),

            np.mean(
                log_spectrum[20:40]
            ),

            np.mean(
                log_spectrum[40:80]
            ),

            np.mean(
                log_spectrum[80:160]
            ),

            np.mean(
                log_spectrum[160:320]
            ),

            np.mean(
                log_spectrum[320:640]
            )
        ]

        frames.append(features)

    if not frames:
        return None

    features = np.asarray(
        frames,
        dtype=np.float32
    )

    fingerprint = np.concatenate(
        [
            np.mean(features, axis=0),
            np.std(features, axis=0),
            np.median(features, axis=0)
        ]
    )

    norm = np.linalg.norm(
        fingerprint
    )

    if norm > 0:
        fingerprint = (
            fingerprint / norm
        )

    return fingerprint


def cosine_similarity(a, b):

    if a is None or b is None:
        return 0.0

    denominator = (
        np.linalg.norm(a)
        *
        np.linalg.norm(b)
    )

    if denominator == 0:
        return 0.0

    return float(
        np.dot(a, b)
        /
        denominator
    )


def setup_voice():

    os.makedirs(
        SECURITY_DIR,
        exist_ok=True
    )

    print()
    print("=" * 50)
    print("J.A.R.V.I.S. VOICE ENROLLMENT")
    print("=" * 50)

    print()
    print("I will record your voice.")
    print("Speak naturally.")
    print()

    input(
        "Press ENTER when ready..."
    )

    audio = record_voice(5)

    if audio is None:

        print(
            "❌ Recording failed."
        )

        return False

    fingerprint = extract_features(
        audio
    )

    if fingerprint is None:

        print(
            "❌ Could not create voice profile."
        )

        return False

    # Save recording
    wav_audio = np.int16(
        np.clip(
            audio,
            -1,
            1
        )
        * 32767
    )

    wavfile.write(
        VOICE_PROFILE,
        SAMPLE_RATE,
        wav_audio
    )

    print()
    print("=" * 50)
    print("✅ VOICE PROFILE CREATED")
    print("=" * 50)

    print()
    print("Saved to:")

    print(
        VOICE_PROFILE
    )

    return True


def verify_user():

    print()
    print("=" * 50)
    print("J.A.R.V.I.S. VOICE AUTHENTICATION")
    print("=" * 50)

    if not os.path.exists(
        VOICE_PROFILE
    ):

        print()
        print("❌ No voice profile found.")

        print()
        print(
            "Run: python setup_voice.py"
        )

        return False

    try:

        sample_rate, enrolled_audio = (
            wavfile.read(
                VOICE_PROFILE
            )
        )

        enrolled_audio = (
            enrolled_audio.astype(
                np.float32
            )
            / 32767.0
        )

        enrolled_features = (
            extract_features(
                enrolled_audio
            )
        )

        if enrolled_features is None:

            print(
                "❌ Invalid voice profile."
            )

            return False

        test_audio = record_voice(4)

        if test_audio is None:
            return False

        test_features = (
            extract_features(
                test_audio
            )
        )

        if test_features is None:

            print(
                "❌ Could not analyze voice."
            )

            return False

        similarity = cosine_similarity(
            enrolled_features,
            test_features
        )

        score = max(
            0,
            min(
                100,
                similarity * 100
            )
        )

        print()
        print("=" * 50)
        print(
            f"VOICE MATCH SCORE: {score:.2f}%"
        )
        print("=" * 50)

        # Initial security threshold
        threshold = 90.0

        if score >= threshold:

            print()
            print("🔓 ACCESS GRANTED")
            print("Welcome back, boss.")

            return True

        print()
        print("🔒 ACCESS DENIED")
        print("Voice does not match.")

        return False

    except Exception as error:

        print()
        print(
            "VOICE VERIFICATION ERROR:"
        )

        print(error)

        return False