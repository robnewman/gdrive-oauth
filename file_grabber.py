#!/usr/bin/env python

# Super simple proof-of-concept script to
# download a gsheet from Google Drive

import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
# Try to load saved client credentials
gauth.LoadCredentialsFile("credentials.json")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("credentials.json")

drive = GoogleDrive(gauth)

# Grab the file of interest
file_name_to_download = "OAuth2-test-sheet"
file_name_downloaded = "OAuth2-test-sheet-NEW"

# Iterate through a list of files
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file1 in file_list:
    print 'title: %s, id: %s' % (file1['title'], file1['id'])
    if file1['title'] == file_name_to_download:
        print ' file Title identified: %s'% (file1['title']) 
        my_local_file = drive.CreateFile({'id': file1['id']})
        if os.path.exists("files/"+file_name_downloaded):
            os.remove("files/"+file_name_downloaded)
        my_local_file.GetContentFile(
            "files/"+file_name_downloaded,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        print '%s downloaded' % file_name_downloaded
        break
