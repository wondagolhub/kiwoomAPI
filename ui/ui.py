from kiwoom.kiwoom import kiwoom
from PyQt5.QtWidgets import *
import sys


class UI_class():
    def __init__(self):
        print("유저 인터페이스 및 이벤트 루프 구간입니다.")
        self.app = QApplication(sys.argv)
        self.kiwoom = kiwoom()  # 인스턴화(변수할당) 시키지 않으면 키움로그인시 핸들값이 없습니다. 에러 발생

        self.app.exec()  # 이벤트 루프 실행. 프로그램이 종료되지 않게 만드는것이 핵심./.종료 명령어를 입력해주지 않으면 종료 되지 않음.
