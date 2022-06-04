# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Josh Hong

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
from pathlib import Path

#======================
# Code for retrieving and parsing
# Google News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        '''
        Initializes a NewsStory object
                
        guid (string): globally unique identifier
        title (string): title of the news story
        description (string): brief description of the contents of the news story
        link (string): link to more content
        pubdate (string): date published

        A NewsStory object has five attributes:
            self.guid (string, determined by input text)
            self.title (string, determined by input text)
            self.description (string, determined by input text)
            self.link (string, determined by input text)
            self.pubdate (datetime, determined by input text)
        '''
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        '''
        Safely access self.guid outside of the class

        Returns: self.guid
        '''
        return self.guid

    def get_title(self):
        '''
        Safely access self.title outside of the class

        Returns: self.title
        '''
        return self.title

    def get_description(self):
        '''
        Safely access self.description outside of the class

        Returns: self.description
        '''
        return self.description

    def get_link(self):
        '''
        Safely access self.link outside of the class

        Returns: self.link
        '''
        return self.link

    def get_pubdate(self):
        '''
        Safely access self.pubdate outside of the class

        Returns: self.pubdate
        '''
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS
# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        '''
        Initializes a PhraseTrigger object
                
        phrase (string): trigger phrase, non case-sensitive

        A PhraseTrigger object has one attribute:
            self.phrase (string, determined by input text)
        '''
        self.phrase = phrase

    def is_phrase_in(self, text):
        '''     
        text (string): snippet of text possibly containing the phrase trigger

        Returns: True if the phrase is present in the text, False otherwise
        '''
        for char in text:
            if char in string.punctuation:
                text = text.replace(char, ' ')
        text = text.lower().split()
        phrase_list = self.phrase.lower().split()

        if phrase_list[0] in text:
            start = text.index(phrase_list[0])
            end = start + len(phrase_list)
            return text[start:end] == phrase_list
        else:
            return False

# Problem 3
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        '''
        story (NewsStory): an object with the NewsStory class

        Returns: True if a news items's title contains the 
        trigger phrase, or False otherwise
        '''
        return self.is_phrase_in(story.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        '''
        story (NewsStory): an object with the NewsStory class

        Returns: True if a news items's description contains the 
        trigger phrase, or False otherwise
        '''
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS
class TimeTrigger(Trigger):
    est = pytz.timezone('EST')  # timezone passed to all instances of TimeTriggers
    def __init__(self, timestamp):
        '''
        Initializes a TimeTrigger object
                
        timestamp (string): string, with 24-hr format: d mmm yyyy hh:mm:ss
        
        A TimeTrigger object has one attribute:
            self.timestamp (datetime, converted from input string)
        '''
        # named attribute timestamp to avoid confusion w Python module time
        self.timestamp = self.est.localize(datetime.strptime(timestamp,'%d %b %Y %H:%M:%S'))

# Problem 6
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        '''
        story (NewsStory): an object with the NewsStory class

        Returns: True if a news items's publication date was prior
        to the timestamp of the trigger, or False otherwise
        '''
        pubdate = story.get_pubdate()
        if pubdate.tzinfo:
            return pubdate < self.timestamp
        else:
            return self.est.localize(pubdate) < self.timestamp 

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        '''
        story (NewsStory): an object with the NewsStory class

        Returns: True if a news items's publication date was prior
        to the timestamp of the trigger, or False otherwise
        '''
        pubdate = story.get_pubdate()
        if pubdate.tzinfo:
            return pubdate > self.timestamp
        else:
            return self.est.localize(pubdate) > self.timestamp 

# COMPOSITE TRIGGERS
# Problem 7
class NotTrigger(Trigger):
    def __init__(self,T):
        '''
        Initializes a NotTrigger object
                
        T (Trigger): an object with a Trigger Superclass
        
        A NotTrigger object has one attribute:
            self.T (Trigger, determined by input object)
        '''
        self.T = T

    def evaluate(self,story):
        '''
        story (NewsStory): an object with the NewsStory class

        Returns: False if the output of another Trigger 
        object is True, or True otherwise
        '''
        return not self.T.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
    def __init__(self,T1,T2):
        '''
        Initializes an AndTrigger object
                
        T1 (Trigger): an object with a Trigger Superclass
        T2 (Trigger): an object with a Trigger Superclass
        
        An AndTrigger object has two attributes:
            self.T1 (Trigger, determined by input object)
            self.T2 (Trigger, determined by input object)
        '''
        self.T1 = T1
        self.T2 = T2

    def evaluate(self,story):
        '''
        story (NewsStory): an object with the NewsStory class

        Returns: True if the output of both Trigger
        objects are True, or False otherwise
        '''
        return self.T1.evaluate(story) and self.T2.evaluate(story)

# Problem 9
class OrTrigger(Trigger):
    def __init__(self,T1,T2):
        '''
        Initializes an OrTrigger object
                
        T1 (Trigger): an object with a Trigger Superclass
        T2 (Trigger): an object with a Trigger Superclass
        
        An OrTrigger object has two attributes:
            self.T1 (Trigger, determined by input object)
            self.T2 (Trigger, determined by input object)
        '''
        self.T1 = T1
        self.T2 = T2

    def evaluate(self,story):
        '''
        story (NewsStory): an object with the NewsStory class

        Returns: True if the output of either Trigger
        objects are True, or False otherwise
        '''
        return self.T1.evaluate(story) or self.T2.evaluate(story)

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    triggered = []
    for story in stories:
        for trig in triggerlist:
            if trig.evaluate(story):
                triggered.append(story)
                break
    return triggered

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    trigger_file = open(filename, 'r')
    trigger_list = []
    trigger_dict = {}

    for line in trigger_file:
        line = line.rstrip()
        if line.startswith('ADD'):
            line = line.split(',')
            for i in range(1,len(line)):
                trigger_list.append(trigger_dict[line[i]])
            return trigger_list
        elif not (len(line) == 0 or line.startswith('//')):
            trigger_dict = trigger_parse_helper(trigger_dict,line)
    return None

def trigger_parse_helper(trig_dict,line):
    """
    trig_dict: dictionary containing trigger objects 
        from lines parsed in the text file
    line: current line being parsed in the text file

    Returns: a copy of the trigger dictionary containing previously 
        parsed trigger objects as well as the trigger object parsed
        from the current line.
    """
    trig_map = {
        'TITLE': TitleTrigger,
        'DESCRIPTION': DescriptionTrigger,
        'AND': AndTrigger,
        'OR': OrTrigger,
        'NOT': NotTrigger,
        'BEFORE': BeforeTrigger,
        'AFTER': AfterTrigger
    }
    
    trig_copy = trig_dict.copy()
    items = line.split(',')

    if items[1] == 'AND' or items[1] == 'OR':
        arg1, arg2 = trig_copy[items[2]],trig_copy[items[3]]
        trig_copy[items[0]] = trig_map[items[1]](arg1,arg2)
    elif items[1] == 'NOT':
        trig_copy[items[0]] = trig_map[items[1]](trig_copy[items[2]])
    else:
        trig_copy[items[0]] = trig_map[items[1]](items[2])
    return trig_copy

SLEEPTIME = 20 #seconds -- how often we poll

def main_thread(master):
    try:
        # get triggers from trigger config
        trigger_txt = Path(__file__).parent / 'triggers.txt'
        triggerlist = read_trigger_config(trigger_txt)
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:
            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)

            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)

if __name__ == '__main__':
    root = Tk()
    root.title("RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()