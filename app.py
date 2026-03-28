"""
Convertidor de Video a MP3
Extrae el audio de un archivo de video y lo guarda en formato MP3.
Requiere ffmpeg en la carpeta bin\\ (configurado por setup.bat).
"""

import os
import sys
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def find_ffmpeg():
    """Locate the ffmpeg executable bundled with the app or on the system PATH."""
    base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    candidates = [
        os.path.join(base_dir, "bin", "ffmpeg.exe"),
        os.path.join(base_dir, "ffmpeg.exe"),
    ]
    for path in candidates:
        if os.path.isfile(path):
            return path
    # Fall back to system PATH
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            timeout=5,
        )
        if result.returncode == 0:
            return "ffmpeg"
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return None


def make_startupinfo():
    """Return a STARTUPINFO that hides the console window on Windows."""
    si = None
    if sys.platform == "win32":
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0  # SW_HIDE
    return si


# ---------------------------------------------------------------------------
# Main application
# ---------------------------------------------------------------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Convertidor de Video a MP3")
        self.geometry("620x400")
        self.resizable(False, False)
        self.configure(bg="#f5f5f5")
        self._center_window()
        self._build_ui()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _center_window(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"+{x}+{y}")

    def _build_ui(self):
        # ── Header ──────────────────────────────────────────────────────
        header = tk.Frame(self, bg="#1565C0", height=65)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header,
            text="🎵  Convertidor de Video a MP3",
            font=("Segoe UI", 15, "bold"),
            bg="#1565C0",
            fg="white",
        ).pack(expand=True)

        # ── Content ─────────────────────────────────────────────────────
        content = tk.Frame(self, bg="#f5f5f5", padx=24, pady=18)
        content.pack(fill="both", expand=True)

        tk.Label(
            content,
            text="Archivo de video:",
            font=("Segoe UI", 10, "bold"),
            bg="#f5f5f5",
        ).pack(anchor="w")

        file_row = tk.Frame(content, bg="#f5f5f5")
        file_row.pack(fill="x", pady=(4, 16))

        self._file_var = tk.StringVar()
        tk.Entry(
            file_row,
            textvariable=self._file_var,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
        ).pack(side="left", fill="x", expand=True, ipady=5)

        tk.Button(
            file_row,
            text="📁  Buscar…",
            command=self._browse,
            bg="#1565C0",
            fg="white",
            activebackground="#0d47a1",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 10),
            cursor="hand2",
            padx=12,
        ).pack(side="right", padx=(8, 0), ipady=5)

        self._btn_convert = tk.Button(
            content,
            text="🎬  Convertir a MP3",
            command=self._start_conversion,
            bg="#2E7D32",
            fg="white",
            activebackground="#1B5E20",
            activeforeground="white",
            relief="flat",
            font=("Segoe UI", 13, "bold"),
            cursor="hand2",
            pady=10,
        )
        self._btn_convert.pack(fill="x", pady=(0, 14))

        self._progress = ttk.Progressbar(content, mode="indeterminate")
        self._progress.pack(fill="x", pady=(0, 10))

        self._status_var = tk.StringVar(
            value="Listo.  Selecciona un archivo de video para comenzar."
        )
        self._status_lbl = tk.Label(
            content,
            textvariable=self._status_var,
            font=("Segoe UI", 10),
            bg="#f5f5f5",
            wraplength=560,
            justify="left",
        )
        self._status_lbl.pack(anchor="w")

        # Result box (hidden until conversion succeeds)
        self._result_frame = tk.Frame(
            content, bg="#E8F5E9", relief="solid", bd=1
        )
        self._result_lbl = tk.Label(
            self._result_frame,
            text="",
            bg="#E8F5E9",
            font=("Segoe UI", 10),
            wraplength=540,
            justify="left",
            padx=10,
            pady=8,
        )
        self._result_lbl.pack(fill="x")

    # ------------------------------------------------------------------
    # Event handlers
    # ------------------------------------------------------------------

    def _browse(self):
        filetypes = [
            (
                "Archivos de video",
                "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.m4v *.mpeg *.mpg *.3gp",
            ),
            ("Todos los archivos", "*.*"),
        ]
        path = filedialog.askopenfilename(
            title="Seleccionar archivo de video",
            filetypes=filetypes,
        )
        if path:
            self._file_var.set(path)
            self._result_frame.pack_forget()
            self._status_var.set("Archivo seleccionado. Haz clic en 'Convertir a MP3'.")
            self._status_lbl.config(fg="black")

    def _start_conversion(self):
        path = self._file_var.get().strip()
        if not path:
            messagebox.showwarning(
                "Sin archivo",
                "Por favor selecciona un archivo de video primero.",
            )
            return
        if not os.path.isfile(path):
            messagebox.showerror("Archivo no encontrado", f"No se encontró:\n{path}")
            return

        ffmpeg = find_ffmpeg()
        if not ffmpeg:
            messagebox.showerror(
                "ffmpeg no encontrado",
                "No se encontró ffmpeg.\n\n"
                "Ejecuta setup.bat para instalar todos los componentes necesarios.",
            )
            return

        self._btn_convert.config(state="disabled")
        self._result_frame.pack_forget()
        self._progress.start(10)
        self._status_var.set("Convirtiendo… Por favor espera.")
        self._status_lbl.config(fg="#555555")
        self.update()

        thread = threading.Thread(
            target=self._convert, args=(path, ffmpeg), daemon=True
        )
        thread.start()

    # ------------------------------------------------------------------
    # Conversion (runs in background thread)
    # ------------------------------------------------------------------

    def _convert(self, input_path, ffmpeg):
        try:
            out_path = os.path.splitext(input_path)[0] + ".mp3"
            cmd = [
                ffmpeg,
                "-y",
                "-i", input_path,
                "-vn",                    # disable video stream
                "-acodec", "libmp3lame", # MP3 encoder
                "-q:a", "2",             # quality: 0 (best) - 9 (worst)
                out_path,
            ]
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                startupinfo=make_startupinfo(),
            )
            if proc.returncode == 0:
                self.after(0, self._on_success, out_path)
            else:
                self.after(0, self._on_error, proc.stderr or "Error desconocido")
        except Exception as exc:
            self.after(0, self._on_error, str(exc))

    # ------------------------------------------------------------------
    # Result callbacks (run on the main thread via after())
    # ------------------------------------------------------------------

    def _on_success(self, out_path):
        self._progress.stop()
        self._btn_convert.config(state="normal")
        self._status_var.set("✓  Conversión completada exitosamente.")
        self._status_lbl.config(fg="#2E7D32")

        self._result_lbl.config(text=f"MP3 guardado en:\n{out_path}")
        self._result_frame.pack(fill="x", pady=(10, 0))

        if messagebox.askyesno(
            "¡Listo!",
            f"Audio extraído exitosamente.\n\n{out_path}\n\n¿Abrir la carpeta?",
        ):
            folder = os.path.dirname(out_path)
            try:
                if sys.platform == "win32":
                    os.startfile(folder)
                else:
                    subprocess.Popen(["xdg-open", folder])
            except Exception:
                pass

    def _on_error(self, error_msg):
        self._progress.stop()
        self._btn_convert.config(state="normal")
        self._status_var.set("✗  Error durante la conversión.")
        self._status_lbl.config(fg="#C62828")
        messagebox.showerror(
            "Error al convertir",
            f"Ocurrió un error:\n\n{error_msg[:600]}",
        )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app = App()
    app.mainloop()
