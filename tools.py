import execjs
import base64
import requests
import json
from PIL import ImageGrab

import aircv as ac
import cv2

import time


import os,sys
from pynput.mouse import Button, Controller
'''
功能说明：
    1.getText 传入一张图片路径，利用百度api识别图片上的文字
    2.getImg  传入name和一个矩形坐标，对矩形所在区域屏幕截图，保存为name图片文件
    3.getImgText 利用百度api识别截图上的文字
    4.matchImg 截图在原图上的坐标
    5.isTrue  判断当前屏幕是否包含指定图像，若包含则返回坐标
    6.clidk 鼠标左键单击
    7.task  顺序点击指定文件夹所有的截图位置
'''

def getText(url):
    #调用百度api接口，识别图片中的文字
    with open(url,'rb') as f:
        base64_data = base64.b64encode(f.read())
        ret = 'data:image/png;base64,'+base64_data.decode()

    ctx = execjs.compile("""
    function url(data){
        return encodeURIComponent(data);
    }
    """)
    res = ctx.call('url',ret)

    data = "type=commontext&image="+res+"&image_url="

    #print(data)
    with open('data.txt','w') as f:
        f.write(data)

    url='http://ai.baidu.com/aidemo'
    headers={
        'Referer':'http://ai.baidu.com/tech/ocr/general',
        'X-Requested-With':'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':'BAIDUID=E6E17F57FC7973622103F6A88195060A:FG=1; PSTM=1544416884; BIDUPSID=36949600BAB0D182A554A204095286C5; BDUSS=puNlhzekZHQ2Y1NzQzOTJVc2tQOGd0T0FPVGstTEZuLXFSYWZ2WEhHdVZGRHRjQVFBQUFBJCQAAAAAAAAAAAEAAAAXu0DTs8i8dNfPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJWHE1yVhxNcY0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; docVersion=0; BDSFRCVID=zY0OJeC62mw4lJ39-5UxUObCj6n-KPOTH6aoneJZuED9eaSunIbkEG0PDU8g0KA-S2EqogKK0eOTHkCF_2uxOjjg8UtVJeC6EG0P3J; H_BDCLCKID_SF=tRAOoC8ytDvjDb7GbKTD-tFO5eT22-us-T7m2hcH0KLKMU3Ih4j_eDr03JnPW-jm2JvLo4cdaMb1MRjveJC5MpJB3tObtfQZ-Tve0q5TtUJ88DnTDMRhqqJXqqjyKMnitIT9-pno0hQrh459XP68bTkA5bjZKxtq3mkjbIOFfDD5bKDRjjK3-tcH-xQ0KnLXKKOLV-cwtp7keq8CD4cbj-ApDNuLtlQOQmOa5bFKaj6vVh72y5jHhPC8yR6t0x085C6gLRrYKJvpsIJMQh_WbT8ULecgJfQDaKviaKJHBMb1jpODBT5h2M4qMxtOLR3pWDTm_q5TtUt5OCcnK4-Xj6O0DGQP; Hm_lvt_8b973192450250dd85b9011320b455ba=1546587702,1546588134,1546588590,1546655396; delPer=0; PSINO=5; H_PS_PSSID=1439_21088_20880_28206_28132_27245_27508; Hm_lpvt_8b973192450250dd85b9011320b455ba=1546668909; seccode=a1b3fcb145313457c2744a287a7a8120'
    }

    r = requests.post(url,headers=headers,data = data,verify=False)
    

    words = json.loads(r.text)["data"]["words_result"]
    words_res = []
    for w in words:
        words_res.append(w["words"])
    res = (words_res,r.text)
    return res
    
def getImg(name,x1,y1,x2,y2):
    #截取屏幕指定区域图像
    im = ImageGrab.grab().crop(box=(x1,y1,x2,y2))
    im.save(name)    

def getImgText(name,x1,y1,x2,y2):
    #识别指定区域屏幕截图的文字
    getImg(name,x1,y1,x2,y2)
    return getText(name)
  
def matchImg(imgsrc,imgobj,confidencevalue=0.5):#imgsrc=原始图像，imgobj=待查找的图片
    imsrc = ac.imread(imgsrc)
    imobj = ac.imread(imgobj)
 
    match_result = ac.find_template(imsrc,imobj,confidencevalue)  # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)), 'result': (422.0, 400.0)}
    if match_result is not None:
        match_result['shape']=(imsrc.shape[1],imsrc.shape[0])#0为高，1为宽

    return match_result
def isTrue(img_url,Precision ):
    #判断是否存在相似照片如果存在，则单击,Precision(精度) 
    while True:
        getImg('src.png',0,0,1920,1080);
        res = matchImg('src.png',img_url,Precision);
        time.sleep(1/60)
        if(res!=None):
            return res
            break
def click(pos,count):
    #鼠标左键单击
    mouse = Controller()
    mouse.position = pos
    mouse.click(Button.left,count)

def task(url):
    path=sys.path[0]+'\\'+url
    filelist = os.listdir(path)
    for file in filelist:
        res = isTrue(url+file,0.95)
        click(res["result"],1)

def main():
    task('image/')
  
if __name__ == '__main__':
    main()
