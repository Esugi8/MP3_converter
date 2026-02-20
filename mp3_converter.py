import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

# MoviePy 2.0対応のインポート
try:
    from moviepy import VideoFileClip
except ImportError:
    from moviepy.editor import VideoFileClip

class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MKV to MP3 高機能トリマー")
        self.root.geometry("450x350")

        # 変数管理
        self.file_path = tk.StringVar()
        self.duration_text = tk.StringVar(value="ファイルを選択してください")
        self.total_seconds = 0

        # UI作成
        self.create_widgets()

    def create_widgets(self):
        padding = {'padx': 10, 'pady': 5}

        # --- ファイル選択エリア ---
        frame_file = tk.LabelFrame(self.root, text="1. ファイル選択", padx=10, pady=10)
        frame_file.pack(fill="x", **padding)

        tk.Entry(frame_file, textvariable=self.file_path, width=40).pack(side="left", padx=5)
        tk.Button(frame_file, text="参照", command=self.select_file).pack(side="left")
        
        self.lbl_info = tk.Label(frame_file, textvariable=self.duration_text, fg="blue")
        self.lbl_info.pack(fill="x", side="bottom", pady=5)

        # --- 時間指定エリア ---
        frame_time = tk.LabelFrame(self.root, text="2. トリミング範囲指定 (時:分:秒)", padx=10, pady=10)
        frame_time.pack(fill="x", **padding)

        # 開始時間
        tk.Label(frame_time, text="開始:").grid(row=0, column=0)
        self.start_h = self.create_spinbox(frame_time, 0, 1)
        self.start_m = self.create_spinbox(frame_time, 0, 2)
        self.start_s = self.create_spinbox(frame_time, 0, 3)

        # 終了時間
        tk.Label(frame_time, text="終了:").grid(row=1, column=0, pady=5)
        self.end_h = self.create_spinbox(frame_time, 1, 1)
        self.end_m = self.create_spinbox(frame_time, 1, 2)
        self.end_s = self.create_spinbox(frame_time, 1, 3)

        # --- 実行エリア ---
        self.btn_convert = tk.Button(
            self.root, text="MP3に変換して保存", 
            command=self.convert_mkv_to_mp3, 
            bg="#28a745", fg="white", font=("Arial", 10, "bold"),
            height=2
        )
        self.btn_convert.pack(fill="x", **padding)

    def create_spinbox(self, parent, row, col):
        # 00〜59まで選択できるスピンボックス
        sb = tk.Spinbox(parent, from_=0, to=59, width=5, format="%02.0f")
        sb.grid(row=row, column=col, padx=2)
        return sb

    def select_file(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Video files", "*.mkv *.mp4 *.avi *.mov"),
                ("All files", "*.*")
                ]
        )
        if path:
            self.file_path.set(path)
            try:
                # 動画の長さを取得して表示
                with VideoFileClip(path) as clip:
                    self.total_seconds = clip.duration
                    h = int(self.total_seconds // 3600)
                    m = int((self.total_seconds % 3600) // 60)
                    s = int(self.total_seconds % 60)
                    
                    self.duration_text.set(f"動画の長さ: {h:02}:{m:02}:{s:02}")
                    
                    # 終了時間のデフォルト値を動画の長さに設定
                    self.set_spinbox_value(self.end_h, h)
                    self.set_spinbox_value(self.end_m, m)
                    self.set_spinbox_value(self.end_s, s)
            except Exception as e:
                messagebox.showerror("エラー", "動画情報の取得に失敗しました。")

    def set_spinbox_value(self, sb, value):
        sb.delete(0, "end")
        sb.insert(0, f"{value:02}")

    def get_seconds(self, h_sb, m_sb, s_sb):
        h = int(h_sb.get())
        m = int(m_sb.get())
        s = int(s_sb.get())
        return h * 3600 + m * 60 + s

    def convert_mkv_to_mp3(self):
        input_file = self.file_path.get()
        if not input_file:
            messagebox.showerror("エラー", "ファイルを選択してください。")
            return

        start_total = self.get_seconds(self.start_h, self.start_m, self.start_s)
        end_total = self.get_seconds(self.end_h, self.end_m, self.end_s)

        if start_total >= end_total:
            messagebox.showerror("エラー", "終了時間は開始時間より後に設定してください。")
            return

        try:
            with VideoFileClip(input_file) as clip:
                # トリミング
                if hasattr(clip, "subclipped"):
                    trimmed_clip = clip.subclipped(start_total, end_total)
                else:
                    trimmed_clip = clip.subclip(start_total, end_total)

                output_file = os.path.splitext(input_file)[0] + "_trimmed.mp3"
                
                # 音声の書き出し
                if clip.audio:
                    trimmed_clip.audio.write_audiofile(output_file)
                    messagebox.showinfo("成功", f"保存完了:\n{output_file}")
                else:
                    messagebox.showerror("エラー", "音声が含まれていません。")
                
                trimmed_clip.close()

        except Exception as e:
            messagebox.showerror("エラー", f"変換失敗:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConverterApp(root)
    root.mainloop()