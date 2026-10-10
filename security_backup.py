import os
import numpy as np
import sounddevice as sd
from scipy.io import wavfile


# ============================================================
# J.A.R.V.I.S. VOICE SECURITY
#
# IMPORTANT:
# Existing functions are preserved:
#
# record_voice()
# setup_voice()
# load_enrolled_features()
# verify_audio()
# verify_user()
#
# This version adds a strict silence / background-noise gate.
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

# Minimum actual microphone signal.
MIN_RMS = 0.012

# Minimum amount of the recording that must contain
# meaningful audio.
MIN_ACTIVITY_RATIO = 0.15

# Speech frames must be above the estimated noise floor.
NOISE_MULTIPLIER = 2.5

# Voice similarity threshold.
MATCH_THRESHOLD = 93.0


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
# CHECK WHETHER REAL AUDIO EXISTS
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

        return False

    # Remove DC offset.
    audio = audio - np.mean(audio)

    # --------------------------------------------------------
    # OVERALL VOLUME CHECK
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

    # Absolutely quiet / nearly silent microphone.
    if rms < MIN_RMS:

        print(
            "VOICE SECURITY: Silence detected."
        )

        return False

    if peak < 0.03:

        print(
            "VOICE SECURITY: No usable voice signal."
        )

        return False

    # --------------------------------------------------------
    # SPLIT AUDIO INTO 50ms FRAMES
    # --------------------------------------------------------

    frame_size = int(
        0.050 * SAMPLE_RATE
    )

    frame_rms_values = []

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

        frame_rms_values.append(
            frame_rms
        )

    if not frame_rms_values:

        return False

    frame_rms_values = np.asarray(
        frame_rms_values,
        dtype=np.float32
    )

    # --------------------------------------------------------
    # ESTIMATE BACKGROUND NOISE
    # --------------------------------------------------------

    noise_floor = float(
        np.percentile(
            frame_rms_values,
            20
        )
    )

    speech_level = max(
        MIN_RMS * 0.8,
        noise_floor * NOISE_MULTIPLIER
    )

    active_frames = np.sum(
        frame_rms_values >= speech_level
    )

    activity_ratio = (
        active_frames
        /
        len(frame_rms_values)
    )

    # Too little actual audio.
    if activity_ratio < MIN_ACTIVITY_RATIO:

        print(
            "VOICE SECURITY: "
            "No clear speech detected."
        )

        return False

    return True


# ============================================================
# NORMALIZE AUDIO
# ============================================================
## 1. Replace `normalize_audio()` with this


def normalize_audio(audio):

    if audio is None or len(audio) == 0:
        return None

    audio = np.asarray(
        audio,
        dtype=np.float32
    )

    # --------------------------------------------------------
    # CHECK RAW MICROPHONE SIGNAL FIRST
    # --------------------------------------------------------

    # Remove DC offset
    audio = audio - np.mean(audio)

    # Measure the ORIGINAL microphone level.
    # IMPORTANT:
    # Do this BEFORE normalization because normalization
    # can make tiny background noise look like speech.
    raw_rms = np.sqrt(
        np.mean(
            np.square(audio)
        )
    )

    raw_peak = np.max(
        np.abs(audio)
    )

    print(
        f"VOICE SECURITY: RMS={raw_rms:.5f} "
        f"PEAK={raw_peak:.5f}"
    )

    # --------------------------------------------------------
    # HARD SILENCE / VERY LOW NOISE REJECTION
    # --------------------------------------------------------

    if raw_rms < 0.012:

        print(
            "VOICE SECURITY: Recording is too quiet."
        )

        return None

    if raw_peak < 0.04:

        print(
            "VOICE SECURITY: No strong audio detected."
        )

        return None

    # --------------------------------------------------------
    # NORMALIZE ONLY AFTER SILENCE CHECK
    # --------------------------------------------------------

    maximum = raw_peak

    if maximum <= 0:

        return None

    audio = audio / maximum

    return audio


## 2. In `extract_features()`, replace the current beginning




def extract_features(audio):





    if audio is None or len(audio) == 0:
        return None

    # --------------------------------------------------------
    # KEEP ORIGINAL AUDIO FOR VOICE ACTIVITY ANALYSIS
    # --------------------------------------------------------

    raw_audio = np.asarray(
        audio,
        dtype=np.float32
    )

    raw_audio = raw_audio - np.mean(
        raw_audio
    )

    raw_rms = np.sqrt(
        np.mean(
            np.square(raw_audio)
        )
    )

    raw_peak = np.max(
        np.abs(raw_audio)
    )

    print(
        f"VOICE SECURITY: "
        f"raw RMS={raw_rms:.5f}, "
        f"peak={raw_peak:.5f}"
    )

    # --------------------------------------------------------
    # FIRST GATE: ABSOLUTE SILENCE / VERY LOW SIGNAL
    # --------------------------------------------------------

    if raw_rms < 0.012:

        print(
            "VOICE SECURITY: "
            "No clear speech detected."
        )

        return None

    if raw_peak < 0.04:

        print(
            "VOICE SECURITY: "
            "Audio signal too weak."
        )

        return None

    # --------------------------------------------------------
    # VOICE ACTIVITY CHECK
    # --------------------------------------------------------

    chunk_size = int(
        0.050 * SAMPLE_RATE
    )

    active_chunks = 0
    total_chunks = 0

    for start in range(
        0,
        len(raw_audio),
        chunk_size
    ):

        chunk = raw_audio[
            start:start + chunk_size
        ]

        if len(chunk) < chunk_size:
            continue

        chunk_rms = np.sqrt(
            np.mean(
                np.square(chunk)
            )
        )

        total_chunks += 1

        # Use RAW audio here.
        # Do NOT use normalized audio.
        if chunk_rms > 0.018:

            active_chunks += 1

    if total_chunks == 0:

        return None

    activity_ratio = (
        active_chunks /
        total_chunks
    )

    print(
        f"VOICE SECURITY: "
        f"activity={activity_ratio:.2%}"
    )

    # Require enough meaningful audio.
    if activity_ratio < 0.12:

        print(
            "VOICE SECURITY: "
            "No clear speech detected."
        )

        return None

    # --------------------------------------------------------
    # NOW NORMALIZE
    # --------------------------------------------------------

    audio = normalize_audio(
        raw_audio
    )

    if audio is None:

        return None


## 3. Keep the rest of your existing `extract_features()` unchanged

# ============================================================
# FEATURE EXTRACTION
# ============================================================

def extract_features(audio):

    audio = normalize_audio(
        audio
    )

    if audio is None:

        return None

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

        frame = frame * np.hamming(
            len(frame)
        )

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

        frames.append(
            features
        )

    if not frames:

        return None

    features = np.asarray(
        frames,
        dtype=np.float32
    )

    fingerprint = np.concatenate(
        [
            np.mean(
                features,
                axis=0
            ),

            np.std(
                features,
                axis=0
            ),

            np.median(
                features,
                axis=0
            )
        ]
    )

    norm = np.linalg.norm(
        fingerprint
    )

    if norm <= 0:

        return None

    fingerprint = (
        fingerprint / norm
    )

    return fingerprint


# ============================================================
# COSINE SIMILARITY
# ============================================================

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


# ============================================================
# CREATE VOICE PROFILE
# ============================================================

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

    audio = record_voice(
        5
    )

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


# ============================================================
# LOAD ENROLLED VOICE
# ============================================================

def load_enrolled_features():

    if not os.path.exists(
        VOICE_PROFILE
    ):

        return None

    try:

        sample_rate, enrolled_audio = (
            wavfile.read(
                VOICE_PROFILE
            )
        )

        if sample_rate != SAMPLE_RATE:

            print(
                "VOICE PROFILE ERROR:"
            )

            print(
                f"Expected {SAMPLE_RATE} Hz, "
                f"got {sample_rate} Hz."
            )

            return None

        enrolled_audio = (
            enrolled_audio.astype(
                np.float32
            )
            / 32767.0
        )

        return extract_features(
            enrolled_audio
        )

    except Exception as error:

        print(
            "VOICE PROFILE ERROR:",
            error
        )

        return None


# ============================================================
# VERIFY EXISTING AUDIO
#
# IMPORTANT:
# This function DOES NOT record another sample.
#
# It receives the audio that voice_ai.py already captured.
# ============================================================

def verify_audio(
    audio,
    announce=False,
    threshold=MATCH_THRESHOLD
):

    if audio is None:

        return False

    enrolled_features = (
        load_enrolled_features()
    )

    if enrolled_features is None:

        print(
            "❌ No valid enrolled voice profile."
        )

        return False

    try:

        # Convert SpeechRecognition AudioData
        # into raw PCM audio.

        wav_data = audio.get_wav_data(
            convert_rate=SAMPLE_RATE,
            convert_width=2
        )

        audio_array = np.frombuffer(
            wav_data,
            dtype=np.int16
        ).astype(
            np.float32
        ) / 32767.0

        # ====================================================
        # CRITICAL SILENCE GATE
        # ====================================================

        if not audio_has_voice(
            audio_array
        ):

            print(
                "🔒 VOICE REJECTED - "
                "no clear speech detected."
            )

            return False

        # ====================================================
        # EXTRACT VOICE FEATURES
        # ====================================================

        test_features = extract_features(
            audio_array
        )

        if test_features is None:

            print(
                "🔒 VOICE REJECTED - "
                "voice features unavailable."
            )

            return False

        # ====================================================
        # COMPARE
        # ====================================================

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

        print(
            f"VOICE MATCH: {score:.2f}%"
        )

        # ====================================================
        # DECISION
        # ====================================================

        if score >= threshold:

            if announce:

                print(
                    "🔓 VOICE AUTHENTICATION SUCCESSFUL"
                )

            return True

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
# OLD VERIFICATION FUNCTION
#
# KEPT FOR COMPATIBILITY WITH YOUR EXISTING SYSTEM.
# ============================================================

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

        test_audio = record_voice(
            4
        )

        if test_audio is None:

            return False

        enrolled_features = (
            load_enrolled_features()
        )

        test_features = extract_features(
            test_audio
        )

        if (
            enrolled_features is None
            or
            test_features is None
        ):

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

        if score >= MATCH_THRESHOLD:

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