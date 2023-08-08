from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from config.errorCode import *


class kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()  # 부모(QAxWidget) 생성자를 실행
        print("kiwoom() class start==>")

        # QEventLoop() 이벤트 루프 ##
        self.event_loop = None
        ###############################
        self.account_num = None  # 계좌번호
        self.get_ocx_instance()  # 키움API 프로그램 제어
        self.event_connect()     # 연결 요청
        self.signal_login_comconnect() #로그인이 완료되면 이벤트 루프

        self.get_account_info()  # 계좌정보 요청
        self.detail_account_info() # 예수금 정보

    def get_ocx_instance(self):  # make_kiwoom_instance
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")  # setControl 함수는 QAxBase -> QAxWidget로 상속받음.
        # 응용프로그램 제어 경로 설정 - 레지스트리

    def event_connect(self):  # 이벤트 실행
        self.OnEventConnect.connect(self.login_slots) #연결 이벤트
        # Error : AttributeError: 'kiwoom' object has no attribute 'OnEventConnect'
        # 해결책 : KOA Studio에서 Open API가 정상적으로 접속된다면
        # 키움증권의 OPEN API가 파이썬 32bit와 호환되기 때문에, 파이썬 32bit을 사용하지 않아서 발생=> 가상환경 새로 설정
        self.OnReceiveTrData.connect(self.trdata_slot) #요청 이벤트

    def login_slots(self, err_code):  # 연결 결과(데이터) 받음
        # print(err_code)
        print(error_code_list(self,err_code))
        self.event_loop.exit()  # 로그인 결과를 받으면 이벤트 루프를 종료함.

    def signal_login_comconnect(self):
        self.dynamicCall("CommConnect()")
        self.event_loop = QEventLoop()
        self.event_loop.exec_()  # 로그인 완료 될 때까지 프로그램 진행을 막음.



    def get_account_info(self):
        account_list = self.dynamicCall("GetLoginInfo(string)","ACCNO")  #USER_ID  ACCNO
        self.account_num = account_list.split(';')[0]
        print("나의 보유 계좌번호 %s " % self.account_num)
    def detail_account_info(self):
        print("예수금 가져오기")
        self.dynamicCall("SetInputValue(String,String)","계좌번호",self.account_num)
        self.dynamicCall("SetInputValue(String,String)", "비밀번호", "0000")
        self.dynamicCall("SetInputValue(String,String)", "비밀번호입력매체구분", "00")
        self.dynamicCall("SetInputValue(String,String)", "조회구분", "2")
        self.dynamicCall("CommRqData(String, String, int, String)","예수금상세현황요청","opw00001","0","2000")
    def trdata_slot(self,sScrNo,sRQName,sTrCode,sRecordName, sPrevNext):
        '''
        :param sScrNo:
        :param sRQName:
        :param sTrCode:
        :param sRecordName:
        :param sPrevNext:
        :return:
        '''
        # [OnReceiveTrData() 이벤트] 화면번호, 사용자, TR이름, 레코드, 연속조회 0: 연속
        if sRQName == "예수금상세현황요청":
            deposit = self.dynamicCall("GetCommData(String,String,int, String)", sTrCode, sRQName, 0, "예수금")
            print("예수금 %s" % deposit)


#
# [OPT10081: 주식일봉차트조회요청예시]
#
# OnReceiveTrData(...)
# {
# if (strRQName == _T("주식일봉차트"))
#     {
#         int
#     nCnt = OpenAPI.GetRepeatCnt(sTrcode, strRQName);
#     for (int nIdx = 0; nIdx < nCnt; nIdx++)
#     {
#         strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T("거래량"));   strData.Trim(); // nIdx번째의 거래량 데이터 구함
#     strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T("시가"));   strData.Trim();
#     strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T("고가"));   strData.Trim();
#     strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T("저가"));   strData.Trim();
#     strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T("현재가"));   strData.Trim();
#     }
#     }
# }




