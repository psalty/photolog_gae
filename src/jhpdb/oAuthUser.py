import facebook
from google.appengine.ext import db
import logging
import config


class FacebookUser(db.Model):
    nick_name = db.StringProperty()
    id = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    updated = db.DateTimeProperty(auto_now=True)
    name = db.StringProperty(required=True)
    profile_url = db.StringProperty(required=True)
    access_token = db.StringProperty(required=True)
    upf = db.LinkProperty()
    def update_upf(self,hlink):
        self.upf = hlink
        self.put()


def get_user_by_key(key):
    if key:
        return FacebookUser.get(key)
        


def get_current_user_from_json(uid,atoken):
    logging.debug("iphone cookie")
    # Store a local instance of the user data so we don't need
    # a round-trip to Facebook on every request
    user = FacebookUser.get_by_key_name(uid)
    if not user:
        graph = facebook.GraphAPI(atoken)
        profile = graph.get_object("me")
        user = FacebookUser(key_name=str(profile["id"]),
        id=str(profile["id"]),
        name=profile["name"],
        profile_url=profile["link"],
        access_token=atoken)
        user.put()
    elif user.access_token != atoken:
        user.access_token = atoken
        user.put()

    return user

def get_current_user(h_request):
#    logging.debug(h_request.request)
    if not hasattr(h_request, "_current_user"):
        h_request._current_user = None
        cookie = facebook.get_user_from_cookie(
            h_request.request.cookies, config.FACEBOOK_APP_ID, config.FACEBOOK_APP_SECRET)
        if cookie:
            # Store a local instance of the user data so we don't need
            # a round-trip to Facebook on every request
            user = FacebookUser.get_by_key_name(cookie["uid"])
            if not user:
                graph = facebook.GraphAPI(cookie["access_token"])
                profile = graph.get_object("me")
                user = FacebookUser(key_name=str(profile["id"]),
                            id=str(profile["id"]),
                            name=profile["name"],
                            profile_url=profile["link"],
                            access_token=cookie["access_token"])
                user.put()
            elif user.access_token != cookie["access_token"]:
                user.access_token = cookie["access_token"]
                user.put()
            h_request._current_user = user

    return h_request._current_user

def get_current_user_pyamf(request):
        cookie = facebook.get_user_from_cookie(
            request.cookies, config.FACEBOOK_APP_ID, config.FACEBOOK_APP_SECRET)
        if cookie:
            # Store a local instance of the user data so we don't need
            # a round-trip to Facebook on every request
            user = FacebookUser.get_by_key_name(cookie["uid"])
            if not user:
                graph = facebook.GraphAPI(cookie["access_token"])
                profile = graph.get_object("me")
                user = FacebookUser(key_name=str(profile["id"]),
                            id=str(profile["id"]),
                            name=profile["name"],
                            profile_url=profile["link"],
                            access_token=cookie["access_token"])
                user.put()
            elif user.access_token != cookie["access_token"]:
                user.access_token = cookie["access_token"]
                user.put()

            return user
        else:
            return None

def profile_update_upf(ukey,update_value):
    user = FacebookUser.get(ukey)
    user.update_upf(update_value)
    return update_value

def get_all_users():
    user_query = FacebookUser.all()
    user = user_query.fetch(100)
    return user

def get_user_by_id(id):
    user_query = FacebookUser.gql("WHERE id =:1",id)
    user = user_query.get()
    
    return user