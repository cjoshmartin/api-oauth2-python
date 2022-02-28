import json
import datetime

from weight_api import get_weight
from withings_api_example.weight_utils import unit_conversion, kg_to_ibs
from tests.sample_weight_data import fake_response


def test_unit_conversion():
    unit = -3
    value = 86790
    expected = 86.790

    assert unit_conversion(unit, value) == expected


def test_kg_to_ibs():
    value = 86.790
    expected = 191.3392

    assert kg_to_ibs(value) == expected


def test_get_weight_api_works():
    measurements = fake_response.get('body').get("measuregrps")

    for measurement in measurements:
        date = measurement.get('date')
        for measure in measurement.get('measures'):
            unit = measure.get('unit')
            value = measure.get('value')
            type = measure.get('type')

            converted_date = datetime.datetime.fromtimestamp(date)

            if type == 1 or type == 8:
                print(f"{type} {converted_date.strftime('%m/%d/%y')} {round(kg_to_ibs(unit_conversion(unit, value)), 2)}Ibs")
            elif type == 6:
                print(f"{type} {converted_date.strftime('%m/%d/%y')} {round(unit_conversion(unit, value), 2)}%")

    assert True
