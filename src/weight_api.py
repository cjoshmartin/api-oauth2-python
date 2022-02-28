import requests

def get_weight(access_token):
    # GET Some info with this token
    headers = {'Authorization': 'Bearer ' + access_token}
    payload = {
        'action': 'getmeas',
        "meastypes": "1,6,8",
        "category": "1",
        # "startdate": "1645833600",
        # "enddate": "2020-07-02"
    }

    # List devices of returned user
    r_getdevice = requests.post(
        f'https://wbsapi.withings.net/measure',
        headers=headers,
        data=payload
    )

    return r_getdevice
