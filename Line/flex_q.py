
from django.shortcuts import render

from linebot.models import *
from linebot import *

from User.models import Choice, Question
from Line.line_config import line_config_info


lineAPI = line_config_info()
line_bot_api = LineBotApi(lineAPI["channel_access_token"])


def FlexQuestion (question_number):
    question = Question.objects.get(number = question_number)
    question_text = str(question.name)
    question_img = f'{lineAPI["url_website"]}{question.img}'
    print('question_img=',f'{question_img}')

    choice = Choice.objects.filter(question = question).order_by('number')
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
                "text": "ข้อที่ 1: ",
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
                "text": "ข้อที่ 2: ",
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
                "text": "ข้อที่ 3: ",
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
                "text": "ข้อที่ 4: ",
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
          "label": f"ข้อที่ {str(choice[0].number)}",
          "text": str(choice[0].number)
        },
        "height": "sm",
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": f"ข้อที่ {str(choice[1].number)}",
          "text": str(choice[1].number)
        },
        "height": "sm",
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": f"ข้อที่ {str(choice[2].number)}",
          "text": str(choice[2].number)
        },
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": f"ข้อที่ {str(choice[3].number)}",
          "text": str(choice[3].number)
        },
        "style": "primary"
      }
    ]
  }
}
    )

    return flex_message
