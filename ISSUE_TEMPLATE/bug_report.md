# Bug Report (버그 리포트)

## Description (설명)

Please provide a concise and clear description of the bug.
(e.g., "Error occurs when splitting a 10GB .mkv file," or "Application crashes when selecting NVIDIA P7 preset in Settings.")

(예: "10GB .mkv 파일을 분할할 때 오류 발생", 또는 "설정에서 NVIDIA P7 프리셋 선택 시 애플리케이션 충돌")

## Steps to Reproduce (발생 단계)

1.  List the steps to reproduce the bug in order.
    (e.g., 1. Go to 'Video Splitter' tab. 2. Select a .mp4 video file. 3. Set split size to '100 MB'. 4. Click 'Start Splitting'.)
2.  ...
3.  ...

(예: 1. '영상 분할기' 탭으로 이동합니다. 2. .mp4 비디오 파일을 선택합니다. 3. 분할 크기를 '100 MB'로 설정합니다. 4. '분할 시작'을 클릭합니다.)

## Expected Result (예상 결과)

Please describe the correct expected behavior.
(e.g., "The video should be split into multiple 100MB segments without error," or "The application should prompt to select a valid FFmpeg path if not found.")

(예: "비디오가 오류 없이 여러 개의 100MB 세그먼트로 분할되어야 합니다", 또는 "FFmpeg 경로를 찾을 수 없는 경우 유효한 경로를 선택하라는 메시지가 표시되어야 합니다.")

## Actual Result (실제 결과)

Please describe the actual error or incorrect behavior that occurred.
(e.g., "The progress bar stops at 50% and never completes," or "A 'subprocess error' popup appears.")

(예: "진행률 표시줄이 50%에서 멈추고 완료되지 않습니다", 또는 "'subprocess error' 팝업이 나타납니다.")

## Additional Information (추가 정보) (Optional - 선택 사항)

* **Operating System and Python version:** (e.g., Windows 10/11, Python 3.10)
  (예: Windows 10/11, Python 3.10)

* **Video Tool Suite (VTS) Version:** (e.g., v2.0.0, or commit hash)
  (예: v2.0.0, 또는 커밋 해시)

* **Problematic Video File Details (if relevant):** (e.g., Specific file name, format (e.g., WebM, MKV), codec (e.g., VP9, H.265/HEVC), resolution (e.g., 1080p, 4K), file size (e.g., 50MB, 2GB), duration.)
  (관련된 경우 문제가 되는 비디오 파일 세부 정보: 예: 특정 파일 이름, 형식, 코덱, 해상도, 파일 크기, 길이 등.)

* **Settings Used:** (e.g., Split size, Target format, GPU acceleration enabled/disabled, Thread count.)
  (예: 분할 크기, 변환 대상 포맷, GPU 가속 활성화 여부, 스레드 수 등 사용된 설정.)

* **Screenshots or Error Messages:** (Please attach a screenshot or the content of the error message. Since VTS v2 uses FFmpeg directly, any console output logs are very helpful.)
  (오류 발생 시 화면 캡처 또는 오류 메시지 내용을 첨부해주세요. VTS v2는 FFmpeg를 직접 사용하므로 콘솔 출력 로그가 매우 도움이 됩니다.)

* **Any other helpful information:** (e.g., FFmpeg version installed on your system, specific GPU model if related to hardware acceleration.)
  (기타 도움이 될 만한 정보: 예: 시스템에 설치된 FFmpeg 버전, 하드웨어 가속과 관련된 경우 특정 GPU 모델.)
