from django.db.models import Count,Sum
from django.shortcuts import render
from pymysql import NULL
from User.AFAuthentications import checkRTAFPassdword
from django.http import HttpResponse
from .models import Player,PlayerData
from django.contrib.auth.decorators import login_required
from Line.line_config import line_config_info

from linebot.models import *
from linebot import *

lineAPI = line_config_info()
line_bot_api = LineBotApi(lineAPI["channel_access_token"])

@login_required
def DisplayUnits(request):
    Players = Player.objects.values("unit").annotate(count=Count('unit'))
    data = {"Players" : Players}
    return render(request,'unit.html',data)

def DisplayRanking(request):
    scores = PlayerData.objects.values("score").aggregate(total=Sum('score'))
    print(scores)
    for score in scores:
        print(score)
    return render(request,'ranking.html')

def RTAFLoginPage(request):
    return render(request, 'rtaf-login.html')

def Register(request):
    mobile = request.POST.get("mobile")
    work_phone =  request.POST.get("work_phone")
    rtaf_email = request.session['rtaf_email']
    if mobile is not "" and work_phone is not "":
        find_email = Player.objects.filter(email = rtaf_email)
        if find_email:
            InsertInfo = Player.objects.get(email = rtaf_email)
            InsertInfo.mobile = mobile
            InsertInfo.office_phone = work_phone
            InsertInfo.state = 3
            InsertInfo.save()
            emoji = [
                {
                    "index": 30,
                    "productId": "5ac21a18040ab15980c9b43e",
                    "emojiId": "007"
                }
            ]
            text_message = TextSendMessage(text='ท่านได้ลงทะเบียนเรียบร้อยแล้ว $ สามารถร่วมกิจกรรมตอบคำถาม ในวันจันทร์ที่ 13 มิถุนายน 2565 เวลา 1400', emojis=emoji)
            user_line_id = Player.objects.filter(email = rtaf_email).values("line_id")
            line_bot_api.push_message(user_line_id[0]["line_id"], text_message)
            del request.session['rtaf_email']
            return render(request,"register_done.html")
    else:
        return render(request,"rtaf-login.html")

def RTAFLogin(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    
    if username is not None and password is not None:
        RTAFAuth = checkRTAFPassdword(request,username,password)
        if RTAFAuth['result'] == "Process-Complete":
            email = RTAFAuth['user']
            fullname = f"{RTAFAuth['fname']} {RTAFAuth['lname']} "
            rank = RTAFAuth['rank']
            unit = RTAFAuth['user_orgname']
            position = RTAFAuth['user_position']
            state = 1
            findPlayer = Player.objects.filter(email = email)
            request.session['rtaf_email'] = email
            if findPlayer:
                data = {"data" : findPlayer[0]}
                return render(request,'line-login.html',data)
            else:
                data = {"email" : email}
                AddPlayer = Player.objects.create(line_id = "unknown",
                                                  fullname = fullname,
                                                  email = email,
                                                  rank = rank,
                                                  unit = unit,
                                                  position = position,
                                                  state = state)
                return render(request,'line-login.html',data)
        else:
            data = {"message" : RTAFAuth['result']}
            return render(request, 'rtaf-error.html',data)
    else:
        return render(request, 'rtaf-login.html')