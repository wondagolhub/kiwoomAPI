from ui.ui import UI_class
from config.errorCode import *

class Main():
    def __init__(self):
        print("Main()클래스 실행구간입니다.")
        # 함수테스트 print(error_code_list(self,0))
        UI_class()


if __name__ == "__main__":   ### 처음 실행 부분(Main이 실행용 파일이라는 의미)  #print(__name__)
    Main()