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

    print(f"[Engine Config] SYSTEM_FFMPEG: {SYSTEM_FFMPEG}")
    print(f"[Engine Config] SYSTEM_FFPROBE: {SYSTEM_FFPROBE}")

    return SYSTEM_FFMPEG, SYSTEM_FFPROBE

def get_video_duration(input_path):
    if not SYSTEM_FFPROBE: 
        print("[Duration Probe] SYSTEM_FFPROBE is not set.")
        return 0
    try:
        cmd = [SYSTEM_FFPROBE, '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_path]
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        res = subprocess.run(cmd, capture_output=True, text=True, check=True, startupinfo=startupinfo)
        dur = float(res.stdout.strip())
        print(f"[Duration Probe] Duration for '{os.path.basename(input_path)}': {dur}s")
        return dur
    except Exception as e:
        print(f"[Duration Probe Exception] {e}")
        return 0

def get_encoding_params(codec, threads, qp, nv_preset, intel_preset, amd_usage):
    hw_configs = []
    
    # NVIDIA Configuration (NVENC)
    nv_codec = 'h264_nvenc' if codec == 'H.264' else 'hevc_nvenc' if codec == 'H.265' else 'av1_nvenc'
    nv_params = [
        "-preset", nv_preset, "-rc", "constqp", "-qp", str(qp), "-b:v", "0",
        "-spatial-aq", "1", "-temporal-aq", "1", "-rc-lookahead", "32",
        "-bf", "3", "-b_ref_mode", "middle", "-pix_fmt", "yuv420p"
    ]
    if codec == 'AV1':
        nv_params = [p for p in nv_params if p not in ["-temporal-aq", "1", "-b_ref_mode", "middle"]]
    hw_configs.append({'name': f'NVIDIA {codec}', 'args': ['-c:v', nv_codec] + nv_params})

    # Intel Configuration (QSV)
    qsv_codec = 'h264_qsv' if codec == 'H.264' else 'hevc_qsv' if codec == 'H.265' else 'av1_qsv'
    qsv_params = ["-preset", intel_preset, "-global_quality", str(qp), "-look_ahead", "1", "-pix_fmt", "nv12"]
    hw_configs.append({'name': f'Intel {codec}', 'args': ['-c:v', qsv_codec] + qsv_params})

    # AMD Configuration (AMF)
    amf_codec = 'h264_amf' if codec == 'H.264' else 'hevc_amf' if codec == 'H.265' else 'av1_amf'
    amf_params = ["-usage", amd_usage, "-rc", "cqp", "-qp_i", str(qp), "-qp_p", str(qp), "-qp_b", str(qp), "-pix_fmt", "yuv420p"]
    hw_configs.append({'name': f'AMD {codec}', 'args': ['-c:v', amf_codec] + amf_params})

    # CPU Configuration (Fallback)
    cpu_c = {'H.264': 'libx264', 'H.265': 'libx265', 'AV1': 'libsvtav1'}.get(codec)
    cpu_args = ['-c:v', cpu_c, '-crf', str(qp), '-preset', 'faster' if 'libx26' in cpu_c else '8', '-threads', str(threads), '-pix_fmt', 'yuv420p']

    return hw_configs, cpu_args

def _detect_physical_gpus():
    """Detect installed GPUs via nvidia-smi and PowerShell CIM"""
    gpu_names = []
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    # Try nvidia-smi first (fastest for NVIDIA GPUs)
    try:
        res = subprocess.run(['nvidia-smi', '-L'], capture_output=True, text=True, startupinfo=startupinfo, timeout=1)
        if res.returncode == 0 and res.stdout:
            gpu_names.append(res.stdout.upper())
    except:
        pass

    # Query OS via PowerShell Get-CimInstance (replaces deprecated WMIC)
    try:
        ps_cmd = 'Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name'
        res = subprocess.run(['powershell', '-NoProfile', '-Command', ps_cmd], capture_output=True, text=True, startupinfo=startupinfo, timeout=2)
        if res.returncode == 0 and res.stdout:
            gpu_names.append(res.stdout.upper())
    except:
        pass

    combined_gpu_info = " ".join(gpu_names)
    return combined_gpu_info

def is_hw_encoder_working(args):
    if not SYSTEM_FFMPEG:
        print("[HW Probe] SYSTEM_FFMPEG is not configured.")
        return False
    
    try:
        encoder_name = args[args.index('-c:v') + 1]
    except (ValueError, IndexError):
        print(f"[HW Probe] Failed to parse encoder from arguments: {args}")
        return False

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    print(f"\n--- Checking Hardware Encoder: {encoder_name} ---")

    # [Step 1] Check if the encoder is supported in the FFmpeg binary
    try:
        result = subprocess.run([SYSTEM_FFMPEG, '-hide_banner', '-encoders'], 
                                capture_output=True, text=True, startupinfo=startupinfo)
        if encoder_name not in result.stdout:
            print(f"[HW Probe Step 1] Encoder '{encoder_name}' NOT found in FFmpeg build.")
            return False
        print(f"[HW Probe Step 1] Encoder '{encoder_name}' exists in FFmpeg build.")
    except Exception as e:
        print(f"[HW Probe Step 1 Exception] {e}")
        return False

    # [Step 2] Check physical GPU device presence via Windows Native APIs
    gpus_detected = _detect_physical_gpus()
    print(f"[HW Probe Step 2] Detected GPU Info: {gpus_detected.strip()}")

    if 'nvenc' in encoder_name:
        if "NVIDIA" in gpus_detected or "GEFORCE" in gpus_detected or "RTX" in gpus_detected or "GTX" in gpus_detected:
            print("[HW Probe Step 2] Valid NVIDIA GPU matched.")
            return True
    elif 'qsv' in encoder_name:
        if "INTEL" in gpus_detected or "ARC" in gpus_detected:
            print("[HW Probe Step 2] Valid Intel GPU matched.")
            return True
    elif 'amf' in encoder_name:
        if "AMD" in gpus_detected or "RADEON" in gpus_detected:
            print("[HW Probe Step 2] Valid AMD GPU matched.")
            return True

    # [Step 3] Fallback check: Minimum valid resolution test (192x192)
    test_cmd = [
        SYSTEM_FFMPEG,
        '-hide_banner',
        '-y',
        '-f', 'lavfi',
        '-i', 'color=s=192x192:d=0.1',
        '-c:v', encoder_name,
        '-f', 'null',
        '-'
    ]
    try:
        print(f"[HW Probe Step 3] Running fallback stream test: {' '.join(test_cmd)}")
        res = subprocess.run(test_cmd, capture_output=True, text=True, startupinfo=startupinfo, timeout=2)
        if res.returncode == 0:
            print(f"[HW Probe Step 3] Encoder '{encoder_name}' verified successfully.")
            return True
        else:
            print(f"[HW Probe Step 3] Return code: {res.returncode}")
            if res.stderr:
                print(f"[HW Probe Step 3 stderr]\n{res.stderr.strip()}")
            return False
    except Exception as e:
        print(f"[HW Probe Step 3 Exception] {e}")
        return False