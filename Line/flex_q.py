
from django.shortcuts import render

from linebot.models import *
from linebot import *

from User.models import Choice, Question
from Line.line_config import line_config_info


lineAPI = line_config_info()
line_bot_api = LineBotApi(lineAPI["channel_access_token"])

def FlexReady(question_number):
  flex_message = FlexSendMessage(
    alt_text= "พร้อมร่วมกิจกรรมหรือไม่",
        contents={
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://www.ipswichfirst.com.au/wp-content/uploads/2020/04/Are-You-Ready.jpg",
    "size": "full",
    "aspectRatio": "20:15",
    "aspectMode": "cover",
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
     {
        "type": "text",
        "text": f"คุณพร้อมร่วมกิจกรรมหรือยัง",
        "weight": "bold",
        "size": "lg",
        "align": "center",
        "contents": []
      },
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "flex": 0,
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "พร้อม ",
          "text": "พร้อม"
        },
        "height": "sm",
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "ไม่พร้อม ",
          "text": "ไม่พร้อม"
        },
        "height": "sm",
        "style": "primary"
      },
    ]
  }
}
    )
  return flex_message
def FlexQuestion (question_number):
    question = Question.objects.get(number = question_number)
    question_text = str(question.name)
    question_img = f'{lineAPI["url_website"]}{question.img}'
    print('question_img=',f'{question_img}')

    if question.number == 1:
      question.number = "๑"
    elif question.number == 2:
      question.number = "๒"
    elif question.number == 3:
      question.number = "๓"
    elif question.number == 4:
      question.number = "๔"
    elif question.number == 5:
      question.number = "๕"
    elif question.number == 6:
      question.number = "๖"
    elif question.number == 7:
      question.number = "๗"
    elif question.number == 8:
      question.number = "๘"
    elif question.number == 9:
      question.number = "๙"
    elif question.number == 10:
      question.number = "๑๐"


    choice = Choice.objects.filter(question = question).order_by('number')
    if choice[0].number == 1:
      choice1 =  str(choice[0].number)
      choice1 = "ก"
    if choice[1].number == 2:
      choice2 =  str(choice[1].number)
      choice2 = "ข"
    if choice[2].number == 3:
      choice3 =  str(choice[2].number)
      choice3 = "ค"
    if choice[3].number == 4:
      choice4 =  str(choice[3].number)
      choice4 = "ง"
      
    flex_message = FlexSendMessage(
        alt_text= question_text,
        contents={
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": question_img,
    "size": "full",
    "aspectRatio": "20:15",
    "aspectMode": "cover",
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
     {
        "type": "text",
        "text": f"คำถามข้อที่ {question.number}",
        "weight": "bold",
        "size": "lg",
        "align": "center",
        "contents": []
      },
      {
        "type": "text",
        "text": f"{question.name}",
        "weight": "regular",
        "size": "md",
        "align": "start",
        "wrap": True,
        "contents": []
      },
      {
        "type": "text",
        "text": "ตัวเลือก",
        "weight": "bold",
        "size": "lg",
        "align": "center",
        "contents": []
      },
      {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "margin": "lg",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "ก: ",
                "size": "sm",
                "color": "#AAAAAA",
                "flex": 1,
                "contents": []
              },
              {
                "type": "text",
                "text": f"{choice[0].answer}",
                "size": "sm",
                "color": "#666666",
                "flex": 5,
                "wrap": True,
                "contents": []
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "ข: ",
                "size": "sm",
                "color": "#AAAAAA",
                "flex": 1,
                "contents": []
              },
              {
                "type": "text",
                "text": f"{choice[1].answer}",
                "size": "sm",
                "color": "#666666",
                "flex": 5,
                "wrap": True,
                "contents": []
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "ค: ",
                "size": "sm",
                "color": "#AAAAAA",
                "flex": 1,
                "contents": []
              },
              {
                "type": "text",
                "text": f"{choice[2].answer}",
                "size": "sm",
                "color": "#666666",
                "flex": 5,
                "wrap": True,
                "contents": []
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "ง: ",
                "size": "sm",
                "color": "#AAAAAA",
                "flex": 1,
                "contents": []
              },
              {
                "type": "text",
                "text": f"{choice[3].answer}",
                "size": "sm",
                "color": "#666666",
                "flex": 5,
                "wrap": True,
                "contents": []
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "flex": 0,
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": f"ตัวเลือก: {choice1}",
          "text": choice1
        },
        "height": "sm",
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": f"ตัวเลือก: {choice2}",
          "text": choice2
        },
        "height": "sm",
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": f"ตัวเลือก: {choice3}",
          "text": choice3
        },
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": f"ตัวเลือก: {choice4}",
          "text": choice4
        },
        "style": "primary"
      }
    ]
  }
}
    )

    return flex_message
