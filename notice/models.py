from django.db import models

# Create your models here.
class University(models.Model):
    c_name = models.CharField('中文名',max_length=100)
    e_name = models.CharField('英文名',max_length=100)
    school_type = models.CharField('学校类型',max_length=100)
    address = models.CharField('学校地理位置',max_length=100)
    TOEFL_score = models.CharField('托福成绩',max_length=100)
    SAT_score = models.CharField('SAT成绩',max_length=100)
    instructions = models.TextField('学校简介')
