# Video Tool Suite (VTS)

**Video Converter & Splitter / 영상 변환 및 분할 도구**

A comprehensive video utility suite that integrates **Video Conversion** and **Video Splitting** into a single application. It supports single/batch processing, hardware acceleration, and a bilingual (Korean/English) user interface.

This is a GUI-based application developed in Python using Tkinter. Unlike the previous version, this suite interacts directly with **FFmpeg** via subprocess for maximum performance and stability, removing the dependency on `moviepy`.

## Functionality and Features

This program provides a tabbed interface to manage various video tasks:

* **Integrated Suite:** Combines a Video Converter and a Video Splitter in one app. Both tools can run concurrently.
* **Bilingual Interface:** Supports both English and Korean user interfaces, switchable at runtime.
* **Global Settings:** A dedicated settings tab to manage FFmpeg paths, CPU threads, and GPU acceleration settings shared across tools.

### 1. Video Converter (Tab 1)

* **Input Formats:** Supports common formats like .mp4, .avi, .mov, .mkv, .wmv, .flv, .webm, .ts, .mts.
* **Output Formats:** Convert to MP4, AVI, MOV, WebM, or GIF.
* **Single File & Batch Mode:**
    * **Single:** Convert one file with detailed progress.
    * **Batch:** Convert all videos in a folder. Original files are automatically moved to a backup folder ("Old_video_collection") after conversion.
* **Hardware Acceleration:** Supports **NVIDIA (NVENC)**, **Intel (QSV)**, and **AMD (AMF)** encoding.
    * Users can select specific presets (e.g., NVIDIA P1~P7) for performance or quality.
    * Automatic fallback to CPU (libx264/libx265) if hardware acceleration fails.

### 2. Video Splitter (Tab 2)

* **Size-Based Splitting:** Split large video files into smaller parts based on a target size (e.g., "100 MB" or "4 GB").
* **High-Speed Processing:** Uses stream copying (`-c copy`), meaning no re-encoding is performed. Splitting is extremely fast and preserves original quality.
* **Automatic Calculation:** Automatically calculates the number of segments based on total file size and duration.

### 3. Settings (Tab 3)

* **FFmpeg Path:** Manually select `ffmpeg.exe` and `ffprobe.exe` if not detected automatically.
* **CPU Settings:** Adjust thread count and preferred codec (H.264, H.265, AV1).
* **GPU Settings:** Fine-tune Quality (CRF/QP) and specific hardware presets (NVIDIA P1-P7, Intel Speed/Quality, etc.).

## Prerequisites

1.  **FFmpeg (Essential):**
    * This application requires **FFmpeg** and **FFprobe**.
    * If they are in your system PATH, the app detects them automatically.
    * If not, you can manually browse and select the `ffmpeg.exe` location in the "Settings" tab.
2.  **Python (for running script directly):**
    * Python 3.x installed.
    * No heavy external libraries like `moviepy` are required anymore. Standard libraries (`tkinter`, `subprocess`, `threading`, `json`) are used.
3.  **(Optional) GPU Drivers:**
    * For hardware acceleration, ensure your NVIDIA/Intel/AMD GPU drivers are up to date.

## How to Use

### A. Using the Executable (`.exe`)

1.  Run `VideoToolSuite.exe`.
2.  **Select Mode (Top Tabs):**
    * **Converter:** Choose "Single File" or "Batch Folder". Select input, choose format, and click Start.
    * **Splitter:** Select a video file, enter the desired split size (e.g., 4 GB), and click "Start Splitting".
    * **Settings:** Verify FFmpeg is detected. Adjust "GPU Quality" (lower is better, e.g., 23) or Presets if needed.
3.  **Check Progress:**
    * Progress bars indicate the current status.
    * The bottom status bar shows detailed messages and remaining time.

### B. Running the Python Script

1.  Clone the repository.
    ```bash
    git clone [https://github.com/nopigom119/Video-Tool-Suite-VTS.git](https://github.com/nopigom119/Video-Tool-Suite-VTS.git)
    ```
2.  Run the script:
    ```bash
    python video_control_all_in_one_v2.py
    ```
    *(Note: The script name may vary depending on your saved filename)*

## License

This program is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)**.

* **Non-Commercial Use Only.**
* **Attribution Required.**
* **Share Alike.**

---

# Video Tool Suite (VTS)

**영상 변환 및 분할 도구 (Video Converter & Splitter)**

**영상 변환(Converter)** 과 **영상 분할(Splitter)** 기능을 하나로 통합한 올인원 유틸리티입니다. 단일/일괄 처리, 하드웨어 가속 설정을 지원하며 한국어/영어 인터페이스를 제공합니다.

이전 버전과 달리 `moviepy` 의존성을 제거하고, **FFmpeg**를 `subprocess`로 직접 제어하여 성능과 안정성을 극대화했습니다.

## 주요 기능

이 프로그램은 탭 기반 인터페이스를 통해 다양한 영상 작업을 관리합니다:

* **통합 도구:** 변환기와 분할기가 하나의 앱에 통합되어 있으며, 두 기능은 동시에 실행될 수 있습니다.
* **다국어 지원:** 실행 중 언제든지 한국어/영어로 전환할 수 있습니다.
* **통합 설정:** FFmpeg 경로, CPU 스레드, GPU 가속 설정을 한 곳에서 관리합니다.

### 1. 영상 변환기 (Converter)

* **지원 입력:** .mp4, .avi, .mov, .mkv, .ts, .webm 등 대부분의 포맷.
* **지원 출력:** MP4, AVI, MOV, WebM, GIF.
* **단일 및 일괄 변환:**
    * **단일:** 개별 파일 변환 및 상세 진행률 표시.
    * **일괄:** 폴더 내 모든 영상 변환. 변환 후 원본 파일은 "Old\_video\_collection" 폴더로 자동 백업되어 관리가 용이합니다.
* **하드웨어 가속:** **NVIDIA (NVENC)**, **Intel (QSV)**, **AMD (AMF)** 인코딩을 지원합니다.
    * NVIDIA P1(고속)~P7(고화질) 등 세부 프리셋을 사용자가 직접 선택할 수 있습니다.
    * 가속 실패 시 자동으로 CPU(libx264)로 전환됩니다.

### 2. 영상 분할기 (Splitter)

* **용량 기반 분할:** 원하는 크기(예: 100MB, 4GB) 단위로 영상을 자동으로 나눕니다.
* **초고속 처리:** 스트림 복사(`-c copy`) 방식을 사용하여 인코딩 없이 원본 화질 그대로 매우 빠르게 분할합니다.
* **자동 계산:** 전체 용량과 시간을 분석하여 필요한 파트 수를 자동으로 계산합니다.

### 3. 설정 (Settings)

* **FFmpeg 경로:** 시스템에 설치된 FFmpeg를 자동 감지하거나, 사용자가 직접 `exe` 파일을 지정할 수 있습니다.
* **인코딩 설정:** CPU 스레드 개수, 코덱(H.264, H.265, AV1) 선택, GPU 화질(QP) 및 프리셋을 상세하게 조정 가능합니다.

## 사전 준비 사항

1.  **FFmpeg (필수):**
    * 이 프로그램은 **FFmpeg**와 **FFprobe**가 필요합니다.
    * 환경 변수(PATH)에 등록되어 있다면 자동 인식하며, 없다면 [설정] 탭에서 직접 경로를 지정해 주세요.
2.  **Python (스크립트 실행 시):**
    * Python 3.x가 필요합니다.
    * 별도의 무거운 라이브러리 설치가 필요 없습니다 (기본 내장 라이브러리 사용).
3.  **(선택) 그래픽 드라이버:**
    * 하드웨어 가속을 사용하려면 각 제조사(NVIDIA/Intel/AMD)의 최신 드라이버가 필요합니다.

## 사용 방법

### A. 실행 파일 사용 (`.exe`)

1.  `VideoToolSuite.exe`를 실행합니다.
2.  **모드 선택 (상단 탭):**
    * **영상 변환기:** 파일 또는 폴더를 선택하고 포맷을 지정한 뒤 변환을 시작합니다.
    * **영상 분할기:** 영상을 선택하고 분할할 크기(예: 100 MB)를 입력한 뒤 시작합니다.
    * **통합 설정:** FFmpeg가 정상적으로 잡혔는지 확인하고, 필요한 경우 가속 프리셋을 변경합니다.
3.  **진행 확인:**
    * 각 탭의 진행률 표시줄과 하단 상태바를 통해 작업 상황을 실시간으로 확인합니다.

### B. Python 스크립트 실행

1.  저장소를 클론하거나 다운로드합니다.
    ```bash
    git clone [https://github.com/nopigom119/Video-Tool-Suite-VTS.git](https://github.com/nopigom119/Video-Tool-Suite-VTS.git)
    ```
2.  스크립트를 실행합니다:
    ```bash
    python video_control_all_in_one_v2.py
    ```

## 라이선스

본 프로그램은 **크리에이티브 커먼즈 저작자표시-비영리-동일조건변경허락 4.0 국제 라이선스 (CC BY-NC-SA 4.0)** 에 따라 이용할 수 있습니다.

* **저작자 표시 필수**
* **비영리 목적으로만 이용 가능**
* **동일 조건 변경 허락**

## 문의 (Contact)

For inquiries about this program, please contact [rycbabd@gmail.com].
