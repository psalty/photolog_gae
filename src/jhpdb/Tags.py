'''
Created on May 19, 2010

@author: jaehong park
@email : psalty@gmail.com
'''
from google.appengine.ext import db

class Tags(db.Model):
    tag = db.CategoryProperty()
    cnt = db.IntegerProperty()
    
    
def update_tagcounter(kw):
    newtags = Tags.gql("WHERE tag =:1",kw)
    newTag = newtags.get()
    if newTag:
        newTag.cnt +=1;
    else:
        newTag = Tags()
        newTag.cnt = 1;
        newTag.tag = kw
    newTag.put()

def decrement_tagcounter(tag):
    oldtags = Tags.gql("WHERE tag =:1",tag)
    oldTag = oldtags.get()
    if oldTag:
        oldTag.cnt -=1;
        if oldTag.cnt == 0:
            oldTag.delete()
        else:
            oldTag.put()
