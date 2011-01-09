'''
Created on May 19, 2010

@author: jaehong park
@email : psalty@gmail.com
'''
import os,logging,config
from jhpdb.Tags import Tags
from jhpdb.Content import photolog_delete,photolog_update_title,photolog_update_desc,photolog_update_tags,photolog_list_all,photolog_get_node,photolog_get_related_node,photolog_get_user_node,photolog_list_with_cursor
from jhpdb.ImageContent import Thumb,Image,Instax,ImageTag,photolog_create_image,photolog_create_flickr,photolog_create_picasa,pyamf_add_image_node
from jhpdb.TextContent import AddTrackBackContent
from jhpdb.Woven import photolog_list_all_woven_from,photolog_interweave,photolog_unweave
from jhpdb.CVGrapeMap import photolog_cvmanp_view,photolog_cvmap_tooltip,photolog_cvmap_list_next_level
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.api import images
from pyamf.remoting.gateway.google import WebAppGateway
from pyamf.remoting.gateway import expose_request
from flickr import people_findByUsername,tags_getListUser,photos_search
from jhpdb.oAuthUser import get_current_user,get_user_by_id,get_current_user_pyamf,profile_update_upf,get_user_by_key,get_current_user_from_json
from django.utils import simplejson
from xml.dom.minidom import Document
from xml.dom.minidom import parseString

TEMPLATE_DIR='tmplt/'

INDEX_PAGE='index.html'
INDEX_TILE='index_tile.html'
MAIN_CONTENT_VIEW='Grapeview.html'
PROFILE_PAGE='mycontents.html'
LOGIN_PAGE='loginout.html'
ADD_VIEW='add_entry.html'
MY_CONTENT_LIST='mylist.html'
MY_STITCHED_NODE='children.html'
TAG_LIST='tag_list.html'
THUMB_LIST='thumb_list.html'
APPEND_VIEW='appendview.html'
NOE_PER_PAGE=30


template.register_template_library('jhp.filter')

class MainPage(webapp.RequestHandler):
    def get(self):
        fbuser = get_current_user(self)
        admin_ggl_user = users.get_current_user()

        if admin_ggl_user:
            admin_logintout = users.create_logout_url("/")
        else:
            admin_logintout = users.create_login_url("/")
        
#        obj_contents = photolog_list_with_cursor(self.request.get("keyword"),NOE_PER_PAGE)
        if(self.request.get("mode") == "tile"):
            obj_contents = photolog_list_all(self.request.get("keyword"))
        else:
            obj_contents = photolog_list_all(self.request.get("keyword"),3)
            
        tag_query = Tags.all()
        tags = tag_query.fetch(1000)
        
        template_values = {
            'admin_loginout' : admin_logintout,
            'current_fb_user' : fbuser,
            'facebook_app_id' : config.FACEBOOK_APP_ID,
            'google_track_id' : config.GOOGLE_TRACKER_ID,
            'keywords' : tags,
            'obj_contents' : obj_contents,
            'ip_addr' : self.request.remote_addr,
        }
        
        if(self.request.get("mode") == "tile"):
            path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,INDEX_TILE)
        else: 
            path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,INDEX_PAGE)
        self.response.out.write(template.render(path, template_values).decode('utf-8'))
        
class MorePage(webapp.RequestHandler):
    def get(self):
        obj_contents = photolog_list_with_cursor(self.request.get("keyword"),2)
        
        template_values = {
            'obj_contents' : obj_contents,
        }
        path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,APPEND_VIEW)
        self.response.out.write(template.render(path, template_values).decode('utf-8'))
    
    
# main api switch
class RunView(webapp.RequestHandler):
    def get(self):
        type = self.request.get('type')
        if type == "mcontent":
            photolog_content_view(self)
        elif type == "add.entry":
            photolog_add_entry_view(self)
        elif type == "profile":
            photolog_profile_view(self)
        else:
            return None
# view methods
def photolog_content_view(handler):
        fbuser = get_current_user(handler)

        thisNode = photolog_get_node(handler.request.get('gkey'))
        rnodes = photolog_get_related_node(handler.request.get('gkey'))
        
        out_str = ' '.join(thisNode.tags)

        template_values = {
            'current_fb_user' : fbuser,
            'facebook_app_id' : config.FACEBOOK_APP_ID,
            'google_ad_client' : config.GOOGLE_AD_CLIENT,
            'google_ad_slot' : config.GOOGLE_AD_SLOT,
            'disqus_id' : config.DISQUS_ID,
            'thisNode' : thisNode,
            'tagstr' : out_str,
            'rnodes' : rnodes,
            'ip_addr' : handler.request.remote_addr,
        }
        path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,MAIN_CONTENT_VIEW)
        handler.response.out.write(template.render(path, template_values).decode('utf-8'))

def photolog_profile_view(handler):
        if handler.request.get('email'):
            fbuser = get_current_user(handler)
            requested_user = get_user_by_id(handler.request.get('email'))
                
            facebook_contents = photolog_get_user_node('facebook',requested_user)
            template_values = {
                'current_fb_user' : fbuser,
                'requested_user' : requested_user,
                'facebook_app_id' : config.FACEBOOK_APP_ID,
                'facebook_contents' : facebook_contents,
                'ip_addr' : handler.request.remote_addr,
                }
            path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,PROFILE_PAGE)
        else:
            fbuser = get_current_user(handler)
            if not fbuser:
                template_values = {
                    'redirect_url' : handler.request.path,
                }
                path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,LOGIN_PAGE)
            else:
                facebook_contents = photolog_get_user_node('facebook',fbuser)

                template_values = {
                    'current_fb_user' : fbuser,
                    'facebook_app_id' : config.FACEBOOK_APP_ID,
                    'facebook_contents' : facebook_contents,
                    'ip_addr' : handler.request.remote_addr,
                    }
                path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,PROFILE_PAGE)

        handler.response.out.write(template.render(path, template_values).decode('utf-8'))

def photolog_add_entry_view(handler):
        fbuser = get_current_user(handler)
        
        if not fbuser:
            template_values = {
                'redirect_url' : handler.request.path,
                'facebook_app_id' : config.FACEBOOK_APP_ID
                }
            path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,LOGIN_PAGE)
        else:
            if(handler.request.get('pkey')):
                thisNode = photolog_get_node(handler.request.get('pkey'))
            else:
                thisNode = None

            template_values = {
                'current_fb_user' : fbuser,
                'facebook_app_id' : config.FACEBOOK_APP_ID,
                'pnode' : thisNode,
                'ip_addr' : handler.request.remote_addr,
                }
            path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,ADD_VIEW)
        handler.response.out.write(template.render(path, template_values).decode('utf-8'))

class RunCreate(webapp.RequestHandler):
    def post(self):
        logging.debug(self.request.headers['User-Agent'])
        user_agent = self.request.headers['User-Agent']
# Comment is for local app luancher server
#       if user_agent == 'app.photolog':
        if user_agent == 'app.photolog,gzip(gfe)':
            fbuser = get_current_user_from_json(self.request.get('uid'),self.request.get('access_token'))
            logging.debug("iphone upload")
        else:
            fbuser = get_current_user(self)

        target = self.request.get('target')
        
        logging.debug(target)
        
        if target == 'image':
            rnode = photolog_create_image(fbuser,self.request.remote_addr,self.request.get("pics"))
        elif target == 'flickr':
            rnode = photolog_create_flickr(fbuser,
                                           self.request.remote_addr,
                                           self.request.get("user_id"),
                                           self.request.get("photo_id"),
                                           self.request.get("server"),
                                           self.request.get("secret"),
                                           self.request.get("title")
                                           )
        elif target == 'picasa':
            rnode = photolog_create_picasa(fbuser,
                                           self.request.remote_addr,
                                           self.request.get("credit"),
                                           self.request.get("url"),
                                           self.request.get("thumb_s"),
                                           self.request.get("thumb_m"),
                                           self.request.get("title"),
                                           self.request.get("keywords")
                                           )
        else:
            rnode = None
#send Status Information
           
        if rnode:
            self.response.out.write(simplejson.dumps({ 'status' : 'OK' , 'newkey' : str(rnode.key())}))
        else:
            self.response.out.write(simplejson.dumps({ 'status' : 'NOK' , 'newkey' : None}))
        
        #=======================================================================
        # template_values = {
        #                'node' : rnode,
        #                }
        # path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,'preview.html')
        # self.response.out.write(template.render(path, template_values).decode('utf-8'))
        #=======================================================================

class RunList(webapp.RequestHandler):
    def get(self):
        type = self.request.get('type')
        if type == "mycontent":
            photolog_browse_my_list(self)
        elif type == "stitch":
            photolog_stitched_list(self)
        elif type == "nlevel":
            photolog_cvmap_list_next_level(self)


def photolog_browse_my_list(handler):
        fbuser = get_current_user(handler)
        if not fbuser:
            handler.response.out.write(simplejson.dumps({ 'status' : 'NOK' , 'newkey' : None}))
        else:
            handler.request.get('pkey')
            obj_contents = photolog_get_user_node("facebook",fbuser)
            template_values = {
                'pnode' : photolog_get_node(handler.request.get('pkey')),
                'obj_contents' : obj_contents,
                }
            path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,MY_CONTENT_LIST)
            handler.response.out.write(template.render(path, template_values).decode('utf-8'))

def photolog_stitched_list(handler):
        wv = photolog_list_all_woven_from(handler.request.get('pkey'))
        
        template_values = {
            'grapes' : wv,
        }
        path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,MY_STITCHED_NODE)
        handler.response.out.write(template.render(path, template_values).decode('utf-8'))

class RunUpdate(webapp.RequestHandler):
    def post(self):
        target = self.request.get('target')

        if target == 'title':
            rval = photolog_update_title(self.request.get('gkey'),self.request.get('update_value'))
        elif target == 'desc':
            rval = photolog_update_desc(self.request.get('gkey'),self.request.get('update_value'))
        elif target == 'tags':
            rval = photolog_update_tags(self.request.get('gkey'),self.request.get('original_value'),self.request.get('update_value'))
        elif target == 'user_upf':
            rval = profile_update_upf(self.request.get('ukey'),self.request.get('update_value'))
        else:
            rval = None
            
        self.response.out.write(rval)

class RunDelete(webapp.RequestHandler):
    def post(self):
        photolog_delete(self.request.get('gkey'))
        photolog_unweave(self.request.get('gkey'))
        self.response.out.write("/")

class RunMap(webapp.RequestHandler):
    def get(self):
        method = self.request.get('method')
        if method == "view":
            type = self.request.get('type')
            if type == "cvmap":
                photolog_cvmanp_view(self)
        elif method == "tooltip":
            photolog_cvmap_tooltip(self)
            
class PhotologFlickrApiWrapper(webapp.RequestHandler):
    def get(self):
        if self.request.get('method') == 'listkeywords':
            user_object = people_findByUsername(self.request.get('username'))
            data = tags_getListUser(user_object.id)

            template_values = {
                               'nsid' : user_object.id,
                               'keywords' : data,
                               }
            path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,TAG_LIST)
        elif self.request.get('method') == 'listphotos':
            data = photos_search(self.request.get('username'),False,self.request.get('tags').encode('utf-8'))

            template_values = {
                               'photos' : data,
                               }
            path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,THUMB_LIST)
            
        self.response.out.write(template.render(path, template_values).decode('utf-8'))

class RunStitch(webapp.RequestHandler):
    def post(self):
        fbuser = get_current_user(self)

        if fbuser:
            wv = photolog_interweave(self.request.get('gkey'),self.request.get('pkey'))
#        update_relation(self.request.get('gkey'),self.request.get('pkey'))
            self.response.out.write(simplejson.dumps({ 'status' : 'NOK'}))

#TODO: external API
class RunApi(webapp.RequestHandler):
    def post(self):
        self.response.out.write("success")
    def get(self):
        method = self.request.get('method')
        logging.debug(method)
        
        if method == "photo.list.all":
            doc = Document()
            root = doc.createElement("channel")
            doc.appendChild(root)

            obj_contents = photolog_list_all('',5)
            for obj in obj_contents:
                dom = parseString(obj.to_xml().encode('utf-8'))
                root.appendChild(dom.getElementsByTagName("entity")[0])
        elif method == "user.info":
            doc = Document()
            root = doc.createElement("channel")
            doc.appendChild(root)

            key = method = self.request.get('key')
            userinfo = get_user_by_key(key)
            dom = parseString(userinfo.to_xml().encode('utf-8'))
            root.appendChild(dom.getElementsByTagName("entity")[0])
        elif method == "photo.one":
            gkey = self.request.get('gkey')
            if gkey:
                obj = photolog_get_node(gkey)
                doc = obj.get_info_in_xml()
                #dom = parseString(obj.to_xml().encode('utf-8'))
                #root.appendChild(dom.getElementsByTagName("entity")[0])
            else:
                return
            
        self.response.out.write(doc.toxml())
        
@expose_request
def PhotologUploadWebcam(request,data,ipaddr):
    logging.debug(request)
    fbuser = get_current_user_pyamf(request)
    if fbuser:
        tmpImg = images.Image(str(data))
        newNode = pyamf_add_image_node(fbuser,ipaddr,tmpImg._image_data)
    if newNode:
        return str(newNode.key())
    else:
        return None
        
def main():
    logging.getLogger().setLevel(logging.DEBUG)
    services = {
        'myservice.uploadWebcam' : PhotologUploadWebcam,
    }
    
    gateway = WebAppGateway(services,logger=logging,debug=True)
    
    application_paths = [('/',MainPage),
                         ('/mmore',MorePage),
                         ('/flex',gateway),
                         ('/trackback/.*',AddTrackBackContent),
                         ('/thumb',Thumb),
                         ('/img',Image),
                         ('/instax',Instax),
                         ('/imgtg',ImageTag),
                         ('/view',RunView),
                         ('/update',RunUpdate),
                         ('/create',RunCreate),
                         ('/list',RunList),
                         ('/stitch',RunStitch),
                         ('/delete',RunDelete),
                         ('/map',RunMap),
                         ('/photolog_flickr_api_helper',PhotologFlickrApiWrapper),
                         ('/api',RunApi)
                         ]
    
    application = webapp.WSGIApplication(application_paths,debug=True)
    
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
