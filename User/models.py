from datetime import datetime
from django.utils import timezone
import re

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.db.models import Sum,  Count



class StateChoice(models.IntegerChoices):
    IDLE = 0, _('ยังไม่ได้ลงทะเบียน')
    RTAF = 1, _('อัพเดทข้อมูล ทอ.')
    LINE = 2, _('อัพเดทจาก Line')
    FINISH = 3, _('ลงทะเบียนสมบูรณ์')

class Player(models.Model):
    class Meta:        
        verbose_name_plural = "ผู้ลงทะเบียน"
    line_id = models.CharField(verbose_name='Line ID', max_length=255)  
    fullname = models.CharField(verbose_name='ชื่อ-นามสกุล', max_length=255 ,blank=True , null = True)
    rank = models.CharField(verbose_name='ยศ', max_length=255 ,blank=True , null = True)
    unit = models.CharField(verbose_name='สังกัด', max_length=255 ,blank=True , null = True)
    email = models.CharField(verbose_name='อีเมล์', max_length=255 ,blank=True , null = True)
    mobile = models.CharField(verbose_name='เบอร์มือถือ', max_length=10 ,blank=True , null = True)
    office_phone = models.CharField(verbose_name='เบอร์ที่ทำงาน', max_length=10 ,blank=True , null = True)
    position = models.CharField(verbose_name='ตำแหน่ง', max_length=255 ,blank=True , null = True)
    state = models.IntegerField(verbose_name = "สถานะ" ,choices = StateChoice.choices, default = StateChoice.IDLE)
    last_response = models.DateTimeField(auto_now = True)
    img = models.CharField(verbose_name='รูปภาพ', max_length=255, default="-")  
    created = models.DateTimeField(auto_now_add=True)
    ready = models.BooleanField(verbose_name = "พร้อม", default = False)
    score = models.IntegerField(verbose_name="คะแนนรวม", null=True, blank=True, default=0)
    time = models.IntegerField(verbose_name="เวลารวม", null=True, blank=True,default=0)

    def is_idle(self):
        now = datetime.now(timezone.utc)
        # wait some time
        then = self.last_response
        # diff is a datetime.timedelta instance
        diff = now - then
        diff_minute = diff.seconds / 60
        print('diff_minute=',diff_minute)

        return diff_minute > 2
    
    @property
    def total_score(self):
        score = self.answer.aggregate(Sum('score'))
        if score["score__sum"]:
            return score["score__sum"]
        else:
            return 0
    @property
    def time_score(self):
        player_answer = self.answer.all()
        
        if player_answer.exists():
            total_time_score = sum([ts.time_score() for ts in player_answer])
            return total_time_score
        else:
            return 0

    def __str__(self):
        return f'{self.fullname}'

# <---------------------------------------------------------------->

class Question (models.Model):
    class Meta:        
        verbose_name_plural = "คำถาม"

    number = models.IntegerField(verbose_name="ข้อที่", null=True, blank=True)
    name = models.CharField(verbose_name = "โจทย์" ,max_length=255, blank=True, null = True)
    img = models.ImageField(verbose_name= "รูปภาพ",upload_to ='uploads/')
    is_current = models.BooleanField(verbose_name = "คำถามปัจจุบัน", default = False)
    send_time = models.DateTimeField(verbose_name="เวลาส่งคำถาม",null=True,blank=True)
    


    def __str__(self):
        return f'{self.number}'

# <---------------------------------------------------------------->

class Choice (models.Model):
    class Meta:        
        verbose_name_plural = "คำตอบ"

    question = models.ForeignKey(
        Question,
        null=True,
        blank=True,
        on_delete = models.SET_NULL,
        related_name='User_ATK_FK') 

    number = models.IntegerField(verbose_name="ตัวเลือก", null=True, blank=True)
    answer = models.CharField(verbose_name = "คำตอบ" ,max_length=255, blank=True, null = True)
    correct = models.BooleanField(verbose_name = "ถูก/ผิด", default=False ,null=True, blank=True)

    def __str__(self):
        return f'{self.answer}'

# <---------------------------------------------------------------->

class PlayerData (models.Model):
    class Meta:        
        verbose_name_plural = "ผู้ตอบแบบสอบถาม"

    player = models.ForeignKey(
        Player,
        null=True,
        blank=True,
        on_delete = models.SET_NULL,
        related_name='answer') 

    question = models.ForeignKey(
        Question,
        null=True,
        blank=True,
        on_delete = models.SET_NULL,
        related_name='คำถาม') 
   
    choice_selected = models.ForeignKey(
        Choice,
        null=True,
        blank=True,
        on_delete = models.SET_NULL,
        related_name='คำตอบ') 

    score = models.IntegerField(verbose_name="คะแนน", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, verbose_name = "เวลาที่บันทึก")

    def time_score(self):
        if self.timestamp and self.question.send_time:
            diff_time = self.timestamp - self.question.send_time
            return int(diff_time.total_seconds())
        else:
            return 0

    def save(self, *args, **kwargs):
        diff_time = timezone.now() - self.question.send_time
        print(timezone.now())
        print(self.question.send_time)
        print("Sum = ",diff_time.total_seconds())
        self.player.time += int(diff_time.total_seconds())
        if self.score == 1:
            self.player.score += 1

        self.player.save()
        
        super(PlayerData, self).save(*args, **kwargs)


class Raking(Player):
    class Meta:
        proxy = True
        verbose_name =  verbose_name_plural = "คำนวนคะแนน"




    


