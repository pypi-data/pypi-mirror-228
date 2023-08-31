import requests
def robots_chat(robot1,robot2,talk):
    robot1 = robot1
    robot2 = robot2
    if robot1 == "" :robot1 = "小红"
    if robot2 == "" :robot2 = "小明"
    talk = talk
    while True:
        res = requests.post("http://api.qingyunke.com/api.php?key=free&appid=0&msg=" + talk)
        res = res.json()
        print(robot1,": ",res["content"])
        talk = res["content"]
        res = requests.post("https://api.ownthink.com/bot?spoken=" + talk)
        res = res.json()
        print(robot2,": ",res["data"]["info"]["text"])
        talk = res["data"]["info"]["text"]