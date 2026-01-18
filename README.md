# Video Tool Suite (VTS)

**Video Converter & Splitter / 영상 변환 및 분할 도구**

A comprehensive video utility suite that integrates **Video Conversion** and **Video Splitting** into a single application. It supports single/batch processing, drag-and-drop actions, hardware acceleration, and a bilingual (Korean/English) user interface.

This is a GUI-based application developed in Python using Tkinter. Unlike the previous version, this suite interacts directly with **FFmpeg** via subprocess for maximum performance and stability, removing the dependency on `moviepy`.

> **⚠️ IMPORTANT: FFmpeg Required**
> This application relies entirely on **FFmpeg**. You **MUST** have FFmpeg installed or the executable files available. Without FFmpeg, no conversion or splitting will work.

## Functionality and Features

This program provides a tabbed interface to manage various video tasks:

* **Integrated Suite:** Combines a Video Converter and a Video Splitter in one app. Both tools can run concurrently.
* **Bilingual Interface:** Supports both English and Korean user interfaces, switchable at runtime.
* **Drag & Drop Support:** Easily load files or folders by dragging them directly into the application window.
* **Global Settings:** A dedicated settings tab to manage FFmpeg paths, CPU threads, and GPU acceleration settings shared across tools.

### 1. Video Converter (Tab 1)

* **Input Formats:** Supports common formats like .mp4, .avi, .mov, .mkv, .wmv, .flv, .webm, .ts, .mts.
* **Output Formats:** Convert to MP4, AVI, MOV, WebM, or GIF.
* **Single File (Queue Mode):**
    * **Task Queue:** Add multiple files to a list and process them sequentially.
    * **Smart Control:** Cancel specific tasks via checkboxes or retry only failed/stopped items.
    * **Drag & Drop:** Drag a video file to automatically add it to the input field.
* **Batch Folder Mode:**
    * **Batch Processing:** Convert all videos in a specific folder.
    * **Auto-Archiving:** Successfully converted original files are automatically moved to an `_Originals` folder for better organization (Optional).
    * **Process Log:** A dedicated log window displays detailed progress and status messages.
    * **Smart Input:** Dragging a file automatically sets its parent folder as the input directory.
* **Hardware Acceleration:** Supports **NVIDIA (NVENC)**, **Intel (QSV)**, and **AMD (AMF)** encoding.
    * Users can select specific presets (e.g., NVIDIA P1~P7) for performance or quality.
    * Automatic fallback to CPU (libx264/libx265) if hardware acceleration fails.

### 2. Video Splitter (Tab 2)

* **Size-Based Splitting:** Split large video files into smaller parts based on a target size (e.g., "100 MB" or "4 GB").
* **High-Speed Processing:** Uses stream copying (`-c copy`), meaning no re-encoding is performed. Splitting is extremely fast and preserves original quality.
* **Automatic Calculation:** Automatically calculates the number of segments based on total file size and duration.
* **Drag & Drop:** Simply drag a video file to set it as the input.

### 3. Settings (Tab 3)

* **FFmpeg Path:** Manually select `ffmpeg.exe` and `ffprobe.exe` if not detected automatically.
* **CPU Settings:** Adjust thread count and preferred codec (H.264, H.265, AV1).
* **GPU Settings:** Fine-tune Quality (CRF/QP) and specific hardware presets (NVIDIA P1-P7, Intel Speed/Quality, etc.).

## Prerequisites (CRITICAL)

### 1. FFmpeg Installation (Mandatory)
**This application does NOT include FFmpeg.** You must set it up yourself.

* **Option A (Recommended):** Install FFmpeg and add it to your **System PATH**. The application will automatically detect it.
* **Option B (Manual):** Download `ffmpeg.exe` and `ffprobe.exe`. Then, go to the **[Settings]** tab in the app and manually select the location of these files.
* *Download Link:* [FFmpeg Official Website](https://ffmpeg.org/download.html)

### 2. Python (for running script directly)
* Python 3.x installed.
* **Required Library:** `tkinterdnd2` is required for Drag & Drop functionality.
    ```bash
    pip install tkinterdnd2
    ```

### 3. (Optional) GPU Drivers
* For hardware acceleration, ensure your NVIDIA/Intel/AMD GPU drivers are up to date.

## How to Use

### A. Using the Executable (`.exe`)

1.  **Install/Locate FFmpeg first.** (See Prerequisites above)
2.  Run `VideoToolSuite.exe`.
3.  **Check Settings:** Go to the **Settings** tab immediately. Ensure "FFmpeg" and "FFprobe" paths are detected. If empty, click "Browse" to select them.
4.  **Select Mode (Top Tabs):**
    * **Converter:** Drag & drop files/folders and start processing.
    * **Splitter:** Drag & drop a video, set split size, and start.
5.  **Check Progress:**
    * Progress bars indicate the current status.
    * The bottom status bar shows detailed messages and remaining time.

### B. Running the Python Script

1.  Clone the repository.
    ```bash
    git clone https://github.com/nopigom119/Video-Tool-Suite-VTS-.git
    ```
2.  Install dependencies:
    ```bash
    pip install tkinterdnd2
    ```
3.  Run the script:
    ```bash
    python video_control_all_in_one_v3.py
    ```

## License

This program is licensed under the **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)**.

* **Non-Commercial Use Only.**
* **Attribution Required.**
* **Share Alike.**

---

# Video Tool Suite (VTS)

**영상 변환 및 분할 도구 (Video Converter & Splitter)**

**영상 변환(Converter)** 과 **영상 분할(Splitter)** 기능을 하나로 통합한 올인원 유틸리티입니다. 직관적인 드래그 앤 드롭(Drag & Drop) 인터페이스, 작업 대기열(Queue) 시스템, 하드웨어 가속을 지원하며 한국어/영어 인터페이스를 제공합니다.

이전 버전과 달리 `moviepy` 의존성을 제거하고, **FFmpeg**를 `subprocess`로 직접 제어하여 성능과 안정성을 극대화했습니다.

> **⚠️ 중요: FFmpeg 설치 필수**
> 이 프로그램은 **FFmpeg**가 없으면 작동하지 않습니다. 프로그램 실행 전 반드시 FFmpeg를 설치하거나 실행 파일(`ffmpeg.exe`)을 준비해야 합니다.

## 주요 기능

이 프로그램은 탭 기반 인터페이스를 통해 다양한 영상 작업을 관리합니다:

* **통합 도구:** 변환기와 분할기가 하나의 앱에 통합되어 있으며, 두 기능은 동시에 실행될 수 있습니다.
* **다국어 지원:** 실행 중 언제든지 한국어/영어로 전환할 수 있습니다.
* **드래그 앤 드롭 (Drag & Drop):** 파일이나 폴더를 프로그램 창에 끌어다 놓는 것만으로 간편하게 입력할 수 있습니다.
* **통합 설정:** FFmpeg 경로, CPU 스레드, GPU 가속 설정을 한 곳에서 관리합니다.

### 1. 영상 변환기 (Converter)

* **지원 입력:** .mp4, .avi, .mov, .mkv, .ts, .webm 등 대부분의 포맷.
* **지원 출력:** MP4, AVI, MOV, WebM, GIF.
* **단일 변환 (대기열 모드):**
    * **작업 대기열:** 여러 개의 파일을 목록에 추가해두고 한 번에 순차적으로 처리할 수 있습니다.
    * **스마트 제어:** 체크박스를 통해 특정 작업만 취소하거나, 실패한 작업만 선별하여 다시 시작할 수 있습니다.
    * **드래그 앤 드롭:** 파일을 드래그하면 자동으로 입력창에 등록됩니다.
* **일괄 변환 (폴더 모드):**
    * **폴더 처리:** 특정 폴더 내의 모든 영상을 지정된 포맷으로 일괄 변환합니다.
    * **자동 아카이빙:** 변환 성공 시 원본 파일을 `_Originals` 폴더로 자동 이동시켜 작업 폴더를 깔끔하게 유지합니다. (옵션)
    * **처리 로그:** 실시간 로그 창을 통해 변환 상세 과정을 확인할 수 있습니다.
    * **스마트 입력:** 폴더뿐만 아니라 파일을 드래그해도 자동으로 해당 파일이 있는 폴더를 입력 경로로 설정합니다.
* **하드웨어 가속:** **NVIDIA (NVENC)**, **Intel (QSV)**, **AMD (AMF)** 인코딩을 지원합니다.
    * NVIDIA P1(고속)~P7(고화질) 등 세부 프리셋을 사용자가 직접 선택할 수 있습니다.
    * 가속 실패 시 자동으로 CPU(libx264)로 전환됩니다.

### 2. 영상 분할기 (Splitter)

* **용량 기반 분할:** 원하는 크기(예: 100MB, 4GB) 단위로 영상을 자동으로 나눕니다.
* **초고속 처리:** 스트림 복사(`-c copy`) 방식을 사용하여 인코딩 없이 원본 화질 그대로 매우 빠르게 분할합니다.
* **자동 계산:** 전체 용량과 시간을 분석하여 필요한 파트 수를 자동으로 계산합니다.
* **드래그 앤 드롭:** 분할할 파일을 간편하게 드래그하여 입력할 수 있습니다.

### 3. 설정 (Settings)

* **FFmpeg 경로:** 시스템에 설치된 FFmpeg를 자동 감지하거나, 사용자가 직접 `exe` 파일을 지정할 수 있습니다.
* **인코딩 설정:** CPU 스레드 개수, 코덱(H.264, H.265, AV1) 선택, GPU 화질(QP) 및 프리셋을 상세하게 조정 가능합니다.

## 사전 준비 사항 (필독)

### 1. FFmpeg 설치 (가장 중요)
**이 프로그램에는 FFmpeg가 포함되어 있지 않습니다.** 사용자가 직접 준비해야 합니다.

* **방법 A (권장):** FFmpeg를 설치하고 **시스템 환경 변수(PATH)**에 등록하세요. 프로그램이 자동으로 인식합니다.
* **방법 B (수동):** `ffmpeg.exe`와 `ffprobe.exe` 파일을 다운로드한 뒤, 프로그램의 **[통합 설정]** 탭에서 '찾기' 버튼을 눌러 파일 위치를 지정해 주세요.
* *다운로드 링크:* [FFmpeg 공식 홈페이지](https://ffmpeg.org/download.html)

### 2. Python (스크립트 실행 시)
* Python 3.x가 필요합니다.
* **필수 라이브러리:** 드래그 앤 드롭 기능을 위해 `tkinterdnd2`가 필요합니다.
    ```bash
    pip install tkinterdnd2
    ```

### 3. (선택) 그래픽 드라이버
* 하드웨어 가속을 사용하려면 각 제조사(NVIDIA/Intel/AMD)의 최신 드라이버가 필요합니다.

## 사용 방법

### A. 실행 파일 사용 (`.exe`)

1.  **FFmpeg를 먼저 준비하세요.** (위의 사전 준비 사항 참고)
2.  `VideoToolSuite.exe`를 실행합니다.
3.  **설정 확인:** 가장 먼저 **[통합 설정]** 탭으로 이동하여 FFmpeg 경로가 잡혀있는지 확인하세요. 비어있다면 직접 지정해야 합니다.
4.  **모드 선택 (상단 탭):**
    * **영상 변환기 (단일):** 파일을 드래그하거나 선택 후 [목록 추가] -> [변환 시작]을 클릭합니다.
    * **영상 변환기 (일괄):** 폴더를 드래그하여 놓고 포맷을 지정한 뒤 시작합니다.
    * **영상 분할기:** 영상을 드래그하여 놓고 분할할 크기(예: 100 MB)를 입력한 뒤 시작합니다.
5.  **진행 확인:**
    * 각 탭의 진행률 표시줄과 하단 상태바를 통해 작업 상황을 실시간으로 확인합니다.

### B. Python 스크립트 실행

1.  저장소를 클론하거나 다운로드합니다.
    ```bash
    git clone https://github.com/nopigom119/Video-Tool-Suite-VTS-.git
    ```
2.  필요한 패키지를 설치합니다.
    ```bash
    pip install tkinterdnd2
    ```
3.  스크립트를 실행합니다:
    ```bash
    python video_control_all_in_one_v3.py
    ```

## 라이선스

본 프로그램은 **크리에이티브 커먼즈 저작자표시-비영리-동일조건변경허락 4.0 국제 라이선스 (CC BY-NC-SA 4.0)** 에 따라 이용할 수 있습니다.

* **저작자 표시 필수**
* **비영리 목적으로만 이용 가능**
* **동일 조건 변경 허락**

## 문의 (Contact)

For inquiries about this program, please contact [rycbabd@gmail.com].
