# 🎵 Convertidor de Video a MP3

Aplicación de escritorio para **Windows** que extrae el audio de cualquier video y lo
guarda en formato **MP3** — sin tecnicismos, solo clic y listo.

---

## ▶️ Cómo usarlo (usuarios finales)

### Primera vez (configuración de un solo paso)

1. **Descarga** el repositorio como ZIP → botón verde **Code → Download ZIP**.
2. **Extrae** el ZIP en cualquier carpeta (p. ej. `C:\VideoAMP3`).
3. Haz **doble clic en `setup.bat`**.  
   El asistente descarga automáticamente Python y ffmpeg (necesita internet).
4. Cuando termine, haz **doble clic en `run.bat`** para abrir la aplicación.

> ⚠️ Windows puede mostrar una advertencia de seguridad al ejecutar los archivos `.bat`.
> Haz clic en **"Más información" → "Ejecutar de todas formas"** para continuar.

---

### Usar la aplicación

| Paso | Acción |
|------|--------|
| 1 | Haz clic en **📁 Buscar…** y selecciona tu video |
| 2 | Haz clic en **🎬 Convertir a MP3** |
| 3 | El archivo `.mp3` se guarda en la **misma carpeta** que el video |
| 4 | Elige **Sí** para abrir la carpeta con el resultado |

---

## 📋 Formatos de video soportados

MP4 · AVI · MKV · MOV · WMV · FLV · WebM · M4V · MPEG · MPG · 3GP

---

## ⚙️ Tecnología

| Componente | Descripción |
|------------|-------------|
| **Python 3.11 Embedded** | Ejecutado localmente, sin necesidad de instalar Python |
| **ffmpeg** | Motor de conversión de audio/video (descarga automática) |
| **tkinter** | Interfaz gráfica incluida en Python |

El instalador (`setup.bat`) descarga todo lo necesario en la propia carpeta de la
aplicación.  No modifica el sistema ni requiere permisos de administrador.

---

## 🖥️ Requisitos

- Windows 10 / 11 (también 7 y 8.1 con actualizaciones)
- Conexión a internet **solo** durante la configuración inicial (`setup.bat`)

---

## 📁 Estructura del proyecto

```
VideoAMP3/
├── app.py        ← Código de la aplicación
├── setup.bat     ← Configura Python + ffmpeg (ejecutar una vez)
├── run.bat       ← Lanza la aplicación
├── .gitignore
└── README.md
```

Después de `setup.bat`:
```
VideoAMP3/
├── python\       ← Python 3.11 Embedded (generado por setup.bat)
├── bin\          ← ffmpeg.exe (generado por setup.bat)
└── …
```
