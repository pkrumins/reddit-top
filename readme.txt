This is the Reddit Top program. It's a top-like program for monitoring stories
on reddit.com from the console.

It was written by Peteris Krumins (peter@catonmat.net).
His blog is at http://www.catonmat.net  --  good coders code, great reuse.

The code is licensed under the GNU GPL license.

The code was written as a part of the article "Follow Reddit from the Console"
on my website. The whole article can be read at:

    http://www.catonmat.net/blog/follow-reddit-from-the-console/

I explained some parts of the code in this program in another article "How
Reddit Top and Hacker Top Programs Were Made". It can be read here:

http://www.catonmat.net/blog/how-reddit-top-and-hacker-top-programs-were-made/

------------------------------------------------------------------------------

Table of contents:

    [1] The Reddit Top program.
    [2] Program's usage.
    [3] Keyboard shortcuts.
    [4] Future TODO improvements.


[1]-The-Reddit-Top-program----------------------------------------------------

This program monitors Reddit ( http://reddit.com ) for new stories and
displays them in the console via ncurses.

The program is written in Python programming language and is supposed to
be run on Unix type operating systems, such as Linux.

It uses one external Python module:

    * simplejson - for parsing the reddit stories.
    It can be installed via `easy_install simplejson` command or can be
    downloaded from http://undefined.org/python/#simplejson

See my original article for a screenshot:

    http://www.catonmat.net/blog/follow-reddit-from-the-console/


[2]-Reddit-Top-usage----------------------------------------------------------

Usage: ./reddit_top.py [-h|--help] - displays help message

Usage: ./reddit_top.py [-s|--subreddit subreddit]
                       [-i|--interval interval]
                       [-u|--utf8 <on|off>]
                       [-n|--new]

    -s or --subreddit specifies which subreddit to monitor.
    The default is Reddit's front page - http://www.reddit.com
    Some examples are 'programming', 'science', 'wtf', 'linux' and others.
    See http://www.reddit.com/reddits/ for all the possible subreddits!

    -i or --interval specifies refresh interval.
    The default refresh interval is 1 minute. Here are a few
    examples:  10s (10 seconds), 12m (12 minutes), 2h (2 hours). 

    -u or --utf8 turns on utf8 output mode.
    Default: off. Use this if you know for sure that your
    terminal supports it, otherwise your terminal might turn into garbage.

    -n or --new follows only the newest (just submitted) reddit stories.
    Default: follow front page stories.


[3]-Keyboard-shortcuts--------------------------------------------------------

q - quits the program.
u - forces an update of the stories.
m - changes the display mode.
up/down arrows (or j/k) - scrolls the news list up or down.


[4]-Future-TODO-improvements--------------------------------------------------

* Add a feature to open a story in web browser. (Someone suggested to use
  webbrowser module)

* Fix it to work on Windows. (Perhaps try the Console module)

* Merge it with "Hacker Top" program (see below) and create "Social Top"
  program. Then write plugins for Digg, and other websites.

  Hacker Top is here:
  http://www.catonmat.net/blog/follow-hacker-news-from-the-console/

* Add ability to login and vote for the favorite stories.


------------------------------------------------------------------------------


Have fun using it!


Sincerely,
Peteris Krumins
http://www.catonmat.net

