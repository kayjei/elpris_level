"""
A sensor created to read temperature from myUplink public API
For more details about this platform, please refer to the documentation at
https://github.com/kayjei/homeassistant-myuplink

For API documentation, refer to https://dev.myuplink.com/ and swagger https://api.myuplink.com/swagger/index.html
"""
from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant.helpers.entity import Entity
from .calculate import levelCalculation
import dateutil.parser as dp
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_ENTITY_ID

import logging

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ENTITY_ID): cv.string
})

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the sensor platform"""
    #_LOGGER.debug(hass.data["nordpool"])
    #_LOGGER.debug(config)
 
    current = None
    data = None
    level = None

    devices = []
    
    devices.append(SensorDevice(hass, config, level, current, data))

    add_devices(devices)

class SensorDevice(Entity):
    def __init__(self, hass, config, value, current, data):
        self._config = config
        self._entity_id = 'sensor.elpris_level'
        self._value = value
        self._current = current
        self._data = data
        self._hass = hass
        self.update()

    def update(self):
        """Temperature"""
        level = levelCalculation.do_calculate(self._hass, self._config)
        _LOGGER.debug("Updating: %s", self._entity_id)
        self._value = level

    @property
    def unique_id(self):
        """Return the id of the sensor"""
        return self._entity_id

    @property
    def name(self):
        return "Elpris nivå"

    @property
    def state(self):
        """Return the state of the sensor"""
        return self._value

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        _LOGGER.debug("Trying attributes")
        return levelCalculation.attr_calculate(self._hass, self._config)