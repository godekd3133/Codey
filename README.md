# Codey

PyQt5 데스크톱 창에서 소스 코드를 다른 프로그래밍 언어로 변환해 주는 도구입니다. 입력 창에 코드를 붙여 넣고 원본/대상 언어를 고르면, OpenAI 채팅 완성 API(`gpt-3.5-turbo`)에 변환을 요청해 결과를 출력 창에 보여 줍니다.

## 소개

- 커밋은 2024-06-13부터 2024-06-14까지 4건이고("Added Code", "finish" 등), 저장소 설명은 없습니다.
- 인원과 제작 동기는 저장소에서 확인되지 않습니다.
- 지원 언어는 Python, Java, C++ 세 가지이며, 원본과 대상을 각각 드롭다운으로 고릅니다. "Annotation"을 켜면 변환 결과에 두 언어 사이의 핵심 차이를 한국어 주석으로 달도록 요청합니다.

## 핵심 구현

모든 코드는 `codey.py` 한 파일의 `LanguageConverter`(`QMainWindow`) 클래스에 있습니다.

### 화면 구성

창 크기를 1280x720으로 고정하고(`setFixedSize`), 위젯을 레이아웃 매니저 없이 `setGeometry`로 좌표를 지정해 배치합니다. 디자인 이미지(`images/`의 로고, 입력/출력 아이콘, 변환·복사·저장 버튼, 텍스트 영역 배경)를 `drawImage` 헬퍼로 `QLabel`에 그려 얹고, 그 위에 투명한 `QTextEdit`, `QPushButton`, `QComboBox`를 놓아 시안에 맞춘 어두운 테마를 만들었습니다.

### 변환 요청 (`convert`, `get_completion`)

```python
if self.annotation_checkbox.isChecked():
    promptstr = f"Convert the following {source_language} code to {target_language} code and include comments ... all comments should be in Korean."
else:
    promptstr = f"Convert the following {source_language} code to {target_language} code:\n{input_text} "

output_text = self.get_completion(promptstr)
self.output_field.setPlainText(output_text)
```

`get_completion`은 프롬프트를 `user` 메시지 하나로 `openai.ChatCompletion.create(model="gpt-3.5-turbo", temperature=0)`에 보내고, 첫 응답의 `content`를 돌려줍니다. 변환 호출이 동기식이라 응답을 기다리는 동안 창이 멈춥니다.

### 결과 복사와 저장

`copy_to_clipboard`는 출력 창의 텍스트를 `pyperclip`으로 클립보드에 복사하고, `save_to_file`은 저장 대화상자(`QFileDialog.getSaveFileName`)로 고른 경로에 텍스트 파일로 씁니다.

## 프로젝트 구조

| 경로 | 내용 |
| --- | --- |
| `codey.py` | 창, 변환 요청, 복사/저장 전부 |
| `images/` | 로고, 버튼, 아이콘, 텍스트 영역 배경 등 디자인 이미지 |
| `.gitignore` | 무시 규칙 |

## 기술 스택

- Python, PyQt5, pyperclip
- openai 파이썬 패키지: `openai.ChatCompletion.create` 호출 방식이라 1.0 이전 버전 API용 코드입니다. 버전 고정 파일(`requirements.txt`)은 없습니다.

## 실행 방법

1. Python에 `PyQt5`, `pyperclip`, `openai`(1.0 이전 버전)를 설치합니다.
2. `python codey.py`로 창을 띄웁니다.
3. 변환은 외부 OpenAI 채팅 API 호출로 이루어집니다. 현재 코드 구조 그대로는 이어서 쓰기 어렵고, 아래 현재 상태에 적은 재작성이 필요합니다.

## 현재 상태

학습용 프로토타입이며 2024-06-14 이후 갱신이 없습니다. 현재 코드 구조로는 그대로 쓰기 어려워 재작성이 필요합니다.

- 변환 호출이 1.0 이전 `openai` 인터페이스(`ChatCompletion`)에 묶여 있고, UI 클래스 안에서 동기식으로 호출됩니다. 재작성할 때는 호출부를 UI에서 분리하고 현행 SDK로 옮기며 비동기 처리(스레드 등)를 넣어야 합니다.
- 변환 결과 구문 강조(`highlight_output`)는 정의만 되어 있고 `convert`에서 호출되지 않습니다. 이 함수의 `//` 주석 처리 분기도 `#`로 문자열을 나누고 있어 그대로 쓰면 오류가 납니다.
- 호버 이미지 `Convert_hover.png`와 창 아이콘 `images/icon.png`는 저장소에 없습니다.
- 변환 버튼 외의 버튼 변수가 같은 이름(`convert_button`)을 재사용하고, 레이아웃 코드 일부가 주석 처리된 채 남아 있는 등 정리가 필요합니다.
- 이 문서는 2024년 6월 시점의 코드를 읽고 정리한 것이며, 현재 환경에서 다시 실행해 확인하지는 않았습니다.
