import os
import shutil
import subprocess
import re
import tempfile
import math
import concurrent.futures
from utils import TimeEstimator

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

def get_video_duration(input_path):
    if not SYSTEM_FFPROBE: return 0
    try:
        cmd = [SYSTEM_FFPROBE, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_path]
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        res = subprocess.run(cmd, capture_output=True, text=True, check=True, startupinfo=startupinfo)
        return float(res.stdout.strip())
    except:
        return 0

def get_encoding_params(codec, threads, qp, nv_preset, intel_preset, amd_usage):
    hw_configs = []
    
    nv_codec = 'h264_nvenc' if codec == 'H.264' else 'hevc_nvenc' if codec == 'H.265' else 'av1_nvenc'
    nv_params = [
        "-preset", nv_preset, "-rc", "constqp", "-qp", str(qp), "-b:v", "0",
        "-spatial-aq", "1", "-temporal-aq", "1", "-rc-lookahead", "32",
        "-bf", "3", "-b_ref_mode", "middle", "-pix_fmt", "yuv420p"
    ]
    if codec == 'AV1':
        nv_params = [p for p in nv_params if p not in ["-temporal-aq", "1", "-b_ref_mode", "middle"]]
    hw_configs.append({'name': f'NVIDIA {codec}', 'args': ['-c:v', nv_codec] + nv_params})

    qsv_codec = 'h264_qsv' if codec == 'H.264' else 'hevc_qsv' if codec == 'H.265' else 'av1_qsv'
    qsv_params = ["-preset", intel_preset, "-global_quality", str(qp), "-look_ahead", "1", "-pix_fmt", "nv12"]
    hw_configs.append({'name': f'Intel {codec}', 'args': ['-c:v', qsv_codec] + qsv_params})

    amf_codec = 'h264_amf' if codec == 'H.264' else 'hevc_amf' if codec == 'H.265' else 'av1_amf'
    amf_params = ["-usage", amd_usage, "-rc", "cqp", "-qp_i", str(qp), "-qp_p", str(qp), "-qp_b", str(qp), "-pix_fmt", "yuv420p"]
    hw_configs.append({'name': f'AMD {codec}', 'args': ['-c:v', amf_codec] + amf_params})

    cpu_c = {'H.264': 'libx264', 'H.265': 'libx265', 'AV1': 'libsvtav1'}.get(codec)
    cpu_args = ['-c:v', cpu_c, '-crf', str(qp), '-preset', 'faster' if 'libx26' in cpu_c else '8', '-threads', str(threads), '-pix_fmt', 'yuv420p']

    return hw_configs, cpu_args

def _detect_physical_gpus():
    gpu_list = []
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    try:
        res = subprocess.run(['nvidia-smi', '-L'], capture_output=True, text=True, startupinfo=startupinfo)
        if res.returncode == 0 and res.stdout.strip():
            gpu_list.append(res.stdout.upper())
    except:
        pass

    try:
        cmd = ["powershell", "-NoProfile", "-Command", "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"]
        res = subprocess.run(cmd, capture_output=True, text=True, startupinfo=startupinfo)
        if res.returncode == 0 and res.stdout.strip():
            gpu_list.append(res.stdout.upper())
    except:
        pass

    try:
        res = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name'], capture_output=True, text=True, startupinfo=startupinfo)
        if res.returncode == 0 and res.stdout.strip():
            gpu_list.append(res.stdout.upper())
    except:
        pass

    return "\n".join(gpu_list)

def is_hw_encoder_working(args):
    if not SYSTEM_FFMPEG:
        return False
    
    try:
        encoder_name = args[args.index('-c:v') + 1]
    except (ValueError, IndexError):
        return False

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    try:
        result = subprocess.run([SYSTEM_FFMPEG, '-hide_banner', '-encoders'], 
                                capture_output=True, text=True, startupinfo=startupinfo)
        if encoder_name not in result.stdout:
            return False
    except:
        return False

    gpu_info = _detect_physical_gpus()
    if 'nvenc' in encoder_name and "NVIDIA" in gpu_info:
        return True
    if 'qsv' in encoder_name and "INTEL" in gpu_info:
        return True
    if 'amf' in encoder_name and ("AMD" in gpu_info or "RADEON" in gpu_info):
        return True

    hw_type = 'cuda' if 'nvenc' in encoder_name else 'qsv' if 'qsv' in encoder_name else 'd3d11va'
    try:
        check_hw = subprocess.run([SYSTEM_FFMPEG, '-hide_banner', '-init_hw_device', hw_type], 
                                  capture_output=True, startupinfo=startupinfo, timeout=2)
        return check_hw.returncode == 0
    except:
        return False