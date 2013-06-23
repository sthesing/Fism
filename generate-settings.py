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

import sys
import json

def main():
    """
    Generates a JSON Settings file for Fism.
    """
    fism_settings = {}
    # Ask general questions
    use_auphonic = not (raw_input('Would you like to use the auphonic module? yn (Default:y): ') == ("n" or "N" or "no" or "No") )
    use_firtz = not (raw_input('Would you like to use the firtz module? yn (Default:y): ') == ("n" or "N" or "no" or "No") )
    use_adn = not (raw_input('Would you like to use the app.net module? yn (Default:y): ') == ("n" or "N" or "no" or "No") )
    
    if use_auphonic:
        auphonic_username = raw_input('Specify your auphonic username: ')
        auphonic_password = raw_input('Specify your auphonic password: ')
        preset = raw_input('Specify the UUID of the auphonic preset you want to use: ')
        if not (auphonic_username and auphonic_password and preset):
            sys.exit("If you want to use the Auphonic module, you need to make these settings.")
        
        auphonic_settings = {'auphonic_username': auphonic_username, 'auphonic_password': auphonic_password, 'preset': preset}
        fism_settings['auphonic_settings'] = auphonic_settings
        
    if use_firtz:
        base_audio_url = raw_input('Specify the url where your audio files are residing, e.g. "http://example.com/audio": ')
        base_web_url = raw_input('Specifiy the base url of the firtz, e.g. "http://example.com/supicast/show": ')
        ftp_host = raw_input('Specify the hostname of your ftp server, e.g. "example.com" (WITHOUT ftp:// or http://): ')
        ftp_path = raw_input('Specify the path to the directory on the server to upload the epi-files, e.g. "feeds/supicast" : ')
        ftp_user = raw_input('Specify your FTP username: ')
        ftp_passw = raw_input('Specify your FTP password: ')
        if not (base_audio_url and base_web_url and ftp_host and ftp_path and ftp_user and ftp_passw):
            sys.exit("If you want to use the Firtz module, you need to make these settings.")
            
        firtz_settings = {'base_audio_url': base_audio_url, 'base_web_url': base_web_url, 
        'ftp_host': ftp_host, 'ftp_path': ftp_path, 'ftp_user' :ftp_user, 'ftp_passw': ftp_passw}
        
        non_auphonic_types = (raw_input('Would you to define non auphonic filetypes to generate links for, e.g. "epub"? yn (Default:n): ') == ("y" or "Y" or "yes" or "Yes"))
        if non_auphonic_types:
            non_auphonic_types = raw_input('Specify a comma separated list of types, e.g. "epub, mobi, pdf": ')
            # Convert tags to list
            non_auphonic_types = non_auphonic_types.split(',')
            
            firtz_settings['non_auphonic_types'] = non_auphonic_types
            
        fism_settings['firtz_settings'] = firtz_settings
            
    if use_adn:
        adntoken = raw_input('Specify a token for app.net (you need a developer account OR you can go to http://dev-lite.jonathonduerig.com/): ')
        use_adn_as_firtz_comments = (raw_input('Would you like to use the app.net for comments in the Firtz? yn (Default:n): ') == ("y" or "Y" or "yes" or "Yes"))
        
        adn_settings = {'adntoken': adntoken, 'use_adn_as_firtz_comments': use_adn_as_firtz_comments}
        fism_settings['adn_settings'] = adn_settings
    
    settings = {'fism_settings': fism_settings}
    filename = "settings.json"
    filename = raw_input('Specify a filename for the settings file. (Default: "settings.json"): ') or "settings.json"
    if not filename.endswith('.json'):
        filename = filename + '.json'
    print "Writing settings to " + filename
    f = open(filename, 'w')
    f.write(json.dumps(settings))
    f.close()
    
if __name__ == '__main__':
	main()
