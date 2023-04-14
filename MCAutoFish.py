import pyautogui
import time
import threading
import json
import pygetwindow

startTime = time.time()
keepRun = True
isAuto = True
counter = 0

try:
    with open("./config.json", "r", encoding="utf8") as data:
        jsonData = json.load(data)
        tx = jsonData["x"]
        ty = jsonData["y"]
        tGreen = jsonData["green"]
        tGray = jsonData["gray"]
        delayTime = jsonData["delayTime"]
        redeploymentTime = jsonData["redeploymentTime"]
        colorTesterTime = jsonData["colorTesterTime"]
        print("读取配置文件完成！")
except:
    keepRun = False
    input("读取配置文件失败！请检查config.json文件是否存在")
else:
    print("程序开始执行")


def getColor(x, y):
    pixel = pyautogui.screenshot().getpixel((x, y))
    return list(pixel)


def getCurrentTime():
    return int(time.time() - startTime) // 1


def resetTimer():
    global isAuto
    time.sleep(delayTime)
    isAuto = True


def autoFish(r, g, b):
    global counter, isAuto
    if (
        tGreen["min"][0] < r < tGreen["max"][0]
        and tGreen["min"][1] < g < tGreen["max"][1]
        and tGreen["min"][2] < b < tGreen["max"][2]
    ) or (
        tGray["min"][0] < r < tGray["max"][0]
        and tGray["min"][1] < g < tGray["max"][1]
        and tGray["min"][2] < b < tGray["max"][2]
    ):
        isAuto = False
        counter += 1
        timer = threading.Thread(
            target=resetTimer, daemon=True, name="resetTimerThread"
        )
        timer.start()
        pyautogui.click(button="right")
        time.sleep(redeploymentTime)
        pyautogui.click(button="right")
    return


while keepRun:
    try:
        title=pygetwindow.getActiveWindow().title
        if title=="Minecraft":
            if isAuto:
                color = getColor(tx, ty)
                autoFish(color[0], color[1], color[2])
            print("\r", "钓鱼统计:", counter, "杆", "", "运行时长:", getCurrentTime(), "秒", end="")
        else:
            print("\r", "程序暂停运行                                                          ", end="")
            continue
        time.sleep(colorTesterTime)
    except:
        pass
    finally:
        continue
