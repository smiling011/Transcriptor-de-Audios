# video_a_audio.py

Extrae el audio de un video y, opcionalmente, lo **transcribe a texto** (genera un `.txt` con marcas de tiempo). La transcripción corre en tu propio computador con [faster-whisper](https://github.com/SYSTRAN/faster-whisper): es gratis, sin límite de duración y no sube nada a internet.

---

## 1. Requisitos (se instalan una sola vez)

### a) Python 3.12
Las librerías todavía no funcionan con Python 3.15, así que usa la versión **3.12**.

- Instálala desde una ventana de comandos (CMD):
  ```
  py install 3.12
  ```
- O descárgala de https://www.python.org/downloads/ (marca la casilla **"Add python.exe to PATH"** al instalar).

Comprueba que quedó instalada:
```
py -3.12 --version
```

### b) FFmpeg
Es lo que separa el audio del video.
```
winget install ffmpeg
```
> Después de instalarlo, **cierra y vuelve a abrir** la ventana de comandos.

### c) La librería de transcripción
```
py -3.12 -m pip install faster-whisper
```

---

## 2. Dónde poner el archivo

Deja `video_a_audio.py` en la **misma carpeta** donde está tu video (por ejemplo, `Descargas`).

Para situarte en esa carpeta desde la ventana de comandos:
```
cd C:\Users\NetW\Downloads
```

---

## 3. Cómo transcribir un video

```
py -3.12 video_a_audio.py "nombre del video.mp4" --transcribir
```

- Escribe el **nombre completo con su extensión** (`.mp4`, `.mkv`, `.mov`, etc.), entre comillas si tiene espacios.
- Truco: escribe las primeras letras del nombre y pulsa la tecla **Tab** para que Windows lo complete solo.

Al terminar, en la misma carpeta quedan dos archivos:
- `nombre del video.wav` → el audio extraído
- `nombre del video.txt` → la transcripción con marcas de tiempo

Ejemplo de una línea del `.txt`:
```
[00:00:05 - 00:00:11] Buenos días a todos, vamos a empezar la sesión.
```

---

## 4. Opciones útiles

| Quiero... | Comando |
|-----------|---------|
| Solo sacar el audio, sin transcribir | `py -3.12 video_a_audio.py "video.mp4"` |
| Más precisión (más lento) | `py -3.12 video_a_audio.py "video.mp4" --transcribir --modelo medium` |
| Más velocidad (menos preciso) | `py -3.12 video_a_audio.py "video.mp4" --transcribir --modelo base` |
| Audio en MP3 en vez de WAV | `py -3.12 video_a_audio.py "video.mp4" --formato mp3` |
| Detectar el idioma automáticamente | `py -3.12 video_a_audio.py "video.mp4" --transcribir --idioma auto` |

**Modelos disponibles** (de más rápido a más preciso): `tiny`, `base`, `small` (por defecto), `medium`, `large-v3`.

---

## 5. Cuánto tarda

En un computador **sin tarjeta gráfica**, la transcripción tarda aproximadamente lo mismo que dura el video, o un poco más. Un video de 2 horas puede tomar entre 1 y 3 horas con el modelo `small`. Déjalo corriendo y listo. La **primera vez** descarga el modelo (unos pocos cientos de MB); las siguientes ya no.

---

## 6. Problemas frecuentes

- **`Python was not found`** → no escribiste `py -3.12` o Python 3.12 no está instalado (ver paso 1a).
- **`pip no se reconoce`** → usa siempre `py -3.12 -m pip install ...`, nunca `pip` a secas.
- **`No se encontró el archivo`** → falta la extensión (`.mp4`) o el video no está en esa carpeta. Usa `dir /b` para ver los nombres exactos.
- **Error al instalar con `av` / "building wheel"** → estás usando Python 3.15. Cambia a `py -3.12`.
- **`ffmpeg no está instalado`** → instálalo (paso 1b) y reabre la ventana de comandos.