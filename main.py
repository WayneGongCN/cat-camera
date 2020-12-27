#!/usr/bin/python3

import sys
import os
import cv2
import time
from datetime import datetime


from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


def main ():
  pwd = sys.path[0]

  # 配置
  CAMERA_ID = 0
  IMAGES_DIR = './images'
  DATE_FORMATE = '%Y/%m/%d %H:%M:%S'
  FILE_DATE_FORMATE = '%Y_%m_%d_%H_%M_%S'


  FROM_ADDRESS = 'xx@xx.com'
  RECEIVER_ADDRESS = ['xx@xx.com']
  ACCOUNT = 'xx@xx.com'
  PASSWORD = 'xx'
  SMTP_URL = 'smtp.xx.com'
  SMTP_PORT = 123


  # 当前时间
  now = datetime.now()
  dateTimeStr = now.strftime(DATE_FORMATE)
  fileDateTimeStr = now.strftime(FILE_DATE_FORMATE)

  mailSubject = 'Cat camera ' + dateTimeStr
  mailContent = '<h2>Cat camera</h2><p>拍摄时间: ' + dateTimeStr + '</p ><img src="cid:image1"/>'

  # 捕获摄像头帧
  cap = cv2.VideoCapture(CAMERA_ID)
  res, frame = cap.read()
  time.sleep(1)
  res, frame = cap.read()
  fileName = 'cat_' + fileDateTimeStr + '.jpg'
  cv2.imwrite(os.path.join(pwd, IMAGES_DIR, fileName), frame)
  cap.release()
  print('拍摄成功')

  # 构造邮件内容
  message = MIMEMultipart('mixed')
  message['From'] = Header("Cat camera<" + FROM_ADDRESS + ">", 'utf-8')
  message['Subject'] = Header(mailSubject, 'utf-8')
  message.attach(MIMEText(mailContent, 'html', 'utf-8'))

  img_file = MIMEImage(open(os.path.join(pwd, IMAGES_DIR, fileName), 'rb').read())
  img_file["Content-Disposition"] = 'attachment; filename="cat.jpg"'
  img_file.add_header('Content-ID', '<image1>')
  message.attach(img_file)

  # 发送邮件
  smtp = SMTP_SSL(SMTP_URL) 
  smtp.login(ACCOUNT, PASSWORD)  
  smtp.sendmail(FROM_ADDRESS, RECEIVER_ADDRESS, message.as_string())
  print("邮件发送成功")


if __name__ == "__main__":
  main()
