import this
import logging
import time
import datetime
from statistics import mean

_LOGGER = logging.getLogger(__name__)

class levelCalculation:

    @staticmethod
    def do_calculate(hass, config):
        data = levelCalculation._get_price_data(hass, config, 'today')
        if data is None:
            return None

        current = levelCalculation._get_price_data(hass, config, config['entity_id'])

        ldiff = mean(data) - min(data)
        hdiff = max(data) - mean(data)
        tdiff = max(data) - min(data)

        lpercent = ldiff / tdiff
        hpercent = hdiff / tdiff

        off_peak = min(data) + (ldiff * hpercent)
        peak = mean(data) + (hdiff * lpercent)

        if current < off_peak:
            return 'off_peak'
        elif current > peak:
            return 'peak'
        else:
            return 'normal'


    @staticmethod
    def define_level(price, off_peak, peak):

            if price is None:
                return None
            elif float(price) < float(off_peak):
                return 'off_peak'
            elif float(price) > float(peak):
                return 'peak'
            else:
                return 'normal'


    @staticmethod
    def attr_calculate(hass, config):
        for day in ['today', 'tomorrow']:
            data = levelCalculation._get_price_data(hass, config, day)
            if data is None:
                return None

            ldiff = mean(data) - min(data)
            hdiff = max(data) - mean(data)
            tdiff = max(data) - min(data)

            lpercent = ldiff / tdiff
            hpercent = hdiff / tdiff

            off_peak = min(data) + (ldiff * hpercent)
            peak = mean(data) + (hdiff * lpercent)

            next_hour = int((datetime.datetime.now() + datetime.timedelta(hours=1)).strftime("%H"))

            if next_hour == 0 and day == 'tomorrow':
                next_hour_level = levelCalculation.define_level(data[next_hour], off_peak, peak)
                attr["next_hour"] = next_hour_level

            if day == 'today':
                next_hour_level = levelCalculation.define_level(data[next_hour], off_peak, peak)
                attrs = {"next_hour": next_hour_level, "today": {}, "tomorrow": {}}

            c = 0

            for i in data:

                level = levelCalculation.define_level(i, off_peak, peak)

                attrs[day][c] = { "price": i, "level": level }
                c += 1

        return attrs


    @staticmethod
    def _get_price_data(hass, config, value):
        data_obj = hass.states.get(config['entity_id'])

        if data_obj is None:
            return None

        data_obj = str(data_obj)
        oc = 0

        for i in data_obj.split(' '):
            if str(i).startswith(f"{value.lower()}="):
                break
            oc += 1

        if value == config['entity_id']:
            return float(data_obj.split(' ', oc)[oc].split('=')[1].split(';')[0])

        data = data_obj.split(' ', oc)[oc].split('[')[1].split(']')[0]
        list_obj = []
        _LOGGER.debug(data)
        for l in data.split(','):
            list_obj.append(float(l.strip()))

        _LOGGER.debug(list_obj)
        return list_obj