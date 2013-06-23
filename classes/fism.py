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

import sys
import json
from classes.firtz import Firtz
from classes.app_dot_net_api import App_dot_net_api
from classes.auphonic import Auphonic

class Fism:
    """
    Fism is a tool for Podcasters using one, two or all of the following list:

    1. [Auphonic](http://auphonic.com)
    2. [Firtz](http://github.com/eazyliving/firtz)
    3. [App.net](http://app.net)

    It has three modules handling these three use cases.
    
    """
    def __init__(self, settings='settings.json'):
        # Sometimes, settings can be None, in that case it should be 
        # standard, too.
        if not settings:
            settings = 'settings.json'
        
        # Read settings from JSON-File
        try:
            f = open(settings,'r')
            settings = json.loads(f.read())
            f.close()
        except IOError, e:
            print "## Error ##"
            print "No settings file could not be found."
            print "Please retry and specify a settings file or create the standard 'settings.json' file in the main directory of Fism."
            print "If you want to generate one, use setup.py!"
            sys.exit(e)
        except ValueError, e:
            print "## Error ##"
            print "There is a problem with your settings file."
            print "Please fix it and retry."
            print "If you want to generate one, use setup.py!"
            sys.exit(e)
        
        # Use only what is inside "fism_settings"
        try:
            settings = settings['fism_settings']
        except KeyError, e:
            print "## Error ##"
            print "There is a problem with your settings file."
            print "It seems to be valid JSON, but not a valid Fism settings file."
            print "The key '" + e.message + "' is missing."
            print "Please fix it and retry."
            print "If you want to generate one, use setup.py!"
            sys.exit()
            
        
        
        
        # Settings for Firtz
        self.firtz_settings = settings['firtz_settings']
        
        # Settings for Auphonic
        self.auphonic_settings = settings['auphonic_settings']
        
        # Settings for ADN
        self.adn_settings = settings['adn_settings']
        
        # Initialize the modules
        self.firtz = Firtz(self.firtz_settings)
        self.auphonic = Auphonic(self.auphonic_settings)
        self.adn = App_dot_net_api(access_token=self.adn_settings['adntoken'])
        self.use_adn_as_firtz_comments = self.adn_settings['use_adn_as_firtz_comments']
        self.base_web_url = self.firtz_settings['base_web_url']
        
        #TODO Logfile
    
    def start(self, slug, audio_file, title, track, subtitle, summary, 
              post_text, tags=None, chapters_file=None, epi_dict=None, 
              prep_epi=None):
        
        # Make the auphonic production, upload, wait for it to finish
        self.start_auphonic(slug, audio_file, title, track, subtitle,
                            summary, tags, chapters_file)
        # Create an epi-file, upload it
        self.start_firtz(slug, epi_dict, prep_epi)
        # Post about your new episode on app.net
        post_id = self.start_adn(slug, post_text)
        
        # Write the post_id to the epi file and upload it.
        if self.use_adn_as_firtz_comments:
            self.firtz.write_to_epi(slug, {'adnthread': str(post_id)})
            self.firtz.upload_epi(slug)
        
        
    def start_auphonic(self, slug, audio_file, title, track, subtitle,
                        summary, tags=None, chapters_file=None):
        
        ##########################################################
        # Module 1: Auphonic                                     #
        ##########################################################
        
        # Make and start the auphonic production
        status_code = self.auphonic.start(audio_file, title, track, \
                            subtitle, summary, slug, tags, chapters_file)
        if not int(status_code) == 3:
            sys.exit("Something went wrong. Check your production on \
                http://auphonic.com")
    
    def start_firtz(self, slug, epi_dict=None, prep_epi=None):
                
        ##########################################################
        # Module 2: Firtz                                        #
        ##########################################################
        
        # Perpare and upload the epi File
        self.firtz.prepare_epi(slug, epi_dict, prep_epi)
        # upload everything to the firtz
        self.firtz.upload_epi(slug)
    
    def start_adn(self, slug, post_text):
        
        ##########################################################
        # Module 3: App.net                                      #
        ##########################################################
        
        # Make the link
        link = self.base_web_url + slug
        # Post to adn
        post_id = self.adn.post(post_text, link)
        return post_id
        

