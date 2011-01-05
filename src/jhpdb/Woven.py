'''
Created on May 19, 2010

@author: jaehong park
@email : psalty@gmail.com
'''
from google.appengine.ext import db
from jhpdb.Content import Content
import logging

class Nodes(db.Model):
    anode = db.ReferenceProperty()
    index = db.IntegerProperty()
    
def photolog_list_all_woven_nodes():
    nd_query = Nodes.all()
    nds = nd_query.fetch(100)
    return nds

class Woven(db.Model):
    source = db.ReferenceProperty(Nodes,None,'source_node')
    target = db.ReferenceProperty(Nodes,None,'target_node')

def photolog_list_all_woven():
    wv_query = Woven.all()
    wv = wv_query.fetch(100)
    return wv

def photolog_list_all_woven_from(fkey):
    wv_query = Woven.gql("WHERE source =:1",fkey)
    wv = wv_query.fetch(100)
    return wv

#Interwoven
def photolog_interweave(fnodeKey,tnodeKey):
    logging.debug("interwoven")
    logging.debug(fnodeKey)
    logging.debug(tnodeKey)
    
    source_node_query = Nodes.gql("WHERE anode =:1",db.Key(fnodeKey))
    source_node = source_node_query.get()
    
    if not source_node:
        source_node = Nodes()
        source_node.anode = db.Key(fnodeKey)
        source_node.put()
        
    target_node_query = Nodes.gql("WHERE anode =:1",db.Key(tnodeKey))
    target_node = target_node_query.get()
    
    if not target_node:
        target_node = Nodes()
        target_node.anode = db.Key(tnodeKey)
        target_node.put()
    
    wv_query = Woven.gql("WHERE source =:1 AND target =:2",source_node.key(),target_node.key())
    
    wv = wv_query.get()
    
    if wv:
        logging.debug("interwoven exist")
        return None
    else:
        wv = Woven()
        wv.source = source_node
        wv.target = target_node
        
    wv.put()
    return wv

def photolog_unweave(gKey):
    wv_query = Woven.gql("WHERE source =:1",db.Key(gKey))
    wv = wv_query.get()
    if wv:
        wv.delete()
    
    wv_query = Woven.gql("WHERE target =:1",db.Key(gKey))
    wv = wv_query.get()
    if wv:
        wv.delete()