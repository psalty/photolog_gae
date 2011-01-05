'''
Created on May 19, 2010

@author: jaehong park
@email : psalty@gmail.com
'''
import os,logging
from jhpdb.Tags import Tags
from jhpdb.Content import photolog_delete,photolog_update_title,photolog_update_desc,photolog_update_tags,photolog_list_all,photolog_get_node,photolog_get_related_node,photolog_get_user_node
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
from flickr import people_findByUsername,tags_getListUser,photos_search
from jhpdb.oAuthUser import get_current_user,get_user_by_id,get_all_users


TEMPLATE_DIR='tmplt/'
USER_LIST='userprofiles.html'

class AdminPage(webapp.RequestHandler):
    def get(self):
        user_list = get_all_users()
        admin_logintout = users.create_logout_url("/")
        
        template_values = {
            'admin_logintout' : admin_logintout,
            'user_list' : user_list,
            }
        path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,USER_LIST)
        self.response.out.write(template.render(path, template_values).decode('utf-8'))
        

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    
    application_paths = [('/admin/',AdminPage),
                         ('/admin/view',AdminPage),
                         ]
    
    application = webapp.WSGIApplication(application_paths,debug=True)
    
    run_wsgi_app(application)

if __name__ == "__main__":
    main()