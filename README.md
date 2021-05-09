# Installation

- PyQt5 [link](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- pynput [link](https://pynput.readthedocs.io/en/latest/index.html)
- VLC [link](https://www.videolan.org/vlc/download-windows.html)

```bash
pip install PyQt5
pip install pynput
# pip install python-vlc
# pip install -U word_forms

pip install opencv-python
pip install selenium
```

# Library
- twinword (https://rapidapi.com/twinword/api/word-dictionary/pricing)
-> 10000 / month quota

# Commands
- PyQt5 ui file to python code.
```bash
python -m PyQt5.uic.pyuic -x [FILENAME].ui -o [FILENAME].py
```

# Data Structure
```json
{
    "word" : {
        "google" : [], // google dictionary
        "twin" : [], // twin dictionary
    }
}
```
vgfccc
# TODO

1. 보고 있는 모니터 왼쪽 위로 출력
2. Kindle 옵션 추가한 뒤 Kindle로 보고 있는 경우 처리
3. 단어, 문장에 따른 입력 시나리오
4. Twinword API 분석
https://www.twinword.com/api/
5. 동사 원형 찾는 방법 (Google 사용) vs API
https://github.com/gutfeeling/word_forms
6. json viewer
7. auto capture