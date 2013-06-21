##! /usr/bin/python
# -*- coding: utf8 -*-
## Copyright (c) 2013 Stefan Thesing
##
##This file is part of Fism.
##
##Fism is free software: you can redistribute it and/or modify
##it under the terms of the GNU General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##Fism is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with Fism. If not, see http://www.gnu.org/licenses/.

__author__ = "Stefan Thesing <software@webdings.de>"
__version__ = "0.5.0"
__date__ = "Date: 2013/06/19"
__copyright__ = "Copyright (c) 2013 Stefan Thesing"
__license__ = "GPL"

import sys
import argparse
from classes.fism import Fism

if __name__ == "__main__":
    """
    Fism is a tool for Podcasters using one, two or all of the following list:

    1. [Auphonic](http://auphonic.com)
    2. [Firtz](http://github.com/eazyliving/firtz)
    3. [App.net](http://app.net)

    See the the Fism class or the README.md for further info.
    
    This file here only handles the command line interface, i.e. parsing the
    arguments.
    """
    #################################################
    # Define command line arguments                 #
    #################################################
    
    # Define the parser
    parser = argparse.ArgumentParser(description=
        'Fism is a tool for Podcasters using one, two or all of the \
        following list: \
        1. [Auphonic](http://auphonic.com) \
        2. [Firtz](http://github.com/eazyliving/firtz) \
        3. [App.net](http://app.net) \
         \
        It has three modules handling these three use cases.')
    
    # General arguments
    parser.add_argument('slug', help='the episode slug, e.g. \
        "suc001-crazy-title"')
    parser.add_argument('--settings',  help='relative or absolute \
        path to a settings file, Default: "settings.json"')
    
    # Auphonic arguments
    parser.add_argument('--audio', 
        help='[Auphonic]: relative or absolute path to the audio file, \
            e.g. "recording/audio.ogg" or "/home/user/recordings/audio.ogg"')
    parser.add_argument('--title', help='[Auphonic]: the episode title, e.g. \
        "SUC001 Crazy Title"')
    parser.add_argument('--track', help='[Auphonic]: the episode track \
        number, e.g. "001"')
    parser.add_argument('--subtitle', help='[Auphonic]: the episode subtitle, \
        e.g. "First Episode of a new Podcast"')
    parser.add_argument('--summary', help='[Auphonic]: the episode summary, \
        e.g. "In the first episode, I talked to..."')
    parser.add_argument('--tags', help='[Auphonic][Optional]: the episode tags. \
        Separated by commata and in quotes e.g. "\'podcast, interview\'"')
    parser.add_argument('--chapters',  
        help='[Auphonic][Optional]: relative or absolute path to the chapters file, \
            e.g. "prep/chapters.txt" or "/home/user/prep/chapters.txt"')
    
    # Firtz arguments    
    parser.add_argument('--epi_dict', help='[Firtz][Optional]: a comma separated list \
        of key-value pairs for the epi-file. The whole expression must be in \
        double quotes, each key and each value must be in single quotes, and \
        the separator is a colon. E.g. "\'date\':\'1945-05-23\', \
        \'title\':\'Test\'"')
    parser.add_argument('--prep_epi', help='[Firtz][Optional]: relative or absolute \
        path to a prepared epi file, e.g. "prep/suc001-crazy-title.epi" or \
        "/home/user/prep/suc001-crazy-title.epi"')
    
    # ADN arguments
    parser.add_argument('--post', 
        help='The text of your post on app.net, e.g. "New Episode of my \
            #Podcast: SUC001 Crazy Title http://example.com/podcast/suc001-crazy-title"')
    
    #################################################
    # Parse and process command line arguments      #
    #################################################
    
    # Well... parse them.
    args = parser.parse_args()
    
    # Init the Fism with the settings
    fism = Fism(args.settings)
    
    # OK, at this point, the parser hasn't detected any errors. Fine so far.
    # Let's check for some rudimentary consistency:
    # If you have one of the auphonic arguments, you need all of them.
    if args.audio or args.title or args.track or args.subtitle or args.summary or args.tags or args.chapters:
        # OK, one of them is there. Let's check if the others are there:
        if not (args.audio and args.title and args.track and args.subtitle and args.summary):
            print "It seems you want to use the auphonic module."
            print "Some mandatory argument for the auphonic module is missing."
            print "Mandatory arguments for the auphonic module are:"
            print "--audio, --title, --track, --subtitle, --summary"
            sys.exit("Please supply all mandatory arguments for auphonic.")
    
    # Check if the settings are configured to use adn as comments for the Firtz:
    if fism.use_adn_as_firtz_comments:
        # Check if the user has provided us with a adn post
        if not args.post:
            print "Your settings indicate you use ADN posts in your Firtz."
            sys.exit("Please supply text for an ADN post.")
            
    # Prepare the more complex arguments for the fism
    # Convert tags to a list
    if args.tags:
        args.tags = args.tags.split(',')
    
    # Convert epi_dict from string to an actual dict    
    
    if args.epi_dict and args.epi_dict != 'None':
    # Holy FSM, what have I done?
    # Getting something like a dict via command line is a f***ing pain in the..
    # ... well, it's complicated. Especially if values of the dict could 
    # possibly look like "Well, you know, there's this guy who said "Flubbsy" 
    # all the time!"
    # With commas, single quotes, double quotes, who knows.
    # So here's a quick hack to try to enable this. It works, but only if the
    # user doesn't make mistakes.

        # An empty dict
        epi_dict = {}
        # Split to a list containing the key-value pairs
        pairs = args.epi_dict.split(',')
        ## Iterate the list and split those into a list of two separate strings
        for pair in pairs:
            sepstr = pair.split(':')
            # Now, any quotes, double quotes and spaces that are at the 
            # beginning or and of these strings need to be removed.
            sepstr[0] = sepstr[0].strip()
            sepstr[0] = sepstr[0].strip('\'')
            sepstr[1] = sepstr[1].strip()
            sepstr[1] = sepstr[1].strip('\'')
            epi_dict[sepstr[0]] = sepstr[1]

    else:
        epi_dict = None
    
    # Start the Fism!
    fism.start(args.slug, args.audio, args.title, args.track, args.subtitle,   
               args.summary, args.post, args.tags, args.chapters, 
               epi_dict, args.prep_epi)

