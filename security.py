import os
import numpy as np
import sounddevice as sd
from scipy.io import wavfile

from speechbrain.inference.speaker import SpeakerRecognition


# ============================================================
# J.A.R.V.I.S. VOICE SECURITY
#
# ECAPA-TDNN speaker verification
#
# Existing public functions preserved:
#
# record_voice()
# setup_voice()
# load_enrolled_features()
# verify_audio()
# verify_user()
#
# ============================================================


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

SECURITY_DIR = os.path.join(
    BASE_DIR,
    "security"
)

VOICE_PROFILE = os.path.join(
    SECURITY_DIR,
    "enrolled_voice.wav"
)

SAMPLE_RATE = 16000


# ============================================================
# SECURITY SETTINGS
# ============================================================

# IMPORTANT:
#
# Your recent tests:
#
# Your voice:
#     0.5480
#
# Other person's voice:
#     0.2812
#
# Therefore 0.25 was TOO LOW.
#
# Start with 0.40.
#
# We can calibrate this later using more samples.
#
MATCH_THRESHOLD = 0.40


# Minimum microphone RMS.
MIN_RMS = 0.008

# Minimum microphone peak.
MIN_PEAK = 0.03

# Minimum percentage of frames containing signal.
MIN_ACTIVITY_RATIO = 0.05


# ============================================================
# LOAD ECAPA MODEL
# ============================================================

print()
print("=" * 60)
print("J.A.R.V.I.S. VOICE SECURITY")
print("=" * 60)

print("Loading ECAPA speaker-recognition model...")

try:

    verification = SpeakerRecognition.from_hparams(
        source="speechbrain/spkrec-ecapa-voxceleb"
    )

    print("✅ ECAPA SPEAKER MODEL READY")

except Exception as error:

    verification = None

    print()
    print("❌ ECAPA MODEL FAILED TO LOAD")
    print(error)


# ============================================================
# RECORD VOICE
# ============================================================

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


# ============================================================
# CHECK WHETHER REAL VOICE/AUDIO EXISTS
# ============================================================

def audio_has_voice(audio):

    if audio is None:
        return False

    audio = np.asarray(
        audio,
        dtype=np.float32
    )

    if len(audio) < int(
        0.25 * SAMPLE_RATE
    ):

        print(
            "VOICE SECURITY: Recording too short."
        )

        return False

    # Remove DC offset.
    audio = audio - np.mean(audio)

    # --------------------------------------------------------
    # OVERALL SIGNAL
    # --------------------------------------------------------

    rms = float(
        np.sqrt(
            np.mean(
                np.square(audio)
            )
        )
    )

    peak = float(
        np.max(
            np.abs(audio)
        )
    )

    print(
        f"VOICE SECURITY: "
        f"RMS={rms:.5f} "
        f"PEAK={peak:.5f}"
    )

    # --------------------------------------------------------
    # SILENCE CHECK
    # --------------------------------------------------------

    if rms < MIN_RMS:

        print(
            "VOICE SECURITY: Silence detected."
        )

        return False

    if peak < MIN_PEAK:

        print(
            "VOICE SECURITY: "
            "No usable voice signal."
        )

        return False

    # --------------------------------------------------------
    # FRAME ACTIVITY
    # --------------------------------------------------------

    frame_size = int(
        0.050 * SAMPLE_RATE
    )

    active_frames = 0
    total_frames = 0

    for start in range(
        0,
        len(audio) - frame_size + 1,
        frame_size
    ):

        frame = audio[
            start:start + frame_size
        ]

        frame_rms = float(
            np.sqrt(
                np.mean(
                    np.square(frame)
                )
            )
        )

        total_frames += 1

        if frame_rms > MIN_RMS:

            active_frames += 1

    if total_frames == 0:

        return False

    activity_ratio = (
        active_frames /
        total_frames
    )

    print(
        f"VOICE SECURITY: "
        f"activity={activity_ratio:.2%}"
    )

    if activity_ratio < MIN_ACTIVITY_RATIO:

        print(
            "VOICE SECURITY: "
            "No clear speech detected."
        )

        return False

    return True


# ============================================================
# PREPARE AUDIO
# ============================================================

def prepare_audio(audio):

    if audio is None:

        return None

    audio = np.asarray(
        audio,
        dtype=np.float32
    )

    if len(audio) == 0:

        return None

    # Remove DC offset.
    audio = audio - np.mean(audio)

    # Prevent invalid values.
    audio = np.nan_to_num(
        audio,
        nan=0.0,
        posinf=0.0,
        neginf=0.0
    )

    return audio


# ============================================================
# SAVE VOICE PROFILE
# ============================================================

def setup_voice():

    os.makedirs(
        SECURITY_DIR,
        exist_ok=True
    )

    print()
    print("=" * 60)
    print("J.A.R.V.I.S. VOICE ENROLLMENT")
    print("=" * 60)

    print()
    print("We are going to create a NEW voice profile.")
    print()
    print("Please:")
    print("  • Stay close to the microphone.")
    print("  • Speak normally.")
    print("  • Use your natural voice.")
    print("  • Avoid background noise.")
    print("  • Speak continuously for several seconds.")
    print()

    input(
        "Press ENTER when ready..."
    )

    audio = record_voice(
        25
    )

    if audio is None:

        print(
            "❌ Recording failed."
        )

        return False

    # --------------------------------------------------------
    # CHECK RECORDING
    # --------------------------------------------------------

    if not audio_has_voice(audio):

        print()
        print(
            "❌ No clear voice detected."
        )

        print(
            "Please run enrollment again."
        )

        return False

    audio = prepare_audio(
        audio
    )

    if audio is None:

        print(
            "❌ Could not prepare recording."
        )

        return False

    # --------------------------------------------------------
    # SAVE PROFILE
    # --------------------------------------------------------

    wav_audio = np.int16(
        np.clip(
            audio,
            -1.0,
            1.0
        )
        * 32767
    )

    wavfile.write(
        VOICE_PROFILE,
        SAMPLE_RATE,
        wav_audio
    )

    print()
    print("=" * 60)
    print("✅ VOICE PROFILE CREATED")
    print("=" * 60)

    print()
    print("Saved to:")
    print(
        VOICE_PROFILE
    )

    return True


# ============================================================
# GET ENROLLED AUDIO
# ============================================================

def get_enrolled_audio():

    if not os.path.exists(
        VOICE_PROFILE
    ):

        return None

    try:

        sample_rate, audio = wavfile.read(
            VOICE_PROFILE
        )

        # ----------------------------------------------------
        # SAMPLE RATE CHECK
        # ----------------------------------------------------

        if sample_rate != SAMPLE_RATE:

            print(
                "VOICE PROFILE ERROR:"
            )

            print(
                f"Expected {SAMPLE_RATE} Hz, "
                f"got {sample_rate} Hz."
            )

            return None

        # ----------------------------------------------------
        # CONVERT TO FLOAT32
        # ----------------------------------------------------

        if audio.dtype == np.int16:

            audio = (
                audio.astype(
                    np.float32
                )
                / 32767.0
            )

        else:

            audio = audio.astype(
                np.float32
            )

        # ----------------------------------------------------
        # CHECK PROFILE
        # ----------------------------------------------------

        if not audio_has_voice(
            audio
        ):

            print(
                "VOICE PROFILE ERROR: "
                "No usable speech found."
            )

            return None

        audio = prepare_audio(
            audio
        )

        return audio

    except Exception as error:

        print(
            "VOICE PROFILE ERROR:",
            error
        )

        return None


# ============================================================
# LOAD ENROLLED FEATURES
#
# Compatibility function.
#
# ECAPA works directly from the enrolled waveform,
# so this returns the enrolled audio.
# ============================================================

def load_enrolled_features():

    return get_enrolled_audio()


# ============================================================
# ECAPA VERIFICATION HELPER
# ============================================================

def compare_voice(
    enrolled_audio,
    test_audio,
    threshold=MATCH_THRESHOLD
):

    if verification is None:

        print(
            "❌ ECAPA model is not available."
        )

        return False

    if enrolled_audio is None:

        return False

    if test_audio is None:

        return False

    try:

        import torch

        # ----------------------------------------------------
        # CONVERT TO TORCH
        # ----------------------------------------------------

        enrolled_tensor = torch.tensor(
            enrolled_audio,
            dtype=torch.float32
        ).unsqueeze(
            0
        )

        test_tensor = torch.tensor(
            test_audio,
            dtype=torch.float32
        ).unsqueeze(
            0
        )

        # ----------------------------------------------------
        # ECAPA SPEAKER VERIFICATION
        # ----------------------------------------------------

        with torch.no_grad():

            score, prediction = (
                verification.verify_batch(
                    enrolled_tensor,
                    test_tensor
                )
            )

        score_value = float(
            score.squeeze().item()
        )

        prediction_value = int(
            prediction.squeeze().item()
        )

        print()
        print("=" * 60)

        print(
            f"ECAPA SPEAKER SCORE: "
            f"{score_value:.4f}"
        )

        print(
            f"ECAPA PREDICTION: "
            f"{prediction_value}"
        )

        print(
            f"SECURITY THRESHOLD: "
            f"{threshold:.4f}"
        )

        print("=" * 60)

        # ----------------------------------------------------
        # SECURITY DECISION
        #
        # IMPORTANT:
        #
        # We require BOTH:
        #
        # 1. SpeechBrain prediction == 1
        #
        # AND
        #
        # 2. Our own stronger score threshold
        #
        # This prevents a score such as 0.2812 from
        # being accepted simply because SpeechBrain
        # returned prediction 1.
        # ----------------------------------------------------

        if (
            prediction_value == 1
            and
            score_value >= threshold
        ):

            return True

        return False

    except Exception as error:

        print()
        print(
            "VOICE VERIFICATION ERROR:"
        )

        print(error)

        return False


# ============================================================
# VERIFY EXISTING SPEECHRECOGNITION AUDIO
#
# IMPORTANT:
#
# This does NOT record another microphone sample.
#
# voice_ai.py gives us its already-recorded AudioData.
#
# ============================================================

def verify_audio(
    audio,
    announce=False,
    threshold=MATCH_THRESHOLD
):

    if verification is None:

        print(
            "❌ ECAPA model is not available."
        )

        return False

    if audio is None:

        return False

    # --------------------------------------------------------
    # LOAD ENROLLED PROFILE
    # --------------------------------------------------------

    enrolled_audio = get_enrolled_audio()

    if enrolled_audio is None:

        print()
        print(
            "❌ No valid enrolled voice profile."
        )

        print(
            "Run your voice enrollment first."
        )

        return False

    try:

        # ----------------------------------------------------
        # CONVERT SPEECHRECOGNITION AudioData
        # ----------------------------------------------------

        wav_data = audio.get_wav_data(
            convert_rate=SAMPLE_RATE,
            convert_width=2
        )

        test_audio = np.frombuffer(
            wav_data,
            dtype=np.int16
        ).astype(
            np.float32
        ) / 32767.0

        # ----------------------------------------------------
        # AUDIO GATE
        # ----------------------------------------------------

        if not audio_has_voice(
            test_audio
        ):

            print()
            print(
                "🔒 VOICE REJECTED - "
                "no clear speech detected."
            )

            return False

        # ----------------------------------------------------
        # PREPARE AUDIO
        # ----------------------------------------------------

        test_audio = prepare_audio(
            test_audio
        )

        if test_audio is None:

            print(
                "🔒 VOICE REJECTED - "
                "invalid audio."
            )

            return False

        # ----------------------------------------------------
        # ECAPA COMPARISON
        # ----------------------------------------------------

        authenticated = compare_voice(
            enrolled_audio,
            test_audio,
            threshold
        )

        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        if authenticated:

            if announce:

                print()
                print(
                    "🔓 VOICE AUTHENTICATION SUCCESSFUL"
                )

            return True

        print()
        print(
            "🔒 VOICE REJECTED"
        )

        return False

    except Exception as error:

        print()
        print(
            "VOICE VERIFICATION ERROR:"
        )

        print(error)

        return False


# ============================================================
# DIRECT MICROPHONE VERIFICATION
#
# Kept for compatibility with existing JARVIS code.
# ============================================================

def verify_user():

    print()
    print("=" * 60)
    print("J.A.R.V.I.S. VOICE AUTHENTICATION")
    print("=" * 60)

    if verification is None:

        print()
        print(
            "❌ ECAPA model is not available."
        )

        return False

    # --------------------------------------------------------
    # PROFILE CHECK
    # --------------------------------------------------------

    if not os.path.exists(
        VOICE_PROFILE
    ):

        print()
        print(
            "❌ No voice profile found."
        )

        print()
        print(
            "Run your voice enrollment first."
        )

        return False

    try:

        # ----------------------------------------------------
        # RECORD TEST VOICE
        # ----------------------------------------------------

        test_audio = record_voice(
            4
        )

        if test_audio is None:

            return False

        # ----------------------------------------------------
        # AUDIO GATE
        # ----------------------------------------------------

        if not audio_has_voice(
            test_audio
        ):

            print()
            print(
                "🔒 ACCESS DENIED"
            )

            print(
                "No clear speech detected."
            )

            return False

        # ----------------------------------------------------
        # PREPARE TEST AUDIO
        # ----------------------------------------------------

        test_audio = prepare_audio(
            test_audio
        )

        if test_audio is None:

            return False

        # ----------------------------------------------------
        # LOAD ENROLLED PROFILE
        # ----------------------------------------------------

        enrolled_audio = get_enrolled_audio()

        if enrolled_audio is None:

            print(
                "❌ Could not load enrolled voice."
            )

            return False

        # ----------------------------------------------------
        # ECAPA COMPARISON
        # ----------------------------------------------------

        authenticated = compare_voice(
            enrolled_audio,
            test_audio,
            MATCH_THRESHOLD
        )

        # ----------------------------------------------------
        # ACCESS DECISION
        # ----------------------------------------------------

        if authenticated:

            print()
            print(
                "🔓 ACCESS GRANTED"
            )

            print(
                "Welcome back, boss."
            )

            return True

        print()
        print(
            "🔒 ACCESS DENIED"
        )

        print(
            "Voice does not match."
        )

        return False

    except Exception as error:

        print()
        print(
            "VOICE VERIFICATION ERROR:"
        )

        print(error)

        return False