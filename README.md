# Video Tool Suite (VTS)

**Integrated Video Management Utility / 통합 비디오 관리 도구**

A high-performance video processing suite designed for **Video Conversion** and **High-Speed Splitting**. This tool leverages native **FFmpeg** integration with advanced hardware acceleration discovery for professional-grade stability and speed.

> **⚠️ MANDATORY: FFmpeg & FFprobe**
> This application requires **ffmpeg.exe** and **ffprobe.exe**. You must specify their individual paths in the **Settings** tab for the application to function correctly.

## Core Capabilities

* **Integrated Architecture:** Concurrent operation of Video Converter and Splitter tools within a single UI.
* **Hardware Intelligence:** OS-level hardware discovery (via WMIC) to automatically assign NVIDIA (NVENC), Intel (QSV), or AMD (AMF) encoders.
* **Production-Ready UI:** Modern CustomTkinter interface with full Dark Mode support and recursive Drag & Drop handling.
* **Queue Management:** Advanced task sequencing for single files and automated folder-wide batch processing.

### 1. Advanced Video Converter
* **Hybrid Encoding:** Real-time toggling between Hardware Acceleration and optimized CPU fallbacks (libx264/libx265).
* **Smart Archiving:** Automatically segregates original files into a dedicated `_Originals` folder post-conversion.
* **Granular Control:** Direct adjustment of QP (Quality Parameter) and multi-threading allocation for background tasks.

### 2. Stream-Copy Splitter
* **Lossless Splitting:** Uses `-c copy` logic to split massive files by size without re-encoding, preserving 100% original quality.
* **Size-Proportional Logic:** Automatically calculates segment distribution based on user-defined GB/MB targets.

## Technical Roadmap (Planned Improvements)

The following modules are scheduled for modification and enhancement to address current technical constraints:

* **ETA Logic Overhaul:** Current time estimation is conceptual. A new velocity-weighted algorithm will be implemented to provide accurate completion times for parallel GPU tasks.
* **Precise Splitter Alignment:** Improving keyframe-aware splitting to minimize size offsets caused by GOP (Group of Pictures) boundaries.
* **Task Priority Management:** Implementing a priority flag system within the task queue for urgent video processing.

## Installation & Setup

### 1. Prerequisites
* **Python 3.8+**
* **FFmpeg/FFprobe binaries** (GPL Full build recommended)
* **Required Libraries:**
    ```bash
    pip install customtkinter tkinterdnd2
    ```

### 2. Running the Application
1.  Clone the repository:
    ```bash
    git clone [https://github.com/nopigom119/Video-Tool-Suite-VTS-.git](https://github.com/nopigom119/Video-Tool-Suite-VTS-.git)
    ```
2.  Launch the suite:
    ```bash
    python main.py
    ```

## License
Licensed under **CC BY-NC-SA 4.0 (Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International)**.

## Contact
For technical inquiries: [rycbabd@gmail.com](mailto:rycbabd@gmail.com)

---

# Video Tool Suite (VTS)

**영상 변환 및 고속 분할 통합 솔루션**

**영상 변환(Converter)**과 **영상 분할(Splitter)** 기능을 하나로 통합한 고성능 유틸리티입니다. **FFmpeg** 엔진과의 직접 연동 및 OS 기반 하드웨어 탐색 기술을 통해 최상의 변환 속도와 안정성을 제공합니다.

> **⚠️ 필수 사항: FFmpeg & FFprobe**
> 본 프로그램은 **ffmpeg.exe** 및 **ffprobe.exe** 파일이 반드시 필요합니다. **Settings** 탭에서 각 실행 파일의 경로를 직접 지정해야 정상적으로 작동합니다.

## 핵심 기능

* **통합 아키텍처:** 하나의 UI 내에서 변환기와 분할기 도구를 동시에 독립적으로 실행할 수 있습니다.
* **지능형 하드웨어 감지:** WMIC를 통한 OS 레벨 쿼리로 NVIDIA, Intel, AMD 그래픽카드를 자동 감지하여 최적의 인코더를 할당합니다.
* **모던 디자인 UI:** 다크 모드가 완벽 지원되는 CustomTkinter 기반 인터페이스와 직관적인 드래그 앤 드롭 기능을 지원합니다.
* **대기열 시스템:** 단일 파일 대기열 처리 및 폴더 단위 일괄 변환(Batch) 기능을 지원합니다.

### 1. 고성능 영상 변환기
* **하이브리드 인코딩:** 하드웨어 가속과 최적화된 CPU 소프트웨어 인코딩(libx264/libx265) 간의 자동 전환을 지원합니다.
* **스마트 아카이빙:** 변환 완료 후 원본 파일을 `_Originals` 폴더로 자동 분류하여 관리 편의성을 높입니다.
* **상세 제어:** QP(화질 지수) 설정 및 작업별 쓰레드 할당량을 사용자가 직접 조절할 수 있습니다.

### 2. 스트림 복사 분할기
* **무손실 분할:** `-c copy` 로직을 사용하여 재인코딩 없이 대용량 파일을 지정된 크기로 매우 빠르게 나눕니다.
* **자동 계산 시스템:** 사용자가 입력한 용량(GB/MB) 단위를 기준으로 최적의 분할 파트 수를 자동 계산합니다.

## 기술 로드맵 (개선 및 추가 예정 기능)

현재의 기술적 제약을 해결하기 위해 다음 모듈들의 수정 및 보강이 계획되어 있습니다:

* **ETA(남은 시간) 로직 전면 개정:** 현재의 단순 추정 방식을 개선하여, 병렬 GPU 처리 상황에서도 정확한 완료 시간을 산출하는 속도 가중치 알고리즘을 도입합니다.
* **분할 정밀도 고도화:** 스트림 복사 시 발생하는 키프레임 오차를 최소화하여 설정 용량과의 일치성을 높이는 정밀 분할 로직을 강화합니다.
* **작업 우선순위 제어:** 대규모 작업 대기열 내에서 특정 작업에 높은 우선순위를 부여하는 플래그 시스템을 추가합니다.

## 설치 및 실행 방법

### 1. 사전 요구 사항
* **Python 3.8 이상**
* **FFmpeg/FFprobe 실행 파일** (GPL Full 빌드 권장)
* **필수 라이브러리 설치:**
    ```bash
    pip install customtkinter tkinterdnd2
    ```

### 2. 프로그램 실행
1.  저장소 클론:
    ```bash
    git clone [https://github.com/nopigom119/Video-Tool-Suite-VTS-.git](https://github.com/nopigom119/Video-Tool-Suite-VTS-.git)
    ```
2.  스크립트 실행:
    ```bash
    python main.py
    ```

## 라이선스
본 프로그램은 **CC BY-NC-SA 4.0 (크리에이티브 커먼즈 저작자표시-비영리-동일조건변경허락 4.0 국제)** 라이선스를 따릅니다.

## 문의 사항
기술 관련 문의: [rycbabd@gmail.com](mailto:rycbabd@gmail.com)