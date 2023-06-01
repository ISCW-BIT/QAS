from django.db.models import Count,Sum
from django.shortcuts import render
from django.shortcuts import redirect
from pymysql import NULL
from User.AFAuthentications import checkRTAFPassdword
from django.http import HttpResponse
from .models import Player,PlayerData,Raking
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Min
from Line.line_config import line_config_info

from linebot.models import *
from linebot import *

lineAPI = line_config_info()
line_bot_api = LineBotApi(lineAPI["channel_access_token"])

@login_required
def DisplayUnits(request):
    players = Player.objects.values("unit").annotate(count=Count('unit')).order_by('-count')
    all_player = Player.objects.count()
    data = {"players" : players,
            "all_player": all_player}
    return render(request,'unit.html',data)

def DisplayRanking(request):
    ranking = Player.objects.values("fullname","unit","score","time").exclude(time=0).order_by('-score','time')[:30]
    data = {"rankings": ranking}
    print("data = ",data)
    return render(request,'ranking.html',data)

def RTAFLoginPage(request):
    return render(request, 'rtaf-login.html')

def Register(request):
    if lineAPI["is_rtaf_authen"]:
        mobile = request.POST.get("mobile")
        work_phone =  request.POST.get("work_phone")
        rtaf_email = request.session['rtaf_email']
        if mobile != "" and work_phone != "":
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
                text_message = TextSendMessage(text='ท่านได้ลงทะเบียนเรียบร้อยแล้ว $ สามารถร่วมกิจกรรมตอบคำถาม ในวันอังคารที่ 13 มิถุนายน 2566 เวลา 16.00 - 17.00', emojis=emoji)
                user_line_id = Player.objects.filter(email = rtaf_email).values("line_id")
                line_bot_api.push_message(user_line_id[0]["line_id"], text_message)
                del request.session['rtaf_email']
                return render(request,"register_done.html")
        else:
            return render(request,"rtaf-login.html")
    else:
        if 'user_line_id' in request.session:
            user_line_id = request.session['user_line_id']
            fullname = request.POST.get("fullname")
            age = request.POST.get("age")
            position = request.POST.get("position")
            unit = request.POST.get("unit")
            provide = request.POST.get("provide")
            address = request.POST.get("address")
            if fullname is not None and age is not None and position is not None and unit is not None and provide is not None and address is not None:
                update_info = Player.objects.filter(line_id = user_line_id)
                data = {"is_rtaf_authen": lineAPI["is_rtaf_authen"],
                        "line_url": lineAPI["line_url"]}
                if update_info:
                    update_info = Player.objects.get(line_id = user_line_id)
                    update_info.fullname = fullname
                    update_info.age = age
                    update_info.position = position
                    update_info.unit = unit
                    update_info.provide = provide
                    update_info.address = address
                    update_info.state = 3
                    update_info.save()

                    emoji = [
                        {
                            "index": 30,
                            "productId": "5ac21a18040ab15980c9b43e",
                            "emojiId": "007"
                        }
                    ]
                    text_message = TextSendMessage(text=f'ท่านได้ลงทะเบียนเรียบร้อยแล้ว $ สามารถร่วมกิจกรรมตอบคำถาม ในวันอังคารที่ 13 มิถุนายน 2566 เวลา 16.00 - 17.00', emojis=emoji)
                    user_line_id = Player.objects.filter(line_id = user_line_id).values("line_id")
                    line_bot_api.push_message(user_line_id[0]["line_id"], text_message)
                    return render(request,"register_done.html",data)
                else:
                    return redirect("/line/auth")
            else:
                return redirect("/line/auth")
        else:
            return redirect("/line/auth")


        

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
                return render(request,'register.html',data)
            else:
                data = {"email" : email}
                AddPlayer = Player.objects.create(line_id = "unknown",
                                                  fullname = fullname,
                                                  email = email,
                                                  rank = rank,
                                                  unit = unit,
                                                  position = position,
                                                  state = state)
                return render(request,'register.html',data)
        else:
            data = {"message" : RTAFAuth['result']}
            print(data)
            return render(request, 'rtaf-error.html',data)
    else:
        return render(request, 'rtaf-login.html')