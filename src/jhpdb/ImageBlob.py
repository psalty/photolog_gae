'''
Created on May 19, 2010

@author: jaehong park
@email : psalty@gmail.com
'''
import logging
from google.appengine.ext import db
from google.appengine.api.images import get_serving_url
from google.appengine.api import images

class ImageBlob(db.Model):
    img_src = db.BlobProperty()
    thumb = db.BlobProperty()
    instax_src = db.BlobProperty()
    
def create_image_blob(img):
    newBlob = ImageBlob()
    logging.debug('create_image_blob')
    newBlob.img_src = db.Blob(img)
    tmpImg = images.Image(img)
    logging.debug('resize')
    addImg = images.resize(tmpImg._image_data,240,0)
    newBlob.instax_src = db.Blob(addImg)
    logging.debug('crop')
    addImg = images.crop(addImg,0.0,0.0,80.0/images.Image(addImg).width,80.0/images.Image(addImg).height)
    newBlob.thumb = db.Blob(addImg);
    newBlob.put()
    return newBlob
