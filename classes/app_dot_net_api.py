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
from lib.appdotnet import *

class App_dot_net_api(appdotnet):
    """
    A class handling the ADN-Stuff, it uses App.net API-Wrapper by Simon de 
    la Rouviere. https://github.com/simondlr/Python-App.net-API-Wrapper
    """
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None,
                 scope=None, access_token=None):
        appdotnet.__init__(self, client_id, client_secret, redirect_uri,
                 scope, access_token)
    
    def post(self, text, link=None):
        """
        Creates an adn post with the supplied text, 
        makes an inline link to the episode specified by slug,
        and returns its post id as an iteger.
        """
        
        # TODO Inline Link? How do I do this?
        # TODO Language Annotation?
        # TODO Error if text is too long
        if link:
            text = text + " " + link
        
        # ###################################################################
        # Here's a little test code I use I'm, working with json post data  #
        # from a file, so I don't spam the ADN-API                          #
        # Just ignore it.                                                   #
        #####################################################################
        #f = open('example-data/log_post.json', 'r')
        #post = f.read()
        #f.close()
        #####################################################################
                        
        # Here is the real request
        # Call parent function
        post = self.createPost(text)
        
        # Return the post id
        return json.loads(post)['data']['id']
