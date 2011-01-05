#!/usr/bin/python
"""tbclient.py: A command-line trackback client.
If you're running Linux, change the path above to point to your Python installation.
Then you can run it ./tbclient.py -tburl foo -title bar, etc.
Otherwise run it python tblcient.py -tburl foo -title bar.
"""
__author__ = "Matt Croydon <matt@ooiio.com>"
__copyright__ = "Copyright 2003, Matt Croydon"
__license__ = "GPL"
__version__ = "0.0.2"
__history__ = """
0.0.2: 1/30/03 - It works!  Unleashing, er, releasing to the public.
0.0.1: 1/30/03 - Initial version, dealing with command line args, learning.
"""
import sys, tblib

def usage():
  print """Usage: tblib <args>
  Valid arguments:
    -tburl foo: ping the trackback url foo
    -title foo: title of your trackback or weblog post
    -excerpt foo: Uses foo as the excerpt to be posted to the trackback
    -url foo: The url to point to (usually the url of the post in which you ref the trackback)
    -blogname foo: The name of your weblog"""

if len(sys.argv) == 1:
  usage()
else:
  tb = tblib.TrackBack()
  print "Trackback command line client here.  Preparing TrackBack..."
  for x in range(len(sys.argv)):
    if sys.argv[x] == "-tburl":
      print "TrackBack URL: " + sys.argv[x+1]  
      tb.tbUrl = sys.argv[x+1]
    if sys.argv[x] == "-title":
      print "TrackBack Title: " + sys.argv[x+1]
      tb.title = sys.argv[x+1]
    if sys.argv[x] == "-excerpt":
      print "TrackBack Excerpt: " + sys.argv[x+1]
      tb.excerpt = sys.argv[x+1]
    if sys.argv[x] == "-url":
      print "Your URL: " + sys.argv[x+1]
      tb.url = sys.argv[x+1]
    if sys.argv[x] == "-blogname":
      print "Your Weblog Name: " + sys.argv[x+1]
      tb.blog_name = sys.argv[x+1]
  if tb.tbUrl:
    tb.ping()
    print "Pinging " + tb.tbUrl + "..."
    print "HTTP Response: " + str(tb.httpResponse) + " " + tb.httpReason
    if int(tb.tbErrorCode) == 0:
      print "TrackBack Error Code is: " + tb.tbErrorCode + " (zero is okay)"
    if int(tb.tbErrorCode) == 1:
      print "TrackBack Error Code is: " + tb.tbErrorCode
      print "Error Message: " + tb.tbErrorMessage
  print "Done!"
