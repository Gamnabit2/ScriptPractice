from tkinter import *
from tkinter import font
from io import BytesIO
import urllib
import urllib.request
from PIL import Image, ImageTk
from http.client import HTTPSConnection
from xml.dom.minidom import parse, parseString
from datetime import datetime
import webbrowser

# Tk_DayMovie
DayMovieDoc = None
MovieChart = None
ChartFlag = True
NextList = None
PrevList = None
FrontText = ["순위", "제목", "점유율", "누적관객수"]
SecondText = []
TitleText = []
ColorText = ["red", "green", "yellow", "pink", "orange"]

# 익진
RelYearFrom = 0
RelYearTo = 0
RelYearExist = False
firstRun = True
clickedBtn = False
wrongInput = False
titleStrLabel = None
subtitleStrLabel = None
directorLabel = None
actorLabel = None
userRatingLabel = None

def LoadXML_DayMovie(Day):
    global firstRun
    firstRun = False
    server = "www.kobis.or.kr"
    key = "430156241533f1d058c603178cc3ca0e"
    targetDt = Day

    conn = HTTPSConnection(server)
    conn.request("GET", "/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml?key=" + \
                 key + "&targetDt=" + targetDt)

    req = conn.getresponse()
    if int(req.status) == 200:
        todaydom = parseString(req.read())
        return todaydom
    else:
        return None

def getToday(): # 검색에 용이하게 현재 날짜 가져옴.
    now = datetime.now()

    if now.month / 10 <= 1:
        zeroMonth = '0' + str(now.month)
    else:
        zeroMonth = str(now.month)

    if now.day / 10 <= 1:
        zeroDay = '0' + str(now.day-1)
    else:
        zeroDay = str(now.day-1)

    today = str(now.year) + str(zeroMonth) + str(zeroDay)
    return today

def Image_DayMovie(TitleText):
    global DayMovieDoc
    global MovieChart
    global ChartFlag

    ImgURL = []
    image = []

    for i in range(0, 5):
        if ChartFlag == True:
            server = "openapi.naver.com"
            client_id = "iEV22cE2b1ZJnyGDYXtc"
            client_secret = "xJB_PnOFmw"
            text = urllib.parse.quote(TitleText[i])

            conn = HTTPSConnection(server)
            conn.request("GET", "/v1/search/movie.xml?query=" + text + "&display=10&start=1", None,
                         {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret})

            req = conn.getresponse()
            if int(req.status) == 200:
                ImageDoc = parseString(req.read())
                ImgURL.append(getJpgURL(ImageDoc, TitleText[i]))

        else:
            server = "openapi.naver.com"
            client_id = "iEV22cE2b1ZJnyGDYXtc"
            client_secret = "xJB_PnOFmw"
            text = urllib.parse.quote(TitleText[i+5])

            conn = HTTPSConnection(server)
            conn.request("GET", "/v1/search/movie.xml?query=" + text + "&display=10&start=1", None,
                         {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret})

            req = conn.getresponse()
            if int(req.status) == 200:
                ImageDoc = parseString(req.read())
                ImgURL.append(getJpgURL(ImageDoc, TitleText[i+5]))

    for i in range(0, len(ImgURL)):
        #print(ImgURL[i])
        if ImgURL[i] != None:
            with urllib.request.urlopen(ImgURL[i]) as u:
                raw_data = u.read()
            tmp = Image.open(BytesIO(raw_data))
            tmp = tmp.resize((160, 208), Image.ANTIALIAS)
            tmp = ImageTk.PhotoImage(tmp)
            image.append(tmp)

            JPG = Label(MovieChart, image=image[i], bg="Black")
            JPG.image = image[i]
            JPG.place(x=55 + (180 * i), y=100)
        else:
            image.append(None)

    #MovieChart.mainloop()

def getJpgURL(ImageDoc, title):
    itemList = ImageDoc.getElementsByTagName('item')

    for item in itemList:
        for attr in item.childNodes:
            if attr.nodeName == "title":
                if attr.firstChild.nodeValue.find(title):
                    pass
                else:
                    continue
            if attr.nodeName == "image":
                if attr.hasChildNodes():
                    return attr.firstChild.nodeValue
                    break
            #if attr.nodeName == "userRating":
            #    if attr.hasChildNodes():
            #        return attr.firstChild.nodeValue
            #        break




def Tk_DayMovie():
    global MovieChart
    global DayMovieDoc
    global insertedDate # 삽입되는 날짜
    global clickedBtn   # 검색 버튼 눌렀는지?

    MovieChart = Tk()

    MovieChart.title("MovieChart")
    MovieChart.geometry("1000x600+500+100")

    if firstRun is True:
        insertedDate = getToday()
    DayMovieDoc = LoadXML_DayMovie(insertedDate)
    TitleText = Label_DayMovie(['movieNm', 'rank', 'salesShare', 'audiAcc'])
    Image_DayMovie(TitleText)
    clickedBtn = False

    MovieChart.mainloop()



def CGVLogoButton():
    webbrowser.open_new('http://www.cgv.co.kr/')


def MEGABOXLogoButton():
    webbrowser.open_new('http://www.megabox.co.kr')

def LOTTELogoButton():
    webbrowser.open_new('http://www.lottecinema.co.kr')

def Label_DayMovie(SearchList):
    global DayMovieDoc
    global FrontText
    global SecondText
    global TitleText
    global ColorText
    global ChartFlag
    global NextList

    dailBoxOfficeList = DayMovieDoc.getElementsByTagName('dailyBoxOffice')

    string = ''
    TitleText = []
    count = 0

    ########################################
    # UI
    ########################################
    # 박스오피스 리스트 변경 버튼

    #*****NextList = Button(MovieChart, text=">", command=NextChart)
    #*****NextList.place(x=965, y=200)
    #*****NextList.config(width=2)

    # 영화 검색 버튼
   #***** searchBtn = Button(MovieChart, text="영화 검색", command=Tk_SearchMovie, font='나눔고딕 20')
   #***** searchBtn.config(width=35)
   #***** searchBtn.place(x=200, y=520)
    #########################################

    for movie in dailBoxOfficeList:
        for attr in movie.childNodes:
            for object in SearchList:
                if attr.nodeName == object:
                    if attr.hasChildNodes():
                        SecondText.append(attr.firstChild.nodeValue)
        for i in range(0, 4):
            if i == 1:
                TitleText.append(SecondText[i])
            string += FrontText[i]
            string += " : "
            string += SecondText[i]
            if i != 3:
                string += "\n"

        if count < 5:
            label = Label(MovieChart, text=string, bg=ColorText[count % 5], fg="black", font="나눔고딕 8", width="22")
            label.place(x=55 + (180 * count), y=330)

        string = ''
        SecondText = []
        count += 1

    ########################################
    # 20180527기준 박스오피스 & 검색 버튼
    ########################################
    global boxSubEntry, insertedDate, wrongInput
    # boxSubEntry = Entry(master, text= + " 기준 박스오피스", font='나눔고딕 16', width=8)
    boxSubEntry = Entry(MovieChart, font='나눔고딕 20', width=11)
    boxSubEntry.place(x=265, y=10)
    if firstRun is True:
        boxSubEntry.insert(0, getToday())
    elif firstRun is not True and wrongInput is not True:
        boxSubEntry.insert(0, insertedDate)


    boxSubLa = Label(MovieChart, text="기준 박스오피스", font='나눔고딕 20')
    boxSubLa.place(x=450, y=10)
   #***** dateBtn = Button(MovieChart, text="검색", width=1, font='나눔고딕 16', command=changeDate)
   #***** dateBtn.place(x=650, y=8)
   #*****dateBtn.config(width=10)
    ########################################

    TheaterLa = Label(MovieChart, text="────────────────────── 영화관 바로가기 ──────────────────────", font='나눔고딕 15', fg='gray')
    TheaterLa.place(x=0, y=400)


    MEGABOXImage = Image.open("MegaBox.JPG")
    MEGABOXPhoto = ImageTk.PhotoImage(MEGABOXImage)
    MEGABOX = Button(MovieChart, image=MEGABOXPhoto, command=MEGABOXLogoButton)
    MEGABOX.image = MEGABOXPhoto
    MEGABOX.place(x=100, y=430)

    CGVImage = Image.open("CGV.PNG")
    CGVPhoto = ImageTk.PhotoImage(CGVImage)
    CGV = Button(MovieChart, image=CGVPhoto, command=CGVLogoButton)
    CGV.image = CGVPhoto
    CGV.place(x=420, y=430)

    LOTTEImage = Image.open("Lottecinema.PNG")
    LOTTEPhoto = ImageTk.PhotoImage(LOTTEImage)
    LOTTE = Button(MovieChart, image=LOTTEPhoto, command=LOTTELogoButton)
    LOTTE.image = LOTTEPhoto
    LOTTE.place(x=630, y=430)



    #path = r'E:/[Study]/2018/1학기/과제/Script_Term_Project/CGV_logo.jpg'

    # 영화 예매 사이트 링크 버튼
    #path=r'E:/[Study]/2018/1학기/과제/Script_Term_Project/롯데시네마.PNG'
    #image = Image.open(path)
    #photo = ImageTk.PhotoImage(image)

    #CGV = Button(MovieChart, image=photo, command=CGVLogoButton)
    #CGV.place(x=200, y = 50)
    #CGV.config(width=500, height=200)
    return TitleText


#InitTopText()
Tk_DayMovie()
