from aip import AipFace
from picamera import PiCamera
import urllib.request
import RPi.GPIO as GPIO
import base64
import time
import cv2

GPIO.setmode(GPIO.BCM)
#设置以BCM编号为18的GPIO口为输出模式
GPIO.setup(18,GPIO.OUT)

#API账号信息
APP_ID = '25189630'
API_KEY = 'SYNfrkWeohQE0uebYu5ESpGO'
SECRET_KEY ='nsYLfVtkMUqhDXaUXoH10OGm1VgcI9zd'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)#创建一个客户端用以访问百度云
#图像编码方式
IMAGE_TYPE='BASE64'
camera = PiCamera()#定义一个摄像头对象
#用户组
GROUP = '01'

# def generate():
#     face_cascade = cv2.CascadeClassifier('/usr/local/lib/python3.7/dist-packages/cv2/data/haarcascade_frontalface_default.xml')
#     #打开摄像头
#     camera = cv2.VideoCapture(0)
#     forword_count = 0
#     while (forword_count <= 1):
#         ret, frame = camera.read()
#         faces = face_cascade.detectMultiScale(frame, 1.3, 5)
#         for (x, y, w, h) in faces:
#             cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
# 
# #             f = cv2.resize(gray[y:y + h, x:x + w], (400, 400))
#             cv2.imwrite('faceimage.jpg')
#         cv2.imshow("camera", frame)


#照相函数
def getimage():
    camera.resolution = (1024,768)#摄像界面为1024*768
    camera.start_preview(alpha=200)#开始摄像
    camera.brightness = 60
    camera.exposure_mode = 'auto'
    time.sleep(2)
    camera.capture('faceimage.jpg')#拍照并保存
    time.sleep(2)
    camera.stop_preview()
#对图片的格式进行转换
def transimage():
    f = open('faceimage.jpg','rb')
    img = base64.b64encode(f.read())
    return img
#上传到百度api进行人脸检测
def go_api(image):
    result = client.search(str(image, 'utf-8'), IMAGE_TYPE, GROUP);#在百度云人脸库中寻找有没有匹配的人脸
    print(result)
    if result['error_msg'] == 'SUCCESS':#如果返回指令为成功
        name = result['result']['user_list'][0]['user_id']#获取名字
        score = result['result']['user_list'][0]['score']#获取相似度
        print(score)
        if score > 80:
            if name == '02':
                print("欢迎%s !" % name)
                time.sleep(1)
            if name == 'liang':
                print("欢迎%s !" % name)
                time.sleep(3)
                
        else:
            print("对不起，我不认识你！")
            name = 'Unknow'
            return 0
        curren_time = time.asctime(time.localtime(time.time()))#获取当前时间
 
        #将人员出入的记录保存到Log.txt中
        f = open('Log.txt','a')
        f.write("Person: " + name + "     " + "Time:" + str(curren_time)+'\n')
        f.close()
        return 1
    if result['error_msg'] == 'pic not has face':
        print('检测不到人脸')
        time.sleep(2)
        return -1
    else:
        print(result['error_code']+' ' + result['error_code'])
        return 0
#主函数
if __name__ == '__main__':
    while True:
        
        print('请面向摄像头')

        if True:
            getimage()#拍照
            img = transimage()  #转换照片格式
            res = go_api(img)   #将转换了格式的图片上传到百度云
            if(res == 1):   #是人脸库中的人
                print("欢迎回家，门已打开")
            elif(res == -1):
                print("我没有看见你,我要关门了")
                time.sleep(2)    
            else:
                print("关门")
            time.sleep(2)
            print('请稍等')
            time.sleep(2)
