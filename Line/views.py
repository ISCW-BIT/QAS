import email
import json
import datetime

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from linebot.models import *
from linebot import *
from io import BytesIO

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from .flex_q import FlexQuestion
from .flex_t import FlexGroup, FlexSchool
from User.models import Player, Choice , PlayerData, StateChoice, Question
from Line.line_config import line_config_info
from django.http import HttpResponse
from django.shortcuts import redirect

lineAPI = line_config_info()
line_bot_api = LineBotApi(lineAPI["channel_access_token"])
handler = WebhookHandler(lineAPI["user_id"])


def DisplayLineAuthen(request):
    print("Display Line Login Page")
    email = request.session['rtaf_email']
    findPlayer = Player.objects.filter(email = email)
    data = {"data" : findPlayer[0]}
    return render(request,'line-login.html',data)
    
def LineAuthen(request):
    if request.method == 'POST':
        user_line = request.POST.get("user_id")
        rtaf_email = request.session['rtaf_email']
        picture_url = request.POST.get("picture_url")
        find_player = Player.objects.filter(email = rtaf_email)
        if find_player:
            insert_line = Player.objects.get(email = rtaf_email)
            insert_line.line_id = user_line
            insert_line.img = picture_url
            insert_line.state = 2
            insert_line.save()
            print("save line id")
            return HttpResponse(request.method)
        else:
            print("not found Player")
            return render(request,"rtaf-login.html")
    else:
        print("IT IS",request.method)
        return render(request,"rtaf-login.html")

@csrf_exempt
def GetAnswer(request):
    data = {}
    if request.method == 'POST':
        data = json.loads(request.body.decode()) 
        user_id = data['events'][0]['source']['userId']
        answer = data['events'][0]['message']['text']
        reply_token = data['events'][0]['replyToken']

        current_question = Question.objects.filter(is_current = True)
        if not current_question.exists():

            text_message = TextSendMessage("ร่วมกิจกรรมส่งเสริมการศึกษาพระประวัติและพระกรณียกิจ พระบิดาแห่งกองทัพอากาศ เปิดลงทะเบียนในระหว่าง 31 พ.ค. – 2 มิ.ย.65")
            line_bot_api.reply_message(reply_token,text_message)
        current_question = current_question[0]
        player = Player.objects.filter(lineid = user_id)
        check_player = PlayerData.objects.filter(player = player.email, question = current_question) 

        if check_player.exists() and player.state == StateChoice.FINISH:
            text_message = TextSendMessage("คุณได้ตอบคำถามแล้ว ไม่สามารถตอบซ้ำได้")
            line_bot_api.reply_message(reply_token,text_message)

            return None

        if answer not in ["1","2","3","4"] and player.state == StateChoice.FINISH:
            text_message = TextSendMessage("กรุณาเลือกให้ถูกต้อง")
            line_bot_api.reply_message(reply_token,text_message)

            return None

    return HttpResponse(request.method)

# <---------------------------------------------------------------->
@login_required
def Questions(request ,question_number = 0):
    display_q = Question.objects.all()
    if not request.user.is_superuser:
        html = "<html><body><a href = '{% url 'register_check'%}'>ตรวจสอบรายชื่อผู้ลงทะเบียน</a></body></html>" 
        return HttpResponse(html)
    if question_number != 0 :
        Send_Flex = FlexQuestion(question_number)
        line_bot_api.broadcast(Send_Flex)

        question = Question.objects.all()
        question.update (is_current = False) 
        question = Question.objects.filter(number = question_number)
        question.update (is_current = True) 

    data = {'display_q':display_q}

    return render(request, 'SendQ.html',data)




