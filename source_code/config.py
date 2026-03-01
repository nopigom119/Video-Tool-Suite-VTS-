import os
import json

CONFIG_FILE = "ffmpeg_tool_config.json"
current_language = 'ko'

LANG_STRINGS = {
    'en': {
        'window_title': "Video Tool Suite",
        'toggle_lang_button_text_to_ko': "한국어",
        'toggle_lang_button_text_to_en': "English",
        'tab_main_converter': "Converter",
        'tab_main_splitter': "Splitter",
        'tab_main_settings': "Settings",
        'tab_single': "Single",
        'tab_batch': "Batch",
        'label_target_format': "Target:",
        'button_select_file': "Select File",
        'button_select_folder': "Select Folder",
        'button_add_to_queue': "Add to List",
        'button_start_queue': "Start Processing",
        'button_stop': "STOP",
        'button_remove_selected': "Remove Selected",
        'button_clear_all': "Clear All",
        'button_start_batch_conversion': "Start Batch",
        'button_start_batch_stream_copy': "Fast Batch",
        'button_browse': "Browse",
        'sp_label_size': "Split Size:",
        'sp_button_start': "Start Splitting",
        'placeholder_dnd_single': "Drag & Drop multiple files here",
        'placeholder_dnd_batch': "Drag & Drop folder here",
        'placeholder_dnd_splitter': "Drag & Drop video file here",
        'settings_label_engine': "Engine Configuration",
        'settings_label_ffmpeg_path': "FFmpeg:",
        'settings_label_ffprobe_path': "FFprobe:",
        'settings_label_hw': "Performance & Quality Settings",
        'settings_label_qp': "Target Quality (QP/CRF):",
        'settings_label_codec': "Codec:",
        'settings_label_threads': "Threads:",
        'settings_label_nv_preset': "NVIDIA Preset:",
        'settings_label_intel_preset': "Intel Preset:",
        'settings_label_amd_usage': "AMD Usage:",
        'stat_queued': "Queued: {count}",
        'stat_finished': "Finished: {done}/{total}",
        'stat_eta': "Total ETA: {eta}",
        'status_complete': "Work Complete.",
        'status_stopped': "Stopped / Cancelled.",
        'probing_hw': "Probing HW...",
        'using_cpu': "Using CPU...",
        'bf_check_auto_archive': "Auto Archive Originals",
        'filetype_exe_files': "Executables",
    },
    'ko': {
        'window_title': "영상 도구 모음",
        'toggle_lang_button_text_to_ko': "한국어",
        'toggle_lang_button_text_to_en': "English",
        'tab_main_converter': "변환기",
        'tab_main_splitter': "분할기",
        'tab_main_settings': "설정",
        'tab_single': "개별 변환",
        'tab_batch': "일괄 변환",
        'label_target_format': "대상 포맷:",
        'button_select_file': "파일 선택",
        'button_select_folder': "폴더 선택",
        'button_add_to_queue': "목록 추가",
        'button_start_queue': "변환 시작",
        'button_stop': "중지",
        'button_remove_selected': "선택 삭제",
        'button_clear_all': "전체 비우기",
        'button_start_batch_conversion': "일괄 시작",
        'button_start_batch_stream_copy': "빠른 복사",
        'button_browse': "찾기",
        'sp_label_size': "분할 크기:",
        'sp_button_start': "분할 시작",
        'placeholder_dnd_single': "여기에 여러 파일을 드래그하세요",
        'placeholder_dnd_batch': "여기에 폴더를 드래그하세요",
        'placeholder_dnd_splitter': "여기에 비디오 파일을 드래그하세요",
        'settings_label_engine': "엔진 경로 설정",
        'settings_label_ffmpeg_path': "FFmpeg:",
        'settings_label_ffprobe_path': "FFprobe:",
        'settings_label_hw': "성능 및 품질 설정",
        'settings_label_qp': "목표 품질 (QP/CRF):",
        'settings_label_codec': "코덱:",
        'settings_label_threads': "스레드:",
        'settings_label_nv_preset': "NVIDIA 프리셋:",
        'settings_label_intel_preset': "Intel 프리셋:",
        'settings_label_amd_usage': "AMD 용도:",
        'stat_queued': "대기 중: {count}",
        'stat_finished': "완료됨: {done}/{total}",
        'stat_eta': "총 남은 시간: {eta}",
        'status_complete': "작업이 완료되었습니다.",
        'status_stopped': "작업이 중지되었습니다.",
        'probing_hw': "하드웨어 확인 중...",
        'using_cpu': "CPU 사용 중...",
        'bf_check_auto_archive': "원본 파일 자동 보관",
        'filetype_exe_files': "실행 파일",
    }
}

VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.ts', '.mpg', '.mpeg', '.vob', '.mts', '.m2ts']
TARGET_FORMATS = {"MP4": "mp4", "AVI": "avi", "MOV": "mov", "WebM": "webm", "GIF": "gif"}

def get_string(key, **kwargs):
    global current_language
    s = LANG_STRINGS[current_language].get(key, f"<{key}>")
    if kwargs:
        try: s = s.format(**kwargs)
        except: pass
    return s

def load_config():
    defaults = {
        "ffmpeg_path": "", "ffprobe_path": "", "codec": "H.264", "qp": 23, "threads": 4,
        "nv_preset": "p4", "intel_preset": "fast", "amd_usage": "transcoding",
        "target_format": "MP4", "auto_archive": True, "language": "ko"
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                defaults.update(saved)
                global current_language
                current_language = defaults.get("language", "ko")
        except: pass
    return defaults

def save_config(config_data):
    try:
        config_data["language"] = current_language
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")