"""
PyPortal Smart Lighting Controller
Note: This helper was designed for the LIFX Smart Lighting API
--------------------------------------------------------------
https://learn.adafruit.com/pyportal-smart-lighting-controller

Brent Rubell for Adafruit Industries, 2019
"""
LIFX_URL = 'https://api.lifx.com/v1/lights/'

class LIFX_API:
    """
    Interface for the LIFX HTTP Remote API
    """
    def __init__(self, wifi, lifx_token):
        """
        :param wifi_manager wifi: WiFiManager object from ESPSPI_WiFiManager or ESPAT_WiFiManager
        :param str lifx_token: LIFX API token (https://api.developer.lifx.com/docs/authentication)
        """
        self._wifi = wifi
        self._lifx_token = lifx_token
        self._auth_header = {"Authorization": "Bearer %s" % self._lifx_token,}

    @staticmethod
    def parse_resp(response):
        """Parses a JSON response from the LIFX API
        """
        try:
            for res in response['results']:
                print(res['status'])
        except KeyError:
            print(response['error'])

    def list_lights(self):
        """Enumerates all the lights associated with the LIFX Cloud Account
        """
        response = self._wifi.get(
            url=LIFX_URL+'all',
            headers=self._auth_header
        )
        resp = response.json()
        response.close()
        return resp

    def toggle_light(self, selector, all_lights=False, duration=0):
        """Toggles current state of LIFX light(s).
        :param dict selector: Selector to control which lights are requested.
        :param bool all: Toggle all lights at once. Defaults to false.
        :param double duration: Time (in seconds) to spend performing a toggle. Defaults to 0.
        """
        if all_lights:
            selector = 'all'
        response = self._wifi.post(
            url=LIFX_URL+selector+'/toggle',
            headers = self._auth_header,
            json = {'duration':duration},
        )
        resp = response.json()
        # check the response
        if response.status_code == 422:
            raise Exception('Error, light(s) could not be toggled: '+ resp['error'])
        response.close()
        return resp

    def set_brightness(self, selector, brightness):
        """Sets the state of the lights within the selector.
        :param dict selector: Selector to control which lights are requested.
        :param double brightness: Brightness level of the light, from 0.0 to 1.0.
        """
        response = self._wifi.put(
            url=LIFX_URL+selector+'/state',
            headers=self._auth_header,
            json={'brightness':brightness}
        )
        resp = response.json()
        # check the response
        if response.status_code == 422:
            raise Exception('Error, light could not be set: '+ resp['error'])
        response.close()
        return resp

    def set_light(self, selector, power, color, brightness):
        """Sets the state of the lights within the selector.
        :param dict selector: Selector to control which lights are requested.
        :param str power: Sets the power state of the light (on/off).
        :param str color: Color to set the light to (https://api.developer.lifx.com/v1/docs/colors).
        :param double brightness: Brightness level of the light, from 0.0 to 1.0.
        """
        response = self._wifi.put(
            url=LIFX_URL+selector+'/state',
            headers=self._auth_header,
            json={'power':power,
                  'color':color,
                  'brightness':brightness
                 }
        )
        resp = response.json()
        # check the response
        if response.status_code == 422:
            raise Exception('Error, light could not be set: '+ resp['error'])
        response.close()
        return resp

    def move_effect(self, selector, move_direction, period, cycles, power_on):
        """Performs a linear move effect on a light, or lights.
        :param str move_direction: Move direction, forward or backward.
        :param double period: Time in second per effect cycle.
        :param float cycles: Number of times to move the pattern.
        :param bool power_on: Turn on a light before performing the move.
        """
        response = self._wifi.post(
            url=LIFX_URL+selector+'/effects/move',
            headers = self._auth_header,
            json = {'direction':move_direction,
                    'period':period,
                    'cycles':cycles,
                    'power_on':power_on},
        )
        resp = response.json()
        # check the response
        if response.status_code == 422:
            raise Exception('Error: '+ resp['error'])
        response.close()
        return resp

    def effects_off(self, selector):
        """Turns off any running effects on the selected device.
        :param dict selector: Selector to control which lights are requested.
        """
        response = self._wifi.post(
            url=LIFX_URL+selector+'/effects/off',
            headers=self._auth_header
        )
        resp = response.json()
        # check the response
        if response.status_code == 422:
            raise Exception('Error: '+ resp['error'])
        response.close()
        return resp
