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

import json
import argparse
from classes.fism import Fism

class Interactive:
    """
    Fism is a tool for Podcasters using one, two or all of the following list:

    1. [Auphonic](http://auphonic.com)
    2. [Firtz](http://github.com/eazyliving/firtz)
    3. [App.net](http://app.net)

    See the the Fism class or the README.md for further info.
    
    This file only handles the interactive command line interface.
    """
    def __init__(self):
        # Initialize empty variables
        self.audio = None
        self.title = None
        self.track = None
        self.subtitle = None
        self.summary = None
        self.chapters = None
        self.tags = None
        self.prep_epi = None
        self.epi_dict = None
        self.post = None
        self.adn_to_epi = False

    def ask(self):
        # Ask general questions
        self.slug = raw_input('What\'s the slug of the episode going to be? e.g. "spc001-crazy-title": ')
        self.settings = raw_input('What settings file should be used? \
        (Default:"settings.json"): ') or 'settings.json'
        
        # Ask which modules are to be used.
        self.ask_for_modules()
        # Ask questions for the moduls being used
        if self.use_auphonic:
            self.ask_auphonic()
        if self.use_firtz:
            self.ask_firtz()
        if self.use_adn:
            self.ask_adn()
    
    def ask_for_modules(self):
        """
        Which modules does the user want to use?
        """
        self.use_auphonic = not (raw_input('Would you like to use the \
        auphonic module? yn (Default:y): ') == ("n" or "N" or "no" or "No") )
        self.use_firtz = not (raw_input('Would you like to use the firtz \
        module? yn (Default:y): ') == ("n" or "N" or "no" or "No") )
        self.use_adn = not (raw_input('Would you like to use the app.net \
        module? yn (Default:y): ') == ("n" or "N" or "no" or "No") )
    
    def ask_auphonic(self):
        """
        Data needed for Auphonic
        """
        self.audio = raw_input('Specify relative or absolute path to the \
        audio file, e.g. "recording/audio.ogg" or "/home/user/recordings/audio.ogg": ')
        self.title = raw_input('What\'s the title of the episode going to be? e.g. \
            "SPC001 Crazy Title": ')
        self.track = raw_input('What\'s the track number of the episode going to be? \
            e.g. "001": ')
        self.subtitle = raw_input('What\'s the subtitle of the episode going to be? \
            e.g. "Interview with a crazy person.":')
        self.summary = raw_input('What\'s the summary of the episode going to be? e.g. \
            "In the first episode, I had the pleasure to interview a crazy \
            person, who is...": ')
        self.chapters = raw_input('Specify relative or absolute path to the chapter \
            file, e.g. "recording/chapters.txt" or \
            "/home/user/recordings/chapters.psc": ')
        self.tags = raw_input('Specify a comma separated list of tags, e.g. \
            "interview, crazy, podcast": ')
        # Convert tags to list
        self.tags = self.tags.split(',')
        
    def ask_firtz(self):
        """
        Data needed for the Firtz
        """
        self.prep_epi = raw_input('Specify relative or absolute path to a prepared \
            *.epi file, e.g. "prep/spc001-crazy-title.epi" or \
            "/home/user/prep/spc001-crazy-title.epi". (Default: None): ') or None
        self.epi_dict = {}
        while raw_input('Do you want to specify a(nother) key-value pair for the \
                epi file? E.g. "date: 1945-05-23 23:05:23" yn (Default:n): \
                ') == ("y" or "Y" or "yes" or "Yes"):
            key = raw_input('Specify key, e.g. "date": ')
            value = raw_input('Specify value, e.g. "1945-05-23 23:05:23": ')
            self.epi_dict[key] = value
    
    def ask_adn(self):
        """
        Data needed for ADN
        """
        self.post = raw_input('Write your post text. (Max 256 characters): ')
if __name__ == "__main__":
    
    ia = Interactive()
    ia.ask()
    
    # Init the Fism with the settings    
    fism = Fism((ia.settings or 'settings.json'))
    
    # Start the Fism!
    fism.start(ia.slug, ia.audio, ia.title, ia.track, ia.subtitle, ia.summary,
                ia.post, ia.tags, ia.chapters, ia.epi_dict, ia.prep_epi)
