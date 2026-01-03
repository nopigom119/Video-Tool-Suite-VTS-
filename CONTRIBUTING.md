# Contributing to Video Tool Suite (VTS)

Thank you for your interest in contributing to **Video Tool Suite (VTS)**! All contributions are welcome.
We appreciate any form of contribution, be it bug fixes, feature additions (converter or splitter), documentation improvements, or helping with testing.

## How to Contribute

### 1. Reporting Issues

* Please register new feature suggestions or bug reports on the [Video Tool Suite Issues page](https://github.com/nopigom119/Video-Tool-Suite-VTS/issues).
* Make sure the issue title is concise and clear.
* Provide detailed descriptions of the problem or suggestion in the issue content. Please include:
    * Steps to reproduce the bug.
    * Expected behavior and actual behavior.
    * Your operating system and version.
    * The version of the Video Tool Suite application you are using.
    * Input video file format and codec (if known).
    * Settings used (e.g., Target format, Split size, GPU acceleration presets).
    * Screenshots or error messages (from the application or FFmpeg logs) if applicable.

### 2. Contributing Code

1.  Fork the [Video Tool Suite repository](https://github.com/nopigom119/Video-Tool-Suite-VTS).
2.  Create a new branch in your forked repository for your contribution.
    * Branch names should be descriptive. (e.g., `feature/add-hevc-support`, `bugfix/fix-splitter-calculation`)
3.  Write your code. Please adhere to the [PEP 8](https://www.python.org/dev/peps/pep-0008/) coding style guidelines.
4.  Test your changes thoroughly.
    * Since this project uses **FFmpeg** via `subprocess`, ensure that commands are constructed safely and handle errors gracefully.
    * Test with various hardware configurations (if touching GPU features) and different file types.
5.  Write concise and clear commit messages. (e.g., `feat: Add NVENC P7 preset`, `fix: Handle Unicode filenames in splitter`)
6.  Submit a [pull request](https://github.com/nopigom119/Video-Tool-Suite-VTS/pulls) to the `main` branch of the original Video Tool Suite repository.
    * Clearly describe the changes you have made in your pull request.
    * Link to any relevant issues.

### 3. Contributing to Documentation

* You can contribute to improving documentation, such as the README file, comments within the code, code explanations, usage examples, or tips for troubleshooting.
* Make sure the documentation is clear, concise, and easy to understand.

## Code Writing Rules

* Follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) coding style guidelines.
* Write clear and descriptive docstrings for all public modules, classes, functions, and methods.
* Add comments to your code where necessary to explain complex logic.
* **FFmpeg Interaction:** Pay special attention to how `subprocess` calls to FFmpeg are handled.
    * Ensure `startupinfo` is used to hide console windows on Windows.
    * Properly handle `stdout` and `stderr` to prevent deadlocks and to capture progress correctly.
    * Ensure external processes are terminated if the main application is closed or the task is cancelled.
* **Threading:** As the application uses `threading` and `queue` for concurrency, ensure UI updates are strictly performed in the main thread (e.g., by checking the queue via `root.after`).

## Commit Message Rules

* Write concise and clear commit messages.
* A good commit message should briefly describe the change.
* Consider using [Conventional Commits](https://www.conventionalcommits.org/) for a structured approach (e.g., `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`).

## Pull Request Procedure

1.  Ensure your code adheres to the project's coding standards and works as expected.
2.  Create a pull request from your feature branch to the `main` branch of the `nopigom119/Video-Tool-Suite-VTS` repository.
3.  Provide a clear description of the changes in the pull request.
4.  Be prepared to discuss your changes and make further modifications if requested by the maintainers.

## Inquiries

* For inquiries or discussions about contributing to Video Tool Suite, please use the [Video Tool Suite Issues page](https://github.com/nopigom119/Video-Tool-Suite-VTS/issues).

## License

By contributing to Video Tool Suite, you agree that your contributions will be licensed under its CC BY-NC-SA 4.0 License.

---

# Video Tool Suite (VTS)에 기여하기

**Video Tool Suite (VTS)**에 관심을 가져주셔서 감사합니다! 모든 기여를 환영합니다.
버그 수정, 기능 추가(변환기 또는 분할기), 문서 개선, 테스트 지원 등 어떤 형태의 기여든 감사하게 생각합니다.

## 기여 방법

### 1. 이슈 등록

* 새로운 기능 제안이나 버그 보고는 [Video Tool Suite 이슈 페이지](https://github.com/nopigom119/Video-Tool-Suite-VTS/issues)에 등록해주세요.
* 이슈 제목은 간결하고 명확하게 작성해주세요.
* 이슈 내용에는 문제 상황이나 제안 내용을 상세하게 설명해주세요. 다음 정보를 포함해주세요:
    * 버그 재현 단계.
    * 예상되는 동작과 실제 동작.
    * 사용 중인 운영체제 및 버전.
    * 사용 중인 Video Tool Suite 애플리케이션 버전.
    * 입력 비디오 파일 형식 및 코덱 (알고 있는 경우).
    * 사용된 설정 (예: 변환 포맷, 분할 크기, GPU 가속 프리셋 등).
    * 해당되는 경우 스크린샷 또는 오류 메시지 (애플리케이션 또는 FFmpeg 로그).

### 2. 코드 기여

1.  [Video Tool Suite 저장소](https://github.com/nopigom119/Video-Tool-Suite-VTS)를 포크해주세요.
2.  포크한 저장소에서 기여를 위한 새로운 브랜치를 만들어주세요.
    * 브랜치 이름은 설명적으로 작성해주세요. (예: `feature/HEVC-지원-추가`, `bugfix/분할-계산-오류-수정`)
3.  코드를 작성해주세요. [PEP 8](https://www.python.org/dev/peps/pep-0008/) 코딩 스타일 가이드라인을 준수해주세요.
4.  변경 사항을 철저히 테스트해주세요.
    * 이 프로젝트는 `subprocess`를 통해 **FFmpeg**를 직접 사용하므로, 명령어가 안전하게 구성되고 오류를 적절히 처리하는지 확인해야 합니다.
    * GPU 기능을 수정하는 경우 다양한 하드웨어 구성에서 테스트하고, 여러 파일 형식에 대해 테스트해주세요.
5.  간결하고 명확한 커밋 메시지를 작성해주세요. (예: `feat: NVENC P7 프리셋 추가`, `fix: 유니코드 파일명 분할 오류 수정`)
6.  원본 Video Tool Suite 저장소의 `main` 브랜치로 [풀 리퀘스트](https://github.com/nopigom119/Video-Tool-Suite-VTS/pulls)를 보내주세요.
    * 풀 리퀘스트에 변경한 내용을 명확하게 설명해주세요.
    * 관련된 이슈가 있다면 링크해주세요.

### 3. 문서 기여

* README 파일, 코드 내 주석, 코드 설명, 사용 예시, 문제 해결 팁 등 문서 개선에 기여해주실 수 있습니다.
* 문서 내용은 명확하고 간결하며 이해하기 쉽게 작성해주세요.

## 코드 작성 규칙

* [PEP 8](https://www.python.org/dev/peps/pep-0008/) 코딩 스타일 가이드라인을 준수해주세요.
* 모든 공개 모듈, 클래스, 함수, 메소드에 대해 명확하고 설명적인 독스트링(docstring)을 작성해주세요.
* 복잡한 로직을 설명하기 위해 필요한 경우 코드에 주석을 추가해주세요.
* **FFmpeg 상호작용:** `subprocess`를 통한 FFmpeg 호출 처리에 특히 주의해주세요.
    * Windows에서 콘솔 창이 뜨지 않도록 `startupinfo`를 사용해야 합니다.
    * 교착 상태(Deadlock)를 방지하고 진행 상황을 올바르게 캡처하기 위해 `stdout`과 `stderr`를 적절히 처리해주세요.
    * 메인 애플리케이션이 종료되거나 작업이 취소될 때 외부 프로세스도 함께 종료되도록 해야 합니다.
* **스레딩(Threading):** 애플리케이션이 동시성을 위해 `threading`과 `queue`를 사용하므로, UI 업데이트는 반드시 메인 스레드에서 수행되어야 합니다(예: `root.after`를 통해 큐 확인).

## 커밋 메시지 규칙

* 간결하고 명확한 커밋 메시지를 작성해주세요.
* 좋은 커밋 메시지는 변경 사항을 간략하게 설명해야 합니다.
* 구조화된 접근 방식을 위해 [Conventional Commits](https://www.conventionalcommits.org/ko/v1.0.0/) 사용을 고려해보세요 (예: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`).

## 풀 리퀘스트 절차

1.  코드가 프로젝트의 코딩 표준을 준수하고 예상대로 작동하는지 확인해주세요.
2.  기능 브랜치에서 `nopigom119/Video-Tool-Suite-VTS` 저장소의 `main` 브랜치로 풀 리퀘스트를 생성해주세요.
3.  풀 리퀘스트에 변경 사항에 대한 명확한 설명을 제공해주세요.
4.  관리자의 요청이 있을 경우 변경 사항에 대해 논의하고 추가 수정을 할 준비가 되어 있어야 합니다.

## 문의

* Video Tool Suite 기여에 대한 문의나 논의는 [Video Tool Suite 이슈 페이지](https://github.com/nopigom119/Video-Tool-Suite-VTS/issues)를 이용해주세요.

## 라이선스

Video Tool Suite에 기여함으로써 귀하의 기여물은 해당 프로젝트의 CC BY-NC-SA 4.0 라이선스에 따라 사용이 허가됨에 동의하는 것으로 간주됩니다.
