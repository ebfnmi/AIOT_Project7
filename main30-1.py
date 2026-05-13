import paho.mqtt.client as mqtt # MQTT 통신 기능을 사용하기 위해 paho 라이브러리를 불러옵니다.
import time # 전송 간격을 조절하는 등 시간 관련 기능을 사용하기 위해 불러옵니다.
from gpiozero import LED # 라즈베리 파이의 GPIO 핀에 연결된 LED를 제어하기 위해 불러옵니다.
import threading # 메시지 수신 대기와 데이터 전송을 동시에 처리하기 위해 스레드 기능을 불러옵니다.

greenLed = LED(16) # 16번 GPIO 핀에 연결된 초록색 LED 객체를 생성합니다.
blueLed = LED(20) # 20번 GPIO 핀에 연결된 파란색 LED 객체를 생성합니다.
redLed = LED(21) # 21번 GPIO 핀에 연결된 빨간색 LED 객체를 생성합니다.

def on_message(client, userdata, msg): # 브로커로부터 메시지가 도착했을 때 실행될 콜백 함수를 정의합니다.
    print(msg.topic+" "+str(msg.payload)) # 받은 메시지의 주제와 데이터(Payload)를 터미널에 출력합니다.
    message = msg.payload.decode() # 수신된 바이트 형태의 데이터를 문자열로 변환합니다.
    print(message) # 변환된 문자열 메시지를 화면에 출력하여 확인합니다.
    if message == "green_on": # 수신 메시지가 "green_on"이면 초록색 LED를 점등합니다.
        greenLed.on() # 초록색 LED에 전원을 공급합니다.
    elif message == "green_off": # 수신 메시지가 "green_off"이면 초록색 LED를 소등합니다.
        greenLed.off() # 초록색 LED의 전원을 차단합니다.
    elif message == "blue_on": # 수신 메시지가 "blue_on"이면 파란색 LED를 점등합니다.
        blueLed.on() # 파란색 LED에 전원을 공급합니다.
    elif message == "blue_off": # 수신 메시지가 "blue_off"이면 파란색 LED를 소등합니다.
        blueLed.off() # 파란색 LED의 전원을 차단합니다.
    elif message == "red_on": # 수신 메시지가 "red_on"이면 빨간색 LED를 점등합니다.
        redLed.on() # 빨간색 LED에 전원을 공급합니다.
    elif message == "red_off": # 수신 메시지가 "red_off"이면 빨간색 LED를 소등합니다.
        redLed.off() # 빨간색 LED의 전원을 차단합니다.

client = mqtt.Client() # MQTT 통신을 수행할 클라이언트 객체를 생성합니다.
client.on_message = on_message # 메시지 수신 시 위에서 정의한 함수가 실행되도록 설정합니다.

broker_address="192.168.137.230" # MQTT 브로커(서버)가 설치된 라즈베리 파이의 IP 주소를 지정합니다.
client.connect(broker_address) # 설정한 IP 주소의 브로커 서버에 접속을 시도합니다.
client.subscribe("led",1) # "led"라는 주제를 구독하며 서비스 품질(QoS)은 1단계로 설정합니다.

count = 0 # 전송할 카운트 숫자의 초기값을 0으로 설정합니다.
def send_thread(): # 주기적으로 데이터를 보낼 별도의 함수를 정의합니다.
    global count # 함수 외부의 count 변수를 사용할 수 있도록 지정합니다.
    while 1: # 무한 루프를 통해 데이터를 계속해서 보냅니다.
        count = count + 1 # 카운트 값을 1씩 증가시킵니다.
        client.publish("hello", str(count)) # "hello"라는 주제로 현재 카운트 값을 발행(전송)합니다.
        time.sleep(1.0) # 다음 전송까지 1초 동안 대기합니다.

task = threading.Thread(target = send_thread) # 데이터 전송 함수를 별도의 독립된 스레드로 생성합니다.
task.start() # 생성한 스레드를 실행하여 백그라운드에서 전송을 시작합니다.

client.loop_forever() # 메시지 수신을 무한히 대기하며 프로그램을 유지합니다.