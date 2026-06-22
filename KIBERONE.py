import os
import platform
import sys
import tkinter as tk
from tkinter import filedialog, ttk
import vlc


class UniversalVideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Video Player - Pro")
        self.root.geometry("1100x700")

        # VLC sozlamalari
        self.instance = vlc.Instance("--no-xlib")
        self.player = self.instance.media_player_new()
        self.is_dragging = False

        # --- Interfeys ---
        self.video_frame = tk.Frame(self.root, bg="black")
        self.video_frame.pack(fill=tk.BOTH, expand=True)

        self.controls = tk.Frame(self.root, bg="#1e1e1e", height=100)
        self.controls.pack(fill=tk.X)

        # 1. Asosiy tugmalar
        btn_frame = tk.Frame(self.controls, bg="#1e1e1e")
        btn_frame.pack(fill=tk.X, pady=5)

        tk.Button(btn_frame, text="📂 Fayl", command=self.load_video).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="▶️/⏸️", command=self.toggle_play).pack(side=tk.LEFT, padx=5)

        # 2. Ovoz va Tezlik boshqaruvi
        ctrl_frame = tk.Frame(self.controls, bg="#1e1e1e")
        ctrl_frame.pack(fill=tk.X, pady=5)

        tk.Button(ctrl_frame, text="Vol -", command=lambda: self.adjust_volume(-10)).pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl_frame, text="Vol +", command=lambda: self.adjust_volume(10)).pack(side=tk.LEFT, padx=5)

        tk.Label(ctrl_frame, text=" Tezlik:", bg="#1e1e1e", fg="white").pack(side=tk.LEFT)
        for speed in [0.5, 1.0, 1.5, 2.0]:
            tk.Button(ctrl_frame, text=f"{speed}x", command=lambda s=speed: self.set_speed(s)).pack(side=tk.LEFT,
                                                                                                    padx=2)

        # 3. Slider
        self.slider = ttk.Scale(self.controls, from_=0, to=100, orient=tk.HORIZONTAL)
        self.slider.pack(fill=tk.X, padx=10)
        self.slider.bind("<ButtonRelease-1>", self.on_slider_release)

        # VLC ulash
        self.root.update()
        self.player.set_hwnd(self.video_frame.winfo_id())
        self.update_ui()

    def load_video(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.player.set_media(self.instance.media_new(file_path))
            self.player.play()

    def toggle_play(self):
        self.player.pause() if self.player.is_playing() else self.player.play()

    def adjust_volume(self, delta):
        current = self.player.audio_get_volume()
        self.player.audio_set_volume(max(0, min(100, current + delta)))

    def set_speed(self, speed):
        self.player.set_rate(speed)

    def on_slider_release(self, event):
        self.player.set_position(self.slider.get() / 100)

    def update_ui(self):
        if self.player.is_playing():
            pos = self.player.get_position()
            if pos != -1: self.slider.set(pos * 100)
        self.root.after(200, self.update_ui)


if __name__ == "__main__":
    root = tk.Tk()
    app = UniversalVideoPlayer(root)
    root.mainloop()