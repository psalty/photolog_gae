'''
Created on May 19, 2010

@author: jaehong park
@email : psalty@gmail.com
'''
import logging
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.api import memcache
from jhpdb.Tags import decrement_tagcounter,update_tagcounter
from jhpdb.oAuthUser import FacebookUser


class Content(polymodel.PolyModel):
    owner = db.UserProperty()
    fb_owner = db.ReferenceProperty(FacebookUser)
    timestamp = db.DateTimeProperty(auto_now_add=True)
    title = db.StringProperty()
    tags = db.ListProperty(db.Category)
    rate = db.RatingProperty()
    ip_addr = db.StringProperty()
    iszombie = db.BooleanProperty()
    rkeys = db.ListProperty(db.Key)
    geotag = db.GeoPtProperty()
    content_text = db.TextProperty()

    def update_content_text(self,text):
        self.content_text = text;
        self.put()

    def update_title(self,title):
        self.title = title;
        self.put()

    def delete_relation(self,gkey):
        self.rkeys.remove(db.Key(gkey));
        self.put();

    def update_relation(self,gkey):
        self.rkeys.append(db.Key(gkey));
        logging.debug(self.rkeys)
        self.put();

    @property
    def owner_name(self):
        return self.fb_owner.name;
    
    def owner_id(self):
        return self.fb_owner.id;
    
    def owner_profile_url(self):
        return self.fb_owner.profile_url

    def get_xml_rep(self):
        return self.to_xml(self.__class__)

def photolog_update_title(gkey,update_value):
    logging.debug(gkey)
    logging.debug(update_value)
    node = Content.get(gkey)
    node.update_title(update_value)
    return update_value

def photolog_update_desc(gkey,update_value):
    node = Content.get(gkey)
    node.update_content_text(update_value)
    return update_value

def photolog_list_all(keyword='',limit=5):
    if keyword:
        ctt_query = Content.all().order('-timestamp').filter("iszombie", False).filter("tags",keyword)
    else:
        ctt_query = Content.all().order('-timestamp').filter("iszombie", False)
    logging.debug(limit)
    contents = ctt_query.fetch(limit)
    cursor = ctt_query.cursor()
    memcache.set('plist_cursor', cursor)
    
    return contents

def photolog_list_with_cursor(keyword='',limit=30):
    if keyword:
        ctt_query = Content.all().order('-timestamp').filter("iszombie", False).filter("tags",keyword)
    else:
        ctt_query = Content.all().order('-timestamp').filter("iszombie", False)

    last_cursor = memcache.get('plist_cursor')
    if last_cursor:
        ctt_query.with_cursor(last_cursor)

    contents = ctt_query.fetch(limit)
    cursor = ctt_query.cursor()
    memcache.set('plist_cursor', cursor)
    
    return contents



def photolog_get_node(gkey):
    node = Content.get(gkey)
    return node

def photolog_get_related_node(gkey):
    gKey = db.Key(gkey)
    rnodes = Content.gql("WHERE rkeys =:1 AND iszombie != TRUE",gKey)
    return rnodes

def photolog_get_user_node(account_type,user_auth):

    if account_type == "facebook":
        ctt_query = Content.gql("WHERE fb_owner =:1",user_auth)
        contents = ctt_query.fetch(100)

    if account_type == "google":
        ctt_query = Content.gql("WHERE owner =:1",user_auth)
        contents = ctt_query.fetch(100)

    return contents

def photolog_update_tags(gkey,original_value,update_value):
    node = Content.get(gkey)
    logging.debug(original_value)
    logging.debug(update_value)
    
    node.add_tag(update_value)
    node.remove_tag(original_value)
    decrement_tagcounter(original_value)
    update_tagcounter(update_value)
    return update_value

def photolog_delete(gkey):
    node = Content.get(db.Key(gkey))
    for tg in node.tags:
        decrement_tagcounter(tg)
    node.delete()
