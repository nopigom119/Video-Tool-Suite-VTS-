import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, scrolledtext
from tkinterdnd2 import DND_FILES, TkinterDnD
import os
import threading
import queue
import shutil
import subprocess
import json
import re
import time
import datetime
from collections import deque

# --- Configuration File Management ---
CONFIG_FILE = "ffmpeg_tool_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(config):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
    except Exception as e:
        print(f"Error saving config: {e}")

# --- FFmpeg Path Configuration ---
SYSTEM_FFMPEG = None
SYSTEM_FFPROBE = None

def configure_ffmpeg_path(custom_ffmpeg=None, custom_ffprobe=None):
    global SYSTEM_FFMPEG, SYSTEM_FFPROBE
    
    ffmpeg_path = custom_ffmpeg
    ffprobe_path = custom_ffprobe

    if not ffmpeg_path or not os.path.exists(ffmpeg_path):
        ffmpeg_path = shutil.which("ffmpeg")
    
    if not ffprobe_path or not os.path.exists(ffprobe_path):
        ffprobe_path = shutil.which("ffprobe")

    if ffmpeg_path and os.path.exists(ffmpeg_path):
        os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path
        SYSTEM_FFMPEG = ffmpeg_path
    else:
        SYSTEM_FFMPEG = None

    if ffprobe_path and os.path.exists(ffprobe_path):
        SYSTEM_FFPROBE = ffprobe_path
    else:
        SYSTEM_FFPROBE = None

    return SYSTEM_FFMPEG, SYSTEM_FFPROBE

_config = load_config()
configure_ffmpeg_path(_config.get("ffmpeg_path"), _config.get("ffprobe_path"))


# --- Language Configuration ---
current_language = 'ko' 

LANG_STRINGS = {
    'en': {
        'window_title': "Video Tool Suite",
        'toggle_lang_button_text_to_ko': "한국어",
        'toggle_lang_button_text_to_en': "English",
        'tab_main_converter': "Video Converter",
        'tab_main_splitter': "Video Splitter",
        'tab_main_settings': "Global Settings",
        'tab_single_file': "Single Conversion",
        'tab_batch_folder': "Batch Folder",
        'tab_gpu_nvidia': "NVIDIA (NVENC)",
        'tab_gpu_intel': "Intel (QSV)",
        'tab_gpu_amd': "AMD (AMF)",
        'label_target_format': "Target Format:",
        'button_select_file': "Select File",
        'button_select_folder': "Select Folder",
        'button_add_to_queue': "Add to List",
        'button_start_queue': "Start Processing",
        'button_stop': "STOP / Cancel Selected",
        'button_clear_list': "Clear List",
        'button_start_batch_conversion': "Start Batch",
        'button_start_batch_stream_copy': "Fast Batch",
        'button_browse': "Browse",
        'sp_labelframe_input': "Input Video",
        'sp_labelframe_settings': "Split Settings",
        'sp_label_size': "Split Size:",
        'sp_label_unit': "Unit:",
        'sp_button_start': "Start Splitting",
        'sf_labelframe_select_file': "Add Task (Drag & Drop Here)",
        'sf_labelframe_queue': "Conversion List",
        'sf_label_original_extension': "Ext:",
        'bf_labelframe_input_folder': "Input Folder (Drag & Drop Here)",
        'bf_labelframe_conversion_settings': "Settings",
        'bf_labelframe_log': "Process Log",
        'bf_check_auto_archive': "Move original to '_Originals' after success",
        'settings_labelframe_ffmpeg': "FFmpeg Engine Path",
        'settings_label_ffmpeg_path': "FFmpeg:",
        'settings_label_ffprobe_path': "FFprobe:",
        'settings_ffmpeg_help': "Select Full GPL version of FFmpeg/FFprobe.",
        'settings_labelframe_cpu': "General / CPU",
        'settings_label_codec': "Codec:",
        'settings_label_cpu_threads': "Threads:",
        'settings_label_cpu_total': "/ {total_cores}",
        'settings_labelframe_gpu': "GPU Settings",
        'settings_label_gpu_quality': "Quality (QP/CQ):",
        'settings_gpu_quality_tooltip': "Lower is better. 18=Lossless-like, 23=Good, 28=Fair.",
        'settings_label_nv_preset': "Preset:",
        'settings_help_nv': "• Preset: p1(Fastest) ~ p7(Best Quality).",
        'settings_label_intel_preset': "Preset:",
        'settings_help_intel': "• Preset: Speed vs Quality balance.",
        'settings_label_amd_usage': "Usage:",
        'settings_help_amd': "• Usage: 'transcoding' recommended.",
        'status_initial_prompt': "Ready.",
        'status_complete': "Work Complete.",
        'status_stopped': "Stopped / Cancelled.",
        'dialog_title_warning': "Warning",
        'dialog_title_error': "Error",
        'dialog_title_info': "Info",
        'dialog_msg_no_files_to_convert_info': "No files found.",
        'dnd_err_folder_on_file': "Please drop a video file, not a folder.",
        'filetype_video_files': "Video Files",
        'filetype_all_files': "All Files",
        'filetype_exe_files': "Executables",
    },
    'ko': {
        'window_title': "영상 도구 모음",
        'toggle_lang_button_text_to_ko': "한국어",
        'toggle_lang_button_text_to_en': "English",
        'tab_main_converter': "영상 변환기",
        'tab_main_splitter': "영상 분할기",
        'tab_main_settings': "통합 설정",
        'tab_single_file': "단일 변환",
        'tab_batch_folder': "일괄 변환",
        'tab_gpu_nvidia': "NVIDIA",
        'tab_gpu_intel': "Intel",
        'tab_gpu_amd': "AMD",
        'label_target_format': "변환 포맷:",
        'button_select_file': "파일 선택",
        'button_select_folder': "폴더 선택",
        'button_add_to_queue': "목록 추가",
        'button_start_queue': "변환 시작",
        'button_stop': "중지 / 선택 취소",
        'button_clear_list': "목록 비우기",
        'button_start_batch_conversion': "일괄 시작",
        'button_start_batch_stream_copy': "일괄 빠른 변환",
        'button_browse': "찾기",
        'sp_labelframe_input': "입력 파일 (드래그 앤 드롭 가능)",
        'sp_labelframe_settings': "분할 설정",
        'sp_label_size': "분할 크기:",
        'sp_label_unit': "단위:",
        'sp_button_start': "분할 시작",
        'sf_labelframe_select_file': "작업 추가 (드래그 앤 드롭 가능)",
        'sf_labelframe_queue': "변환 목록",
        'sf_label_original_extension': "확장자:",
        'bf_labelframe_input_folder': "입력 폴더 (드래그 앤 드롭 가능)",
        'bf_labelframe_conversion_settings': "변환 설정",
        'bf_labelframe_log': "처리 로그",
        'bf_check_auto_archive': "변환 성공 시 원본을 '_Originals' 폴더로 자동 이동",
        'settings_labelframe_ffmpeg': "FFmpeg 엔진 경로",
        'settings_label_ffmpeg_path': "FFmpeg:",
        'settings_label_ffprobe_path': "FFprobe:",
        'settings_ffmpeg_help': "반드시 Full 버전(gpl)의 FFmpeg를 선택하세요.",
        'settings_labelframe_cpu': "일반 / CPU",
        'settings_label_codec': "코덱:",
        'settings_label_cpu_threads': "스레드:",
        'settings_label_cpu_total': "/ {total_cores}",
        'settings_labelframe_gpu': "GPU 설정",
        'settings_label_gpu_quality': "품질 (QP):",
        'settings_gpu_quality_tooltip': "낮을수록 고화질. 18=원본급, 23=좋음, 28=보통.",
        'settings_label_nv_preset': "프리셋:",
        'settings_help_nv': "• 프리셋: p1(가장 빠름) ~ p7(고화질).",
        'settings_label_intel_preset': "프리셋:",
        'settings_help_intel': "• 프리셋: 속도와 품질 균형.",
        'settings_label_amd_usage': "용도:",
        'settings_help_amd': "• 용도: 파일 변환 추천.",
        'status_initial_prompt': "준비 완료.",
        'status_complete': "작업이 완료되었습니다.",
        'status_stopped': "작업이 중지되거나 취소되었습니다.",
        'dialog_title_warning': "경고",
        'dialog_title_error': "오류",
        'dialog_title_info': "알림",
        'dialog_msg_no_files_to_convert_info': "파일이 없습니다.",
        'dnd_err_folder_on_file': "폴더가 아닌 비디오 파일을 드롭해주세요.",
        'filetype_video_files': "비디오 파일",
        'filetype_all_files': "모든 파일",
        'filetype_exe_files': "실행 파일",
    }
}

def get_string(key, **kwargs):
    s = LANG_STRINGS[current_language].get(key, f"<{key}>")
    if kwargs:
        try:
            s = s.format(**kwargs)
        except:
            pass
    return s

VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.ts', '.mpg', '.mpeg', '.vob', '.mts', '.m2ts']
TARGET_FORMATS = {"MP4": "mp4", "AVI": "avi", "MOV": "mov", "WebM": "webm", "GIF": "gif"}

class TimeEstimator:
    def __init__(self, history_len=5):
        self.start_time = None
        self.last_update_time = None
        self.last_progress = 0
        self.speed_history = deque(maxlen=history_len)
        self.last_eta_str = "--:--"

    def start(self):
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.last_progress = 0
        self.speed_history.clear()
        self.last_eta_str = "--:--"

    def update(self, current_progress):
        now = time.time()
        dt = now - self.last_update_time
        
        # Update every 1.0s to prevent jitter
        if dt < 1.0: 
            return self.last_eta_str

        dp = current_progress - self.last_progress
        if dp < 0: dp = 0

        instant_speed = dp / dt if dt > 0 else 0
        self.speed_history.append(instant_speed)
        
        if len(self.speed_history) > 0:
            avg_speed = sum(self.speed_history) / len(self.speed_history)
        else:
            avg_speed = instant_speed

        self.last_update_time = now
        self.last_progress = current_progress
        
        if avg_speed <= 0.01:
            self.last_eta_str = "--:--"
        else:
            remaining_percent = 100 - current_progress
            remaining_seconds = remaining_percent / avg_speed
            self.last_eta_str = str(datetime.timedelta(seconds=int(remaining_seconds)))
            
        return self.last_eta_str

class ScrollableTaskFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.canvas = tk.Canvas(self, bg="#2E2E2E", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.bind('<Configure>', self._on_canvas_configure)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas.find_withtag("all")[0], width=event.width)

class VideoToolSuite:
    def __init__(self, root_window):
        self.root = root_window 
        self.root.geometry("1100x900")
        
        self.style = ttk.Style()
        self.setup_dark_theme()

        self.progress_queue = queue.Queue()
        
        # --- State Management ---
        # Separate flags to allow concurrent execution
        self.is_running = False          # For Converter
        self.is_splitter_running = False # For Splitter
        
        self.current_process = None      # Converter Process
        self.splitter_process = None     # Splitter Process
        
        self.tasks_queue_data = [] 
        self.task_widgets = []     
        self.current_task_index = -1 
        
        self.eta_calculator = TimeEstimator(history_len=5)

        self.total_cpu_cores = os.cpu_count() if os.cpu_count() else 1
        self.cpu_threads_to_use = tk.IntVar(value=max(1, self.total_cpu_cores // 2))
        
        self.ffmpeg_path_var = tk.StringVar(value=SYSTEM_FFMPEG if SYSTEM_FFMPEG else "")
        self.ffprobe_path_var = tk.StringVar(value=SYSTEM_FFPROBE if SYSTEM_FFPROBE else "")
        self.selected_video_codec = tk.StringVar(value='H.264')
        self.gpu_quality_target_crf = tk.IntVar(value=23)
        self.nv_preset = tk.StringVar(value='p4') 
        self.intel_preset = tk.StringVar(value='fast')
        self.amd_usage = tk.StringVar(value='transcoding')

        self.sf_input_filepath = tk.StringVar()
        self.sf_original_extension = tk.StringVar()
        self.sf_target_format = tk.StringVar()
        
        self.bf_input_folder_path = tk.StringVar()
        self.bf_target_format = tk.StringVar()
        self.bf_auto_archive = tk.BooleanVar(value=True)

        self.sp_input_filepath = tk.StringVar()
        self.sp_split_size = tk.StringVar(value="100")
        self.sp_split_unit = tk.StringVar(value="MB")

        self.create_main_layout()
        self.update_ui_language()
        self.root.after(100, self.process_queue)

    def setup_dark_theme(self):
        bg_color = "#2E2E2E"
        fg_color = "#FFFFFF"
        accent_color = "#007ACC"
        entry_bg = "#3C3C3C"
        button_bg = "#444444"
        
        self.root.configure(bg=bg_color)
        self.style.theme_use('clam')

        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabelframe", background=bg_color, foreground=fg_color, relief="flat", borderwidth=1)
        self.style.configure("TLabelframe.Label", background=bg_color, foreground=accent_color, font=("Segoe UI", 10, "bold"))
        self.style.configure("Highlight.TLabelframe", background=bg_color, foreground=fg_color, relief="solid", borderwidth=1, bordercolor=accent_color)
        self.style.configure("Highlight.TLabelframe.Label", background=bg_color, foreground=accent_color, font=("Segoe UI", 10, "bold"))

        self.style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 9))
        self.style.configure("TButton", background=button_bg, foreground=fg_color, borderwidth=0, font=("Segoe UI", 9))
        self.style.map("TButton", background=[('active', accent_color), ('disabled', '#555555')], foreground=[('disabled', '#AAAAAA')])
        self.style.configure("TEntry", fieldbackground=entry_bg, foreground=fg_color, borderwidth=0, insertcolor=fg_color)
        self.style.configure("TCombobox", fieldbackground=entry_bg, background=button_bg, foreground=fg_color, arrowcolor=fg_color)
        self.style.map("TCombobox", fieldbackground=[('readonly', entry_bg)], selectbackground=[('readonly', entry_bg)], selectforeground=[('readonly', fg_color)])
        self.style.configure("TNotebook", background=bg_color, borderwidth=0)
        self.style.configure("TNotebook.Tab", background=button_bg, foreground=fg_color, padding=[10, 5], font=("Segoe UI", 9))
        self.style.map("TNotebook.Tab", background=[('selected', accent_color)], expand=[('selected', [1, 1, 1, 0])])
        self.style.configure("Horizontal.TProgressbar", background=accent_color, troughcolor=entry_bg, borderwidth=0, thickness=10)
        self.style.configure("Red.TButton", background="#AA0000", foreground="white")
        self.style.map("Red.TButton", background=[('active', "#CC0000")])
        self.style.configure("TCheckbutton", background=bg_color, foreground=fg_color, font=("Segoe UI", 9))
        self.style.map("TCheckbutton", background=[('active', bg_color)])

    def create_main_layout(self):
        top_bar = ttk.Frame(self.root, padding=(15, 10))
        top_bar.pack(fill=tk.X)
        ttk.Label(top_bar, text="VIDEO TOOL SUITE", font=("Segoe UI", 16, "bold"), foreground="#007ACC").pack(side=tk.LEFT)
        self.lang_toggle_button = ttk.Button(top_bar, command=self.toggle_language)
        self.lang_toggle_button.pack(side=tk.RIGHT)

        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.root_notebook = ttk.Notebook(main_frame)
        self.root_notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tab_converter_frame = ttk.Frame(self.root_notebook, padding="10")
        self.root_notebook.add(self.tab_converter_frame, text="Converter")
        self.create_converter_ui(self.tab_converter_frame)

        self.tab_splitter_frame = ttk.Frame(self.root_notebook, padding="20")
        self.root_notebook.add(self.tab_splitter_frame, text="Splitter")
        self.create_splitter_ui(self.tab_splitter_frame)

        self.tab_settings_frame = ttk.Frame(self.root_notebook, padding="20")
        self.root_notebook.add(self.tab_settings_frame, text="Settings")
        self.create_settings_ui(self.tab_settings_frame)

    # ---------------------------------------------------------
    # UI Creation: Converter
    # ---------------------------------------------------------
    def create_converter_ui(self, parent):
        self.conv_notebook = ttk.Notebook(parent)
        self.conv_notebook.pack(fill=tk.BOTH, expand=True)

        # === 1. Single File (Queue Mode) Tab ===
        self.sf_tab_frame = ttk.Frame(self.conv_notebook, padding="15")
        self.conv_notebook.add(self.sf_tab_frame, text="") 
        
        lf_add = ttk.LabelFrame(self.sf_tab_frame, text="Add Task", padding="15")
        lf_add.pack(fill=tk.X, pady=(0, 10))
        self.sf_labelframe_select_file_widget = lf_add
        
        # Register DND
        self.register_dnd(lf_add, self.handle_dnd_single_file)

        f1 = ttk.Frame(lf_add); f1.pack(fill=tk.X)
        ttk.Entry(f1, textvariable=self.sf_input_filepath, state="readonly", font=("Segoe UI", 10)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.sf_button_select_file_widget = ttk.Button(f1, command=self.sf_select_file, width=12); self.sf_button_select_file_widget.pack(side=tk.RIGHT)
        
        f2 = ttk.Frame(lf_add); f2.pack(fill=tk.X, pady=(10, 0))
        self.sf_label_original_extension_widget = ttk.Label(f2, text="Ext:"); self.sf_label_original_extension_widget.pack(side=tk.LEFT)
        ttk.Label(f2, textvariable=self.sf_original_extension, font=("Segoe UI", 10, "bold"), foreground="#CCCCCC").pack(side=tk.LEFT, padx=5)
        
        self.sf_label_target_format_widget = ttk.Label(f2, text="Target:"); self.sf_label_target_format_widget.pack(side=tk.LEFT, padx=(20, 5))
        self.sf_format_combobox = ttk.Combobox(f2, textvariable=self.sf_target_format, values=list(TARGET_FORMATS.keys()), state="readonly", width=8)
        self.sf_format_combobox.pack(side=tk.LEFT)

        self.sf_button_add_to_queue = ttk.Button(f2, command=self.sf_add_to_queue, width=15)
        self.sf_button_add_to_queue.pack(side=tk.RIGHT)

        lf_queue = ttk.LabelFrame(self.sf_tab_frame, text="Task Queue", padding="10")
        lf_queue.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.sf_labelframe_queue_widget = lf_queue

        self.sf_queue_frame = ScrollableTaskFrame(lf_queue)
        self.sf_queue_frame.pack(fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(self.sf_tab_frame); btn_frame.pack(fill=tk.X, pady=5)
        self.sf_button_stop = ttk.Button(btn_frame, text="STOP", command=self.stop_processing, style="Red.TButton", state="disabled")
        self.sf_button_stop.pack(side=tk.LEFT, padx=5)
        self.sf_button_clear = ttk.Button(btn_frame, command=self.sf_clear_list)
        self.sf_button_clear.pack(side=tk.LEFT, padx=5)
        self.sf_button_start_queue = ttk.Button(btn_frame, command=self.sf_start_queue_processing)
        self.sf_button_start_queue.pack(side=tk.RIGHT, padx=5)

        # === 2. Batch Folder Tab ===
        self.bf_tab_frame = ttk.Frame(self.conv_notebook, padding="15")
        self.conv_notebook.add(self.bf_tab_frame, text="")

        lf_in = ttk.LabelFrame(self.bf_tab_frame, text="Input", padding="15"); lf_in.pack(fill=tk.X, pady=(0, 10))
        self.bf_labelframe_input_folder_widget = lf_in
        
        # Register DND
        self.register_dnd(lf_in, self.handle_dnd_batch_folder)

        f_b1 = ttk.Frame(lf_in); f_b1.pack(fill=tk.X)
        ttk.Entry(f_b1, textvariable=self.bf_input_folder_path, state="readonly", font=("Segoe UI", 10)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.bf_button_select_input_folder_widget = ttk.Button(f_b1, command=self.bf_select_input_folder, width=12); self.bf_button_select_input_folder_widget.pack(side=tk.RIGHT)

        lf_set = ttk.LabelFrame(self.bf_tab_frame, text="Settings", padding="15"); lf_set.pack(fill=tk.X, pady=(0, 10))
        self.bf_labelframe_conversion_settings_widget = lf_set
        
        f_b2 = ttk.Frame(lf_set); f_b2.pack(fill=tk.X)
        self.bf_label_target_format_widget = ttk.Label(f_b2, text="Format:"); self.bf_label_target_format_widget.pack(side=tk.LEFT)
        self.bf_format_combobox = ttk.Combobox(f_b2, textvariable=self.bf_target_format, values=list(TARGET_FORMATS.keys()), state="readonly", width=10)
        self.bf_format_combobox.pack(side=tk.LEFT, padx=10)
        self.bf_check_auto_archive_widget = ttk.Checkbutton(f_b2, variable=self.bf_auto_archive, text="Auto Archive Originals")
        self.bf_check_auto_archive_widget.pack(side=tk.LEFT, padx=20)
        self.bf_stream_copy_button_widget = ttk.Button(f_b2, command=lambda: self.bf_start_batch_thread('remux'), state="disabled"); self.bf_stream_copy_button_widget.pack(side=tk.RIGHT, padx=5)
        self.bf_convert_button_widget = ttk.Button(f_b2, command=lambda: self.bf_start_batch_thread('re-encode'), state="disabled"); self.bf_convert_button_widget.pack(side=tk.RIGHT, padx=5)
        self.bf_button_stop = ttk.Button(f_b2, text="STOP", command=self.stop_processing, style="Red.TButton", state="disabled")
        self.bf_button_stop.pack(side=tk.RIGHT, padx=20)

        lf_log = ttk.LabelFrame(self.bf_tab_frame, text="Log", padding="10"); lf_log.pack(fill=tk.BOTH, expand=True)
        self.bf_labelframe_log_widget = lf_log
        self.bf_log_text = scrolledtext.ScrolledText(lf_log, bg="#222222", fg="#DDDDDD", font=("Consolas", 9), state='disabled', height=10)
        self.bf_log_text.pack(fill=tk.BOTH, expand=True)
    def create_splitter_ui(self, parent):
        lf_in = ttk.LabelFrame(parent, text="Input Video", padding="15")
        lf_in.pack(fill=tk.X, pady=(0, 15))
        self.sp_labelframe_input_widget = lf_in
        
        self.register_dnd(lf_in, self.handle_dnd_splitter_file)

        f1 = ttk.Frame(lf_in); f1.pack(fill=tk.X)
        ttk.Entry(f1, textvariable=self.sp_input_filepath, state="readonly", font=("Segoe UI", 10)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.sp_button_select_file_widget = ttk.Button(f1, command=self.sp_select_file, width=12); self.sp_button_select_file_widget.pack(side=tk.RIGHT)

        lf_set = ttk.LabelFrame(parent, text="Split Settings", padding="15")
        lf_set.pack(fill=tk.X, pady=(0, 15))
        self.sp_labelframe_settings_widget = lf_set

        f2 = ttk.Frame(lf_set); f2.pack(fill=tk.X)
        self.sp_label_size_widget = ttk.Label(f2, text="Split Size:"); self.sp_label_size_widget.pack(side=tk.LEFT)
        ttk.Entry(f2, textvariable=self.sp_split_size, width=10).pack(side=tk.LEFT, padx=10)
        self.sp_label_unit_widget = ttk.Label(f2, text="Unit:"); self.sp_label_unit_widget.pack(side=tk.LEFT, padx=(20, 5))
        ttk.Combobox(f2, textvariable=self.sp_split_unit, values=["GB", "MB"], state="readonly", width=5).pack(side=tk.LEFT)

        self.sp_start_button_widget = ttk.Button(parent, command=self.sp_start_splitting_thread, state="disabled")
        self.sp_start_button_widget.pack(pady=10, fill=tk.X, ipady=5)
        
        # Use specific stop command for splitter
        self.sp_button_stop = ttk.Button(parent, text="STOP", command=self.stop_splitter, style="Red.TButton", state="disabled")
        self.sp_button_stop.pack(pady=5, fill=tk.X)

        self.sp_progress_label_widget = ttk.Label(parent, text="", font=("Segoe UI", 10))
        self.sp_progress_label_widget.pack(anchor='w', pady=(0, 2))
        self.sp_progress_bar = ttk.Progressbar(parent, orient=tk.HORIZONTAL, mode='determinate')
        self.sp_progress_bar.pack(fill=tk.X, ipady=5)
    def create_settings_ui(self, parent):
        lf_ff = ttk.LabelFrame(parent, text="FFmpeg", padding="15"); lf_ff.pack(fill=tk.X, pady=(0, 15))
        self.settings_labelframe_ffmpeg_widget = lf_ff
        r1 = ttk.Frame(lf_ff); r1.pack(fill=tk.X, pady=2)
        self.settings_label_ffmpeg_path_widget = ttk.Label(r1, width=10); self.settings_label_ffmpeg_path_widget.pack(side=tk.LEFT)
        ttk.Entry(r1, textvariable=self.ffmpeg_path_var, state='readonly').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.settings_button_browse_ffmpeg = ttk.Button(r1, command=lambda: self.browse_ffmpeg_path("ffmpeg")); self.settings_button_browse_ffmpeg.pack(side=tk.LEFT)
        r2 = ttk.Frame(lf_ff); r2.pack(fill=tk.X, pady=2)
        self.settings_label_ffprobe_path_widget = ttk.Label(r2, width=10); self.settings_label_ffprobe_path_widget.pack(side=tk.LEFT)
        ttk.Entry(r2, textvariable=self.ffprobe_path_var, state='readonly').pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.settings_button_browse_ffprobe = ttk.Button(r2, command=lambda: self.browse_ffmpeg_path("ffprobe")); self.settings_button_browse_ffprobe.pack(side=tk.LEFT)
        self.settings_ffmpeg_help_label = ttk.Label(lf_ff, font=("Segoe UI", 8), foreground="#888888"); self.settings_ffmpeg_help_label.pack(anchor='w', pady=(5,0))

        lf_cpu = ttk.LabelFrame(parent, text="CPU", padding="15"); lf_cpu.pack(fill=tk.X, pady=(0, 15))
        self.settings_labelframe_cpu_widget = lf_cpu
        self.settings_label_codec_widget = ttk.Label(lf_cpu); self.settings_label_codec_widget.pack(side=tk.LEFT)
        ttk.Combobox(lf_cpu, textvariable=self.selected_video_codec, values=['H.264', 'H.265', 'AV1'], state='readonly', width=8).pack(side=tk.LEFT, padx=(5, 20))
        self.settings_label_cpu_threads_widget = ttk.Label(lf_cpu); self.settings_label_cpu_threads_widget.pack(side=tk.LEFT)
        ttk.Spinbox(lf_cpu, from_=1, to=self.total_cpu_cores, textvariable=self.cpu_threads_to_use, width=5).pack(side=tk.LEFT, padx=5)
        self.settings_label_cpu_total_widget = ttk.Label(lf_cpu, foreground="#888888"); self.settings_label_cpu_total_widget.pack(side=tk.LEFT)

        lf_gpu = ttk.LabelFrame(parent, text="GPU", padding="15"); lf_gpu.pack(fill=tk.BOTH, expand=True)
        self.settings_labelframe_gpu_widget = lf_gpu
        q_frame = ttk.Frame(lf_gpu); q_frame.pack(fill=tk.X, pady=(0, 10))
        self.settings_label_gpu_quality_widget = ttk.Label(q_frame); self.settings_label_gpu_quality_widget.pack(side=tk.LEFT)
        ttk.Scale(q_frame, from_=0, to=51, orient=tk.HORIZONTAL, variable=self.gpu_quality_target_crf, command=lambda v: self.gpu_quality_target_crf.set(int(float(v)))).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        ttk.Label(q_frame, textvariable=self.gpu_quality_target_crf, width=3).pack(side=tk.LEFT)
        self.settings_gpu_quality_tooltip_widget = ttk.Label(lf_gpu, font=("Segoe UI", 8), foreground="#888888"); self.settings_gpu_quality_tooltip_widget.pack(anchor='w', pady=(0, 10))

        self.gpu_notebook = ttk.Notebook(lf_gpu); self.gpu_notebook.pack(fill=tk.BOTH, expand=True)
        self.nv_settings_frame = ttk.Frame(self.gpu_notebook, padding="15"); self.gpu_notebook.add(self.nv_settings_frame, text="NVIDIA")
        self.settings_label_nv_preset_widget = ttk.Label(self.nv_settings_frame); self.settings_label_nv_preset_widget.grid(row=0, column=0, sticky='w', pady=5)
        ttk.Combobox(self.nv_settings_frame, textvariable=self.nv_preset, values=['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'slow', 'medium', 'fast'], state='readonly', width=15).grid(row=0, column=1, sticky='w', padx=10)
        self.settings_help_nv_label = ttk.Label(self.nv_settings_frame, justify='left', wraplength=400, foreground="#AAAAAA"); self.settings_help_nv_label.grid(row=1, column=0, columnspan=2, sticky='w', pady=10)
        self.intel_settings_frame = ttk.Frame(self.gpu_notebook, padding="15"); self.gpu_notebook.add(self.intel_settings_frame, text="Intel")
        self.settings_label_intel_preset_widget = ttk.Label(self.intel_settings_frame); self.settings_label_intel_preset_widget.grid(row=0, column=0, sticky='w', pady=5)
        ttk.Combobox(self.intel_settings_frame, textvariable=self.intel_preset, values=['veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'], state='readonly', width=15).grid(row=0, column=1, sticky='w', padx=10)
        self.settings_help_intel_label = ttk.Label(self.intel_settings_frame, justify='left', wraplength=400, foreground="#AAAAAA"); self.settings_help_intel_label.grid(row=1, column=0, columnspan=2, sticky='w', pady=10)
        self.amd_settings_frame = ttk.Frame(self.gpu_notebook, padding="15"); self.gpu_notebook.add(self.amd_settings_frame, text="AMD")
        self.settings_label_amd_usage_widget = ttk.Label(self.amd_settings_frame); self.settings_label_amd_usage_widget.grid(row=0, column=0, sticky='w', pady=5)
        ttk.Combobox(self.amd_settings_frame, textvariable=self.amd_usage, values=['transcoding', 'ultralowlatency', 'lowlatency', 'webcam'], state='readonly', width=15).grid(row=0, column=1, sticky='w', padx=10)
        self.settings_help_amd_label = ttk.Label(self.amd_settings_frame, justify='left', wraplength=400, foreground="#AAAAAA"); self.settings_help_amd_label.grid(row=1, column=0, columnspan=2, sticky='w', pady=10)

    # ---------------------------------------------------------
    # UI Helpers & Update
    # ---------------------------------------------------------
    def toggle_language(self):
        global current_language
        current_language = 'en' if current_language == 'ko' else 'ko'
        self.update_ui_language()

    def update_ui_language(self):
        self.root.title(get_string('window_title'))
        self.lang_toggle_button.config(text=get_string('toggle_lang_button_text_to_en') if current_language == 'ko' else get_string('toggle_lang_button_text_to_ko'))
        self.root_notebook.tab(self.tab_converter_frame, text=get_string('tab_main_converter'))
        self.root_notebook.tab(self.tab_splitter_frame, text=get_string('tab_main_splitter'))
        self.root_notebook.tab(self.tab_settings_frame, text=get_string('tab_main_settings'))

        self.conv_notebook.tab(self.sf_tab_frame, text=get_string('tab_single_file'))
        self.conv_notebook.tab(self.bf_tab_frame, text=get_string('tab_batch_folder'))
        
        self.sf_labelframe_select_file_widget.config(text=get_string('sf_labelframe_select_file'))
        self.sf_button_select_file_widget.config(text=get_string('button_select_file'))
        self.sf_label_original_extension_widget.config(text=get_string('sf_label_original_extension'))
        self.sf_label_target_format_widget.config(text=get_string('label_target_format'))
        self.sf_button_add_to_queue.config(text=get_string('button_add_to_queue'))
        self.sf_labelframe_queue_widget.config(text=get_string('sf_labelframe_queue'))
        self.sf_button_stop.config(text=get_string('button_stop'))
        self.sf_button_clear.config(text=get_string('button_clear_list'))
        self.sf_button_start_queue.config(text=get_string('button_start_queue'))

        self.bf_labelframe_input_folder_widget.config(text=get_string('bf_labelframe_input_folder'))
        self.bf_button_select_input_folder_widget.config(text=get_string('button_select_folder'))
        self.bf_labelframe_conversion_settings_widget.config(text=get_string('bf_labelframe_conversion_settings'))
        self.bf_label_target_format_widget.config(text=get_string('label_target_format'))
        self.bf_convert_button_widget.config(text=get_string('button_start_batch_conversion'))
        self.bf_stream_copy_button_widget.config(text=get_string('button_start_batch_stream_copy'))
        self.bf_check_auto_archive_widget.config(text=get_string('bf_check_auto_archive'))
        self.bf_labelframe_log_widget.config(text=get_string('bf_labelframe_log'))
        self.bf_button_stop.config(text=get_string('button_stop'))
        
        self.sp_labelframe_input_widget.config(text=get_string('sp_labelframe_input'))
        self.sp_button_select_file_widget.config(text=get_string('button_select_file'))
        self.sp_labelframe_settings_widget.config(text=get_string('sp_labelframe_settings'))
        self.sp_label_size_widget.config(text=get_string('sp_label_size'))
        self.sp_label_unit_widget.config(text=get_string('sp_label_unit'))
        self.sp_start_button_widget.config(text=get_string('sp_button_start'))
        self.sp_button_stop.config(text=get_string('button_stop'))

        self.settings_labelframe_ffmpeg_widget.config(text=get_string('settings_labelframe_ffmpeg'))
        self.settings_label_ffmpeg_path_widget.config(text=get_string('settings_label_ffmpeg_path'))
        self.settings_label_ffprobe_path_widget.config(text=get_string('settings_label_ffprobe_path'))
        self.settings_button_browse_ffmpeg.config(text=get_string('button_browse'))
        self.settings_button_browse_ffprobe.config(text=get_string('button_browse'))
        self.settings_ffmpeg_help_label.config(text=get_string('settings_ffmpeg_help'))
        self.settings_labelframe_cpu_widget.config(text=get_string('settings_labelframe_cpu'))
        self.settings_label_codec_widget.config(text=get_string('settings_label_codec'))
        self.settings_label_cpu_threads_widget.config(text=get_string('settings_label_cpu_threads'))
        self.settings_label_cpu_total_widget.config(text=get_string('settings_label_cpu_total', total_cores=self.total_cpu_cores))
        self.settings_labelframe_gpu_widget.config(text=get_string('settings_labelframe_gpu'))
        self.settings_label_gpu_quality_widget.config(text=get_string('settings_label_gpu_quality'))
        self.settings_gpu_quality_tooltip_widget.config(text=get_string('settings_gpu_quality_tooltip'))
        self.gpu_notebook.tab(self.nv_settings_frame, text=get_string('tab_gpu_nvidia'))
        self.settings_label_nv_preset_widget.config(text=get_string('settings_label_nv_preset'))
        self.settings_help_nv_label.config(text=get_string('settings_help_nv'))
        self.gpu_notebook.tab(self.intel_settings_frame, text=get_string('tab_gpu_intel'))
        self.settings_label_intel_preset_widget.config(text=get_string('settings_label_intel_preset'))
        self.settings_help_intel_label.config(text=get_string('settings_help_intel'))
        self.gpu_notebook.tab(self.amd_settings_frame, text=get_string('tab_gpu_amd'))
        self.settings_label_amd_usage_widget.config(text=get_string('settings_label_amd_usage'))
        self.settings_help_amd_label.config(text=get_string('settings_help_amd'))

    def browse_ffmpeg_path(self, target):
        fp = filedialog.askopenfilename(title=f"Select {target}.exe", filetypes=[(get_string('filetype_exe_files'), "*.exe"), (get_string('filetype_all_files'), "*.*")])
        if fp:
            if target == "ffmpeg": self.ffmpeg_path_var.set(fp)
            else: self.ffprobe_path_var.set(fp)
            configure_ffmpeg_path(self.ffmpeg_path_var.get(), self.ffprobe_path_var.get())
            save_config({"ffmpeg_path": self.ffmpeg_path_var.get(), "ffprobe_path": self.ffprobe_path_var.get()})

    def log_message(self, message):
        self.progress_queue.put({"type": "log_append", "message": message})

    def get_video_duration(self, input_path):
        if not SYSTEM_FFPROBE: return 0
        try:
            cmd = [SYSTEM_FFPROBE, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_path]
            startupinfo = subprocess.STARTUPINFO(); startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            res = subprocess.run(cmd, capture_output=True, text=True, check=True, startupinfo=startupinfo)
            return float(res.stdout.strip())
        except: return 0

    # ---------------------------------------------------------
    # Drag & Drop Logic
    # ---------------------------------------------------------
    def register_dnd(self, widget, callback):
        widget.drop_target_register(DND_FILES)
        widget.dnd_bind('<<DropEnter>>', lambda e: self.on_dnd_enter(widget, e))
        widget.dnd_bind('<<DropLeave>>', lambda e: self.on_dnd_leave(widget, e))
        widget.dnd_bind('<<Drop>>', lambda e: self.on_dnd_drop(widget, e, callback))

    def on_dnd_enter(self, widget, event):
        try: widget.configure(style="Highlight.TLabelframe")
        except: pass

    def on_dnd_leave(self, widget, event):
        try: widget.configure(style="TLabelframe")
        except: pass

    def on_dnd_drop(self, widget, event, callback):
        self.on_dnd_leave(widget, event)
        paths = self.parse_dnd_paths(event.data)
        if paths:
            callback(paths[0]) 

    def parse_dnd_paths(self, data):
        # Regex for Windows path handling (curly braces)
        paths = []
        pattern = re.compile(r'\{.*?\}|\S+')
        matches = pattern.findall(data)
        for match in matches:
            path = match.strip('{}')
            if path: paths.append(path)
        return paths

    def handle_dnd_single_file(self, path):
        if os.path.isdir(path):
            messagebox.showwarning(get_string('dialog_title_warning'), get_string('dnd_err_folder_on_file'))
            return
        
        self.sf_input_filepath.set(path)
        self.sf_original_extension.set(os.path.splitext(path)[1])

    def handle_dnd_batch_folder(self, path):
        if os.path.isfile(path):
            path = os.path.dirname(path)
        
        self.bf_input_folder_path.set(path)
        self.update_conversion_options()

    def handle_dnd_splitter_file(self, path):
        if os.path.isdir(path):
            messagebox.showwarning(get_string('dialog_title_warning'), get_string('dnd_err_folder_on_file'))
            return
        self.sp_input_filepath.set(path)
        self.sp_start_button_widget.config(state="normal")

    # ---------------------------------------------------------
    # Logic: Queue & Single File Operations
    # ---------------------------------------------------------
    def sf_select_file(self):
        fp = filedialog.askopenfilename(title=get_string('dialog_title_select_video_file'), filetypes=[(get_string('filetype_video_files'), " ".join(f"*{e}" for e in VIDEO_EXTENSIONS)), (get_string('filetype_all_files'), "*.*")])
        if fp:
            self.sf_input_filepath.set(fp)
            self.sf_original_extension.set(os.path.splitext(fp)[1])

    def sf_add_to_queue(self):
        filepath = self.sf_input_filepath.get()
        target_fmt = self.sf_target_format.get()
        if not filepath or not target_fmt: return

        filename = os.path.basename(filepath)
        
        row_frame = ttk.Frame(self.sf_queue_frame.scrollable_frame, padding=5)
        row_frame.pack(fill=tk.X, pady=2, expand=True) 
        
        chk_var = tk.IntVar()
        chk = ttk.Checkbutton(row_frame, variable=chk_var)
        chk.pack(side=tk.LEFT, padx=(0, 5))

        pb = ttk.Progressbar(row_frame, orient=tk.HORIZONTAL, mode='determinate', length=200)
        pb.pack(side=tk.RIGHT, padx=10)

        lbl_status = ttk.Label(row_frame, text="Ready", width=25, anchor="e", font=("Segoe UI", 9))
        lbl_status.pack(side=tk.RIGHT, padx=5)

        lbl_info = ttk.Label(row_frame, text=f"{filename} -> {target_fmt}", font=("Segoe UI", 9))
        lbl_info.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.tasks_queue_data.append({
            "filepath": filepath,
            "target_fmt": target_fmt,
            "status": "Ready",
            "chk_var": chk_var 
        })
        self.task_widgets.append({
            "frame": row_frame,
            "status_lbl": lbl_status,
            "progress_bar": pb
        })
        
        self.update_conversion_options()

    def sf_clear_list(self):
        if self.is_running: return
        for w in self.task_widgets:
            w['frame'].destroy()
        self.task_widgets.clear()
        self.tasks_queue_data.clear()
        
        self.update_conversion_options()

    def sf_start_queue_processing(self):
        if self.is_running or not self.tasks_queue_data: return
        self.is_running = True
        self.set_ui_state(processing=True, mode="single")
        
        threading.Thread(target=self.execute_queue_processing, daemon=True).start()

    def execute_queue_processing(self):
        try:
            # Reset failed/stopped/cancelled tasks to 'Ready' for retry
            for i, task in enumerate(self.tasks_queue_data):
                if task['status'] in ["Error", "Stopped", "Cancelled"]:
                    task['status'] = "Ready"
                    self.progress_queue.put({"type": "queue_update", "index": i, "status": "Ready", "progress": 0})

            total_tasks = len(self.tasks_queue_data)
            
            for i, task in enumerate(self.tasks_queue_data):
                if not self.is_running: break 
                
                if task['status'] == "Done": 
                    continue

                self.current_task_index = i
                filepath = task['filepath']
                target_fmt = task['target_fmt']
                ext = TARGET_FORMATS.get(target_fmt)
                output_path = os.path.join(os.path.dirname(filepath), f"{os.path.splitext(os.path.basename(filepath))[0]}_converted.{ext}")

                self.progress_queue.put({"type": "queue_update", "index": i, "status": "Processing...", "progress": 0})
                
                hw_configs, cpu_args = self._get_encoding_params()
                success = False
                
                if ext == 'gif':
                    args = ['-vf', f'fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse']
                    success, _ = self.run_ffmpeg_direct(filepath, output_path, args, task_index=i)
                else:
                    for hw in hw_configs:
                        if not self.is_running: break
                        if task['status'] == "Cancelled": break 
                        success, _ = self.run_ffmpeg_direct(filepath, output_path, hw['args'], task_index=i)
                        if success: break
                    
                    if not success and self.is_running and task['status'] != "Cancelled":
                         success, _ = self.run_ffmpeg_direct(filepath, output_path, cpu_args, task_index=i)

                if task['status'] == "Cancelled":
                    final_status = "Cancelled"
                    success = False
                elif not self.is_running:
                    final_status = "Stopped"
                    success = False
                else:
                    final_status = "Done" if success else "Error"

                self.progress_queue.put({"type": "queue_update", "index": i, "status": final_status, "progress": 100 if success else 0})
                task['status'] = final_status

        except Exception as e:
            print(f"Critical Worker Error: {e}")

        finally:
            # Ensure completion signal is sent even if thread crashes
            self.progress_queue.put({"type": "queue_complete"})

    # ---------------------------------------------------------
    # Logic: Batch Operations
    # ---------------------------------------------------------
    def bf_select_input_folder(self):
        fp = filedialog.askdirectory(title=get_string('dialog_title_select_input_folder'))
        if fp:
            self.bf_input_folder_path.set(fp)
            self.update_conversion_options()

    def bf_start_batch_thread(self, mode):
        if self.is_running: return
        inp = self.bf_input_folder_path.get()
        fmt = self.bf_target_format.get()
        if not inp or not fmt: return
        
        self.is_running = True
        self.set_ui_state(processing=True, mode="batch")
        self.bf_log_text.config(state='normal')
        self.bf_log_text.delete(1.0, tk.END)
        self.bf_log_text.config(state='disabled')
        
        threading.Thread(target=self.execute_batch_conversion, args=(mode, inp, fmt), daemon=True).start()

    def execute_batch_conversion(self, mode, inp_folder, fmt):
        ext = TARGET_FORMATS.get(fmt)
        files = [os.path.join(inp_folder, f) for f in os.listdir(inp_folder) 
                 if os.path.isfile(os.path.join(inp_folder, f)) 
                 and os.path.splitext(f)[1].lower() in VIDEO_EXTENSIONS 
                 and os.path.splitext(f)[1].lower() != f".{ext}"]
        
        if not files:
            self.progress_queue.put({"type": "batch_error", "message": get_string('dialog_msg_no_files_to_convert_info')})
            return

        self.log_message(f"Found {len(files)} files to process.")
        
        for i, inp in enumerate(files):
            if not self.is_running: break
            
            fn = os.path.basename(inp)
            outp = os.path.join(os.path.dirname(inp), f"{os.path.splitext(fn)[0]}_{'fast' if mode=='remux' else 'conv'}.{ext}")
            
            self.log_message(f"[{i+1}/{len(files)}] Processing: {fn}")
            
            success = False
            msg = ""
            
            if mode == 'remux':
                args = ['-c', 'copy']
                success, msg = self.run_ffmpeg_direct(inp, outp, args)
            else:
                hw_configs, cpu_args = self._get_encoding_params()
                for hw in hw_configs:
                    if not self.is_running: break
                    success, msg = self.run_ffmpeg_direct(inp, outp, hw['args'])
                    if success: break
                if not success and self.is_running:
                    success, msg = self.run_ffmpeg_direct(inp, outp, cpu_args)

            if success:
                self.log_message(f" > Success.")
                if self.bf_auto_archive.get():
                    try:
                        archive_dir = os.path.join(inp_folder, "_Originals")
                        os.makedirs(archive_dir, exist_ok=True)
                        dest_path = os.path.join(archive_dir, fn)
                        if os.path.exists(dest_path):
                            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            name, e = os.path.splitext(fn)
                            dest_path = os.path.join(archive_dir, f"{name}_{ts}{e}")
                        shutil.move(inp, dest_path)
                        self.log_message(f" > Archived to: _Originals/{os.path.basename(dest_path)}")
                    except Exception as e:
                        self.log_message(f" > Archive Failed: {e}")
            else:
                self.log_message(f" > Failed: {msg}")

        self.progress_queue.put({"type": "batch_complete"})

    # ---------------------------------------------------------
    # Logic: Core FFmpeg & Stop
    # ---------------------------------------------------------
    def stop_processing(self):
        selected_indices = []
        if self.tasks_queue_data:
            for i, task in enumerate(self.tasks_queue_data):
                if task['chk_var'].get() == 1 and task['status'] not in ["Done", "Error", "Cancelled"]:
                    selected_indices.append(i)

        if selected_indices:
            # Cancel specific tasks
            for idx in selected_indices:
                self.tasks_queue_data[idx]['status'] = "Cancelled"
                self.progress_queue.put({"type": "queue_update", "index": idx, "status": "Cancelled", "progress": 0})
                
                if idx == self.current_task_index and self.current_process:
                    print(f"Killing running process for task {idx}")
                    try:
                        self.current_process.terminate()
                    except: pass
            
            for idx in selected_indices:
                self.tasks_queue_data[idx]['chk_var'].set(0)
                
        else:
            # Global Stop
            if self.is_running:
                self.is_running = False
                if self.current_process:
                    try:
                        self.current_process.terminate()
                    except: pass
                self.log_message("!!! STOPPED BY USER !!!")
                self.progress_queue.put({"type": "stopped"})

    def run_ffmpeg_direct(self, input_path, output_path, preset_args, task_index=None):
        if not SYSTEM_FFMPEG: return False, "FFmpeg not found"
        
        duration = self.get_video_duration(input_path)
        cmd = [SYSTEM_FFMPEG, '-y', '-i', input_path] + preset_args + [output_path]
        
        startupinfo = subprocess.STARTUPINFO(); startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        self.eta_calculator.start() 

        try:
            self.current_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                universal_newlines=True, startupinfo=startupinfo, encoding='utf-8', errors='ignore'
            )
            
            for line in self.current_process.stdout:
                if not self.is_running: 
                    self.current_process.terminate()
                    break

                if task_index is not None and self.tasks_queue_data[task_index]['status'] == "Cancelled":
                    self.current_process.terminate()
                    break

                time_match = re.search(r'time=(\d+):(\d+):(\d+\.\d+)', line)
                if time_match and duration > 0:
                    h, m, s = map(float, time_match.groups())
                    current_seconds = h*3600 + m*60 + s
                    percent = min(int((current_seconds / duration) * 100), 99)
                    
                    eta_str = self.eta_calculator.update(percent)
                    
                    if task_index is not None:
                        status_str = f"{percent}%"
                        if eta_str: status_str += f" ({eta_str})"
                        self.progress_queue.put({"type": "queue_update", "index": task_index, "progress": percent, "status": status_str})

            self.current_process.wait()
            ret = self.current_process.returncode
            self.current_process = None
            
            if task_index is not None and self.tasks_queue_data[task_index]['status'] == "Cancelled":
                return False, "Cancelled"
            if not self.is_running: return False, "Stopped"
            
            return (ret == 0), "Error" if ret != 0 else "Success"
            
        except Exception as e: 
            return False, str(e)

    def _get_encoding_params(self):
        threads = str(self.cpu_threads_to_use.get())
        qp = str(self.gpu_quality_target_crf.get())
        codec = self.selected_video_codec.get()
        
        nv_p_user = self.nv_preset.get()
        nv_map = {'p1': 'fast', 'p2': 'fast', 'p3': 'medium', 'p4': 'medium', 'p5': 'medium', 'p6': 'slow', 'p7': 'slow', 'slow': 'slow', 'medium': 'medium', 'fast': 'fast'}
        actual_nv_preset = nv_map.get(nv_p_user, 'medium')
        nv_params = ["-preset", actual_nv_preset, "-rc", "constqp", "-qp", qp, "-b:v", "0", "-spatial_aq", "1", "-pix_fmt", "yuv420p"]
        hw_configs = []
        hw_configs.append({'name': f'NVIDIA {codec}', 'args': ['-c:v', 'h264_nvenc' if codec=='H.264' else 'hevc_nvenc' if codec=='H.265' else 'av1_nvenc'] + nv_params})
        cpu_c = {'H.264': 'libx264', 'H.265': 'libx265', 'AV1': 'libsvtav1'}.get(codec)
        cpu_args = ['-c:v', cpu_c, '-crf', qp, '-preset', 'faster' if 'libx26' in cpu_c else 'preset', '-threads', threads, '-pix_fmt', 'yuv420p']
        return hw_configs, cpu_args

    def set_ui_state(self, processing=True, mode="single"):
        state = "disabled" if processing else "normal"
        stop_state = "normal" if processing else "disabled"
        
        if mode == "single":
            self.sf_button_start_queue.config(state=state)
            self.sf_button_add_to_queue.config(state=state)
            self.sf_button_clear.config(state=state)
            self.sf_button_stop.config(state="normal") 
        elif mode == "batch":
            self.bf_convert_button_widget.config(state=state)
            self.bf_stream_copy_button_widget.config(state=state)
            self.bf_button_stop.config(state=stop_state)
        elif mode == "splitter":
            self.sp_start_button_widget.config(state=state)
            self.sp_button_stop.config(state=stop_state)

    def update_conversion_options(self, event=None):
        sf_ready = bool(self.tasks_queue_data)
        self.sf_button_start_queue.config(state="normal" if sf_ready and not self.is_running else "disabled")
        bf_ready = bool(self.bf_input_folder_path.get()) and bool(self.bf_target_format.get())
        if not self.is_running:
            self.bf_convert_button_widget.config(state="normal" if bf_ready else "disabled")
            self.bf_stream_copy_button_widget.config(state="normal" if bf_ready else "disabled")

    # ---------------------------------------------------------
    # Splitter Logic
    # ---------------------------------------------------------
    def sp_select_file(self):
        if self.is_running: return
        fp = filedialog.askopenfilename(title=get_string('dialog_title_select_video_file'), filetypes=[(get_string('filetype_video_files'), "*.mp4;*.avi;*.mkv;*.mov;*.wmv"), (get_string('filetype_all_files'), "*.*")])
        if fp:
            self.sp_input_filepath.set(fp)
            self.sp_start_button_widget.config(state="normal")

    def sp_start_splitting_thread(self):
        # Check independent splitter state
        if self.is_splitter_running: return
        
        video_path = self.sp_input_filepath.get()
        size_val = self.sp_split_size.get()
        unit = self.sp_split_unit.get()
        
        if not video_path or not os.path.exists(video_path): return
        
        try:
            split_size_float = float(size_val)
            if split_size_float <= 0: raise ValueError
            
            output_dir = filedialog.askdirectory()
            if not output_dir: return

            self.is_splitter_running = True
            
            # Update UI for splitter only
            self.sp_start_button_widget.config(state="disabled")
            self.sp_button_stop.config(state="normal")
            
            self.sp_progress_bar['value'] = 0
            
            threading.Thread(target=self.execute_splitter, args=(video_path, split_size_float, unit, output_dir), daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def execute_splitter(self, video_path, split_size, unit, output_dir):
        try:
            if unit == "MB": split_size_bytes = int(split_size * 1024 * 1024)
            else: split_size_bytes = int(split_size * 1024 * 1024 * 1024)
            
            total_size_bytes = os.path.getsize(video_path)
            num_segments = int(total_size_bytes / split_size_bytes)
            if total_size_bytes % split_size_bytes != 0: num_segments += 1
            
            duration = self.get_video_duration(video_path)
            if duration == 0:
                raise Exception("Cannot determine video duration.")
                
            segment_duration = duration / num_segments
            file_name, file_ext = os.path.splitext(os.path.basename(video_path))
            
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            for i in range(num_segments):
                if not self.is_splitter_running: break
                
                start_time = i * segment_duration
                output_file = os.path.join(output_dir, f"{file_name}_part_{i+1:03d}{file_ext}")
                
                # Fast split using stream copy (-c copy)
                # -ss before -i for fast seek
                cmd = [
                    SYSTEM_FFMPEG, '-y', 
                    '-ss', str(start_time), 
                    '-i', video_path, 
                    '-t', str(segment_duration), 
                    '-c', 'copy', 
                    output_file
                ]
                
                self.splitter_process = subprocess.Popen(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT, 
                    startupinfo=startupinfo
                )
                self.splitter_process.wait()
                
                if self.splitter_process.returncode != 0:
                     raise Exception(f"FFmpeg Error on segment {i+1}")

                self.progress_queue.put({"type": "progress_splitter", "current": i+1, "total": num_segments})

            self.progress_queue.put({"type": "splitter_complete"})
            
        except Exception as e:
            self.progress_queue.put({"type": "splitter_error", "message": str(e)})
        finally:
            self.splitter_process = None

    # ---------------------------------------------------------
    # Main Loop
    # ---------------------------------------------------------
    def stop_splitter(self):
        # Stop only the splitter process
        if self.is_splitter_running:
            self.is_splitter_running = False
            if self.splitter_process:
                try:
                    self.splitter_process.terminate()
                except: pass
            self.log_message("!!! SPLITTER STOPPED BY USER !!!")
            self.progress_queue.put({"type": "splitter_stopped"})
    def process_queue(self):
        try:
            while True:
                msg = self.progress_queue.get_nowait()
                mtype = msg.get("type")
                
                if mtype == "log_append":
                    self.bf_log_text.config(state='normal')
                    self.bf_log_text.insert(tk.END, msg['message'] + "\n")
                    self.bf_log_text.see(tk.END)
                    self.bf_log_text.config(state='disabled')
                
                elif mtype == "queue_update":
                    idx = msg['index']
                    if idx < len(self.task_widgets):
                        w = self.task_widgets[idx]
                        if 'status' in msg: w['status_lbl'].config(text=msg['status'])
                        if 'progress' in msg: w['progress_bar']['value'] = msg['progress']

                elif mtype == "queue_complete":
                    self.is_running = False
                    self.set_ui_state(processing=False, mode="single")
                    messagebox.showinfo(get_string('dialog_title_info'), get_string('status_complete'))

                elif mtype == "batch_complete":
                    self.is_running = False
                    self.set_ui_state(processing=False, mode="batch")
                    self.log_message("=== BATCH JOB COMPLETED ===")
                    messagebox.showinfo(get_string('dialog_title_info'), get_string('status_complete'))

                elif mtype == "stopped":
                    # Stop converter UI only
                    self.set_ui_state(processing=False, mode="single")
                    self.set_ui_state(processing=False, mode="batch")
                    messagebox.showinfo(get_string('dialog_title_info'), get_string('status_stopped'))
                
                # --- Splitter Events (Independent) ---
                elif mtype == "progress_splitter":
                    self.sp_progress_bar['value'] = (msg['current'] / msg['total']) * 100
                    self.sp_progress_label_widget.config(text=f"{msg['current']}/{msg['total']}")

                elif mtype == "splitter_complete":
                    self.is_splitter_running = False
                    self.sp_start_button_widget.config(state="normal")
                    self.sp_button_stop.config(state="disabled")
                    self.sp_progress_bar['value'] = 100
                    messagebox.showinfo(get_string('dialog_title_info'), get_string('status_complete'))
                    
                elif mtype == "splitter_stopped":
                    self.is_splitter_running = False
                    self.sp_start_button_widget.config(state="normal")
                    self.sp_button_stop.config(state="disabled")
                    messagebox.showinfo(get_string('dialog_title_info'), get_string('status_stopped'))

                elif mtype == "splitter_error":
                    self.is_splitter_running = False
                    self.sp_start_button_widget.config(state="normal")
                    self.sp_button_stop.config(state="disabled")
                    messagebox.showerror(get_string('dialog_title_error'), msg.get("message"))

        except queue.Empty: pass
        finally: self.root.after(100, self.process_queue)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = VideoToolSuite(root)
    root.mainloop()