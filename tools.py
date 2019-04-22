import execjs
import base64
import requests
import json
import pyscreenshot as ImageGrab

import aircv as ac
import cv2

import time


import os
import sys
from pynput.mouse import Button, Controller
'''
功能说明：
    1.getText 传入一张图片路径，利用百度api识别图片上的文字 及在图片中的位置
    2.getImg  传入name和一个矩形坐标，对矩形所在区域屏幕截图，保存为name图片文件
    3.getImgText 利用百度api识别截图上的文字
    4.matchImg 截图在原图上的坐标
    5.isTrue  判断当前屏幕是否包含指定图像，若包含则返回坐标
    6.clidk 鼠标左键单击
    7.task  顺序点击指定文件夹所有的截图位置
    8。getTextLocation  获得文字在屏幕上的坐标
'''


def getText(url):
    # 调用百度api接口，识别图片中的文字 及在图片中的位置
    with open(url, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        ret = 'data:image/png;base64,' + base64_data.decode()

    ctx = execjs.compile("""
    function url(data){
        return encodeURIComponent(data);
    }
    """)
    res = ctx.call('url', ret)

    data = "type=general_location&image=" + res + "&image_url="

    # print(data)
    with open('data.txt', 'w') as f:
        f.write(data)

    url = 'http://ai.baidu.com/aidemo'
    headers = {
        'Referer': 'http://ai.baidu.com/tech/ocr/general',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': "BAIDUID=A20DA411DE7867CCB53C83ECAFC339DD:FG=1; BIDUPSID=A20DA411DE7867CCB53C83ECAFC339DD; PSTM=1554996762; BDUSS=5welRRemF4TzNKZVp4TllnMlBIRnJNSW4tRFlya3dkMn4wWXBvaG1tMzg0OTVjSVFBQUFBJCQAAAAAAAAAAAEAAAAXu0DTs8i8dNfPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPxWt1z8VrdcMG; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=FmuOJeC62mrNbAQ9lsN5hUrv52OnuL3TH6aoA_aR7vN3BItY15VpEG0PtU8g0Ku-J3-_ogKK0eOTHktF_2uxOjjg8UtVJeC6EG0P3J; H_BDCLCKID_SF=JRCDVCP-tCv_et3Rq4JB2JvH-UIsB63CB2Q-5KL-bRo8oD06etv5yt_J3q5qt6jPy67w3MbdJJjoJq39hUo-KPKjMhLD2UcyJeTxoUJHQCnJhhvGqj3JjP-ebPRiJPQ9QgbWLpQ7tt5W8ncFbT7l5hKpbt-q0x-jLn7ZVD85JK0hMIDr5-t_DTbH-UnLqbKLHmOZ0l8KtJ6K8Roq0jrSKP-kMboH-jLHBKot2IOmWIQHDP-zj5AB26b-Xh0JX6_tQjR4KKJxbUKWeIJo5DckDIumhUJiB5O-Ban7B-bIXKohJh7FM4tW3J0ZyxomtfQxtN4eaDFbJK0bMD0lenOJq6JWqxby26nla6T9aJ5nJDoVqlrPLqLBhbtNjf7PbJKtteOXLl4bQpP-HJ7qBPQCjnKNDP5A-pFDJGcjKl0MLPblbb0xyn_Vy6JDBUnMBMPj5mOnanv23fAKftnOM46JehL3346-35543bRTohFLK-oj-DL4j58-3j; H_PS_PSSID=1443_21127_20880_28774_28723_28833_28584_28603; Hm_lvt_8b973192450250dd85b9011320b455ba=1555936554; Hm_lvt_bfc6c23974fbad0bbfed25f88a973fb0=1555936554; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=5; BDAIUID=5cbdc864ef1641982176820; BDAUID=5cbdc864ef1aa7135309392; Hm_lpvt_bfc6c23974fbad0bbfed25f88a973fb0=1555941478; Hm_lpvt_8b973192450250dd85b9011320b455ba=1555941478; seccode=5ef12a09bd305cbfa027629470e918e7"


    }

    r = requests.post(url, headers=headers, data=data, verify=False)
    words = json.loads(r.text)["data"]['words_result']
    words_res = []
    for w in words:

        x = w['location']['width'] / 2 + w['location']['left']
        y = w['location']['height'] / 2 + w['location']['top']
        location = (x, y)
        words_res.append((w['words'], location))
    res = (words_res, r.text)

    return res


def getImg(name, x1, y1, x2, y2):
    # 截取屏幕指定区域图像
    im = ImageGrab.grab().crop(box=(x1, y1, x2, y2))
    im.save(name)


def getImgText(name, x1, y1, x2, y2):
    # 识别指定区域屏幕截图的文字
    getImg(name, x1, y1, x2, y2)
    return getText(name)


def matchImg(imgsrc, imgobj, confidencevalue=0.5):  # imgsrc=原始图像，imgobj=待查找的图片 图片对比
    imsrc = ac.imread(imgsrc)
    imobj = ac.imread(imgobj)

    # {'confidence': 0.5435812473297119, 'rectangle': ((394, 384), (394, 416), (450, 384), (450, 416)), 'result': (422.0, 400.0)}
    match_result = ac.find_template(imsrc, imobj, confidencevalue)
    if match_result is not None:
        match_result['shape'] = (imsrc.shape[1], imsrc.shape[0])  # 0为高，1为宽

    return match_result


def isTrue(img_url, Precision):
    # 判断是否存在相似照片如果存在，则单击,Precision(精度)
    while True:
        getImg('src.png', 0, 0, 1920, 1080)
        res = matchImg('src.png', img_url, Precision)
        time.sleep(1 / 60)

        if(res != None):
            return res
            break


def click(pos, count):
    # 鼠标左键单击
    mouse = Controller()
    mouse.position = pos
    mouse.click(Button.left, count)


def task(url):
    path = sys.path[0] + '/' + url
    filelist = os.listdir(path)
    for file in filelist:
        res = isTrue(url + file, 0.95)
        click(res["result"], 1)


def getTextLocation(text):
    '''找到文字坐在屏幕的坐标'''
    getImg("src.png", 0, 0, 1366, 768)
    word_res = getText('src.png')[0]
    for word in word_res:
        print(word[0])
        if(str(word[0]) == text):
            return word[1]


def main():
    task('image/')


if __name__ == '__main__':
    main()


'''

POST /aidemo HTTP/1.1
Host: ai.baidu.com
Connection: keep-alive
Content-Length: 185
Origin: http://ai.baidu.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Accept: */*
Referer: http://ai.baidu.com/tech/ocr/general
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: BAIDUID=A20DA411DE7867CCB53C83ECAFC339DD:FG=1; BIDUPSID=A20DA411DE7867CCB53C83ECAFC339DD; PSTM=1554996762; BDUSS=5welRRemF4TzNKZVp4TllnMlBIRnJNSW4tRFlya3dkMn4wWXBvaG1tMzg0OTVjSVFBQUFBJCQAAAAAAAAAAAEAAAAXu0DTs8i8dNfPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPxWt1z8VrdcMG; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=FmuOJeC62mrNbAQ9lsN5hUrv52OnuL3TH6aoA_aR7vN3BItY15VpEG0PtU8g0Ku-J3-_ogKK0eOTHktF_2uxOjjg8UtVJeC6EG0P3J; H_BDCLCKID_SF=JRCDVCP-tCv_et3Rq4JB2JvH-UIsB63CB2Q-5KL-bRo8oD06etv5yt_J3q5qt6jPy67w3MbdJJjoJq39hUo-KPKjMhLD2UcyJeTxoUJHQCnJhhvGqj3JjP-ebPRiJPQ9QgbWLpQ7tt5W8ncFbT7l5hKpbt-q0x-jLn7ZVD85JK0hMIDr5-t_DTbH-UnLqbKLHmOZ0l8KtJ6K8Roq0jrSKP-kMboH-jLHBKot2IOmWIQHDP-zj5AB26b-Xh0JX6_tQjR4KKJxbUKWeIJo5DckDIumhUJiB5O-Ban7B-bIXKohJh7FM4tW3J0ZyxomtfQxtN4eaDFbJK0bMD0lenOJq6JWqxby26nla6T9aJ5nJDoVqlrPLqLBhbtNjf7PbJKtteOXLl4bQpP-HJ7qBPQCjnKNDP5A-pFDJGcjKl0MLPblbb0xyn_Vy6JDBUnMBMPj5mOnanv23fAKftnOM46JehL3346-35543bRTohFLK-oj-DL4j58-3j; delPer=0; PSINO=5; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_PSSID=1443_21127_20880_28774_28723_28833_28584_28603; ZD_ENTRY=baidu; Hm_lvt_8b973192450250dd85b9011320b455ba=1555936554; Hm_lvt_bfc6c23974fbad0bbfed25f88a973fb0=1555936554; BDAIUID=5cbdba71c8ce08475386169; BDAUID=5cbdba71c8d237420885900; Hm_lpvt_8b973192450250dd85b9011320b455ba=1555937906; Hm_lpvt_bfc6c23974fbad0bbfed25f88a973fb0=1555937906; seccode=711cda59389368420b4f33822f61d8cb


image: 
image_url: http://aip.bdstatic.com/portal/dist/1555683028116/ai_images/technology/ocr/general/demo/commontext/2.png
type: commontext
detect_direction: false


POST /aidemo HTTP/1.1
Host: ai.baidu.com
Connection: keep-alive
Content-Length: 197
Origin: http://ai.baidu.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Accept: */*
Referer: http://ai.baidu.com/tech/ocr/general
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: BAIDUID=A20DA411DE7867CCB53C83ECAFC339DD:FG=1; BIDUPSID=A20DA411DE7867CCB53C83ECAFC339DD; PSTM=1554996762; BDUSS=5welRRemF4TzNKZVp4TllnMlBIRnJNSW4tRFlya3dkMn4wWXBvaG1tMzg0OTVjSVFBQUFBJCQAAAAAAAAAAAEAAAAXu0DTs8i8dNfPAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPxWt1z8VrdcMG; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=FmuOJeC62mrNbAQ9lsN5hUrv52OnuL3TH6aoA_aR7vN3BItY15VpEG0PtU8g0Ku-J3-_ogKK0eOTHktF_2uxOjjg8UtVJeC6EG0P3J; H_BDCLCKID_SF=JRCDVCP-tCv_et3Rq4JB2JvH-UIsB63CB2Q-5KL-bRo8oD06etv5yt_J3q5qt6jPy67w3MbdJJjoJq39hUo-KPKjMhLD2UcyJeTxoUJHQCnJhhvGqj3JjP-ebPRiJPQ9QgbWLpQ7tt5W8ncFbT7l5hKpbt-q0x-jLn7ZVD85JK0hMIDr5-t_DTbH-UnLqbKLHmOZ0l8KtJ6K8Roq0jrSKP-kMboH-jLHBKot2IOmWIQHDP-zj5AB26b-Xh0JX6_tQjR4KKJxbUKWeIJo5DckDIumhUJiB5O-Ban7B-bIXKohJh7FM4tW3J0ZyxomtfQxtN4eaDFbJK0bMD0lenOJq6JWqxby26nla6T9aJ5nJDoVqlrPLqLBhbtNjf7PbJKtteOXLl4bQpP-HJ7qBPQCjnKNDP5A-pFDJGcjKl0MLPblbb0xyn_Vy6JDBUnMBMPj5mOnanv23fAKftnOM46JehL3346-35543bRTohFLK-oj-DL4j58-3j; delPer=0; PSINO=5; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; H_PS_PSSID=1443_21127_20880_28774_28723_28833_28584_28603; ZD_ENTRY=baidu; Hm_lvt_8b973192450250dd85b9011320b455ba=1555936554; Hm_lvt_bfc6c23974fbad0bbfed25f88a973fb0=1555936554; BDAIUID=5cbdba71c8ce08475386169; BDAUID=5cbdba71c8d237420885900; Hm_lpvt_8b973192450250dd85b9011320b455ba=1555937906; Hm_lpvt_bfc6c23974fbad0bbfed25f88a973fb0=1555937906; seccode=711cda59389368420b4f33822f61d8cb


image: 
image_url: http://aip.bdstatic.com/portal/dist/1555683028116/ai_images/technology/ocr/general/demo/general_location/3.png
type: general_location
detect_direction: false

'''
