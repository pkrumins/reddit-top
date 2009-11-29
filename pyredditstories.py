#!/usr/bin/python
# 
# Peteris Krumins (peter@catonmat.net)
# http://www.catonmat.net  --  good coders code, great reuse
#
# Released under GNU GPL
#
# Developed as a part of reddit top program.
# Read how it was designed:
# http://www.catonmat.net/blog/follow-reddit-from-the-console
#

import re
import sys
import time
import socket
import urllib2
import datetime

try:
 import json
except:
 import simplejson as json

version = "1.0"

reddit_url = 'http://www.reddit.com/'
subreddit_url = 'http://www.reddit.com/r/%s/'

class RedesignError(Exception):
    """
    An exception class thrown when it seems that Reddit has redesigned
    """
    pass

class SeriousError(Exception):
    """
    An exception class thrown when something unexpected happened
    """
    pass

class Story(dict):
    """
    Encapsulates the information about a single Reddit story.

    After the object is constructed it contains the following attributes:
    * position
    * reddit_name
    * id
    * title
    * url
    * user
    * score
    * human_time
    * unix_time
    * comments
    """

    def __repr__(self):
        inner = ', '.join([repr(x) for x in (self.position, str(self.reddit_name),
            str(self.id), str(self.title),
            str(self.url), str(self.user), self.score, str(self.human_time),
            self.unix_time, self.comments)])
        return ''.join(('{', inner, '}'))

def stories_per_page():
    """ Returns stories per single web page """
    return 25

def get_stories(subreddit='front_page', pages=1, new=False):
    """
    Finds all stories accross 'pages' pages on a 'subreddit' and returns a
    list of Story objects representing stories.

    If the 'subreddit' is 'front_page' gets stories from http://www.reddit.com/
    Otherwise gets stories from http://www.reddit.com/r/<subreddit>/

    If 'new' is True, gets new stories from http://www.reddit.com/new/
    If 'new' is True and 'subreddit' is set, gets stories from
    http://www.reddit.com/r/<subreddit>/new/
    """

    stories = [] 
    if subreddit == 'front_page':
        url = reddit_url
    else:
        url = subreddit_url % subreddit
    if new: url += 'new/'
    url += '.json'
    base_url = url

    for i in range(pages):
        content = _get_page(url)
        entries = _extract_stories(content)
        stories.extend(entries)
        url = _get_next_page(content, base_url)
        if not url:
            break

    for pos, story in enumerate(stories):
        story.position = pos+1
        story.reddit_name = subreddit

    return stories;

def _extract_stories(content):
    """
    Given a Reddit JSON page, extract stories and return a list of Story objects
    """

    stories = []
    reddit_json = json.loads(content)

    items = reddit_json['data']['children']
    for pos, item in enumerate(items):
        data = item['data']

        story = Story()
        story.id         = data['id']
        story.title      = data['title']
        story.url        = data['url']
        story.user       = data['author']
        story.score      = int(data['score'])
        story.unix_time  = int(data['created_utc'])
        story.human_time = time.ctime(story.unix_time)
        story.comments   = int(data['num_comments'])

        stories.append(story)

    return stories

def _get_page(url, timeout=10):
    """ Gets and returns a web page at url with timeout 'timeout'. """

    old_timeout = socket.setdefaulttimeout(timeout)

    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')

    try:
        response = urllib2.urlopen(request)
        content = response.read()
    except (urllib2.HTTPError, urllib2.URLError, socket.error, socket.sslerror), e:
        socket.setdefaulttimeout(old_timeout)
        raise SeriousError, e

    socket.setdefaulttimeout(old_timeout)
    return content

def _get_next_page(content, base_url):
    reddit_json = json.loads(content)
    after = reddit_json['data']['after']
    if after:
        return base_url + '?after=' + after

def print_stories_paragraph(stories):
    """
    Given a list of Stories, prints them out paragraph by paragraph
    """
    
    for story in stories:
        print 'position:',    story.position
        print 'reddit_name:', story.reddit_name.encode('utf-8')
        print 'id:',          story.id
        print 'title:',       story.title.encode('utf-8')
        print 'url:',         story.url.encode('utf-8')
        print 'score:',       story.score
        print 'comments:',    story.comments
        print 'user:',        story.user.encode('utf-8')
        print 'unix_time:',   story.unix_time
        print 'human_time:',  story.human_time
        print

if __name__ == '__main__':
    from optparse import OptionParser

    description = "A program by Peteris Krumins (http://www.catonmat.net)"
    usage = "%prog [options]"

    parser = OptionParser(description=description, usage=usage)
    parser.add_option("-s", action="store", dest="subreddit", default="front_page",
                      help="Subreddit to retrieve stories from. Default: front_page.")
    parser.add_option("-p", action="store", type="int", dest="pages",
                      default=1, help="How many pages of stories to output. Default: 1.")
    parser.add_option("-n", action="store_true", dest="new", 
                      help="Retrieve new stories. Default: nope.")
    options, args = parser.parse_args()

    try:
        stories = get_stories(options.subreddit, options.pages, options.new)
    except RedesignError, e:
        print >>sys.stderr, "Reddit has redesigned: %s!" % e
        sys.exit(1)
    except SeriousError, e:
        print >>sys.stderr, "Serious error: %s!" % e
        sys.exit(1)

    print_stories_paragraph(stories)

