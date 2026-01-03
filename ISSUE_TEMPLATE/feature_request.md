# Feature Request (기능 제안)

## Description (설명)

Add functionality to cancel ongoing video processing tasks, including **Video Conversion** (Single/Batch) and **Video Splitting**.

**비디오 변환**(단일/일괄) 및 **비디오 분할**을 포함하여 현재 진행 중인 영상 처리 작업을 취소할 수 있는 기능을 추가합니다.

## Proposal (제안 내용)

Introduce a **'Cancel'** button on the user interface (UI) for both the Converter and Splitter tabs. When a task is in progress, this button should be active (replacing or placed next to the 'Start' button). Clicking it should perform the following:

1.  **For Converter (Single File):**
    * Immediately terminate the running FFmpeg subprocess.
    * Attempt to delete the partially created output file (e.g., `_fast.mp4` or `_re-encoded.mp4`) to save disk space.
    * Reset the progress bar and status messages to "Cancelled".

2.  **For Converter (Batch Folder):**
    * Stop the conversion of the *current* file (terminate subprocess and delete partial output).
    * Stop processing the remaining files in the queue.
    * Update the overall progress bar and status to indicate the batch job was cancelled.

3.  **For Splitter:**
    * Terminate the current splitting operation immediately.
    * Stop the loop that calculates and generates subsequent segments.
    * Attempt to delete any partially created segment files from the current operation.

The UI should clearly indicate that the cancellation is processing and confirm when it is complete, re-enabling input fields for a new task.

변환기(Converter) 및 분할기(Splitter) 탭의 사용자 인터페이스(UI)에 **'취소(Cancel)'** 버튼을 도입합니다. 작업이 진행 중일 때 이 버튼이 활성화되어야 합니다('시작' 버튼을 대체하거나 옆에 배치). 클릭 시 다음 작업을 수행해야 합니다:

1.  **변환기 (단일 파일)의 경우:**
    * 실행 중인 FFmpeg 하위 프로세스(subprocess)를 즉시 종료합니다.
    * 디스크 공간 확보를 위해 부분적으로 생성된 출력 파일(예: `_fast.mp4` 또는 `_re-encoded.mp4`)을 삭제를 시도합니다.
    * 진행률 표시줄과 상태 메시지를 "취소됨"으로 재설정합니다.

2.  **변환기 (폴더 일괄)의 경우:**
    * *현재* 파일의 변환을 중단합니다(프로세스 종료 및 부분 출력 삭제).
    * 대기열에 있는 나머지 파일들의 처리를 중단합니다.
    * 전체 진행률 표시줄과 상태를 업데이트하여 일괄 작업이 취소되었음을 알립니다.

3.  **분할기 (Splitter)의 경우:**
    * 현재 분할 작업을 즉시 종료합니다.
    * 후속 구간을 계산하고 생성하는 루프를 중단합니다.
    * 현재 작업으로 인해 부분적으로 생성된 구간 파일들의 삭제를 시도합니다.

UI는 취소가 진행 중임을 명확히 표시하고 완료되면 확인 메시지를 띄운 후, 새로운 작업을 위해 입력 필드들을 다시 활성화해야 합니다.

## Use Case / Motivation (사용 사례 / 동기)

Currently, users have no way to gracefully stop the application once a task starts without force-closing the entire program. This is critical for **Video Tool Suite (VTS)** because:

* **Batch Conversion:** Processing a folder with hundreds of videos can take hours. Users might realize they selected the wrong preset or format after starting.
* **Splitting:** Splitting a very large file (e.g., 50GB) into small chunks can be time-consuming, and users might want to abort if they set the wrong split size.
* **Resource Management:** Video processing consumes significant CPU/GPU resources. Users may need to pause or stop the task instantly to perform other urgent tasks on their PC.

현재 사용자는 작업을 시작한 후 전체 프로그램을 강제로 종료하지 않고는 작업을 정상적으로 중지할 방법이 없습니다. 이는 **Video Tool Suite (VTS)**에 있어 매우 중요합니다:

* **일괄 변환:** 수백 개의 비디오가 있는 폴더를 처리하는 데는 몇 시간이 걸릴 수 있습니다. 사용자는 시작 후 잘못된 프리셋이나 포맷을 선택했다는 것을 깨달을 수 있습니다.
* **분할:** 매우 큰 파일(예: 50GB)을 작은 조각으로 나누는 작업은 시간이 오래 걸릴 수 있으며, 사용자가 분할 크기를 잘못 설정한 경우 중단하고 싶을 수 있습니다.
* **리소스 관리:** 영상 처리는 상당한 CPU/GPU 리소스를 소모합니다. 사용자는 PC에서 다른 긴급한 작업을 수행하기 위해 작업을 즉시 중단해야 할 수 있습니다.

## Additional Information (추가 정보) (Optional - 선택 사항)

* **Technical Implementation:**
    * Since VTS v2 uses `subprocess.Popen` to call FFmpeg directly, the cancel function must call `.terminate()` or `.kill()` on the `self.current_process` object.
    * It must also set the threading flags (`self.converter_running`, `self.splitter_running`) to `False` to break out of any processing loops (especially in Batch and Splitter modes).
    
    (VTS v2는 `subprocess.Popen`을 사용하여 FFmpeg를 직접 호출하므로, 취소 기능은 `self.current_process` 객체에 대해 `.terminate()` 또는 `.kill()`을 호출해야 합니다. 또한 스레딩 플래그(`self.converter_running`, `self.splitter_running`)를 `False`로 설정하여 처리 루프(특히 일괄 및 분할 모드)를 빠져나와야 합니다.)

* **Feedback:** Display "Cancelling..." in the status bar immediately upon clicking.
    (클릭 즉시 상태 표시줄에 "취소 중..."을 표시합니다.)
