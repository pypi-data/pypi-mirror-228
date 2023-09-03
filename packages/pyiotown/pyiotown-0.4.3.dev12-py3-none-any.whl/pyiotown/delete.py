import requests

def data(url, token, _id=None, nid=None, date_from=None, date_to=None, group_id=None, verify=True, timeout=60):
    header = {'Accept':'application/json','token':token}

    # only for administrators
    if group_id is not None:
        header['grpid'] = group_id

    uri = url + "/api/v1.0/data"

    params = []
    
    if nid != None:
        params.append(f"nid={nid}")
        
    if date_from != None:
        params.append(f"from={date_from}")

    if date_to != None:
        params.append(f"to={date_to}")

    if len(params) > 0:
        uri += '?' + '&'.join(params)
        
    result = None
    
    try:
        r = requests.delete(uri, headers=header, verify=verify, timeout=timeout)
    except Exception as e:
        print(e)
        return None
    
    if r.status_code == 200:
        return r.json()
    else:
        return None
