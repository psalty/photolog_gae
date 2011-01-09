'''
Created on May 19, 2010

@author: jaehong park
@email : psalty@gmail.com
'''
import logging,math,os
from google.appengine.ext import db
from jhpdb.Content import Content
from jhpdb.Tags import update_tagcounter
from google.appengine.api import users
from google.appengine.api import images
from google.appengine.ext import webapp
from flickr import Photo
from ImageBlob import ImageBlob
from ImageBlob import create_image_blob
from xml.dom.minidom import Document

#image class
class ImageContent(Content):
    img_src = db.ReferenceProperty(ImageBlob)

    def update_username(self,uname):
        logging.debug(uname)
        self.user_name = uname
        self.put()

    def  update_tags(self,tags):
        if tags:
            for tg in tags.split():
                self.tags.append(db.Category(tg))
                update_tagcounter(tg)
            self.put()

    def remove_tag(self,tag):
        self.tags.remove(db.Category(tag))
        self.put()
        
    def add_tag(self,tag):
        self.tags.append(db.Category(tag))
        self.put()
        
    def get_info_in_xml(self):
        if os.environ.get('HTTP_HOST'): 
            host = os.environ['HTTP_HOST']
        else: 
            host = os.environ['SERVER_NAME']

        doc = Document()
        root = doc.createElement("channel")
        doc.appendChild(root)

        fb_id = doc.createElement("fb_id")
        fb_id_val = doc.createTextNode(self.fb_owner.id)
        fb_id.appendChild(fb_id_val)

        if self.title != None:
            ttl = doc.createElement("title")
            ttl_val = doc.createTextNode(self.title)
            ttl.appendChild(ttl_val)
            root.appendChild(ttl)

        thumb_nail = doc.createElement("small")
        thumb_nail_val = doc.createTextNode("http://%s/thumb?thumb_id=%s"%(host,self.img_src.key()))
        thumb_nail.appendChild(thumb_nail_val)
        
        med = doc.createElement("medium")
        med_val = doc.createTextNode("http://%s/instax?instax_id=%s"%(host,self.img_src.key()))
        med.appendChild(med_val)
        
        orimg = doc.createElement("big")
        orimg_val = doc.createTextNode("http://%s/img?img_id=%s"%(host,self.img_src.key()))
        orimg.appendChild(orimg_val)
        
        root.appendChild(fb_id)

        root.appendChild(thumb_nail)
        root.appendChild(med)
        root.appendChild(orimg)
        
        return doc
        
        
class FlickrContent(Content):
    user_id = db.StringProperty()
    photo_id = db.StringProperty()
    server = db.StringProperty()
    secret = db.StringProperty()
    user_name = db.StringProperty()
    real_author = db.StringProperty()
    
    def update_username(self,uname):
        logging.debug(uname)
        self.user_name = uname
        self.put()
        
    def update_real_author(self,rname):
        self.real_author = rname
        self.put()

    def update_tags(self,tags):
        if tags:
            for tg in tags:
                self.tags.append(db.Category(tg.text))
                update_tagcounter(tg.text)
            self.put()

    def remove_tag(self,tag):
        self.tags.remove(db.Category(tag))
        self.put()
        
    def add_tag(self,tag):
        self.tags.append(db.Category(tag))
        self.put()

    def get_info_in_xml(self):
        if os.environ.get('HTTP_HOST'): 
            host = os.environ['HTTP_HOST']
        else: 
            host = os.environ['SERVER_NAME']

        doc = Document()
        root = doc.createElement("channel")
        doc.appendChild(root)

        fb_id = doc.createElement("fb_id")
        fb_id_val = doc.createTextNode(self.fb_owner.id)
        fb_id.appendChild(fb_id_val)

        if self.title != None:
            ttl = doc.createElement("title")
            ttl_val = doc.createTextNode(self.title)
            ttl.appendChild(ttl_val)
            root.appendChild(ttl)

        thumb_nail = doc.createElement("small")
        thumb_nail_val = doc.createTextNode("http://farm4.static.flickr.com/%s/%s_%s_s.jpg"%(self.server,self.photo_id,self.secret))
        thumb_nail.appendChild(thumb_nail_val)
        
        med = doc.createElement("medium")
        med_val = doc.createTextNode("http://farm4.static.flickr.com/%s/%s_%s_m.jpg"%(self.server,self.photo_id,self.secret))
        med.appendChild(med_val)
        
        orimg = doc.createElement("big")
        orimg_val = doc.createTextNode("http://static.flickr.com/%s/%s_%s.jpg"%(self.server,self.photo_id,self.secret))
        orimg.appendChild(orimg_val)
        
        root.appendChild(fb_id)

        root.appendChild(thumb_nail)
        root.appendChild(med)
        root.appendChild(orimg)
        
        return doc

class PicasaContent(Content):
    photo_path = db.LinkProperty()
    thumb_small = db.LinkProperty()
    thumb_medium = db.LinkProperty()
    thumb_large = db.LinkProperty()
    credit = db.StringProperty()

    def update_tags(self,tags):
        if tags:
            for tg in tags.split():
                self.tags.append(db.Category(tg))
                update_tagcounter(tg)
            self.put()

    def remove_tag(self,tag):
        self.tags.remove(db.Category(tag))
        self.put()
        
    def add_tag(self,tag):
        self.tags.append(db.Category(tag))
        self.put()

    def get_info_in_xml(self):
        if os.environ.get('HTTP_HOST'): 
            host = os.environ['HTTP_HOST']
        else: 
            host = os.environ['SERVER_NAME']

        doc = Document()
        root = doc.createElement("channel")
        doc.appendChild(root)

        fb_id = doc.createElement("fb_id")
        fb_id_val = doc.createTextNode(self.fb_owner.id)
        fb_id.appendChild(fb_id_val)

        if self.title != None:
            ttl = doc.createElement("title")
            ttl_val = doc.createTextNode(self.title)
            ttl.appendChild(ttl_val)
            root.appendChild(ttl)

        thumb_nail = doc.createElement("small")
        thumb_nail_val = doc.createTextNode(self.thumb_small)
        thumb_nail.appendChild(thumb_nail_val)
        
        med = doc.createElement("medium")
        med_val = doc.createTextNode(self.thumb_medium)
        med.appendChild(med_val)
        
        orimg = doc.createElement("big")
        orimg_val = doc.createTextNode(self.thumb_large)
        orimg.appendChild(orimg_val)
        
        root.appendChild(fb_id)

        root.appendChild(thumb_nail)
        root.appendChild(med)
        root.appendChild(orimg)
        
        return doc

class Thumb(webapp.RequestHandler):
    def get(self):
        grain = db.get(self.request.get("thumb_id"))
        if grain.thumb:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(grain.thumb)
        else:
            self.response.out.write("No image")

class Image(webapp.RequestHandler):
    def get(self):
        grain = db.get(self.request.get("img_id"))
        if grain.img_src:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(grain.img_src)
        else:
            self.response.out.write("No image")

class Instax(webapp.RequestHandler):
    def get(self):
        grain = db.get(self.request.get("instax_id"))
        if grain.instax_src:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(grain.instax_src)
        else:
            self.response.out.write("No image")
            
class ImageTag(webapp.RequestHandler):
    def get(self):
        logging.debug("ImagTag")
        self.response.out.write("""<img src='/thumb?thumb_id=%s'>"""%self.request.get("thumb_id"))


def imge_size(l):
    x = len(l)
    
    if x==None or x<5:
        x = 5
        
    rval = 20 * math.log(x, math.e)
    if rval > 75:
        rval = 75
    return rval

def photolog_create_image(fbuser,addr,img):
    if  img == None:
        return None
    logging.debug('photolog_create_image')
    if fbuser:
        newNode = ImageContent()
        if newNode:
            newNode.fb_owner = fbuser
            newNode.img_src = create_image_blob(img)
            logging.debug('add to blobk')
            newNode.ip_addr = addr
            newNode.iszombie = False
            newNode.put();
        else:
            newNode=None
    else:
        newNode=None
    return newNode;


def photolog_create_flickr(fbuser,addr,uid,photo_id,server,secret,title):
    if fbuser:
        newNode = FlickrContent()
        newNode.fb_owner    = fbuser
        newNode.user_id     = uid
        newNode.photo_id    = photo_id
        newNode.server      = server
        newNode.secret      = secret
        newNode.title       = title
        newNode.ip_addr     = addr
        newNode.iszombie    = False
        newNode.put()
        # this required flickr node first to update the rest of information
        photo = Photo(photo_id)
        newNode.update_tags(photo.tags)
        newNode.update_username(photo.owner.username)
        newNode.update_real_author(photo.owner.realname)
    else:
        newNode = None
        
    return newNode

def photolog_create_picasa(fbuser,addr,credit,url,ths,thm,title,keywords):
    if fbuser:
        newNode = PicasaContent()
        newNode.fb_owner = fbuser
        newNode.photo_path = url
        newNode.thumb_small = ths
        newNode.thumb_medium = thm
        newNode.credit = credit
        newNode.title = title
        newNode.ip_addr = addr
        newNode.iszombie = False
        newNode.put()
        newNode.update_tags(keywords)
    else:
        newNode = None
    return newNode

def pyamf_add_image_node(fbuser,addr,img):
    if  img == None:
        return None
        
    newNode = ImageContent()

    if fbuser:
        newNode.fb_owner = fbuser

    if img:
        newNode.img_src = db.Blob(img)
        tmpImg = images.Image(img)

#        if tmpImg.width >= tmpImg.height:
#            addImg = images.resize(tmpImg._image_data,0,240)
#        else:
        addImg = images.resize(tmpImg._image_data,240,0)
        
        newNode.instax_src = db.Blob(addImg)
        
        addImg = images.crop(addImg,0.0,0.0,80.0/images.Image(addImg).width,80.0/images.Image(addImg).height)
        newNode.thumb = db.Blob(addImg);
    
    
    newNode.ip_addr = addr
    newNode.iszombie = False
    
    newNode.put();

    return newNode


#TODO:Add Blog Support
class AddBlogContent(webapp.RequestHandler):
    def post(self):
        newNode = add_blog_node(self.request.remote_addr,
                                  self.request.get("credit"),
                                  self.request.get("url"),
                                  self.request.get("thumb_s"),
                                  self.request.get("thumb_m"),
                                  self.request.get("title"))

def add_blog_node(addr,img,title,description,link):
    if  img == None:
        return None
        
    newNode = ImageContent()

    if users.get_current_user():
        newNode.owner = users.get_current_user()

    if img:
        newNode.img_src = db.Blob(img)
        tmpImg = images.Image(img)
            
#        if tmpImg.width >= tmpImg.height:
#            addImg = images.resize(tmpImg._image_data,0,240)
#        else:
        addImg = images.resize(tmpImg._image_data,240,0)
        
        newNode.instax_src = db.Blob(addImg)
        
        addImg = images.crop(addImg,0.0,0.0,80.0/images.Image(addImg).width,80.0/images.Image(addImg).height)
        newNode.thumb = db.Blob(addImg);
    
    
    newNode.ip_addr = addr
    newNode.iszombie = False
    
    newNode.put();

    return newNode