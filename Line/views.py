import json

from django.db.models import Count
from django.utils import timezone
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from linebot.models import *
from linebot import *

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
    if lineAPI["is_rtaf_authen"]:
        if 'rtaf_email' in request.session:
            email = request.session['rtaf_email']
            findPlayer = Player.objects.filter(email = email)
            data = {
                    "is_rtaf_authen":lineAPI["is_rtaf_authen"],
                    "liff_id":lineAPI["liff_id"],
                    "data" : findPlayer[0]
                    }
            return render(request,'register.html',data)
        else:
            return render(request,'rtaf-login.html')
    else:
        if 'user_line_id' in request.session:
            findPlayer = Player.objects.filter(line_id = request.session['user_line_id'])
            if findPlayer:
                data = {
                        "is_rtaf_authen": lineAPI["is_rtaf_authen"],
                        "liff_id": lineAPI["liff_id"],
                        "data": findPlayer[0],
                        "action": "update_info"
                        }
                return render(request,'register.html',data)
        else:
            data = {
                    "is_rtaf_authen": lineAPI["is_rtaf_authen"],
                    "liff_id": lineAPI["liff_id"],
                    "action": "new_register"
                    }
            return render(request,'register.html',data)
    
def LineAuthen(request):
    if lineAPI["is_rtaf_authen"]:
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
    else:
        user_line = request.POST.get("user_line_id")
        picture_url = request.POST.get("picture_url")
        find_line_id = Player.objects.filter(line_id = user_line)
        request.session['user_line_id'] = user_line
        if find_line_id.exists():
            data = {"data": "line already registered"}
            return JsonResponse(data)      
        else: 
            add_player = Player.objects.create(line_id = user_line,
                                               img = picture_url,
                                               state = 2)
            data = {"data": "line register successfully"}
            return JsonResponse(data)      


def arabic_convert(number):
    if number == "๑":
        number = 1
    if number == "๒":
        number = 2
    if number == "๓":
        number = 3
    if number == "๔":
        number = 4
    if number == "๕":
        number = 5
    if number == "๖":
        number = 6
    if number == "๗":
        number = 7
    if number == "๘":
        number = 8
    if number == "๙":
        number = 9
    if number == "๑๐":
        number = 10
    return number

def ThaiNum_convert(number):
    if number == 1:
        number = "๑"
    if number == 2:
        number = "๒"
    if number == 3:
        number = "๓"
    if number == 4:
        number = "๔"
    if number == 5:
        number = "๕"
    if number == 6:
        number = "๖"
    if number == 7:
        number = "๗"
    if number == 8:
        number = "๘"
    if number == 9:
        number = "๙"
    if number == 10:
        number = "๑๐"
    return number


@csrf_exempt
def GetAnswer(request):
    data = {}
    print("data = ",data)


    text_message = TextSendMessage(text=f'method GET = {data}')
    line_bot_api.push_message("Ua8a60fa72a4ca7ea52e79d8803cb454b", text_message)
    
    if request.method == 'POST':
        data = json.loads(request.body.decode())

        text_message = TextSendMessage(text=f'method POST = {data}')
        line_bot_api.push_message("Ua8a60fa72a4ca7ea52e79d8803cb454b", text_message)

        user_id = data['events'][0]['source']['userId']
        answer = data['events'][0]['message']['text']
        reply_token = data['events'][0]['replyToken']
        current_question = Question.objects.filter(is_current = True)

        print("data = ",data)
        print("answer = ",answer)

        # if answer in ["พร้อม","ไม่พร้อม"]:
        #     player = Player.objects.filter(line_id = user_id,state = StateChoice.FINISH)
        #     if player.exists():
        #         update_player = Player.objects.get(line_id = user_id,state = StateChoice.FINISH)
        #         if answer == "พร้อม":
        #             update_player.ready = True
        #             update_player.save()
        #             text_message = TextSendMessage(f"คุณพร้อมร่วมกิจกรรมแล้ว กิจกรรมเริ่ม 13 มิ.ย. 65")
        #             line_bot_api.reply_message(reply_token,text_message)
        #         if answer == "ไม่พร้อม":
        #             update_player.ready = False
        #             update_player.save()
        #             text_message = TextSendMessage(f"คุณจะไม่สามารถเข้าร่วมกิจกรรมตอบคำถามได้")
        #             line_bot_api.reply_message(reply_token,text_message)
        #     else:
        #         text_message = TextSendMessage(f"กรุณาลงทะเบียนให้ครบถ้วนก่อนร่วมกิจกรรมตอบคำถาม")
        #         line_bot_api.reply_message(reply_token,text_message)

        if not current_question.exists():
            url = lineAPI["url_website"]
            text_message = TextSendMessage(f"ร่วมกิจกรรมส่งเสริมการศึกษาพระประวัติและพระกรณียกิจ พระบิดาแห่งกองทัพอากาศ เปิดลงทะเบียนใน 8 มิ.ย.65 เป็นต้นไป ผ่านช่องทาง: {url}rtaf/")
            line_bot_api.reply_message(reply_token,text_message)

        if current_question.exists():
            player = Player.objects.filter(line_id = user_id)
            if player.exists() and player[0].state == StateChoice.FINISH:

                if answer.startswith(("ก", "ข", "ค", "ง")):
                    check_answer = PlayerData.objects.filter(player = player[0], question = current_question[0]) 
                    answer = answer.split("-")
                    question = arabic_convert(answer[1])
                    answer = answer[0]
                    if question == current_question[0].number:
                        if check_answer.exists() and player[0].state == StateChoice.FINISH:
                            text_message = TextSendMessage("คุณได้ตอบคำถามแล้ว ไม่สามารถตอบซ้ำได้")
                            line_bot_api.reply_message(reply_token,text_message)
                            return None
                        else:
                            if answer in ["ก","ข","ค","ง"] and player[0].state == StateChoice.FINISH:
                                if answer == "ก":
                                    answer_num = 1
                                if answer == "ข":
                                    answer_num = 2
                                if answer == "ค":
                                    answer_num = 3
                                if answer == "ง":
                                    answer_num = 4
                                choice_selected = Choice.objects.filter(question = current_question[0], number = int(answer_num))
                                choice_check = Choice.objects.get(question = current_question[0], number = int(answer_num))
                                print('choice_selected=',choice_selected)

                                if choice_check.correct == True :
                                    add_score = 1
                                else :
                                    add_score = 0
                                
                                player_data = PlayerData(player = player[0], question = current_question[0] , choice_selected = choice_selected[0], score = add_score)
                                player_data.save()

                                question_thai = ThaiNum_convert(current_question[0].number)


                                reply_text = f'ได้รับคำตอบของท่านแล้ว\n คำถามข้อที่ : {question_thai}\n ตัวเลือก : {answer}. {choice_selected[0].answer}'    
                                text_message = TextSendMessage(reply_text)
                                line_bot_api.reply_message(reply_token,text_message)
                                return None  
                            else:
                                text_message = TextSendMessage("กรุณาเลือกคำตอบให้ถูกต้อง")
                                line_bot_api.reply_message(reply_token,text_message)
                                return None   

                    else:
                        question_thai = ThaiNum_convert(current_question[0].number)
                        reply_text = f"ท่านตอบผิดข้อ คำถามปัจจุบันคือข้อ {question_thai}"
                        text_message = TextSendMessage(reply_text)
                        line_bot_api.reply_message(reply_token,text_message)
                else:
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
        return redirect('/units/')

    # # # Send Ready
    # if int(question_number) == 11:
    #     Send_Flex = FlexReady(question_number)
    #     line_bot_api.broadcast(Send_Flex)

    # Send Question
    if int(question_number) <= 10:
        if question_number != 0 :
            Send_Flex = FlexQuestion(question_number)
            line_bot_api.broadcast(Send_Flex)

            # player_ready = Player.objects.filter(ready = True)
            # for player in player_ready:
            #     print(player.line_id)
            #     line_bot_api.push_message(player.line_id,Send_Flex)

            send_time = Question.objects.get(number = question_number)
            send_time.send_time = timezone.now()
            send_time.save()

            question = Question.objects.all()
            question.update (is_current = False) 
            question = Question.objects.filter(number = question_number)
            question.update (is_current = True) 

    data = {'display_q':display_q}

    return render(request, 'SendQ.html',data)




