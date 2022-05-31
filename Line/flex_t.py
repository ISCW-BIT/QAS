
from django.shortcuts import render

from linebot.models import *
from linebot import *

from User.models import Player

line_bot_api = LineBotApi('487xE2UTmdeK8ycDSEWWTlC0/7dRlbiAot2j95rvcIERFNbY7L+XXtt8T53Vx+7+u/BDCarSPOmwBP7FzfJbno9iFX+ns0Vu5uXf40DS28h2auBpnBZZnoSWGBmp/gyfWFnbjehTcn13qE/iThZkpAdB04t89/1O/w1cDnyilFU=')

def FlexGroup():

    img_register = f'https://stellar-dynamics.com/uploads/uploads/ประชม_SISDregister.png'
    
    flex_message = FlexSendMessage(
        alt_text='hello',
        contents={
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://www2.si.mahidol.ac.th/tmec2019/media/k2/items/cache/8376aace7af18ea8cafa499d7e69a6ec_XL.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "label": "Line",
      "uri": "https://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "กลุ่มผู้ลงทะเบียน",
        "weight": "bold",
        "size": "xl",
        "contents": []
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
          "label": "นักเรียน",
          "text": "101"
        },
        "height": "sm",
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "ข้าราชการ ทอ.",
          "text": "102"
        },
        "height": "sm",
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "ประชาชนทั่วไป",
          "text": "103"
        },
        "style": "primary"
      }
    ]
  }
}
    )

    return flex_message


def FlexSchool():

    flex_message = FlexSendMessage(
        alt_text='hello',
        contents={
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": "https://www2.si.mahidol.ac.th/tmec2019/media/k2/items/cache/8376aace7af18ea8cafa499d7e69a6ec_XL.jpg",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "label": "Line",
      "uri": "https://linecorp.com/"
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "กลุ่มผู้ลงทะเบียน",
        "weight": "bold",
        "size": "xl",
        "contents": []
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
          "label": "รร.ดอนเมืองทหารอากาศบำรุง",
          "text": "201"
        },
        "style": "primary"
      },
            {
        "type": "button",
        "action": {
          "type": "message",
          "label": "รร.มัธยมสังคีตวิทยา",
          "text": "202"
        },
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "รร.ฤทธิยะวรรณาลัย",
          "text": "203"
        },
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "รร.ฤทธิยะวรรณาลัย ๒",
          "text": "204"
        },
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "รร.สายปัญญารังสิต",
          "text": "205"
        },
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "รร.รัตนโกสินทร์สมโภช",
          "text": "206"
        },
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "รร.ดอนเมืองจาตุรจินดา",
          "text": "207"
        },
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "รร.สีกัน(วัฒนานันท์อุปถัมภ์)",
          "text": "208"
        },
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "รร.หอวังปทุมธานี",
          "text": "209"
        },
        "style": "primary"
      },
      {
        "type": "button",
        "action": {
          "type": "message",
          "label": "รร.ธัญบุรี",
          "text": "210"
        },
        "style": "primary"
      },
    ]
  }
}
    )

    return flex_message

