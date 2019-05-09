from django.db import models
from mongoengine import *

# Create your models here.

connect('JDComments_A21Jeans', host = '127.0.0.1', port = 27017)

class comment(Document):
    user_name = StringField()
    comment_star = IntField()
    comment_con = StringField()
    comment_time = DateTimeField()
    comment_id = IntField()

    meta = {'collection': 'comment'}