import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinterdnd2 import DND_FILES, TkinterDnD
import customtkinter as ctk
import os
import threading
import queue
import shutil
import subprocess
import datetime
import tempfile
import math
import time
import re

import config
from utils import TimeEstimator, parse_dnd_paths
from ui_components import ScrollableTaskFrame
import ffmpeg_engine as engine

class VideoToolSuite(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self):
        super().__init__()
        
        # Initialize DnD context for CustomTkinter
        self.TkdndVersion = TkinterDnD._require(self)
        
        # Appearance and Theme settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.geometry("1200x980")
        
        # Core State and Isolated Process Handlers
        self.progress_queue = queue.Queue()
        self.is_running = False          
        self.is_splitter_running = False 
        self.current_process = None      # Standard/Single conversion handler
        self.splitter_process = None     # Splitter tool handler
        self.tasks_queue_data = [] 
        self.task_widgets = []     
        self.current_task_index = -1 
        self.temp_dirs = [] 
        
        # ETA Calculator initialization (Synchronized with utils.py)
        self.eta_calculator = TimeEstimator(history_len=10)

        # Load Persistent Configuration
        self.app_cfg = config.load_config()
        engine.configure_ffmpeg_path(self.app_cfg.get("ffmpeg_path"), self.app_cfg.get("ffprobe_path"))

        # GUI Sync Variables
        self.total_cpu_cores = os.cpu_count() or 1
        self.cpu_threads_to_use = tk.IntVar(value=self.app_cfg.get("threads", 4))
        self.ffmpeg_path_var = tk.StringVar(value=engine.SYSTEM_FFMPEG or "")
        self.ffprobe_path_var = tk.StringVar(value=engine.SYSTEM_FFPROBE or "")
        self.selected_video_codec = tk.StringVar(value=self.app_cfg.get("codec", "H.264"))
        self.gpu_quality_target_crf = tk.IntVar(value=self.app_cfg.get("qp", 23))
        
        self.nv_preset = tk.StringVar(value=self.app_cfg.get("nv_preset", "p4"))
        self.intel_preset = tk.StringVar(value=self.app_cfg.get("intel_preset", "fast"))
        self.amd_usage = tk.StringVar(value=self.app_cfg.get("amd_usage", "transcoding"))

        self.sf_input_filepath = tk.StringVar()
        self.sf_target_format = tk.StringVar(value=self.app_cfg.get("target_format", "MP4"))
        self.bf_input_folder_path = tk.StringVar()
        self.bf_auto_archive = tk.BooleanVar(value=self.app_cfg.get("auto_archive", True))
        self.sp_input_filepath = tk.StringVar()
        self.sp_split_size = tk.StringVar(value="100")
        self.sp_split_unit = tk.StringVar(value="MB")

        self.stat_queued = tk.StringVar()
        self.stat_done = tk.StringVar()
        self.stat_eta = tk.StringVar()

        self.current_main_tab_names = ["Converter", "Splitter", "Settings"]
        self.current_conv_tab_names = ["Single", "Batch"]

        self.create_main_layout()
        self.update_ui_language()

        # Lifecycle protocols
        self.protocol("WM_DELETE_WINDOW", self.on_app_closing)
        self.after(100, self.process_queue)

    def save_app_settings(self):
        """Persist current UI state to config module"""
        settings = {
            "ffmpeg_path": self.ffmpeg_path_var.get(),
            "ffprobe_path": self.ffprobe_path_var.get(),
            "threads": self.cpu_threads_to_use.get(),
            "codec": self.selected_video_codec.get(),
            "qp": self.gpu_quality_target_crf.get(),
            "nv_preset": self.nv_preset.get(),
            "intel_preset": self.intel_preset.get(),
            "amd_usage": self.amd_usage.get(),
            "target_format": self.sf_target_format.get(),
            "auto_archive": self.bf_auto_archive.get()
        }
        config.save_config(settings)

    def create_main_layout(self):
        top_bar = ctk.CTkFrame(self, height=60, corner_radius=0)
        top_bar.pack(fill=tk.X, padx=10, pady=5)
        ctk.CTkLabel(top_bar, text="VIDEO TOOL SUITE", font=("Segoe UI", 20, "bold"), text_color="#007ACC").pack(side=tk.LEFT, padx=20)
        self.lang_btn = ctk.CTkButton(top_bar, width=80, text="", command=self.toggle_language)
        self.lang_btn.pack(side=tk.RIGHT, padx=20)

        self.main_tabs = ctk.CTkTabview(self)
        self.main_tabs.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)
        self.t_conv = self.main_tabs.add(self.current_main_tab_names[0])
        self.t_split = self.main_tabs.add(self.current_main_tab_names[1])
        self.t_set = self.main_tabs.add(self.current_main_tab_names[2])
        
        self.create_converter_ui(self.t_conv)
        self.create_splitter_ui(self.t_split)
        self.create_settings_ui(self.t_set)

        self.status_bar = ctk.CTkFrame(self, height=35, fg_color="#1E1E1E", corner_radius=0)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        ctk.CTkLabel(self.status_bar, textvariable=self.stat_queued, font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=20)
        ctk.CTkLabel(self.status_bar, textvariable=self.stat_done, font=("Segoe UI", 11)).pack(side=tk.LEFT, padx=20)
        ctk.CTkLabel(self.status_bar, textvariable=self.stat_eta, font=("Segoe UI", 11), text_color="#007ACC").pack(side=tk.RIGHT, padx=20)

    def create_converter_ui(self, parent):
        self.conv_tabs = ctk.CTkTabview(parent)
        self.conv_tabs.pack(fill=tk.BOTH, expand=True)
        self.ts_sf = self.conv_tabs.add(self.current_conv_tab_names[0])
        self.ts_bf = self.conv_tabs.add(self.current_conv_tab_names[1])

        # Single UI
        lf_add = ctk.CTkFrame(self.ts_sf); lf_add.pack(fill=tk.X, padx=10, pady=10)
        self.register_dnd(lf_add, self.handle_dnd_single_file)
        f1 = ctk.CTkFrame(lf_add, fg_color="transparent"); f1.pack(fill=tk.X, padx=10, pady=5)
        self.sf_ent_path = ctk.CTkEntry(f1, textvariable=self.sf_input_filepath); self.sf_ent_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.sf_btn_sel = ctk.CTkButton(f1, width=100, text="", command=self.sf_select_file); self.sf_btn_sel.pack(side=tk.RIGHT, padx=5)
        f2 = ctk.CTkFrame(lf_add, fg_color="transparent"); f2.pack(fill=tk.X, padx=10, pady=5)
        self.sf_lbl_fmt = ctk.CTkLabel(f2, text=""); self.sf_lbl_fmt.pack(side=tk.LEFT, padx=5)
        ctk.CTkComboBox(f2, variable=self.sf_target_format, values=list(config.TARGET_FORMATS.keys())).pack(side=tk.LEFT, padx=5)
        self.sf_btn_add = ctk.CTkButton(f2, width=120, text="", command=self.sf_add_to_queue); self.sf_btn_add.pack(side=tk.RIGHT, padx=5)

        self.sf_queue_frame = ScrollableTaskFrame(self.ts_sf, height=400)
        self.sf_queue_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        f3 = ctk.CTkFrame(self.ts_sf, fg_color="transparent"); f3.pack(fill=tk.X, padx=10, pady=10)
        self.sf_btn_stop = ctk.CTkButton(f3, text="STOP", fg_color="#AA0000", hover_color="#CC0000", command=self.stop_processing, state="disabled"); self.sf_btn_stop.pack(side=tk.LEFT, padx=5)
        self.sf_btn_rem = ctk.CTkButton(f3, text="", command=self.sf_remove_selected); self.sf_btn_rem.pack(side=tk.LEFT, padx=5)
        self.sf_btn_clr = ctk.CTkButton(f3, text="", command=self.sf_clear_all); self.sf_btn_clr.pack(side=tk.LEFT, padx=5)
        self.sf_btn_start = ctk.CTkButton(f3, text="", command=self.sf_start_queue_processing); self.sf_btn_start.pack(side=tk.RIGHT, padx=5)

        # Batch UI
        lf_bin = ctk.CTkFrame(self.ts_bf); lf_bin.pack(fill=tk.X, padx=10, pady=10)
        self.register_dnd(lf_bin, self.handle_dnd_batch_folder)
        self.bf_ent_path = ctk.CTkEntry(lf_bin, textvariable=self.bf_input_folder_path); self.bf_ent_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
        self.bf_btn_sel = ctk.CTkButton(lf_bin, width=100, text="", command=self.bf_select_input_folder); self.bf_btn_sel.pack(side=tk.RIGHT, padx=10)
        lf_bset = ctk.CTkFrame(self.ts_bf); lf_bset.pack(fill=tk.X, padx=10, pady=5)
        self.bf_chk_arch = ctk.CTkCheckBox(lf_bset, text="", variable=self.bf_auto_archive); self.bf_chk_arch.pack(side=tk.LEFT, padx=10)
        self.bf_btn_conv = ctk.CTkButton(lf_bset, text="", command=lambda: self.bf_start_batch_thread('re-encode')); self.bf_btn_conv.pack(side=tk.RIGHT, padx=5)
        self.bf_btn_fast = ctk.CTkButton(lf_bset, text="", command=lambda: self.bf_start_batch_thread('remux')); self.bf_btn_fast.pack(side=tk.RIGHT, padx=5)
        self.bf_log_text = scrolledtext.ScrolledText(self.ts_bf, bg="#1E1E1E", fg="#FFFFFF", font=("Consolas", 10), state='disabled')
        self.bf_log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_splitter_ui(self, parent):
        f_in = ctk.CTkFrame(parent); f_in.pack(fill=tk.X, padx=20, pady=20)
        self.register_dnd(f_in, self.handle_dnd_splitter_file)
        self.sp_ent_path = ctk.CTkEntry(f_in, textvariable=self.sp_input_filepath); self.sp_ent_path.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
        self.sp_btn_sel = ctk.CTkButton(f_in, width=100, text="", command=self.sp_select_file); self.sp_btn_sel.pack(side=tk.RIGHT, padx=10)
        f_set = ctk.CTkFrame(parent); f_set.pack(fill=tk.X, padx=20, pady=10)
        self.sp_lbl_size = ctk.CTkLabel(f_set, text=""); self.sp_lbl_size.pack(side=tk.LEFT, padx=10)
        ctk.CTkEntry(f_set, textvariable=self.sp_split_size, width=100).pack(side=tk.LEFT, padx=5)
        self.sp_cmb_unit = ctk.CTkComboBox(f_set, variable=self.sp_split_unit, values=["GB", "MB"], width=80); self.sp_cmb_unit.pack(side=tk.LEFT, padx=5)
        self.sp_btn_start = ctk.CTkButton(parent, text="", command=self.sp_start_splitting_thread); self.sp_btn_start.pack(fill=tk.X, padx=20, pady=20)
        self.sp_btn_stop = ctk.CTkButton(parent, text="STOP", fg_color="#AA0000", command=self.stop_splitter, state="disabled"); self.sp_btn_stop.pack(fill=tk.X, padx=20)
        self.sp_progress_bar = ctk.CTkProgressBar(parent); self.sp_progress_bar.set(0); self.sp_progress_bar.pack(fill=tk.X, padx=20, pady=20)

    def create_settings_ui(self, parent):
        # 1. Path Configuration
        lf_ff = ctk.CTkFrame(parent); lf_ff.pack(fill=tk.X, padx=20, pady=20)
        self.set_lbl_eng = ctk.CTkLabel(lf_ff, text="", font=("Segoe UI", 14, "bold")); self.set_lbl_eng.pack(anchor="w", padx=15, pady=5)
        r1 = ctk.CTkFrame(lf_ff, fg_color="transparent"); r1.pack(fill=tk.X, padx=10, pady=2)
        ctk.CTkLabel(r1, text="FFmpeg:", width=80).pack(side=tk.LEFT)
        ctk.CTkEntry(r1, textvariable=self.ffmpeg_path_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.set_btn_ff = ctk.CTkButton(r1, text="", width=80, command=lambda: self.browse_ffmpeg_path("ffmpeg")); self.set_btn_ff.pack(side=tk.RIGHT)
        r2 = ctk.CTkFrame(lf_ff, fg_color="transparent"); r2.pack(fill=tk.X, padx=10, pady=2)
        self.set_lbl_fp_path = ctk.CTkLabel(r2, text="", width=80); self.set_lbl_fp_path.pack(side=tk.LEFT)
        ctk.CTkEntry(r2, textvariable=self.ffprobe_path_var).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.set_btn_fp = ctk.CTkButton(r2, text="", width=80, command=lambda: self.browse_ffmpeg_path("ffprobe")); self.set_btn_fp.pack(side=tk.RIGHT)

        # 2. Performance and real-time QP
        lf_hw = ctk.CTkFrame(parent); lf_hw.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        self.set_lbl_perf = ctk.CTkLabel(lf_hw, text="", font=("Segoe UI", 14, "bold")); self.set_lbl_perf.pack(anchor="w", padx=15, pady=5)
        f_top = ctk.CTkFrame(lf_hw, fg_color="transparent"); f_top.pack(fill=tk.X, padx=15)
        self.set_lbl_qp = ctk.CTkLabel(f_top, text=""); self.set_lbl_qp.pack(side=tk.LEFT, padx=5)
        self.qp_val_lbl = ctk.CTkLabel(f_top, text=str(self.gpu_quality_target_crf.get()), width=40, text_color="#007ACC", font=("Segoe UI", 12, "bold"))
        self.qp_val_lbl.pack(side=tk.RIGHT, padx=5)
        ctk.CTkSlider(f_top, from_=0, to=51, variable=self.gpu_quality_target_crf, number_of_steps=51, command=lambda v: self.qp_val_lbl.configure(text=str(int(v)))).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        f4 = ctk.CTkFrame(lf_hw, fg_color="transparent"); f4.pack(fill=tk.X, padx=15, pady=10)
        self.set_lbl_codec = ctk.CTkLabel(f4, text=""); self.set_lbl_codec.pack(side=tk.LEFT, padx=5)
        ctk.CTkOptionMenu(f4, variable=self.selected_video_codec, values=["H.264", "H.265", "AV1"]).pack(side=tk.LEFT, padx=5)
        self.set_lbl_thr = ctk.CTkLabel(f4, text=""); self.set_lbl_thr.pack(side=tk.LEFT, padx=20)
        ctk.CTkEntry(f4, textvariable=self.cpu_threads_to_use, width=60).pack(side=tk.LEFT)

        # 3. Compact HW Specific Tabs
        self.hw_tabs = ctk.CTkTabview(lf_hw, height=110)
        self.hw_tabs.pack(fill=tk.X, padx=15, pady=5)
        t_nv = self.hw_tabs.add("NVIDIA"); t_intel = self.hw_tabs.add("Intel"); t_amd = self.hw_tabs.add("AMD")
        self.set_lbl_nv = ctk.CTkLabel(t_nv, text=""); self.set_lbl_nv.pack(side=tk.LEFT, padx=20)
        ctk.CTkOptionMenu(t_nv, variable=self.nv_preset, values=['p1','p2','p3','p4','p5','p6','p7'], width=120).pack(side=tk.LEFT, padx=10)
        self.set_lbl_intel = ctk.CTkLabel(t_intel, text=""); self.set_lbl_intel.pack(side=tk.LEFT, padx=20)
        ctk.CTkOptionMenu(t_intel, variable=self.intel_preset, values=['veryfast','fast','medium','slow','veryslow'], width=120).pack(side=tk.LEFT, padx=10)
        self.set_lbl_amd = ctk.CTkLabel(t_amd, text=""); self.set_lbl_amd.pack(side=tk.LEFT, padx=20)
        ctk.CTkOptionMenu(t_amd, variable=self.amd_usage, values=['transcoding','ultralowlatency','lowlatency'], width=120).pack(side=tk.LEFT, padx=10)

    def _safe_tab_rename(self, tabview, old_names, new_names):
        curr = tabview.get()
        idx = old_names.index(curr) if curr in old_names else 0
        for old, new in zip(old_names, new_names):
            if old != new: tabview._tab_dict[new] = tabview._tab_dict.pop(old)
        tabview._segmented_button.configure(values=new_names)
        tabview.set(new_names[idx])

    def update_ui_language(self):
        new_main = [config.get_string('tab_main_converter'), config.get_string('tab_main_splitter'), config.get_string('tab_main_settings')]
        new_conv = [config.get_string('tab_single'), config.get_string('tab_batch')]
        self._safe_tab_rename(self.main_tabs, self.current_main_tab_names, new_main)
        self._safe_tab_rename(self.conv_tabs, self.current_conv_tab_names, new_conv)
        self.current_main_tab_names, self.current_conv_tab_names = new_main, new_conv

        self.title(config.get_string('window_title'))
        self.lang_btn.configure(text=config.get_string('toggle_lang_button_text_to_en') if config.current_language == 'ko' else config.get_string('toggle_lang_button_text_to_ko'))
        self.sf_lbl_fmt.configure(text=config.get_string('label_target_format'))
        self.sf_btn_sel.configure(text=config.get_string('button_select_file'))
        self.sf_btn_add.configure(text=config.get_string('button_add_to_queue'))
        self.sf_btn_rem.configure(text=config.get_string('button_remove_selected'))
        self.sf_btn_clr.configure(text=config.get_string('button_clear_all'))
        self.sf_btn_start.configure(text=config.get_string('button_start_queue'))
        self.bf_btn_sel.configure(text=config.get_string('button_select_folder'))
        self.bf_chk_arch.configure(text=config.get_string('bf_check_auto_archive'))
        self.bf_btn_conv.configure(text=config.get_string('button_start_batch_conversion'))
        self.bf_btn_fast.configure(text=config.get_string('button_start_batch_stream_copy'))
        self.sp_lbl_size.configure(text=config.get_string('sp_label_size'))
        self.sp_btn_start.configure(text=config.get_string('sp_button_start'))
        self.sp_btn_sel.configure(text=config.get_string('button_select_file'))
        self.set_lbl_eng.configure(text=config.get_string('settings_label_engine'))
        self.set_lbl_fp_path.configure(text=config.get_string('settings_label_ffprobe_path'))
        self.set_btn_ff.configure(text=config.get_string('button_browse'))
        self.set_btn_fp.configure(text=config.get_string('button_browse'))
        self.set_lbl_perf.configure(text=config.get_string('settings_label_hw'))
        self.set_lbl_qp.configure(text=config.get_string('settings_label_qp'))
        self.set_lbl_codec.configure(text=config.get_string('settings_label_codec'))
        self.set_lbl_thr.configure(text=config.get_string('settings_label_threads'))
        self.set_lbl_nv.configure(text=config.get_string('settings_label_nv_preset'))
        self.set_lbl_intel.configure(text=config.get_string('settings_label_intel_preset'))
        self.set_lbl_amd.configure(text=config.get_string('settings_label_amd_usage'))
        
        self.sf_ent_path.configure(placeholder_text=config.get_string('placeholder_dnd_single'))
        self.bf_ent_path.configure(placeholder_text=config.get_string('placeholder_dnd_batch'))
        self.sp_ent_path.configure(placeholder_text=config.get_string('placeholder_dnd_splitter'))
        self.update_summary_status()

    def update_summary_status(self, current_progress_percent=None):
        """Update localized status and global ETA based on 0-100 progress scale"""
        total = len(self.tasks_queue_data)
        done = sum(1 for t in self.tasks_queue_data if t['status'] == "Done")
        self.stat_queued.set(config.get_string('stat_queued', count=total))
        self.stat_done.set(config.get_string('stat_finished', done=done, total=total))
        
        if self.is_running and current_progress_percent is not None:
            # Synchronize with TimeEstimator.update() scale (0-100)
            self.stat_eta.set(config.get_string('stat_eta', eta=self.eta_calculator.update(current_progress_percent)))
        else:
            self.stat_eta.set(config.get_string('stat_eta', eta="--:--"))

    def toggle_language(self):
        config.current_language = 'en' if config.current_language == 'ko' else 'ko'
        self.update_ui_language()

    def register_dnd(self, widget, callback):
        widget.drop_target_register(DND_FILES)
        widget.dnd_bind('<<DropEnter>>', lambda e: widget.configure(fg_color="#3D3D3D"))
        widget.dnd_bind('<<DropLeave>>', lambda e: widget.configure(fg_color="transparent"))
        widget.dnd_bind('<<Drop>>', lambda e: (widget.configure(fg_color="transparent"), callback(parse_dnd_paths(e.data))))

    def handle_dnd_single_file(self, paths):
        for path in paths:
            if not os.path.isdir(path) and os.path.splitext(path)[1].lower() in config.VIDEO_EXTENSIONS:
                self.sf_add_to_queue(manual_path=path)

    def sf_add_to_queue(self, manual_path=None):
        path = manual_path or self.sf_input_filepath.get(); fmt = self.sf_target_format.get()
        if not path or not fmt: return
        row = ctk.CTkFrame(self.sf_queue_frame, fg_color="#333333"); row.pack(fill=tk.X, pady=2, padx=5)
        chk_var = tk.IntVar(); ctk.CTkCheckBox(row, text="", variable=chk_var, width=20).pack(side=tk.LEFT, padx=5)
        ctk.CTkLabel(row, text="{} -> {}".format(os.path.basename(path), fmt), anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        pb = ctk.CTkProgressBar(row, width=150); pb.set(0); pb.pack(side=tk.RIGHT, padx=10)
        stat_lbl = ctk.CTkLabel(row, text="Ready", width=120, anchor="e"); stat_lbl.pack(side=tk.RIGHT, padx=5)
        self.tasks_queue_data.append({"filepath": path, "target_fmt": fmt, "status": "Ready", "chk_var": chk_var})
        self.task_widgets.append({"frame": row, "status_lbl": stat_lbl, "progress_bar": pb}); self.update_summary_status()

    def sf_remove_selected(self):
        if self.is_running: return
        for i in range(len(self.tasks_queue_data)-1, -1, -1):
            if self.tasks_queue_data[i]['chk_var'].get():
                self.task_widgets[i]['frame'].destroy(); self.task_widgets.pop(i); self.tasks_queue_data.pop(i)
        self.update_summary_status()

    def sf_clear_all(self):
        if self.is_running: return
        for w in self.task_widgets: w['frame'].destroy()
        self.task_widgets.clear(); self.tasks_queue_data.clear(); self.update_summary_status()

    def sf_start_queue_processing(self):
        if self.is_running or not self.tasks_queue_data: return
        self.is_running = True; self.set_ui_state(True, "single")
        self.eta_calculator.reset()
        threading.Thread(target=self.execute_queue_processing, daemon=True).start()

    def execute_queue_processing(self):
        """Worker loop for Single tasks with enhanced logging and per-step progress"""
        try:
            total_tasks = len(self.tasks_queue_data)
            for i, task in enumerate(self.tasks_queue_data):
                if not self.is_running: break
                if task['status'] == "Done": continue
                self.current_task_index = i; filepath = task['filepath']; target_fmt = task['target_fmt']; ext = config.TARGET_FORMATS.get(target_fmt)
                outp = os.path.join(os.path.dirname(filepath), "{}_conv.{}".format(os.path.splitext(os.path.basename(filepath))[0], ext))
                
                self.progress_queue.put({"type": "queue_update", "index": i, "status": config.get_string('probing_hw')})
                
                hw_configs, cpu_args = engine.get_encoding_params(self.selected_video_codec.get(), self.cpu_threads_to_use.get(), self.gpu_quality_target_crf.get(), self.nv_preset.get(), self.intel_preset.get(), self.amd_usage.get())
                working_hw = None
                for hw in hw_configs:
                    if engine.is_hw_encoder_working(hw['args']): working_hw = hw['args']; break
                
                success = False
                if working_hw:
                    # Provide immediate feedback before entering chunked processing
                    self.progress_queue.put({"type": "queue_update", "index": i, "status": "Starting GPU..."})
                    success, _ = self.execute_chunked_task(filepath, outp, working_hw, i, total_tasks)
                
                if not success and self.is_running and task['status'] != "Cancelled":
                    self.progress_queue.put({"type": "queue_update", "index": i, "status": config.get_string('using_cpu')})
                    success, _ = self.run_ffmpeg_direct(filepath, outp, cpu_args, i, total_tasks)

                task['status'] = "Done" if success else "Error"
                self.progress_queue.put({"type": "queue_update", "index": i, "status": task['status'], "progress": 1.0 if success else 0})
                
                # Report final progress for current task to refresh global dashboard
                global_fin = ((i + 1) / total_tasks) * 100
                self.after(0, lambda: self.update_summary_status(global_fin))
        finally:
            self.progress_queue.put({"type": "queue_complete"})

    def execute_chunked_task(self, input_path, output_path, preset_args, task_index, total_tasks):
        """GPU Parallel Encoding with real-time pre-processing feedback"""
        temp_dir = tempfile.mkdtemp(prefix="video_tool_chunk_"); self.temp_dirs.append(temp_dir)
        audio_file = os.path.join(temp_dir, "audio.m4a"); merged_v = os.path.join(temp_dir, "merged.mp4")
        try:
            startupinfo = subprocess.STARTUPINFO(); startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
            # Pre-processing Logs
            self.progress_queue.put({"type": "queue_update", "index": task_index, "status": "Extracting Audio..."})
            subprocess.run([engine.SYSTEM_FFMPEG, '-y', '-i', input_path, '-vn', '-c:a', 'copy', audio_file], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo=startupinfo)
            
            self.progress_queue.put({"type": "queue_update", "index": task_index, "status": "Splitting Video..."})
            subprocess.run([engine.SYSTEM_FFMPEG, '-y', '-i', input_path, '-an', '-c:v', 'copy', '-f', 'segment', '-segment_time', '300', '-reset_timestamps', '1', os.path.join(temp_dir, "seg_%04d.mp4")], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo=startupinfo)
            
            segments = sorted([f for f in os.listdir(temp_dir) if f.startswith("seg_") and f.endswith(".mp4")])
            max_parallel = max(1, self.cpu_threads_to_use.get()); active_processes = []; segment_queue = list(segments); total_segs = len(segments)
            
            while segment_queue or active_processes:
                if not self.is_running or self.tasks_queue_data[task_index]['status'] == "Cancelled":
                    for proc, _ in active_processes:
                        try: proc.terminate()
                        except: pass
                    return False, "Cancelled"
                
                while len(active_processes) < max_parallel and segment_queue:
                    seg = segment_queue.pop(0)
                    cmd = [engine.SYSTEM_FFMPEG, '-y', '-i', os.path.join(temp_dir, seg)] + preset_args + ['-threads', '1', os.path.join(temp_dir, "enc_"+seg)]
                    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo=startupinfo)
                    active_processes.append((proc, seg))
                
                for p_item in active_processes[:]:
                    proc, _ = p_item
                    if proc.poll() is not None:
                        active_processes.remove(p_item)
                        completed = total_segs - len(segment_queue) - len(active_processes)
                        prog = completed / total_segs
                        # Calculate and send global progress (0-100 scale for TimeEstimator)
                        global_prog_percent = ((task_index + prog) / total_tasks) * 100
                        self.progress_queue.put({
                            "type": "queue_update", 
                            "index": task_index, 
                            "progress": prog, 
                            "status": "Encoding {}%".format(int(prog*100)),
                            "global_progress_percent": global_prog_percent
                        })
                time.sleep(0.2)
            
            self.progress_queue.put({"type": "queue_update", "index": task_index, "status": "Merging..."})
            concat_file = os.path.join(temp_dir, "concat.txt")
            with open(concat_file, "w", encoding="utf-8") as f:
                for seg in sorted([f for f in os.listdir(temp_dir) if f.startswith("enc_")]):
                    # Python 3.8 Fix: Handle backslashes outside of f-string expression
                    s_path = os.path.join(temp_dir, seg).replace("\\", "/")
                    f.write("file '{}'\n".format(s_path))
            
            subprocess.run([engine.SYSTEM_FFMPEG, '-y', '-f', 'concat', '-safe', '0', '-i', concat_file, '-c', 'copy', merged_v], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo=startupinfo)
            if os.path.exists(audio_file) and os.path.getsize(audio_file) > 1024:
                subprocess.run([engine.SYSTEM_FFMPEG, '-y', '-i', merged_v, '-i', audio_file, '-c:v', 'copy', '-c:a', 'copy', output_path], check=True, startupinfo=startupinfo)
            else: shutil.copy2(merged_v, output_path)
            return True, "Success"
        except: return False, "Error"
        finally:
            self._cleanup_temp_dir(temp_dir)
            if temp_dir in self.temp_dirs: self.temp_dirs.remove(temp_dir)

    def run_ffmpeg_direct(self, input_path, output_path, preset_args, task_index, total_tasks):
        """CPU/Direct encoding with time parsing and global dashboard feed"""
        duration = engine.get_video_duration(input_path)
        cmd = [engine.SYSTEM_FFMPEG, '-y', '-i', input_path] + preset_args + [output_path]
        startupinfo = subprocess.STARTUPINFO(); startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        try:
            self.current_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, startupinfo=startupinfo, encoding='utf-8', errors='ignore')
            for line in self.current_process.stdout:
                if not self.is_running: break
                m = re.search(r'time=(\d+):(\d+):(\d+\.\d+)', line)
                if m and duration > 0:
                    h, min_v, s = map(float, m.groups())
                    prog = min((h*3600 + min_v*60 + s) / duration, 0.99)
                    global_prog_percent = ((task_index + prog) / total_tasks) * 100
                    self.progress_queue.put({
                        "type": "queue_update", 
                        "index": task_index, 
                        "progress": prog, 
                        "status": "{}%".format(int(prog*100)),
                        "global_progress_percent": global_prog_percent
                    })
            self.current_process.wait(); return (self.current_process.returncode == 0), ""
        except: return False, ""
        finally: self.current_process = None

    def on_app_closing(self):
        self.save_app_settings(); self.is_running = False; self.is_splitter_running = False
        if self.current_process:
            try: self.current_process.terminate()
            except: pass
        if self.splitter_process:
            try: self.splitter_process.terminate()
            except: pass
        for path in self.temp_dirs[:]: self._cleanup_temp_dir(path)
        self.destroy()

    def _cleanup_temp_dir(self, path):
        if os.path.exists(path):
            for _ in range(3):
                try: shutil.rmtree(path, ignore_errors=True); break
                except: time.sleep(0.5)

    def process_queue(self):
        try:
            while True:
                msg = self.progress_queue.get_nowait(); mtype = msg.get("type")
                if mtype == "queue_update":
                    w = self.task_widgets[msg['index']]
                    if 'status' in msg: w['status_lbl'].configure(text=msg['status'])
                    if 'progress' in msg: w['progress_bar'].set(msg['progress'])
                    if 'global_progress_percent' in msg:
                        self.update_summary_status(msg['global_progress_percent'])
                elif mtype == "queue_complete" or mtype == "batch_complete":
                    self.is_running = False; self.set_ui_state(False, "single"); self.update_summary_status()
                    messagebox.showinfo("Done", config.get_string('status_complete'))
                elif mtype == "splitter_complete":
                    self.is_splitter_running = False; self.set_ui_state(False, "splitter")
                    messagebox.showinfo("Done", config.get_string('status_complete'))
                elif mtype == "progress_splitter": self.sp_progress_bar.set(msg['current'] / msg['total'])
        except queue.Empty: pass
        finally: self.after(100, self.process_queue)

    def set_ui_state(self, proc, mode):
        """Granular UI Locking for Single/Batch/Splitter modes"""
        s = "disabled" if proc else "normal"
        if mode == "single" or mode == "batch":
            self.sf_btn_start.configure(state=s); self.sf_btn_stop.configure(state="normal" if proc else "disabled")
            self.sf_btn_add.configure(state=s); self.sf_btn_rem.configure(state=s); self.sf_btn_clr.configure(state=s)
            self.bf_btn_conv.configure(state=s); self.bf_btn_fast.configure(state=s)
        elif mode == "splitter":
            self.sp_btn_start.configure(state=s); self.sp_btn_stop.configure(state="normal" if proc else "disabled")

    def browse_ffmpeg_path(self, target):
        fp = filedialog.askopenfilename(filetypes=[("Executables", "*.exe"), ("All Files", "*.*")])
        if fp:
            if target == "ffmpeg": self.ffmpeg_path_var.set(fp)
            else: self.ffprobe_path_var.set(fp)
            engine.configure_ffmpeg_path(self.ffmpeg_path_var.get(), self.ffprobe_path_var.get()); self.save_app_settings()

    def sf_select_file(self):
        fp = filedialog.askopenfilename(filetypes=[("Video", " ".join(f"*{e}" for e in config.VIDEO_EXTENSIONS))])
        if fp: self.handle_dnd_single_file([fp])

    def bf_select_input_folder(self):
        fp = filedialog.askdirectory()
        if fp: self.bf_input_folder_path.set(fp)
    
    def handle_dnd_batch_folder(self, paths):
        self.bf_input_folder_path.set(paths[0] if os.path.isdir(paths[0]) else os.path.dirname(paths[0]))

    def handle_dnd_splitter_file(self, paths):
        self.sp_input_filepath.set(paths[0]); self.sp_btn_start.configure(state="normal")

    def sp_select_file(self):
        fp = filedialog.askopenfilename(filetypes=[("Video", " ".join(f"*{e}" for e in config.VIDEO_EXTENSIONS))])
        if fp: self.handle_dnd_splitter_file([fp])

    def sp_start_splitting_thread(self):
        if self.is_splitter_running: return
        v, s, u = self.sp_input_filepath.get(), self.sp_split_size.get(), self.sp_split_unit.get()
        if not v or not os.path.exists(v): return
        out = filedialog.askdirectory()
        if not out: return
        self.is_splitter_running = True; self.set_ui_state(True, "splitter")
        threading.Thread(target=self.execute_splitter, args=(v, float(s), u, out), daemon=True).start()

    def execute_splitter(self, video_path, split_size, unit, output_dir):
        try:
            bytes_size = int(split_size * 1024 * 1024 * (1024 if unit == "GB" else 1))
            num_seg = math.ceil(os.path.getsize(video_path) / bytes_size)
            dur = engine.get_video_duration(video_path); seg_dur = dur / num_seg
            startupinfo = subprocess.STARTUPINFO(); startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            for i in range(num_seg):
                if not self.is_splitter_running: break
                out_f = os.path.join(output_dir, "{}_part_{:03d}{}".format(os.path.splitext(os.path.basename(video_path))[0], i+1, os.path.splitext(video_path)[1]))
                cmd = [engine.SYSTEM_FFMPEG, '-y', '-ss', str(i*seg_dur), '-i', video_path, '-t', str(seg_dur), '-c', 'copy', out_f]
                self.splitter_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, startupinfo=startupinfo)
                self.splitter_process.wait()
                self.progress_queue.put({"type": "progress_splitter", "current": i+1, "total": num_seg})
            self.progress_queue.put({"type": "splitter_complete"})
        except: pass
        finally: self.is_splitter_running = False

    def bf_start_batch_thread(self, mode):
        if self.is_running: return
        self.is_running = True; self.set_ui_state(True, "batch"); self.eta_calculator.reset()
        self.bf_log_text.configure(state='normal'); self.bf_log_text.delete(1.0, tk.END); self.bf_log_text.configure(state='disabled')
        threading.Thread(target=self.execute_batch_conversion, args=(mode, self.bf_input_folder_path.get(), self.sf_target_format.get()), daemon=True).start()

    def execute_batch_conversion(self, mode, inp_folder, fmt):
        """Full logic for iterating folders and hardware-probing per file"""
        try:
            ext = config.TARGET_FORMATS.get(fmt)
            files = [f for f in os.listdir(inp_folder) if os.path.isfile(os.path.join(inp_folder, f)) and os.path.splitext(f)[1].lower() in config.VIDEO_EXTENSIONS]
            if not files: return
            total = len(files)
            for i, f_name in enumerate(files):
                if not self.is_running: break
                inp_p = os.path.join(inp_folder, f_name)
                out_p = os.path.join(inp_folder, "{}_batch.{}".format(os.path.splitext(f_name)[0], ext))
                
                hw_configs, cpu_args = engine.get_encoding_params(self.selected_video_codec.get(), self.cpu_threads_to_use.get(), self.gpu_quality_target_crf.get(), self.nv_preset.get(), self.intel_preset.get(), self.amd_usage.get())
                working_hw = None
                for hw in hw_configs:
                    if engine.is_hw_encoder_working(hw['args']): working_hw = hw['args']; break
                
                args = working_hw if (working_hw and mode != 'remux') else (['-c', 'copy'] if mode == 'remux' else cpu_args)
                self.run_ffmpeg_direct(inp_p, out_p, args, i, total)
        finally:
            self.progress_queue.put({"type": "batch_complete"})

    def stop_splitter(self):
        self.is_splitter_running = False
        if self.splitter_process:
            try: self.splitter_process.terminate()
            except: pass

    def stop_processing(self):
        self.is_running = False
        if self.current_process:
            try: self.current_process.terminate()
            except: pass

if __name__ == "__main__":
    app = VideoToolSuite()
    app.mainloop()