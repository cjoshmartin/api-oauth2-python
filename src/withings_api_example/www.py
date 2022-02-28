import datetime

from flask import Flask, request, redirect, render_template, session
import requests

from weight_api import get_weight
from withings_api_example import config
from withings_api_example.weight_utils import kg_to_ibs, unit_conversion

app = Flask(__name__)

CLIENT_ID = config.get('withings_api_example', 'client_id')
CUSTOMER_SECRET = config.get('withings_api_example', 'customer_secret')
STATE = config.get('withings_api_example', 'state')
ACCOUNT_URL = config.get('withings_api_example', 'account_withings_url')
WBSAPI_URL = config.get('withings_api_example', 'wbsapi_withings_url')
CALLBACK_URI = config.get('withings_api_example', 'callback_uri')


@app.route("/")
def get_code():
    """
    Route to get the permission from an user to take his data.
    This endpoint redirects to a Withings' login page on which
    the user has to identify and accept to share his data
    """
    payload = {'response_type': 'code',  # imposed string by the api
               'client_id': CLIENT_ID,
               'state': STATE,
               'scope': 'user.metrics',  # see docs for enhanced scope
               'redirect_uri': CALLBACK_URI,  # URL of this app
               # 'mode': 'demo'  # Use demo mode, DELETE THIS FOR REAL APP
               }

    r_auth = requests \
        .get(
        'https://account.withings.com/oauth2_user/authorize2',
        params=payload
    )

    return redirect(r_auth.url)


@app.route("/get_token")
def get_token():
    """
    Callback route when the user has accepted to share his data.
    Once the auth has arrived Withings servers come back with
    an authentication code and the state code provided in the
    initial call
    """
    code = request.args.get('code')

    payload = {
        "action": "requesttoken",
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CUSTOMER_SECRET,
        'code': code,
        'redirect_uri': CALLBACK_URI
    }

    r_token = requests.post(
        'https://wbsapi.withings.net/v2/oauth2',
        data=payload
    ) \
        .json()

    access_token = r_token.get('body', '').get('access_token', "")
    session["token"] = access_token

    return redirect('/chart')


@app.route('/chart')
def get_chart():
    measurements = get_weight(access_token=session["token"]).json().get('body').get("measuregrps")

    weights = []
    dates = []

    for measurement in measurements:
        date = measurement.get('date')
        for measure in measurement.get('measures'):
            unit = measure.get('unit')
            value = measure.get('value')
            type = measure.get('type')

            converted_date = datetime.datetime.fromtimestamp(date)

            if type == 1:
                dates.append(converted_date.strftime('%m/%d/%y'))
                weights.append(round(kg_to_ibs(unit_conversion(unit, value)), 2))

    return render_template('index.html', data={'weights': weights, "dates": dates})