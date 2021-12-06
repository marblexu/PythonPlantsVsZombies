# PythonPlantsVsZombies
  간단한 Plants Vs Zombies 게임입니다. <br>
  `이 게임은 개인적인 학습과 비상업적인 사용을 위한 것입니다. 만약 이 게임이 저작권을 침해한다면 저에게 알려주세요.`
* 구현된 식물: 해바라기, 콩슈터, 호두, 얼음 완두콩, 체리 폭탄, 삼발슈터, 먹개비, 퍼프 버섯, 감자 지뢰, 스파이크 위드, 겁쟁이 버섯, 스쿼시, 겁쟁이 버섯, 할라페뇨, 태양 버섯, 얼음 버섯, 최면 버섯.
* 구현된 좀비: 좀비, 깃발 좀비, 콘헤드 좀비, 양동이 좀비, 신문 좀비.
* json 파일을 사용하여 레벨 데이터(예: 좀비들의 위치 및 시간, 배경 정보 등)를 저장합니다.
* 맨 처음 스테이지 시작 전 식물 카드를 선택할 수 있게 지원합니다.
* 낮 스테이지, 밤 스테이지, 움직이는 카드 선택 스테이지, 호두 볼링 스테이지를 지원합니다.

# 요구 사항
* Python 3.7 
* 참고: Python 3.7이 권장되지만, 필수는 아닙니다. Linux의 경우, 이미 Python 3 이상이 설치되어 있다면 이 게임을 실행해도 좋습니다. Python 3.7로 직접 업데이트를 하면 Linux Mint가 손상될 수 있습니다.
* Python-Pygame 1.9

# 게임 시작 방법
$ python main.py

# 게임 방법
* 마우스를 사용하여 태양을 모으고, 식물 카드를 선택한 후 식물을 심습니다. 
* source/constant.py 파일의 START_LEVEL_NUM 값을 변경하여 시작 스테이지를 설정할 수 있습니다.
  * 스테이지 1과 2: 낮 스테이지
  * 스테이지 3: 밤 스테이지
  * 스테이지 4: 움직이는 카드 선택 스테이지
  * 스테이지 5: 호두 볼링 스테이지

# 데모
![demo1](https://raw.githubusercontent.com/marblexu/PythonPlantsVsZombies/master/demo/demo1.jpg)
![demo2](https://raw.githubusercontent.com/marblexu/PythonPlantsVsZombies/master/demo/demo2.jpg)

