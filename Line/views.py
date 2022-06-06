from curses import flash
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

from .flex_q import FlexQuestion,FlexReady
from .flex_t import FlexGroup, FlexSchool
from User.models import Player, Choice , PlayerData, StateChoice, Question
from Line.line_config import line_config_info
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse

lineAPI = line_config_info()
line_bot_api = LineBotApi(lineAPI["channel_access_token"])
handler = WebhookHandler(lineAPI["user_id"])

def DisplayLineDuplicate(request):
    return render(request,'line-duplicate.html')

def DisplayLineAuthen(request):
    if 'rtaf_email' in request.session:
        email = request.session['rtaf_email']
        findPlayer = Player.objects.filter(email = email)
        data = {"data" : findPlayer[0]}
        return render(request,'line-login.html',data)
    else:
        return render(request,'rtaf-login.html')
def LineAuthen(request):
    if request.method == 'POST':
        user_line = request.POST.get("user_id")
        rtaf_email = request.session['rtaf_email']
        picture_url = request.POST.get("picture_url")
        find_line_id = Player.objects.filter(line_id = user_line).values("line_id")
        find_player = Player.objects.filter(email = rtaf_email)
        
        if find_line_id.exists():
            my_line = Player.objects.filter(email = rtaf_email,line_id = find_line_id[0]['line_id'])
            if my_line:
                return HttpResponse(request.method)
            else:
                data = {"data": "line used by other"}
                return JsonResponse(data)               
        else:
            if find_player:
                insert_line = Player.objects.get(email = rtaf_email)
                insert_line.line_id = user_line
                insert_line.img = picture_url
                insert_line.state = 2
                insert_line.save()
                HttpResponse(request.method)           
            else:
                return HttpResponse(request.method)
    else:
        return HttpResponse(request.method)

@csrf_exempt
def GetAnswer(request):
    data = {}
    if request.method == 'POST':
        data = json.loads(request.body.decode()) 
        user_id = data['events'][0]['source']['userId']
        answer = data['events'][0]['message']['text']
        reply_token = data['events'][0]['replyToken']
        current_question = Question.objects.filter(is_current = True)

        if answer in ["พร้อม","ไม่พร้อม"]:
            player = Player.objects.filter(line_id = user_id,state = StateChoice.FINISH)
            if player.exists():
                if answer == "พร้อม":
                    player.ready = True
                    text_message = TextSendMessage(f"คุณพร้อมร่วมกิจกรรมแล้ว กิจกรรมเริ่ม 13 มิ.ย. 65")
                    line_bot_api.reply_message(reply_token,text_message)
                if answer == "ไม่พร้อม":
                    player = Player.objects.filter(line_id = user_id)
                    player.ready = False
                    text_message = TextSendMessage(f"คุณจะไม่สามารถเข้าร่วมกิจกรรมตอบคำถามได้")
                    line_bot_api.reply_message(reply_token,text_message)
            else:
                text_message = TextSendMessage(f"กรุณาลงทะเบียนให้ครบถ้วนก่อน")
                line_bot_api.reply_message(reply_token,text_message)

        if not current_question.exists():
            url = lineAPI["url_website"]
            text_message = TextSendMessage(f"ร่วมกิจกรรมส่งเสริมการศึกษาพระประวัติและพระกรณียกิจ พระบิดาแห่งกองทัพอากาศ เปิดลงทะเบียนใน 8 มิ.ย.65 เป็นต้นไป ผ่านช่องทาง: {url}rtaf/")
            line_bot_api.reply_message(reply_token,text_message)

        if current_question.exists():
            player = Player.objects.filter(line_id = user_id)
            if player.exists() and player[0].state == StateChoice.FINISH:

                check_answer = PlayerData.objects.filter(player = player[0], question = current_question[0]) 
                if check_answer.exists() and player[0].state == StateChoice.FINISH:
                    text_message = TextSendMessage("คุณได้ตอบคำถามแล้ว ไม่สามารถตอบซ้ำได้")
                    line_bot_api.reply_message(reply_token,text_message)
                    return None
                else:
                    if answer in ["1","2","3","4"] and player[0].state == StateChoice.FINISH:
                        choice_selected = Choice.objects.filter(question = current_question[0], number = int(answer))
                        choice_check = Choice.objects.get(question = current_question[0], number = int(answer))
                        print('choice_selected=',choice_selected)

                        if choice_check.correct == True :
                            add_score = 1
                        else :
                            add_score = 0
                        
                        player_data = PlayerData(player = player[0], question = current_question[0] , choice_selected = choice_selected[0], score = add_score)
                        player_data.save()
                        reply_text = f'ได้รับคำตอบของท่านแล้ว\n ข้อที่ : {current_question[0].number} ตัวเลือกที่ : {choice_selected[0].number} {choice_selected[0].answer}'    
                        text_message = TextSendMessage(reply_text)
                        line_bot_api.reply_message(reply_token,text_message)
                        return None     

                    if answer not in ["1","2","3","4"] and player[0].state == StateChoice.FINISH:
                        text_message = TextSendMessage("กรุณาเลือกคำตอบให้ถูกต้อง")
                        line_bot_api.reply_message(reply_token,text_message)
                        return None
            else:
                text_message = TextSendMessage(f"คุณยังไม่ได้ลงทะเบียน หรือ ลงทะเบียนไม่สมบูรณ์ กรุณาลงทะเบียนอีกครั้ง")
                line_bot_api.reply_message(reply_token,text_message)

    return HttpResponse(request.method)

# <---------------------------------------------------------------->
@login_required
def Questions(request ,question_number = 0):
    display_q = Question.objects.all()
    if not request.user.is_superuser:
        html = "<html><body><a href = '{% url 'register_check'%}'>ตรวจสอบรายชื่อผู้ลงทะเบียน</a></body></html>" 
        return HttpResponse(html)

    # Send Ready
    if int(question_number) == 11:
        Send_Flex = FlexReady(question_number)
        line_bot_api.broadcast(Send_Flex)

    # Send Question
    if int(question_number) <= 10:
        if question_number != 0:
            Send_Flex = FlexQuestion(question_number)
            player_ready = Player.objects.filter(ready = True)
            for player in player_ready:
                line_bot_api.push_message(player.line_id,Send_Flex)

            question = Question.objects.all()
            question.update (is_current = False) 
            question = Question.objects.filter(number = question_number)
            question.update (is_current = True) 

    data = {'display_q':display_q}

    return render(request, 'SendQ.html',data)




