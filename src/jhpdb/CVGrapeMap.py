'''
Created on May 19, 2010

@author: jaehong park
@email : psalty@gmail.com
'''
import os,logging
from django.utils import simplejson
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from jhpdb.Woven import photolog_list_all_woven_from,photolog_list_all_woven,photolog_list_all_woven_nodes

TEMPLATE_DIR='../tmplt/'
CVMAP='cvgrape.html'
CVTOOLTIP='cvtooltip.html'

def photolog_cvmanp_view(handler):
        logging.debug(handler.request.remote_addr)

#        thisNode = db.get(handler.request.get('gkey'))
#        wv = photolog_list_all_woven_from(handler.request.get('gkey'))
        wv = photolog_list_all_woven()
        nodes = photolog_list_all_woven_nodes()
        
        template_values = {
            'ip_addr' : handler.request.remote_addr,
            'links' : wv,
            'nodes' : nodes,
        }
        
        path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,CVMAP)
        handler.response.out.write(template.render(path, template_values).decode('utf-8'))



def photolog_cvmap_tooltip(handler):
        thisNode = db.get(handler.request.get('gkey'))
        
        template_values = {
            'thisNode' : thisNode,
        }
        
        path = os.path.join(os.path.dirname(__file__),TEMPLATE_DIR,CVTOOLTIP)
        handler.response.out.write(template.render(path, template_values).decode('utf-8'))

def photolog_cvmap_list_next_level(handler):
        wv = photolog_list_all_woven_from(handler.request.get('pkey'))
        
        nodelist = list()
        for node in wv:
            logging.debug(node.to_node.key)
            nodelist.append(str(node.to_node.key))

        logging.debug(simplejson.dumps(nodelist))
        handler.response.out.write(simplejson.dumps(nodelist))