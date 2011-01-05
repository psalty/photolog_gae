'''
Created on May 19, 2010

@author: jaehong park
@email : psalty@gmail.com
'''
from jhpdb.Content import Content
import logging
from google.appengine.ext import db
from google.appengine.api import users
from jhpdb.Tags import update_tagcounter
from google.appengine.ext import webapp

#Simple text class
class TextContent(Content):
    text = db.TextProperty()
    
class TrackbackContent(Content):
    text = db.TextProperty()
    tblink = db.LinkProperty()
    blog_name = db.StringProperty()

class AddTextContent(webapp.RequestHandler):
    def post(self):
        newNode = add_text_node(self.request.remote_addr,self.request.get("text_content"))
        
        if newNode:
            self.response.out.write("""<div width="120px">%s</div>""" % newNode.text)
            self.response.out.write("""<input id='gkey' type='hidden' value='%s'/>""" % newNode.key())
        else:
            self.response.out.write("""<p>creating entry failed</p>""")

class AddTrackBackContent(webapp.RequestHandler):
    def post(self):
        if(self.request.get('url')!='None'):
            pkey = self.request.path.split('/')[2]
            logging.debug(self.request.get('url'))
            logging.debug(self.request.get('blog_name'))
            logging.debug(self.request.get('title'))
            logging.debug(self.request.get('excerpt'))
            gkey = add_trackback_node(self.request.remote_addr,self.request.get('blog_name'),self.request.get('title'),self.request.get('excerpt'),self.request.get('url'))
            
            if(gkey):
#                update_relation(pkey,gkey)
                self.response.out.write("""<?xml version="1.0" encoding="utf-8"?><response><error>0</error></response>""")
            else:
                self.response.out.write("""<?xml version="1.0" encoding="utf-8"?><response><error>1</error><message>Node Creation Failed</message></response>""")
        else:
            self.response.out.write("""<?xml version="1.0" encoding="utf-8"?><response><error>1</error><message>Not Enough Information</message></response>""")

class UpdateText(webapp.RequestHandler):
    def post(self):
        logging.debug(self.request.get('gkey'));
        logging.debug(self.request.get('update_value'));
        update_text(self.request.get('gkey'),self.request.get('update_value'));
        self.response.out.write(self.request.get('update_value'))

def update_text(gKey,text):
    thisGrain = TextContent.get(gKey);

    if users.get_current_user():
        thisGrain.owner = users.get_current_user()
    else:
        return

    thisGrain.text = text;
    thisGrain.put()
    
def add_text_node(addr,ctt):
    if ctt == None:
        return None

    newNode = TextContent()
    
    if users.get_current_user():
        newNode.owner = users.get_current_user()
    if ctt:
        newNode.text = db.Text(ctt)
        newNode.title = newNode.text[0:100]+' ...'

    newNode.ip_addr = addr
    newNode.iszombie = False
        
    newNode.put();

    return newNode

def add_trackback_node(addr,bname,title,ctt,url):
    if ctt == None:
        return None

    newNode = TrackbackContent()
    
    if users.get_current_user():
        newNode.owner = users.get_current_user()
        
    if ctt:
        newNode.text = db.Text(ctt)
        newNode.title = title

    newNode.tags.append(db.Category('trackback'))
    update_tagcounter('trackback')

    newNode.ip_addr = addr
    newNode.iszombie = False
    
    newNode.blog_name = bname
    newNode.tblink = url
    newNode.put();

    return str(newNode.key())