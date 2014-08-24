# encoding: utf-8
from APNSWrapper import *
import os
import re
import binascii
from  datetime  import  *  
from django.conf import settings

settings.configure()

import thread
from shop.models import Item 
items = Item.objects.all()
for item in items:
    print str(item.sold)
    item.sold = 0
    item.save()

