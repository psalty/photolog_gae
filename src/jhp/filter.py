'''
Created on May 19, 2010

@author: jaehong park
@email : psalty@gmail.com
'''
from google.appengine.ext import webapp
import math
from BeautifulSoup import BeautifulSoup

register = webapp.template.create_template_register()

@register.filter
def getNPix(value):
    newHeight = value * 80
    return newHeight

@register.filter
def tag_weight(x):
    if x==None or x<5:
        x = 5
    return 5 * math.log(x, math.e)

@register.filter
def img_weight(l):
    
    x = len(l)
    
    if x==None or x<5:
        x = 5
        
    rval = 20 * math.log(x, math.e)
    
    if rval > 75:
        rval = 75
    
    return rval

@register.filter
def getobjthumb(objdesc):
    soup = BeautifulSoup(objdesc)
        
    object = soup.object
    object['width'] = 120;
    object['height'] = 80;
    embed = soup.embed;
    embed['width'] = 120;
    embed['height'] = 80;
    
    return str(soup)

@register.filter
def getobjInstax(objdesc):
    soup = BeautifulSoup(objdesc)
        
    object = soup.object
    object['width'] = 160;
    object['height'] = 120;
    embed = soup.embed;
    embed['width'] = 160;
    embed['height'] = 120;
    
    return str(soup)

@register.filter
def shortenText(ctt):
    return ctt[0:140]+' ...'

@register.filter
def shortenTitle(ttl):
    if ttl:
        return ttl[0:8]+' ..'
    else:
        return '...'