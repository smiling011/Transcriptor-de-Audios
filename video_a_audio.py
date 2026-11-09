"""
video_a_audio.py
----------------
Extrae el audio de un video y, opcionalmente, lo transcribe a texto.

Requisitos:
  1) FFmpeg instalado y en el PATH
       - Windows: winget install ffmpeg   (o descargar de https://ffmpeg.org)
       - macOS:   brew install ffmpeg
       - Linux:   sudo apt install ffmpeg
  2) Solo si quieres transcribir:
       pip install faster-whisper

Uso:
  python video_a_audio.py mi_video.mp4
  python video_a_audio.py mi_video.mp4 --formato mp3
  python video_a_audio.py mi_video.mp4 --transcribir
  python video_a_audio.py mi_video.mp4 --transcribir --modelo medium --idioma es
"""

import argparse
import os
import shutil
import wave

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
import subprocess
import sys
from pathlib import Path


def extraer_audio(video: Path, formato: str = "wav") -> Path:
    """Convierte el video a audio. WAV mono 16 kHz es el ideal para transcribir."""
    if not video.exists():
        sys.exit(f"❌ No se encontró el archivo: {video}")
    if shutil.which("ffmpeg") is None:
        sys.exit("❌ FFmpeg no está instalado o no está en el PATH.")

    salida = video.with_suffix(f".{formato}")

    comando = ["ffmpeg", "-y", "-i", str(video), "-vn"]  # -vn = sin video
    if formato == "wav":
        comando += ["-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le"]
    elif formato == "mp3":
        comando += ["-ac", "1", "-ar", "16000", "-b:a", "64k"]
    comando.append(str(salida))

    print(f"🎬 Extrayendo audio de: {video.name}")
    resultado = subprocess.run(comando, capture_output=True, text=True)
    if resultado.returncode != 0:
        sys.exit(f"❌ Error de FFmpeg:\n{resultado.stderr[-1500:]}")

    print(f"✅ Audio guardado en: {salida}")
    return salida


def formatear_tiempo(segundos: float) -> str:
    h, resto = divmod(int(segundos), 3600)
    m, s = divmod(resto, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


def cargar_wav_16k(audio: Path):
    """Lee el WAV (mono, 16 kHz, 16 bits) como arreglo numpy, sin depender de la librería 'av'."""
    import numpy as np

    if audio.suffix.lower() != ".wav":
        # Asegura un WAV compatible si el audio vino en otro formato (p. ej. mp3)
        wav = audio.with_name(audio.stem + "_16k.wav")
        subprocess.run(["ffmpeg", "-y", "-i", str(audio), "-ac", "1", "-ar", "16000",
                        "-c:a", "pcm_s16le", str(wav)], capture_output=True, check=True)
        audio = wav

    with wave.open(str(audio), "rb") as f:
        datos = f.readframes(f.getnframes())
    return np.frombuffer(datos, dtype=np.int16).astype(np.float32) / 32768.0


def transcribir(audio: Path, modelo: str = "small", idioma: str | None = "es") -> Path:
    """Transcribe el audio con faster-whisper y guarda un .txt con marcas de tiempo."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("❌ Falta la librería. Instálala con: pip install faster-whisper")

    print(f"📝 Transcribiendo con el modelo '{modelo}' (la primera vez se descarga)...")
    whisper = WhisperModel(modelo, device="auto", compute_type="int8")
    muestras = cargar_wav_16k(audio)
    segmentos, info = whisper.transcribe(muestras, language=idioma, vad_filter=True)

    salida = audio.with_suffix(".txt")
    with open(salida, "w", encoding="utf-8") as f:
        for seg in segmentos:
            linea = f"[{formatear_tiempo(seg.start)} - {formatear_tiempo(seg.end)}] {seg.text.strip()}"
            print(linea)
            f.write(linea + "\n")

    print(f"✅ Transcripción guardada en: {salida} (idioma detectado: {info.language})")
    return salida


def main():
    parser = argparse.ArgumentParser(description="Convierte un video en audio y opcionalmente lo transcribe.")
    parser.add_argument("video", type=Path, help="Ruta del video (mp4, mkv, mov, avi, webm...)")
    parser.add_argument("--formato", choices=["wav", "mp3"], default="wav", help="Formato de salida (por defecto wav)")
    parser.add_argument("--transcribir", action="store_true", help="Además, transcribir el audio a texto")
    parser.add_argument("--modelo", default="small",
                        help="Modelo Whisper: tiny, base, small, medium, large-v3 (más grande = más preciso y lento)")
    parser.add_argument("--idioma", default="es", help="Código de idioma (es, en...). Usa 'auto' para detectarlo")
    args = parser.parse_args()

    audio = extraer_audio(args.video, args.formato)
    if args.transcribir:
        transcribir(audio, args.modelo, None if args.idioma == "auto" else args.idioma)


if __name__ == "__main__":
    main()