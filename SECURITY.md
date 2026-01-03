# Security Policy

This document outlines the security policy for the "Video Tool Suite (VTS)" project.

## Reporting Vulnerabilities

If you discover a security vulnerability in this project, please report it to us at [rycbabd@gmail.com]. We appreciate your responsible disclosure and will make every effort to address the issue promptly.

When reporting a security vulnerability, please try to include as much information as possible, such as:

* A clear and concise description of the vulnerability.
* Steps to reproduce the vulnerability. Include specific video files (or their characteristics), formats, conversion/splitting settings, or sequence of operations if applicable.
* The affected version(s) of the "Video Tool Suite (VTS)" application.
* Any potential impact of the vulnerability (e.g., unexpected program behavior, saving files to unintended locations, potential data corruption, generation of malformed video files, command injection risks).
* Your name/handle (optional, but appreciated for acknowledging your contribution).

We are particularly interested in vulnerabilities related to:

* Improper handling of file paths that could lead to saving files in unintended locations or overwriting critical files during conversion or splitting.
* Issues that could cause denial of service (e.g., application crashes when processing specific video files/formats, encountering very large files, or dealing with excessively long file paths).
* Improper construction of FFmpeg commands via `subprocess` calls.
* Generation of output files that are unexpectedly large, malformed, or contain unintended artifacts.
* Any other behavior that compromises user security or data integrity during the conversion or splitting process.

## Reporting Guidelines

To help us effectively address security vulnerabilities, please provide the following information in your report:

* A clear and concise description of the vulnerability.
* Steps to reproduce the vulnerability. Include specific video files (if shareable, or their properties), selected input/output formats, or the sequence of operations if applicable.
* The affected version(s) of the "Video Tool Suite (VTS)" application.
* Any potential impact of the vulnerability.
* Your name/handle (optional, but appreciated for acknowledging your contribution).

## Vulnerability Classification

We will assess the severity of reported vulnerabilities based on their potential impact. We encourage reporters to provide their own assessment of the severity, but we will make the final determination.

## Public Disclosure Policy

We will not publicly disclose vulnerabilities until a fix has been released and made available to users (e.g., via a new release on the project's distribution platform or repository). We will credit responsible reporters in the release notes or commit messages (unless anonymity is requested).

## Scope

This security policy applies to the "Video Tool Suite (VTS)" application, including its Python source code (`video_control_all_in_one_v2.py`) and any distributed executable files. Please note that this policy does not cover vulnerabilities within **FFmpeg**, **FFprobe**, or the underlying video/audio codecs themselves; those should be reported to their respective maintainers.

## Contact

For security-related inquiries regarding the "Video Tool Suite (VTS)" project, please contact us at [rycbabd@gmail.com].

---

# 보안 정책

이 문서는 "Video Tool Suite (VTS)" (영상 변환 및 분할 도구) 프로젝트의 보안 정책을 설명합니다.

## 취약점 보고

본 프로젝트에서 보안 취약점을 발견한 경우, [rycbabd@gmail.com]으로 보고해 주시기 바랍니다. 책임감 있는 제보에 감사드리며, 문제를 신속하게 해결하기 위해 최선을 다하겠습니다.

보안 취약점을 보고하실 때, 가능한 한 다음 정보를 포함해 주십시오:

* 취약점에 대한 명확하고 간결한 설명.
* 취약점을 재현하는 단계. 해당되는 경우 특정 비디오 파일(또는 그 특성), 형식, 변환/분할 설정 또는 작업 순서를 포함합니다.
* "Video Tool Suite (VTS)" 애플리케이션의 영향을 받는 버전.
* 취약점의 잠재적 영향 (예: 예기치 않은 프로그램 동작, 의도치 않은 위치에 파일 저장, 잠재적인 데이터 손상, 손상된 비디오 파일 생성, 명령어 주입 위험 등).
* 귀하의 이름/핸들 (선택 사항이지만, 기여에 대한 감사를 표하기 위해 권장합니다.)

특히 다음과 관련된 취약점에 관심이 있습니다:

* 변환 또는 분할 과정에서 의도치 않은 위치에 파일을 저장하거나 중요한 파일을 덮어쓸 수 있는 파일 경로의 부적절한 처리.
* 서비스 거부(예: 특정 비디오 파일/형식 처리, 매우 큰 파일 또는 지나치게 긴 파일 경로 처리 시 발생하는 애플리케이션 충돌)를 유발할 수 있는 문제.
* `subprocess` 호출을 통한 FFmpeg 명령어 구성 시의 부적절한 처리 문제.
* 예상치 않게 크거나, 손상되거나, 원치 않는 결과물을 포함하는 출력 파일 생성.
* 변환 또는 분할 과정에서 사용자 보안 또는 데이터 무결성을 손상시키는 기타 모든 동작.

## 보고 지침

보안 취약점을 효과적으로 해결할 수 있도록, 보고 시 다음 정보를 제공해 주십시오.

* 취약점에 대한 명확하고 간결한 설명
* 취약점을 재현하는 단계. 해당되는 경우 특정 비디오 파일(공유 가능한 경우 또는 그 속성), 선택한 입/출력 형식 또는 작업 순서를 포함합니다.
* "Video Tool Suite (VTS)" 애플리케이션의 영향을 받는 버전
* 취약점의 잠재적 영향
* 귀하의 이름/핸들 (선택 사항이지만, 기여에 대한 감사를 표하기 위해 권장합니다.)

## 취약점 분류

보고된 취약점의 심각도는 잠재적 영향을 기준으로 평가합니다. 보고자는 심각도에 대한 자체 평가를 제공할 수 있지만, 최종 결정은 저희가 내립니다.

## 공개 정책

당사는 수정 사항이 릴리스되어 사용자에게 제공될 때까지(예: 프로젝트 배포 플랫폼의 새 릴리스 또는 저장소 업데이트를 통해) 취약점을 공개적으로 공개하지 않습니다. 익명을 요청하지 않는 한, 릴리스 노트 또는 커밋 메시지에 책임감 있는 보고자를 표기할 것입니다.

## 적용 범위

이 보안 정책은 "Video Tool Suite (VTS)" 애플리케이션의 Python 소스 코드(`video_control_all_in_one_v2.py`) 및 배포된 모든 실행 파일에 적용됩니다. 이 정책은 **FFmpeg**, **FFprobe** 또는 기본 비디오/오디오 코덱 자체 내의 취약점에는 적용되지 않으며, 해당 취약점은 각 유지 관리자에게 보고해야 합니다.

## 연락처

"Video Tool Suite (VTS)" 프로젝트 관련 보안 문의는 [rycbabd@gmail.com]으로 연락 주시기 바랍니다.
