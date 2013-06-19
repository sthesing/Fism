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
from ftplib import FTP

class Firtz:
    """
    Class handling epi files for the firtz
    """
    def __init__(self, settings):
        self.settings = settings
        self.non_auphonic_types = settings['non_auphonic_types']
        self.base_audio_url = settings['base_audio_url']
        
        self.base_web_url = settings['base_web_url']
        self.ftp_host = settings['ftp_host']
        self.ftp_path = settings['ftp_path']
        self.ftp_user = settings['ftp_user']
        self.ftp_passw = settings['ftp_passw']
    
    def prepare_epi(self, slug, epi_dict=None, prep_epi=None):
        """
        Writes everything to the epi file that is not put there by
        auphonic.
        Optionally, it can take a dictionary containing key-value
        pairs for the Firtz's epi-files.
        It can also take a prepared epi-file and add to it.
        """
        
        # Open the epi file
        f = open(slug + '.epi', 'w')
        
        # Should a prepared epi file exist, dump its contents into the
        # new epi file
        if prep_epi:
            prep_epi = open(prep_epi, 'r')
            f.write(prep_epi.read())
        f.close()
        
        # Add list of media types that are not autocreated by auphonic
        # taken from the settings file
        
        # We just add this to the epi_dict, if it is present. If not, 
        # we create it.
        if not epi_dict:
            epi_dict = {}
        
        # Now add the filetypes and links to epi_dict
        for typ in self.non_auphonic_types:
            #f.write(typ + ':\n')
            #f.write(self.base_audio_url + slug + '.' + typ + '\n\n')
            epi_dict[typ] = self.base_audio_url + slug + '.' + typ
        
        self.write_to_epi(slug, epi_dict)
        
    def write_to_epi(self, slug, epi_dict):
        # Now let's write the epi_dict to the file. It's not being 
        # checked, first. So tread with care. 
        f = open(slug + '.epi', 'a')
        for key in epi_dict:
            f.write('\n'+ key + ':\n')
            f.write(epi_dict[key] + '\n')
        f.close()
        print 'Written to ' + slug + '.epi'
        
    def upload_epi(self, slug):
        
        print 'Uploading ' + slug + '.epi\n'
        ftp = FTP(self.ftp_host, self.ftp_user, self.ftp_passw)
        ftp.cwd(self.ftp_path)
        #ftp.storbinary('STOR ' + slug + '.epi', open(slug + '.epi', 'rb'))
        ftp.storlines('STOR ' + slug + '.epi', open(slug + '.epi'))
        ftp.quit()
        
        
