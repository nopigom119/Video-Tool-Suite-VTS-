import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import os
import threading
import queue
import shutil
import subprocess
import json
import re
import time
import datetime
import math

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

# --- FFmpeg Path Configuration (Shared) ---
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
        print(f"[SYSTEM] FFmpeg detected: {ffmpeg_path}")
        os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path
        SYSTEM_FFMPEG = ffmpeg_path
    else:
        SYSTEM_FFMPEG = None
        print("[WARNING] FFmpeg not found.")

    if ffprobe_path and os.path.exists(ffprobe_path):
        print(f"[SYSTEM] FFprobe detected: {ffprobe_path}")
        SYSTEM_FFPROBE = ffprobe_path
    else:
        SYSTEM_FFPROBE = None
        print("[WARNING] FFprobe not found.")

    return SYSTEM_FFMPEG, SYSTEM_FFPROBE

# Initial Load
_config = load_config()
configure_ffmpeg_path(_config.get("ffmpeg_path"), _config.get("ffprobe_path"))


# --- Language Configuration ---
current_language = 'ko' 

LANG_STRINGS = {
    'en': {
        'window_title': "Video Tool Suite (Convert & Split)",
        'toggle_lang_button_text_to_ko': "한국어",
        'toggle_lang_button_text_to_en': "English",
        
        # Main Tabs
        'tab_main_converter': "Video Converter",
        'tab_main_splitter': "Video Splitter",
        'tab_main_settings': "Global Settings",

        # Converter Sub-Tabs
        'tab_single_file': "Single File",
        'tab_batch_folder': "Batch Folder",
        
        # GPU Tabs
        'tab_gpu_nvidia': "NVIDIA (NVENC)",
        'tab_gpu_intel': "Intel (QSV)",
        'tab_gpu_amd': "AMD (AMF)",

        # Common Labels/Buttons
        'label_target_format': "Target Format:",
        'button_select_file': "Select File",
        'button_select_folder': "Select Folder",
        'button_start_conversion': "Start Encoding",
        'button_start_stream_copy': "Fast Copy",
        'button_start_batch_conversion': "Start Batch",
        'button_start_batch_stream_copy': "Fast Batch",
        'button_clear_selection': "Clear",
        'button_browse': "Browse",
        
        # Splitter UI
        'sp_labelframe_input': "Input Video",
        'sp_labelframe_settings': "Split Settings",
        'sp_label_size': "Split Size:",
        'sp_label_unit': "Unit:",
        'sp_button_start': "Start Splitting",
        'sp_status_calculating': "Calculating segments...",
        'sp_status_splitting': "Splitting segment {current}/{total}...",
        'sp_status_complete': "Splitting Complete. Files saved to: {folder}",
        'sp_error_size_zero': "Split size must be greater than 0.",
        'sp_error_no_file': "Please select a video file.",
        'sp_error_duration': "Could not determine video duration.",
        
        # Converter UI frames
        'sf_labelframe_select_file': "File Selection",
        'sf_labelframe_original_info': "Original Info",
        'sf_label_original_extension': "Ext:",
        'sf_labelframe_conversion_settings': "Settings",
        'bf_labelframe_input_folder': "Input",
        'bf_labelframe_output_originals_folder': "Output (Originals)",
        'bf_labelframe_conversion_settings': "Settings",
        
        # Settings UI
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
        
        # Status Messages
        'status_initial_prompt': "Ready.",
        'status_converter_prompt': "Converter Mode.",
        'status_splitter_prompt': "Splitter Mode.",
        'status_sf_file_selected': "File: {filename}",
        'status_bf_input_folder_selected': "In: {folder_path}",
        'status_converting_progress': "Processing: {filename} ({percent}%)",
        'status_time_info': " [Rem: {rem} | Tot: {tot}]",
        'status_complete': "Work Complete.",
        'status_error': "Error Occurred.",
        
        # Dialogs
        'dialog_title_warning': "Warning",
        'dialog_title_error': "Error",
        'dialog_title_info': "Info",
        'dialog_title_select_video_file': "Select Video",
        'dialog_title_select_input_folder': "Select Folder",
        'dialog_title_select_output_folder': "Select Output Folder",
        'dialog_msg_conversion_in_progress_warning': "Busy.",
        'dialog_msg_no_files_to_convert_info': "No files found.",
        'filetype_video_files': "Video Files",
        'filetype_all_files': "All Files",
        'filetype_exe_files': "Executables",
    },
    'ko': {
        'window_title': "영상 도구 모음 (변환 및 분할)",
        'toggle_lang_button_text_to_ko': "한국어",
        'toggle_lang_button_text_to_en': "English",
        
        # Main Tabs
        'tab_main_converter': "영상 변환기",
        'tab_main_splitter': "영상 분할기",
        'tab_main_settings': "통합 설정",

        # Converter Sub-Tabs
        'tab_single_file': "단일 변환",
        'tab_batch_folder': "일괄 변환",
        
        # GPU Tabs
        'tab_gpu_nvidia': "NVIDIA",
        'tab_gpu_intel': "Intel",
        'tab_gpu_amd': "AMD",

        # Common Labels/Buttons
        'label_target_format': "변환 포맷:",
        'button_select_file': "파일 선택",
        'button_select_folder': "폴더 선택",
        'button_start_conversion': "변환 시작",
        'button_start_stream_copy': "빠른 변환",
        'button_start_batch_conversion': "일괄 시작",
        'button_start_batch_stream_copy': "일괄 빠른 변환",
        'button_clear_selection': "해제",
        'button_browse': "찾기",
        
        # Splitter UI
        'sp_labelframe_input': "입력 파일",
        'sp_labelframe_settings': "분할 설정",
        'sp_label_size': "분할 크기:",
        'sp_label_unit': "단위:",
        'sp_button_start': "분할 시작",
        'sp_status_calculating': "분할 구간 계산 중...",
        'sp_status_splitting': "분할 진행 중... {current}/{total}",
        'sp_status_complete': "분할 완료. 저장 폴더: {folder}",
        'sp_error_size_zero': "분할 크기는 0보다 커야 합니다.",
        'sp_error_no_file': "동영상 파일을 선택해주세요.",
        'sp_error_duration': "동영상 길이를 확인할 수 없습니다.",

        # Converter UI frames
        'sf_labelframe_select_file': "파일 선택",
        'sf_labelframe_original_info': "원본 정보",
        'sf_label_original_extension': "확장자:",
        'sf_labelframe_conversion_settings': "변환 설정",
        'bf_labelframe_input_folder': "입력 폴더",
        'bf_labelframe_output_originals_folder': "원본 보관 폴더 (선택)",
        'bf_labelframe_conversion_settings': "변환 설정",
        
        # Settings UI
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
        
        # Status Messages
        'status_initial_prompt': "준비 완료.",
        'status_converter_prompt': "변환기 모드.",
        'status_splitter_prompt': "분할기 모드.",
        'status_sf_file_selected': "선택: {filename}",
        'status_bf_input_folder_selected': "입력: {folder_path}",
        'status_converting_progress': "진행 중: {filename} ({percent}%)",
        'status_time_info': " [남은 시간: {rem} | 총 시간: {tot}]",
        'status_complete': "작업이 완료되었습니다.",
        'status_error': "오류가 발생했습니다.",
        
        # Dialogs
        'dialog_title_warning': "경고",
        'dialog_title_error': "오류",
        'dialog_title_info': "알림",
        'dialog_title_select_video_file': "비디오 선택",
        'dialog_title_select_input_folder': "폴더 선택",
        'dialog_title_select_output_folder': "저장 폴더 선택",
        'dialog_msg_conversion_in_progress_warning': "작업 중입니다.",
        'dialog_msg_no_files_to_convert_info': "파일이 없습니다.",
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
SUPPORTED_CODECS_FOR_REMUX = {
    'mp4': {'v': ['h264', 'hevc', 'av1'], 'a': ['aac', 'ac3', 'mp3']},
    'mov': {'v': ['h264', 'hevc', 'av1'], 'a': ['aac', 'ac3', 'mp3']},
    'mkv': 'any'
}

class VideoToolSuite:
    def __init__(self, root_window):
        self.root = root_window
        self.root.geometry("750x880")
        
        # --- Modern Dark Theme Setup ---
        self.style = ttk.Style()
        self.setup_dark_theme()

        # Shared Status & Queue
        self.status = tk.StringVar()
        self.time_info = tk.StringVar()
        self.progress_queue = queue.Queue()
        
        # Concurrency Flags
        self.converter_running = False
        self.splitter_running = False
        self.current_process = None 

        # Hardware Info
        self.total_cpu_cores = os.cpu_count() if os.cpu_count() else 1
        self.cpu_threads_to_use = tk.IntVar(value=max(1, self.total_cpu_cores // 2))
        
        # Settings Variables
        self.ffmpeg_path_var = tk.StringVar(value=SYSTEM_FFMPEG if SYSTEM_FFMPEG else "")
        self.ffprobe_path_var = tk.StringVar(value=SYSTEM_FFPROBE if SYSTEM_FFPROBE else "")
        self.selected_video_codec = tk.StringVar(value='H.264')
        self.gpu_quality_target_crf = tk.IntVar(value=23)
        self.nv_preset = tk.StringVar(value='p4') 
        self.nv_tune = tk.StringVar(value='hq')
        self.intel_preset = tk.StringVar(value='fast')
        self.amd_usage = tk.StringVar(value='transcoding')
        self.amd_quality = tk.StringVar(value='quality')

        # --- Converter Variables ---
        self.sf_input_filepath = tk.StringVar()
        self.sf_original_extension = tk.StringVar()
        self.sf_target_format = tk.StringVar()
        self.bf_input_folder_path = tk.StringVar()
        self.bf_output_folder_originals_path = tk.StringVar()
        self.bf_target_format = tk.StringVar()
        self.bf_files_to_convert_list = []
        self.bf_converted_original_files_paths = []

        # --- Splitter Variables ---
        self.sp_input_filepath = tk.StringVar()
        self.sp_split_size = tk.StringVar(value="100")
        self.sp_split_unit = tk.StringVar(value="MB")

        # Build UI
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

    def create_main_layout(self):
        # Top Bar
        top_bar = ttk.Frame(self.root, padding=(15, 10))
        top_bar.pack(fill=tk.X)
        
        title_lbl = ttk.Label(top_bar, text="VIDEO TOOL SUITE", font=("Segoe UI", 16, "bold"), foreground="#007ACC")
        title_lbl.pack(side=tk.LEFT)
        
        self.lang_toggle_button = ttk.Button(top_bar, command=self.toggle_language)
        self.lang_toggle_button.pack(side=tk.RIGHT)

        # Main Content (Root Notebook)
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.root_notebook = ttk.Notebook(main_frame)
        self.root_notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # --- Tab 1: Converter (Video Convert App) ---
        self.tab_converter_frame = ttk.Frame(self.root_notebook, padding="10")
        self.root_notebook.add(self.tab_converter_frame, text="Converter")
        self.create_converter_ui(self.tab_converter_frame)

        # --- Tab 2: Splitter (Video Div App) ---
        self.tab_splitter_frame = ttk.Frame(self.root_notebook, padding="20")
        self.root_notebook.add(self.tab_splitter_frame, text="Splitter")
        self.create_splitter_ui(self.tab_splitter_frame)

        # --- Tab 3: Settings (Shared) ---
        self.tab_settings_frame = ttk.Frame(self.root_notebook, padding="20")
        self.root_notebook.add(self.tab_settings_frame, text="Settings")
        self.create_settings_ui(self.tab_settings_frame)

        # Status Bar
        status_frame = ttk.Frame(self.root, padding=(10, 5))
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label_widget = ttk.Label(status_frame, textvariable=self.status, font=("Segoe UI", 9, "bold"), foreground="#007ACC")
        self.status_label_widget.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.time_info_label_widget = ttk.Label(status_frame, textvariable=self.time_info, font=("Segoe UI", 9), foreground="#AAAAAA")
        self.time_info_label_widget.pack(side=tk.RIGHT)

        self.root_notebook.bind("<<NotebookTabChanged>>", self.on_main_tab_change)

    # ---------------------------------------------------------
    # UI Creation: Converter
    # ---------------------------------------------------------
    def create_converter_ui(self, parent):
        # Nested Notebook for Single/Batch
        self.conv_notebook = ttk.Notebook(parent)
        self.conv_notebook.pack(fill=tk.BOTH, expand=True)

        # Single File Tab
        self.sf_tab_frame = ttk.Frame(self.conv_notebook, padding="20")
        self.conv_notebook.add(self.sf_tab_frame, text="") # Text set by language update
        
        # -- Single File Widgets --
        lf_sel = ttk.LabelFrame(self.sf_tab_frame, text="File Selection", padding="15")
        lf_sel.pack(fill=tk.X, pady=(0, 15))
        self.sf_labelframe_select_file_widget = lf_sel
        
        f1 = ttk.Frame(lf_sel); f1.pack(fill=tk.X)
        ttk.Entry(f1, textvariable=self.sf_input_filepath, state="readonly", font=("Segoe UI", 10)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.sf_button_select_file_widget = ttk.Button(f1, command=self.sf_select_file, width=12); self.sf_button_select_file_widget.pack(side=tk.RIGHT)
        
        row2 = ttk.Frame(self.sf_tab_frame); row2.pack(fill=tk.X, pady=(0, 15))
        
        lf_info = ttk.LabelFrame(row2, text="Info", padding="10")
        lf_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.sf_labelframe_original_info_widget = lf_info 
        self.sf_label_original_extension_widget = ttk.Label(lf_info, text="Ext:"); self.sf_label_original_extension_widget.pack(side=tk.LEFT)
        ttk.Label(lf_info, textvariable=self.sf_original_extension, font=("Segoe UI", 10, "bold"), foreground="#CCCCCC").pack(side=tk.LEFT, padx=5)

        lf_conv = ttk.LabelFrame(row2, text="Settings", padding="10")
        lf_conv.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.sf_labelframe_conversion_settings_widget = lf_conv 
        self.sf_label_target_format_widget = ttk.Label(lf_conv, text="Format:"); self.sf_label_target_format_widget.pack(side=tk.LEFT)
        self.sf_format_combobox = ttk.Combobox(lf_conv, textvariable=self.sf_target_format, values=list(TARGET_FORMATS.keys()), state="readonly", width=8, font=("Segoe UI", 10))
        self.sf_format_combobox.pack(side=tk.LEFT, padx=10)
        self.sf_format_combobox.bind("<<ComboboxSelected>>", self.update_conversion_options)

        btn_frame = ttk.Frame(self.sf_tab_frame); btn_frame.pack(fill=tk.X, pady=10)
        self.sf_stream_copy_button_widget = ttk.Button(btn_frame, command=lambda: self.sf_start_conversion_thread('remux'), state="disabled")
        self.sf_stream_copy_button_widget.pack(side=tk.RIGHT, padx=5)
        self.sf_convert_button_widget = ttk.Button(btn_frame, command=lambda: self.sf_start_conversion_thread('re-encode'), state="disabled")
        self.sf_convert_button_widget.pack(side=tk.RIGHT, padx=5)

        prog_frame = ttk.Frame(self.sf_tab_frame, padding=(0, 20, 0, 0)); prog_frame.pack(fill=tk.X)
        self.sf_current_file_label_widget = ttk.Label(prog_frame, text="", font=("Segoe UI", 11)); self.sf_current_file_label_widget.pack(anchor='w', pady=(0, 5))
        self.sf_progress_bar = ttk.Progressbar(prog_frame, orient=tk.HORIZONTAL, mode='determinate')
        self.sf_progress_bar.pack(fill=tk.X, ipady=5)

        # Batch Folder Tab
        self.bf_tab_frame = ttk.Frame(self.conv_notebook, padding="20")
        self.conv_notebook.add(self.bf_tab_frame, text="")

        # -- Batch Folder Widgets --
        lf_in = ttk.LabelFrame(self.bf_tab_frame, text="Input", padding="15"); lf_in.pack(fill=tk.X, pady=(0, 10))
        self.bf_labelframe_input_folder_widget = lf_in
        f_b1 = ttk.Frame(lf_in); f_b1.pack(fill=tk.X)
        ttk.Entry(f_b1, textvariable=self.bf_input_folder_path, state="readonly", font=("Segoe UI", 10)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.bf_button_select_input_folder_widget = ttk.Button(f_b1, command=self.bf_select_input_folder, width=12); self.bf_button_select_input_folder_widget.pack(side=tk.RIGHT)

        lf_out = ttk.LabelFrame(self.bf_tab_frame, text="Output", padding="15"); lf_out.pack(fill=tk.X, pady=(0, 10))
        self.bf_labelframe_output_originals_folder_widget = lf_out
        f_b2 = ttk.Frame(lf_out); f_b2.pack(fill=tk.X)
        ttk.Entry(f_b2, textvariable=self.bf_output_folder_originals_path, state="readonly", font=("Segoe UI", 10)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.bf_button_clear_output_folder_originals_widget = ttk.Button(f_b2, command=self.bf_clear_output_folder_originals, width=4, text="X"); self.bf_button_clear_output_folder_originals_widget.pack(side=tk.RIGHT, padx=(5,0))
        self.bf_button_select_output_folder_originals_widget = ttk.Button(f_b2, command=self.bf_select_output_folder_originals, width=8); self.bf_button_select_output_folder_originals_widget.pack(side=tk.RIGHT)

        lf_set = ttk.LabelFrame(self.bf_tab_frame, text="Settings", padding="15"); lf_set.pack(fill=tk.X, pady=(0, 10))
        self.bf_labelframe_conversion_settings_widget = lf_set
        self.bf_label_target_format_widget = ttk.Label(lf_set, text="Format:"); self.bf_label_target_format_widget.pack(side=tk.LEFT)
        self.bf_format_combobox = ttk.Combobox(lf_set, textvariable=self.bf_target_format, values=list(TARGET_FORMATS.keys()), state="readonly", width=10, font=("Segoe UI", 10))
        self.bf_format_combobox.pack(side=tk.LEFT, padx=10)
        self.bf_format_combobox.bind("<<ComboboxSelected>>", self.update_conversion_options)
        
        self.bf_stream_copy_button_widget = ttk.Button(lf_set, command=lambda: self.bf_start_batch_conversion_thread('remux'), state="disabled"); self.bf_stream_copy_button_widget.pack(side=tk.RIGHT, padx=5)
        self.bf_convert_button_widget = ttk.Button(lf_set, command=lambda: self.bf_start_batch_conversion_thread('re-encode'), state="disabled"); self.bf_convert_button_widget.pack(side=tk.RIGHT, padx=5)

        prog_frame_bf = ttk.Frame(self.bf_tab_frame, padding=(0, 20, 0, 0)); prog_frame_bf.pack(fill=tk.X)
        self.bf_current_file_label_widget = ttk.Label(prog_frame_bf, text="", font=("Segoe UI", 10)); self.bf_current_file_label_widget.pack(anchor='w', pady=(0, 2))
        self.bf_progress_bar = ttk.Progressbar(prog_frame_bf, orient=tk.HORIZONTAL, mode='determinate'); self.bf_progress_bar.pack(fill=tk.X, ipady=3)
        self.bf_overall_progress_label_widget = ttk.Label(prog_frame_bf, text="", font=("Segoe UI", 10, "bold"), foreground="#007ACC"); self.bf_overall_progress_label_widget.pack(anchor='w', pady=(10, 2))
        self.bf_overall_progress_bar = ttk.Progressbar(prog_frame_bf, orient=tk.HORIZONTAL, mode='determinate'); self.bf_overall_progress_bar.pack(fill=tk.X, ipady=5)

        self.conv_notebook.bind("<<NotebookTabChanged>>", self.on_converter_tab_change)

    # ---------------------------------------------------------
    # UI Creation: Splitter
    # ---------------------------------------------------------
    def create_splitter_ui(self, parent):
        # Input Selection
        lf_in = ttk.LabelFrame(parent, text="Input Video", padding="15")
        lf_in.pack(fill=tk.X, pady=(0, 15))
        self.sp_labelframe_input_widget = lf_in
        
        f1 = ttk.Frame(lf_in); f1.pack(fill=tk.X)
        ttk.Entry(f1, textvariable=self.sp_input_filepath, state="readonly", font=("Segoe UI", 10)).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.sp_button_select_file_widget = ttk.Button(f1, command=self.sp_select_file, width=12); self.sp_button_select_file_widget.pack(side=tk.RIGHT)

        # Split Settings
        lf_set = ttk.LabelFrame(parent, text="Split Settings", padding="15")
        lf_set.pack(fill=tk.X, pady=(0, 15))
        self.sp_labelframe_settings_widget = lf_set

        f2 = ttk.Frame(lf_set); f2.pack(fill=tk.X)
        self.sp_label_size_widget = ttk.Label(f2, text="Split Size:"); self.sp_label_size_widget.pack(side=tk.LEFT)
        ttk.Entry(f2, textvariable=self.sp_split_size, width=10).pack(side=tk.LEFT, padx=10)
        
        self.sp_label_unit_widget = ttk.Label(f2, text="Unit:"); self.sp_label_unit_widget.pack(side=tk.LEFT, padx=(20, 5))
        ttk.Combobox(f2, textvariable=self.sp_split_unit, values=["GB", "MB"], state="readonly", width=5).pack(side=tk.LEFT)

        # Action
        self.sp_start_button_widget = ttk.Button(parent, command=self.sp_start_splitting_thread, state="disabled")
        self.sp_start_button_widget.pack(pady=20, fill=tk.X, ipady=5)

        # Progress
        self.sp_progress_label_widget = ttk.Label(parent, text="", font=("Segoe UI", 10))
        self.sp_progress_label_widget.pack(anchor='w', pady=(0, 2))
        self.sp_progress_bar = ttk.Progressbar(parent, orient=tk.HORIZONTAL, mode='determinate')
        self.sp_progress_bar.pack(fill=tk.X, ipady=5)

    # ---------------------------------------------------------
    # UI Creation: Settings (Shared)
    # ---------------------------------------------------------
    def create_settings_ui(self, parent):
        # FFmpeg
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

        # CPU
        lf_cpu = ttk.LabelFrame(parent, text="CPU", padding="15"); lf_cpu.pack(fill=tk.X, pady=(0, 15))
        self.settings_labelframe_cpu_widget = lf_cpu
        self.settings_label_codec_widget = ttk.Label(lf_cpu); self.settings_label_codec_widget.pack(side=tk.LEFT)
        ttk.Combobox(lf_cpu, textvariable=self.selected_video_codec, values=['H.264', 'H.265', 'AV1'], state='readonly', width=8).pack(side=tk.LEFT, padx=(5, 20))
        self.settings_label_cpu_threads_widget = ttk.Label(lf_cpu); self.settings_label_cpu_threads_widget.pack(side=tk.LEFT)
        ttk.Spinbox(lf_cpu, from_=1, to=self.total_cpu_cores, textvariable=self.cpu_threads_to_use, width=5).pack(side=tk.LEFT, padx=5)
        self.settings_label_cpu_total_widget = ttk.Label(lf_cpu, foreground="#888888"); self.settings_label_cpu_total_widget.pack(side=tk.LEFT)

        # GPU
        lf_gpu = ttk.LabelFrame(parent, text="GPU", padding="15"); lf_gpu.pack(fill=tk.BOTH, expand=True)
        self.settings_labelframe_gpu_widget = lf_gpu
        
        q_frame = ttk.Frame(lf_gpu); q_frame.pack(fill=tk.X, pady=(0, 10))
        self.settings_label_gpu_quality_widget = ttk.Label(q_frame); self.settings_label_gpu_quality_widget.pack(side=tk.LEFT)
        ttk.Scale(q_frame, from_=0, to=51, orient=tk.HORIZONTAL, variable=self.gpu_quality_target_crf, command=lambda v: self.gpu_quality_target_crf.set(int(float(v)))).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        ttk.Label(q_frame, textvariable=self.gpu_quality_target_crf, width=3).pack(side=tk.LEFT)
        self.settings_gpu_quality_tooltip_widget = ttk.Label(lf_gpu, font=("Segoe UI", 8), foreground="#888888"); self.settings_gpu_quality_tooltip_widget.pack(anchor='w', pady=(0, 10))

        self.gpu_notebook = ttk.Notebook(lf_gpu); self.gpu_notebook.pack(fill=tk.BOTH, expand=True)
        
        # GPU Sub-Tabs (NVIDIA, Intel, AMD)
        self.nv_settings_frame = ttk.Frame(self.gpu_notebook, padding="15"); self.gpu_notebook.add(self.nv_settings_frame, text="NVIDIA")
        self.settings_label_nv_preset_widget = ttk.Label(self.nv_settings_frame); self.settings_label_nv_preset_widget.grid(row=0, column=0, sticky='w', pady=5)
        # [수정됨] state='disabled' -> 'readonly'로 변경하여 사용자 선택 가능하게 함
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
    # Logic & Event Handling
    # ---------------------------------------------------------
    def toggle_language(self):
        global current_language
        current_language = 'en' if current_language == 'ko' else 'ko'
        self.update_ui_language()

    def update_ui_language(self):
        # Window & Root Tabs
        self.root.title(get_string('window_title'))
        self.lang_toggle_button.config(text=get_string('toggle_lang_button_text_to_en') if current_language == 'ko' else get_string('toggle_lang_button_text_to_ko'))
        self.root_notebook.tab(self.tab_converter_frame, text=get_string('tab_main_converter'))
        self.root_notebook.tab(self.tab_splitter_frame, text=get_string('tab_main_splitter'))
        self.root_notebook.tab(self.tab_settings_frame, text=get_string('tab_main_settings'))

        # Converter Tabs
        self.conv_notebook.tab(self.sf_tab_frame, text=get_string('tab_single_file'))
        self.conv_notebook.tab(self.bf_tab_frame, text=get_string('tab_batch_folder'))
        
        # Converter UI Strings
        self.sf_labelframe_select_file_widget.config(text=get_string('sf_labelframe_select_file'))
        self.sf_button_select_file_widget.config(text=get_string('button_select_file'))
        self.sf_labelframe_original_info_widget.config(text=get_string('sf_labelframe_original_info'))
        self.sf_label_original_extension_widget.config(text=get_string('sf_label_original_extension'))
        self.sf_labelframe_conversion_settings_widget.config(text=get_string('sf_labelframe_conversion_settings'))
        self.sf_label_target_format_widget.config(text=get_string('label_target_format'))
        self.sf_convert_button_widget.config(text=get_string('button_start_conversion'))
        self.sf_stream_copy_button_widget.config(text=get_string('button_start_stream_copy'))
        
        self.bf_labelframe_input_folder_widget.config(text=get_string('bf_labelframe_input_folder'))
        self.bf_button_select_input_folder_widget.config(text=get_string('button_select_folder'))
        self.bf_labelframe_output_originals_folder_widget.config(text=get_string('bf_labelframe_output_originals_folder'))
        self.bf_button_select_output_folder_originals_widget.config(text=get_string('button_select_folder'))
        self.bf_button_clear_output_folder_originals_widget.config(text=get_string('button_clear_selection'))
        self.bf_labelframe_conversion_settings_widget.config(text=get_string('bf_labelframe_conversion_settings'))
        self.bf_label_target_format_widget.config(text=get_string('label_target_format'))
        self.bf_convert_button_widget.config(text=get_string('button_start_batch_conversion'))
        self.bf_stream_copy_button_widget.config(text=get_string('button_start_batch_stream_copy'))
        
        # Splitter UI Strings
        self.sp_labelframe_input_widget.config(text=get_string('sp_labelframe_input'))
        self.sp_button_select_file_widget.config(text=get_string('button_select_file'))
        self.sp_labelframe_settings_widget.config(text=get_string('sp_labelframe_settings'))
        self.sp_label_size_widget.config(text=get_string('sp_label_size'))
        self.sp_label_unit_widget.config(text=get_string('sp_label_unit'))
        self.sp_start_button_widget.config(text=get_string('sp_button_start'))

        # Settings UI Strings
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

        self.on_main_tab_change()

    def on_main_tab_change(self, event=None):
        try:
            sel = self.root_notebook.index(self.root_notebook.select())
            if sel == 0: self.status.set(get_string('status_converter_prompt'))
            elif sel == 1: self.status.set(get_string('status_splitter_prompt'))
            else: self.status.set(get_string('status_initial_prompt'))
        except: pass

    def on_converter_tab_change(self, event=None):
        self.update_conversion_options()

    def browse_ffmpeg_path(self, target):
        fp = filedialog.askopenfilename(title=f"Select {target}.exe", filetypes=[(get_string('filetype_exe_files'), "*.exe"), (get_string('filetype_all_files'), "*.*")])
        if fp:
            if target == "ffmpeg": self.ffmpeg_path_var.set(fp)
            else: self.ffprobe_path_var.set(fp)
            configure_ffmpeg_path(self.ffmpeg_path_var.get(), self.ffprobe_path_var.get())
            save_config({"ffmpeg_path": self.ffmpeg_path_var.get(), "ffprobe_path": self.ffprobe_path_var.get()})

    # --- Common Video Logic ---
    def get_video_duration(self, input_path):
        if not SYSTEM_FFPROBE: return 0
        try:
            cmd = [SYSTEM_FFPROBE, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_path]
            startupinfo = subprocess.STARTUPINFO(); startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            res = subprocess.run(cmd, capture_output=True, text=True, check=True, startupinfo=startupinfo)
            return float(res.stdout.strip())
        except: return 0

    # =========================================================
    # CONVERTER FUNCTIONS
    # =========================================================
    def update_conversion_options(self, event=None):
        sf_ready = self.sf_input_filepath.get() and self.sf_target_format.get()
        bf_ready = self.bf_input_folder_path.get() and self.bf_target_format.get()
        if self.converter_running:
            self.sf_convert_button_widget.config(state="disabled")
            self.sf_stream_copy_button_widget.config(state="disabled")
            self.bf_convert_button_widget.config(state="disabled")
            self.bf_stream_copy_button_widget.config(state="disabled")
            return
        
        self.sf_convert_button_widget.config(state="normal" if sf_ready else "disabled")
        if sf_ready: threading.Thread(target=self.check_remux_compatibility_and_update_ui, args=(self.sf_input_filepath.get(), self.sf_target_format.get(), "single"), daemon=True).start()
        
        self.bf_convert_button_widget.config(state="normal" if bf_ready else "disabled")
        if bf_ready:
            f = self.find_first_video_in_folder(self.bf_input_folder_path.get())
            if f: threading.Thread(target=self.check_remux_compatibility_and_update_ui, args=(f, self.bf_target_format.get(), "batch"), daemon=True).start()

    def sf_select_file(self):
        if self.converter_running: return
        fp = filedialog.askopenfilename(title=get_string('dialog_title_select_video_file'), filetypes=[(get_string('filetype_video_files'), " ".join(f"*{e}" for e in VIDEO_EXTENSIONS)), (get_string('filetype_all_files'), "*.*")])
        if fp:
            self.sf_input_filepath.set(fp)
            self.sf_original_extension.set(os.path.splitext(fp)[1])
            self.status.set(get_string('status_sf_file_selected', filename=os.path.basename(fp)))
            self.sf_progress_bar['value'] = 0
        self.update_conversion_options()

    def bf_select_input_folder(self):
        if self.converter_running: return
        fp = filedialog.askdirectory(title=get_string('dialog_title_select_input_folder'))
        if fp:
            self.bf_input_folder_path.set(fp)
            self.status.set(get_string('status_bf_input_folder_selected', folder_path=fp))
            self.bf_progress_bar['value'] = 0; self.bf_overall_progress_bar['value'] = 0
        self.update_conversion_options()

    def bf_select_output_folder_originals(self):
        if self.converter_running: return
        fp = filedialog.askdirectory(title=get_string('dialog_title_select_output_folder'))
        if fp:
            self.bf_output_folder_originals_path.set(fp)

    def bf_clear_output_folder_originals(self):
        if self.converter_running: return
        self.bf_output_folder_originals_path.set("")

    def find_first_video_in_folder(self, folder):
        try:
            for n in os.listdir(folder):
                if os.path.isfile(os.path.join(folder, n)) and os.path.splitext(n)[1].lower() in VIDEO_EXTENSIONS: return os.path.join(folder, n)
        except: pass
        return None

    def check_remux_compatibility_and_update_ui(self, input_file, target_format_name, mode):
        if TARGET_FORMATS.get(target_format_name) == 'gif':
            self.progress_queue.put({"type": "remux_check_result", "mode": mode, "compatible": False, "reason": "status_remux_not_supported_format"})
            return
        if not SYSTEM_FFPROBE: return
        try:
            cmd = [SYSTEM_FFPROBE, '-v', 'quiet', '-print_format', 'json', '-show_streams', input_file]
            startupinfo = subprocess.STARTUPINFO(); startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            res = subprocess.run(cmd, capture_output=True, text=True, check=True, startupinfo=startupinfo)
            streams = json.loads(res.stdout)['streams']
            v_codec = next((s['codec_name'] for s in streams if s['codec_type'] == 'video'), None)
            a_codec = next((s['codec_name'] for s in streams if s['codec_type'] == 'audio'), None)
            supp = SUPPORTED_CODECS_FOR_REMUX.get(TARGET_FORMATS.get(target_format_name))
            compatible = False
            if supp == 'any': compatible = True
            elif supp and v_codec: compatible = (v_codec in supp['v']) and (not a_codec or a_codec in supp['a'])
            reason = 'status_remux_possible' if compatible else 'status_remux_not_possible'
            self.progress_queue.put({"type": "remux_check_result", "mode": mode, "compatible": compatible, "reason": reason})
        except: pass

    def run_ffmpeg_direct(self, input_path, output_path, preset_args, report_key, file_idx=None, total_files=None):
        if not SYSTEM_FFMPEG: return False, "FFmpeg not found"
        
        duration = self.get_video_duration(input_path)
        cmd = [SYSTEM_FFMPEG, '-y', '-i', input_path] + preset_args + [output_path]
        
        startupinfo = subprocess.STARTUPINFO(); startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        try:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                universal_newlines=True, startupinfo=startupinfo, encoding='utf-8', errors='ignore'
            )
            self.current_process = process # Tracking for cancellation if implemented
            
            for line in process.stdout:
                time_match = re.search(r'time=(\d+):(\d+):(\d+\.\d+)', line)
                if time_match and duration > 0:
                    h, m, s = map(float, time_match.groups())
                    current_seconds = h*3600 + m*60 + s
                    percent = min(int((current_seconds / duration) * 100), 99)
                    remaining_seconds = max(0, duration - current_seconds)
                    
                    self.progress_queue.put({
                        "type": "progress_converter", 
                        "conversion_type": "batch" if file_idx else "single",
                        "percent": percent, "filename": os.path.basename(input_path),
                        "file_index": file_idx, "total_files": total_files,
                        "remaining": remaining_seconds, "total_duration": duration
                    })
            
            process.wait()
            if process.returncode == 0: return True, None
            else: return False, "FFmpeg Error"
        except Exception as e: return False, str(e)

    def _get_encoding_params(self):
        threads = str(self.cpu_threads_to_use.get())
        qp = str(self.gpu_quality_target_crf.get())
        codec = self.selected_video_codec.get()
        
        nv_p_user = self.nv_preset.get()
        nv_map = {'p1': 'fast', 'p2': 'fast', 'p3': 'medium', 'p4': 'medium', 'p5': 'medium', 'p6': 'slow', 'p7': 'slow', 'slow': 'slow', 'medium': 'medium', 'fast': 'fast'}
        actual_nv_preset = nv_map.get(nv_p_user, 'medium')

        nv_params = ["-preset", actual_nv_preset, "-rc", "constqp", "-qp", qp, "-b:v", "0", "-spatial_aq", "1", "-pix_fmt", "yuv420p"]
        intel_params = ["-preset", self.intel_preset.get(), "-global_quality", qp, "-pix_fmt", "yuv420p"]
        amd_params = ["-usage", self.amd_usage.get(), "-rc", "cqp", "-qp_i", qp, "-qp_p", qp, "-pix_fmt", "yuv420p"]

        hw_configs = []
        hw_configs.append({'name': f'NVIDIA {codec}', 'args': ['-c:v', 'h264_nvenc' if codec=='H.264' else 'hevc_nvenc' if codec=='H.265' else 'av1_nvenc'] + nv_params})
        
        cpu_c = {'H.264': 'libx264', 'H.265': 'libx265', 'AV1': 'libsvtav1'}.get(codec)
        cpu_args = ['-c:v', cpu_c, '-crf', qp, '-preset', 'faster' if 'libx26' in cpu_c else 'preset', '-threads', threads, '-pix_fmt', 'yuv420p']
        
        return hw_configs, cpu_args

    def sf_start_conversion_thread(self, mode):
        if self.converter_running: return
        self.converter_running = True
        self.update_conversion_options()
        self.sf_progress_bar['value'] = 0
        threading.Thread(target=self.execute_single_conversion, args=(mode,), daemon=True).start()

    def execute_single_conversion(self, mode):
        inp = self.sf_input_filepath.get()
        fmt = self.sf_target_format.get()
        ext = TARGET_FORMATS.get(fmt)
        outp = os.path.join(os.path.dirname(inp), f"{os.path.splitext(os.path.basename(inp))[0]}_{'fast' if mode=='remux' else 're-encoded'}.{ext}")
        
        success = False
        err = ""
        
        if mode == 'remux':
            args = ['-c', 'copy']
            success, err = self.run_ffmpeg_direct(inp, outp, args, None)
        else:
            if ext == 'gif':
                args = ['-vf', f'fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse']
                success, err = self.run_ffmpeg_direct(inp, outp, args, None)
            else:
                hw_configs, cpu_args = self._get_encoding_params()
                for hw in hw_configs:
                    self.progress_queue.put({"type": "status_update_key", "key": 'status_sf_trying_hw_accel', "hw_codec_name": hw['name'], "filename": os.path.basename(inp)})
                    success, err = self.run_ffmpeg_direct(inp, outp, hw['args'], None)
                    if success: break
                if not success:
                    self.progress_queue.put({"type": "status_update_key", "key": 'status_sf_hw_accel_failed_cpu', "filename": os.path.basename(inp)})
                    success, err = self.run_ffmpeg_direct(inp, outp, cpu_args, None)
        
        self.progress_queue.put({"type": "conv_single_complete" if success else "conv_error", "output_filename": os.path.basename(outp), "error_message": err})

    def bf_start_batch_conversion_thread(self, mode):
        if self.converter_running: return
        inp = self.bf_input_folder_path.get()
        fmt = self.bf_target_format.get()
        ext = TARGET_FORMATS.get(fmt)
        self.bf_files_to_convert_list = [os.path.join(inp, f) for f in os.listdir(inp) if os.path.isfile(os.path.join(inp, f)) and os.path.splitext(f)[1].lower() in VIDEO_EXTENSIONS and os.path.splitext(f)[1].lower() != f".{ext}"]
        if not self.bf_files_to_convert_list:
            messagebox.showinfo(get_string('dialog_title_info'), get_string('dialog_msg_no_files_to_convert_info'))
            return
        self.converter_running = True
        self.update_conversion_options()
        self.bf_progress_bar['value'] = 0
        self.bf_converted_original_files_paths = []
        threading.Thread(target=self.execute_batch_conversion, args=(mode, inp, fmt, ext), daemon=True).start()

    def execute_batch_conversion(self, mode, inp_folder, fmt, ext):
        total = len(self.bf_files_to_convert_list)
        for i, inp in enumerate(self.bf_files_to_convert_list):
            fn = os.path.basename(inp)
            outp = os.path.join(os.path.dirname(inp), f"{os.path.splitext(fn)[0]}_{'fast' if mode=='remux' else 're-encoded'}.{ext}")
            self.progress_queue.put({"type": "progress_converter_overall", "current": i, "total": total})
            
            if mode == 'remux':
                # Check compatibility first (simplified)
                args = ['-c', 'copy']
                self.run_ffmpeg_direct(inp, outp, args, None, i+1, total)
            else:
                if ext == 'gif':
                    args = ['-vf', f'fps=10,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse']
                    self.run_ffmpeg_direct(inp, outp, args, None, i+1, total)
                else:
                    hw_configs, cpu_args = self._get_encoding_params()
                    success = False
                    for hw in hw_configs:
                        success, _ = self.run_ffmpeg_direct(inp, outp, hw['args'], None, i+1, total)
                        if success: break
                    if not success: self.run_ffmpeg_direct(inp, outp, cpu_args, None, i+1, total)
                self.bf_converted_original_files_paths.append(inp)

        if mode != 'remux' and self.bf_converted_original_files_paths:
            out_orig = self.bf_output_folder_originals_path.get()
            if out_orig:
                try:
                    os.makedirs(out_orig, exist_ok=True)
                    for orig in self.bf_converted_original_files_paths:
                        dest = os.path.join(out_orig, os.path.basename(orig))
                        if not os.path.exists(dest): shutil.move(orig, dest)
                except Exception as e:
                    print(f"Move error: {e}")

        self.progress_queue.put({"type": "conv_batch_complete"})

    # =========================================================
    # SPLITTER FUNCTIONS
    # =========================================================
    def sp_select_file(self):
        if self.splitter_running: return
        fp = filedialog.askopenfilename(title=get_string('dialog_title_select_video_file'), filetypes=[(get_string('filetype_video_files'), "*.mp4;*.avi;*.mkv;*.mov;*.wmv"), (get_string('filetype_all_files'), "*.*")])
        if fp:
            self.sp_input_filepath.set(fp)
            self.sp_start_button_widget.config(state="normal")

    def sp_start_splitting_thread(self):
        if self.splitter_running: return
        
        video_path = self.sp_input_filepath.get()
        size_val = self.sp_split_size.get()
        unit = self.sp_split_unit.get()

        if not video_path or not os.path.exists(video_path):
            messagebox.showerror(get_string('dialog_title_error'), get_string('sp_error_no_file'))
            return
        
        try:
            split_size_float = float(size_val)
            if split_size_float <= 0: raise ValueError
            
            output_dir = filedialog.askdirectory(title=get_string('dialog_title_select_output_folder'))
            if not output_dir: return

            self.splitter_running = True
            self.sp_start_button_widget.config(state="disabled")
            self.sp_progress_bar['value'] = 0
            
            threading.Thread(target=self.execute_splitter, args=(video_path, split_size_float, unit, output_dir), daemon=True).start()

        except ValueError:
            messagebox.showerror(get_string('dialog_title_error'), get_string('sp_error_size_zero'))

    def execute_splitter(self, video_path, split_size, unit, output_dir):
        try:
            # 1. Calculate Sizes
            if unit == "MB": split_size_bytes = int(split_size * 1024 * 1024)
            else: split_size_bytes = int(split_size * 1024 * 1024 * 1024)
            
            total_size_bytes = os.path.getsize(video_path)
            num_segments = int(total_size_bytes / split_size_bytes)
            if total_size_bytes % split_size_bytes != 0: num_segments += 1

            if num_segments <= 1:
                self.progress_queue.put({"type": "splitter_error", "message": "Video is smaller than split size."})
                return

            # 2. Get Duration
            self.progress_queue.put({"type": "status_update_key", "key": "sp_status_calculating"})
            duration = self.get_video_duration(video_path)
            if duration == 0:
                self.progress_queue.put({"type": "splitter_error", "message": get_string('sp_error_duration')})
                return

            segment_duration = duration / num_segments
            file_name, file_ext = os.path.splitext(os.path.basename(video_path))

            # 3. Split Loop
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            for i in range(num_segments):
                start_time = i * segment_duration
                # Use -to for exact segment length, -ss before -i for fast seek
                # Note: -c copy with -ss may not be frame-perfect, but it's fast (as requested)
                
                output_file = os.path.join(output_dir, f"{file_name}_part_{i+1:03d}{file_ext}")
                
                cmd = [
                    SYSTEM_FFMPEG, '-y',
                    '-ss', str(start_time),
                    '-i', video_path,
                    '-t', str(segment_duration),
                    '-c', 'copy',
                    output_file
                ]

                self.progress_queue.put({"type": "progress_splitter", "current": i+1, "total": num_segments})
                
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo=startupinfo)

            self.progress_queue.put({"type": "splitter_complete", "folder": output_dir})

        except Exception as e:
            self.progress_queue.put({"type": "splitter_error", "message": str(e)})

    # =========================================================
    # MAIN LOOP & QUEUE PROCESSING
    # =========================================================
    def format_seconds(self, seconds):
        if seconds is None: return "--:--"
        return str(datetime.timedelta(seconds=int(seconds)))

    def process_queue(self):
        try:
            while True:
                msg = self.progress_queue.get_nowait()
                mtype = msg.get("type")
                
                # --- Shared Updates ---
                if mtype == "status_update_key":
                    kwargs = {k: v for k, v in msg.items() if k not in ['type', 'key']}
                    txt = get_string(msg['key'], **kwargs)
                    self.status.set(txt)

                # --- Converter Updates ---
                elif mtype == "remux_check_result":
                    self.status.set(get_string(msg['reason']))
                    btn = self.sf_stream_copy_button_widget if msg['mode'] == "single" else self.bf_stream_copy_button_widget
                    btn.config(state="normal" if msg['compatible'] else "disabled")
                
                elif mtype == "progress_converter":
                    p = msg['percent']
                    fn = msg.get('filename', '')
                    rem_sec = msg.get('remaining', 0)
                    tot_sec = msg.get('total_duration', 0)
                    
                    time_str = get_string('status_time_info', rem=self.format_seconds(rem_sec), tot=self.format_seconds(tot_sec))
                    self.time_info.set(time_str)

                    if msg.get('conversion_type') == "single":
                        self.sf_progress_bar['value'] = p
                        self.status.set(get_string('status_converting_progress', filename=fn, percent=p))
                    else:
                        self.bf_progress_bar['value'] = p
                        self.bf_current_file_label_widget.config(text=get_string('status_converting_progress', filename=fn, percent=p))

                elif mtype == "progress_converter_overall":
                    cur, tot = msg['current'], msg['total']
                    if tot > 0: self.bf_overall_progress_bar['value'] = (cur/tot)*100
                    if hasattr(self, 'bf_overall_progress_label_widget'): 
                         self.bf_overall_progress_label_widget.config(text=f"Total: {cur}/{tot}")

                elif mtype in ["conv_single_complete", "conv_batch_complete"]:
                    self.status.set(get_string('status_complete'))
                    self.converter_running = False
                    self.sf_progress_bar['value'] = 100; self.bf_progress_bar['value'] = 100
                    if mtype == "conv_batch_complete": self.bf_overall_progress_bar['value'] = 100
                    self.time_info.set("")
                    self.update_conversion_options()

                elif mtype == "conv_error":
                    self.converter_running = False
                    self.update_conversion_options()
                    messagebox.showerror(get_string('dialog_title_error'), msg.get('error_message'))

                # --- Splitter Updates ---
                elif mtype == "progress_splitter":
                    cur, tot = msg['current'], msg['total']
                    self.sp_progress_bar['value'] = (cur / tot) * 100
                    self.sp_progress_label_widget.config(text=get_string('sp_status_splitting', current=cur, total=tot))
                
                # [수정됨] 완료 시 팝업 창 제거 및 상태바 업데이트로 변경
                elif mtype == "splitter_complete":
                    self.splitter_running = False
                    self.sp_start_button_widget.config(state="normal")
                    self.sp_progress_bar['value'] = 100
                    self.status.set(get_string('sp_status_complete', folder=msg.get('folder')))
                
                elif mtype == "splitter_error":
                    self.splitter_running = False
                    self.sp_start_button_widget.config(state="normal")
                    messagebox.showerror(get_string('dialog_title_error'), msg.get('message'))

        except queue.Empty: pass
        finally: self.root.after(100, self.process_queue)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoToolSuite(root)
    root.mainloop()