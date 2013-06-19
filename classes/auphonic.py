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

import json
import time

try:
    import requests
    from requests.auth import HTTPBasicAuth
except:
    print "Please install python requests!"

# Constants:
API_URL = "https://auphonic.com/api/simple/productions.json"

class Auphonic:
    """
    Handles the interaction with the API of auphonic.com
    """
    def __init__(self, settings):
        """
        Initializes the class with general settings taken from settings.json
        """
        self.preset = settings['preset']
        self.username = settings['auphonic_username']
        self.password = settings['auphonic_password']
        
    def start(self, audio_file, title, track, subtitle, summary, \
              slug, tags=None, chapters_file=None):
        """
        Creates the Auphonic Production, uploads the neccessary files,
        waits for it to finish.
        """
        
        # Create the production, upload and get the UUID
        prod_uuid = self.create_production(audio_file, title, track, 
                            subtitle, summary, slug, tags, chapters_file)
        
        # Wait till the production is finished.
        # Initial request for production status code
        r = requests.get('https://auphonic.com/api/production/'+prod_uuid+'.json', 
                        auth=HTTPBasicAuth(str(self.username), str(self.password)))
        status_code = r.json()['data']['status']
        
        # Check production status every 3 seconds
        # Three status codes end the while loop:
        # "3": "Done", or 
        # "2": "Error"
        while not (int(status_code) == 3) or (int(status_code) == 2):
            print r.json()['data']['status_string']
            time.sleep(3)
            r = requests.get('https://auphonic.com/api/production/'+prod_uuid+'.json', 
                        auth=HTTPBasicAuth(str(self.username), str(self.password)))
            status_code = r.json()['data']['status']
        
        # Now the status is either "Done" or "Error"
        print r.json()['data']['status_string'] 
        return status_code
                  
    def create_production(self, audio_file, title, track, subtitle, 
                           summary, slug, tags=None, chapters_file=None):              
        """
        Called by self.start.
        Creates the production, uploads and returns the UUID
        """
        #############################
        # Prepare data              #
        #############################
        data = {'preset': self.preset,             
                'track': track,
                'title': title,
                'subtitle': subtitle,
                'summary': summary,
                'action': 'start',                
                'output_basename': slug}
                        
        # Add tags, if any
        if tags:
            # Convert tags into a comma separated string
            data['tags'] = ','.join(str(tag) for tag in tags)
        
        #############################
        # Prepare multi-file upload #
        #############################
        files = {}
        # Add audio file
        files['input_file'] = open(audio_file, 'r')
        
        # Add a chapters_file, if any
        if chapters_file:
            files['chapters'] = open(chapters_file, 'r')
        
        #############################
        # Make the API call         #
        #############################            
        r = requests.post(API_URL, 
                          data=data, 
                          files=files,
                          auth=HTTPBasicAuth(str(self.username), str(self.password)))
        
        #Return the UUID
        return r.json()['data']['uuid']
