import RPi.GPIO as GPIO
import time
import cv2
import requests


PIN = 18
LED = 23 # 追加
BUZZER = 19

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)
GPIO.setup(LED, GPIO.OUT, initial=GPIO.LOW)# 追加
GPIO.setup(BUZZER, GPIO.OUT)

try:
    print ('-----Start-----')
    n = 1
    i = 1
    while True:
        if GPIO.input(PIN) == GPIO.HIGH:
            print("{}".format(n) + "回目検知")
            
            #ブザーとLEDをつける
            GPIO.output(BUZZER, GPIO.HIGH)
            GPIO.output(LED, 1)
            
            # 動画ストリームを取得するためのオブジェクト定義
            capture = cv2.VideoCapture(0)
            # 動画ストリームから最新のフレームを取得する
            rtn, frame = capture.read()
            # ファイルに出力する
            if( rtn == True ):
                cv2.imwrite( "capture" + str(i) + ".jpg", frame )
            # 終了処理（ストリームを解放
            capture.release()
            cv2.destroyAllWindows()
            
            #LINEに送る
            url = "https://notify-api.line.me/api/notify"
            access_token = '720a4xtKRutpHEHCEoanU8n1Pj4VY8dQxptJNuCdX1J' #アクセストークンを入力
            #LDmfYOMryP2ocrTUF7dzGq89VjMjVeuCetyilXce8ub
            headers = {'Authorization': 'Bearer ' + access_token}
            message = '帰宅しました' #送るメッセージを入力 
            image = "capture" + str(i) + ".jpg"  # png or jpg を指定
            payload = {'message': message}
            files = {'imageFile': open(image, 'rb')}
            r = requests.post(url, headers=headers, params=payload, files=files,)
                        
            #time.sleep(1)
            GPIO.output(BUZZER, GPIO.LOW)
            GPIO.output(LED, 0)
            time.sleep(1)
            n += 1
            i += 1
            
            """
            # 動画ストリームを取得するためのオブジェクト定義
            capture = cv2.VideoCapture(0)
            # 動画ストリームから最新のフレームを取得する
            rtn, frame = capture.read()
            # ファイルに出力する
            if( rtn == True ):
                cv2.imwrite( "capture" + str(i) + ".jpg", frame )
            # 終了処理（ストリームを解放
            i += 1
            capture.release()
            cv2.destroyAllWindows()
            """
        else:
            print(GPIO.input(PIN))
            time.sleep(2)
except KeyboardInterrupt:
    print("Cancel")
finally:
    GPIO.cleanup()
    print("-----end-----")


