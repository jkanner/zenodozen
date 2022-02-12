# zenodozen

A client for the zenodo API.

### Example Use Case

    import zenodozen as zz

    #-- Read token
    token = zz.readtoken(fn='/path/to/token/.zenodo-sandbox')

    #-- Get record of existing Zenodo entry
    response = zz.retrieve('748570', token)

    # -- Add files
    for fn in glob('/path/to/files/GW*'):
        zz.push_file(fn, token, response, scope='IGWN', project='GWTC2', version='1')
