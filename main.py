# pyinstaller.exe -F -w --onefile --icon=icon.ico main.py
# dos창 없이, 한 파일로 실행파일을 만드는 커맨드

import tkinter as tk # 애플리케이션 gui
from tkinter import messagebox # tk 경고박스 등\
import time # time.sleep() 등에 사용
import threading # 스레드
import sys # 애플리케이션 종료 등
import urllib.request # 웹 정보에 접근, 처리 등
import urllib # 웹 정보에 접근, 처리 등
import webbrowser
from bs4 import BeautifulSoup
LOGTEXT = "" # 삭제 예정 변수. 현재 미사용
ITEM_INPUT = ""
STATUS = "JP"

# 샘플 스레드입니다. 검색버튼을 클릭 시, 샘플 클래스를 호출합니다.
class NewThread(threading.Thread):
    def __init__(self, _window):
        threading.Thread.__init__(self)
        self.win = _window
    def run(self):
        instance = myClass(self.win)

# 샘플 클래스입니다. 새 샘플 스레드에서 실행될 수 있도록 해 두었습니다.
class myClass():
    def __init__(self, _window):
        self.win = _window 

        self.ITEM_OUTPUT_K = ""
        self.ITEM_OUTPUT_J = ""
        self.ITEM_OUTPUT_E = ""

        # 입력 텍스트 읽기
        if (STATUS=="JP"):
            ITEM_INPUT = self.win.entry2.get()
        elif (STATUS=="EN"):
            ITEM_INPUT = self.win.entry3.get()
        elif (STATUS=="KR"):
            ITEM_INPUT = self.win.entry1.get()
        
        self.parsed_input = urllib.parse.quote(ITEM_INPUT, safe='')
        self.win.log.set("검색을 시작합니다")
        print("ITEM_INPUT : ["+ITEM_INPUT+"]")
        print("parsed_input : ["+self.parsed_input+"]")

        # 입력 언어별로 검색
        if (STATUS=="JP"):
            self.res = urllib.request.urlopen("https://jp.finalfantasyxiv.com/lodestone/playguide/db/item/?q="+self.parsed_input).read()
            self.res2 = urllib.request.urlopen("http://ff14.inven.co.kr/dataninfo/item/?itemname="+self.parsed_input).read()
        elif (STATUS=="EN"):
            self.res = urllib.request.urlopen("https://na.finalfantasyxiv.com/lodestone/playguide/db/item/?q="+self.parsed_input).read()
            self.res2 = urllib.request.urlopen("http://ff14.inven.co.kr/dataninfo/item/?itemname="+self.parsed_input.replace("%27","")).read()
        elif (STATUS=="KR"):
            self.res = urllib.request.urlopen("http://ff14.inven.co.kr/dataninfo/item/?itemname="+self.parsed_input.replace("%27","")).read()
        
        self.soup = BeautifulSoup(self.res,'html.parser')
        if(STATUS=="JP" or STATUS=="EN"):
            self.soup2 = BeautifulSoup(self.res2,'html.parser')
        
        # 검색 페이지에서 같은 이름의 아이템을 찾는다
        self.item_url = ""
        self.item_url2 = ""
        # 입력언어가 JP, EN의 경우
        if (STATUS=="JP" or STATUS=="EN"):
            for tmp_url in self.soup.find_all('a',class_='db-table__txt--detail_link'):
                if(tmp_url.get_text()==ITEM_INPUT):
                    self.win.log.set("에오르제아 데이터베이스 검색 완료")
                    self.item_url = tmp_url.get('href')
                    break
                else:
                    pass
            self.items = self.soup2.find_all('a',class_='itemgrade1f') + self.soup2.find_all('a',class_='itemgrade2f') + self.soup2.find_all('a',class_='itemgrade3f')
            for tmp_url in self.items:
                self.win.log.set("인벤을 검색 중 입니다")
                if(len(self.items)==1):
                    self.win.log.set("인벤 검색 완료, 번역명을 찾습니다")
                    self.item_url2 = "find!"
                    self.ITEM_OUTPUT_K = tmp_url.get_text()
                    break
                self.win.log.set(str(len(self.items))+"개의 검색결과 중\n일치하는 것을 찾습니다.")
                self.res_tmp = urllib.request.urlopen("http://ff14.inven.co.kr/dataninfo/item/"+tmp_url.get('href')).read()
                self.soup_tmp = BeautifulSoup(self.res_tmp,'html.parser')
                self.ITEM_OUTPUTS_tmp = []
                for tmp_out in self.soup_tmp.find_all('td',class_='left'):
                    self.ITEM_OUTPUTS_tmp.append(tmp_out.get_text())
                self.ITEM_OUTPUT_J_tmp = self.ITEM_OUTPUTS_tmp[0].strip()
                self.ITEM_OUTPUT_E_tmp = self.ITEM_OUTPUTS_tmp[1].strip()
                if( ( STATUS=="JP" and self.ITEM_OUTPUT_J_tmp==ITEM_INPUT ) or ( STATUS=="EN" and self.ITEM_OUTPUT_E_tmp==ITEM_INPUT )):
                    self.win.log.set("검색 완료, 번역명을 찾습니다")
                    self.item_url2 = "find!"
                    self.ITEM_OUTPUT_K = tmp_url.get_text()
                    break
                else:
                    pass
        # 입력언어가 KR인 경우
        else :
            self.items = self.soup.find_all('a',class_='itemgrade1f') + self.soup.find_all('a',class_='itemgrade2f') + self.soup.find_all('a',class_='itemgrade3f')
            for tmp_url in self.items:
                print(tmp_url.get_text())
                if(tmp_url.get_text()==ITEM_INPUT):
                    self.win.log.set("검색 완료, 번역명을 찾습니다")
                    self.item_url = tmp_url.get('href')
                    break
                else:
                    pass

        if(self.item_url2 == "" and not(self.item_url == "")):
            self.ITEM_OUTPUT_K = "No Data in Inven"
        if(self.item_url == ""):
            self.win.log.set("검색결과가 없습니다")
            return
        
        # 해당 아이템의 링크로
        if(STATUS=="JP"):
            self.res = urllib.request.urlopen("https://na.finalfantasyxiv.com/"+self.item_url).read()
        elif(STATUS=="EN"):
            self.res = urllib.request.urlopen("https://jp.finalfantasyxiv.com/"+self.item_url).read()
        elif(STATUS=="KR") :
            self.res = urllib.request.urlopen("http://ff14.inven.co.kr/dataninfo/item/"+self.item_url).read()

        self.soup = BeautifulSoup(self.res,'html.parser')

        if(STATUS=="JP"):
            self.ITEM_OUTPUT_E = self.soup.find('h2',class_='db-view__item__text__name').get_text().strip()
            if(self.ITEM_OUTPUT_E[-1]==""):
                self.ITEM_OUTPUT_E = self.ITEM_OUTPUT_E[:-1].strip()
            
        elif(STATUS=="EN"):
            self.ITEM_OUTPUT_J = self.soup.find('h2',class_='db-view__item__text__name').get_text().strip()
            if(self.ITEM_OUTPUT_J[-1]==""):
                self.ITEM_OUTPUT_J = self.ITEM_OUTPUT_J[:-1].strip()
        else :
            self.ITEM_OUTPUTS = []
            for tmp_out in self.soup.find_all('td',class_='left'):
                self.ITEM_OUTPUTS.append(tmp_out.get_text())
            self.ITEM_OUTPUT_J = self.ITEM_OUTPUTS[0].strip()
            self.ITEM_OUTPUT_E = self.ITEM_OUTPUTS[1].strip()
        

        if(STATUS=="JP"):
            self.win.entry1.delete(0,'end')
            self.win.entry1.insert(0, self.ITEM_OUTPUT_K)
            self.win.entry3.delete(0,'end')
            self.win.entry3.insert(0, self.ITEM_OUTPUT_E)
        elif(STATUS=="EN"):
            self.win.entry1.delete(0,'end')
            self.win.entry1.insert(0, self.ITEM_OUTPUT_K)
            self.win.entry2.delete(0,'end')
            self.win.entry2.insert(0, self.ITEM_OUTPUT_J)
        else:
            self.win.entry2.delete(0,'end')
            self.win.entry2.insert(0, self.ITEM_OUTPUT_J)
            self.win.entry3.delete(0,'end')
            self.win.entry3.insert(0, self.ITEM_OUTPUT_E)
        self.win.log.set("완료되었습니다")


# 새 윈도우를 만들고, 위젯 및 기능을 넣습니다.
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        

        # 라벨, 그리드 배치를 하였습니다.
        self.lb1 = tk.Label(window, text="KO", width=5)
        self.lb1.grid(row=0,column=0)
        self.lb2 = tk.Label(window, text="JP")
        self.lb2.grid(row=1,column=0)
        self.lb3 = tk.Label(window, text="EN")
        self.lb3.grid(row=2,column=0)

        # 업데이트용 변수와 라벨
        self.log = tk.StringVar()
        self.log.set("Elemental Aegis Error FC")
        self.lb3 = tk.Label(window, textvariable=self.log)
        self.lb3.grid(row=3,column=0,columnspan=3)

        # 입력 가능한 텍스트칸 위젯 Entry
        self.str1=tk.StringVar()
        self.str2=tk.StringVar()
        self.str3=tk.StringVar()

        self.entry1 = tk.Entry(window, textvariable=self.str1, width=25)
        self.entry1.bind('<Return>',self.btn1_function)
        self.entry1.grid(row=0,column=1,columnspan=2)

        self.entry2 = tk.Entry(window, textvariable=self.str2, width=25)
        self.entry2.bind('<Return>',self.btn2_function)
        self.entry2.grid(row=1,column=1,columnspan=2)

        self.entry3 = tk.Entry(window, textvariable=self.str3, width=25)
        self.entry3.bind('<Return>',self.btn3_function)
        self.entry3.grid(row=2,column=1,columnspan=2)

        # 버튼1
        self.btn1 = tk.Button(window, text="-> JP EN", width=10, height=1)
        self.btn1.bind('<Button-1>',self.btn1_function)
        self.btn1.grid(row=0,column=3,rowspan=1)
        # 버튼2
        self.btn2 = tk.Button(window, text="-> KR EN", width=10, height=1)
        self.btn2.bind('<Button-1>',self.btn2_function)
        self.btn2.grid(row=1,column=3,rowspan=1)
        # 버튼3
        self.btn3 = tk.Button(window, text="-> KR JP", width=10, height=1)
        self.btn3.bind('<Button-1>',self.btn3_function)
        self.btn3.grid(row=2,column=3,rowspan=1)

        # 종료 버튼
        self.quit_btn = tk.Button(window, text="QUIT", fg="red", command=self.quit_btn_function, width=10, height=2)
        self.quit_btn.grid(row=3,column=3,rowspan=1)

    # 버튼을 클릭 시 실행합니다
    def btn1_function(self, event):
        global STATUS
        STATUS = "KR"
        NewThread(self).start()

    def btn2_function(self, event):
        global STATUS
        STATUS = "JP"
        NewThread(self).start()

    def btn3_function(self, event):
        global STATUS
        STATUS = "EN"
        NewThread(self).start()

    # 버튼 quit를 클릭 시 실행합니다
    def quit_btn_function(self):
        sys.exit()


window = tk.Tk()

# 타이틀, 파일아이콘, 윈도우상단아이콘, 윈도우크기, 크기재설정여부
window.title("Item Translator")
# window.iconbitmap(default='icon.ico')
# window.tk.call('wm', 'iconphoto', window._w, tk.PhotoImage(file='./icon.png'))
window.geometry("305x125+1200+200")
window.resizable(False,False)

# 앱 시작
app = Application(master=window)
app.mainloop()