"""
Zenodozen

A client for the zenodo API.

Example use case
================

    from zenodozen import *

    # -- List of files you want to add
    filelist = glob('./all_posterior_samples/GW*')

    #-- Read token
    token = readtoken(fn='/path/to/token/.zenodo-sandbox')

    #-- Get record of existing Zenodo entry
    response = retrieve('748570', token)

    # -- Add a bunch of files
    for fn in filelist:
        r =  push_file(fn, token, response, scope='IGWN', project='GWTC2', version='1')

(c) Jonah Kanner
"""

import requests
import json
import os
from glob import glob
from datetime import date

# -- Method to read your zenodo token from a file
def readtoken(fn='/home/jonah.kanner/.zenodo'):
    """
    fn should be the FILENAME of a file containing your zenodo token
    Keep your token secret!
    See: https://zenodo.org/account/settings/applications/tokens/new/
    """
    with open(fn, 'r') as fp:
        token = fp.read()
    return token

def pubdate(token, response, describe=None):
    """ 
    Update the published date to today
    """

    draft_url = response.json()['links']['latest_draft']
    data = {}
    data['metadata'] = response.json()["metadata"]
    params = {'access_token': token}
    headers = {"Content-Type": "application/json"}
    today = date.today().isoformat()

    data['metadata']['publication_date'] = today
    if describe is not None:
        data['metadata']['description'] = describe

    r = requests.put(draft_url, params=params, data=json.dumps(data), headers = {"Content-Type": "application/json"})
    return r
    

# -- Makes a new data set
def make_dataset(token, server='https://sandbox.zenodo.org'):
    """
    Creates a new dataset, and returns the zenodo response
    """
      
    # -- Make new entry on sandbox server
    headers = {"Content-Type": "application/json"}
    params = {'access_token': token}
    r = requests.post('{0}/api/deposit/depositions'.format(server),
                      params=params,
                      json={},
                      headers=headers)

    id = r.json()['id']
    print("Created new entry with id {}".format(id))
    return r


def push_file(path, token, response, scope='IGWN', project='GWTC2', version='1'):
    """
    Method to push a file to zenodo

    PATH should be the path to the file

    TOKEN should be your token

    RESPONSE should be the zenodo response for a data set, as aquired from MAKE_DATASET or RETRIEVE methods
    """
    
    # -- Set up basic info about request
    bucket_url = response.json()["links"]["bucket"]
    params = {'access_token': token}

    # -- Construct file name to be used in zenodo
    filename = os.path.basename(path)
    #filename = '{0}-{1}-v{2}-'.format(scope, project, version) + filename
    filename = '{0}-{1}-'.format(scope, project, version) + filename
    print(filename)


    # The target URL is a combination of the bucket link with the
    # desired filename seperated by a slash.
    with open(path, "rb") as fp:
        r = requests.put(
            "%s/%s" % (bucket_url, filename),
            data=fp,
            params=params,
        )
    return r


# NOTE
# Need to do this:  https://developers.zenodo.org/#new-version

def publish(token, response):
    url = response.json()['links']['publish']
    params = {'access_token': token}
    r = requests.post(
            url,
            params=params,
        )
    return r


def newversion(token, response, desc=None):
    """
    Creates a new version of a deposit
    """
    url = response.json()['links']["newversion"]
    print("url:", url)
    
    params = {'access_token': token}
    r = requests.post(
            url,
            params=params,
        )
    print("New Version response:")
    print(r.json())

    # -- Get response for new version
    draft_url = r.json()['links']['latest_draft']
    draft = requests.get(draft_url, params=params)
    return draft




def retrieve(recid, token, server='https://sandbox.zenodo.org'):
    """
    Retrieve the response for an existing zenodo record

    RECID should be the record ID for an existing zenodo record

    TOKEN should be your token
    """
    r = requests.get("{0}/api/deposit/depositions/{1}?access_token={2}".format(server, recid, token))
    print(json.dumps(r.json(), indent=2))
    return r


def delete_files(token, response):    
    """
    Deletes all files from a draft zenodo deposit
    """
    fileurl = response.json()['links']['files']
    filelist = requests.get(fileurl, params={'access_token':token})

    for item in filelist.json():
        url = item['links']['self']
        requests.delete(url, params={'access_token':token})

    print("Deleted files from draft")
    return filelist
