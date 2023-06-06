"""Tests for the IPP sensor platform."""
from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest

from homeassistant.components.sensor import ATTR_OPTIONS
from homeassistant.const import ATTR_ICON, ATTR_UNIT_OF_MEASUREMENT, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.util import dt as dt_util

from tests.common import MockConfigEntry


@pytest.mark.usefixtures("entity_registry_enabled_by_default")
async def test_sensors(
    hass: HomeAssistant,
    entity_registry: er.EntityRegistry,
    mock_config_entry: MockConfigEntry,
    mock_ipp: AsyncMock,
) -> None:
    """Test the creation and values of the IPP sensors."""
    mock_config_entry.add_to_hass(hass)

    test_time = datetime(2019, 11, 11, 9, 10, 32, tzinfo=dt_util.UTC)
    with patch("homeassistant.components.ipp.sensor.utcnow", return_value=test_time):
        await hass.config_entries.async_setup(mock_config_entry.entry_id)
        await hass.async_block_till_done()

    state = hass.states.get("sensor.test_printer")
    assert state
    assert state.attributes.get(ATTR_ICON) == "mdi:printer"
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) is None
    assert state.attributes.get(ATTR_OPTIONS) == ["idle", "printing", "stopped"]

    entry = entity_registry.async_get("sensor.test_printer")
    assert entry
    assert entry.translation_key == "printer"

    state = hass.states.get("sensor.test_printer_black_ink")
    assert state
    assert state.attributes.get(ATTR_ICON) == "mdi:water"
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) is PERCENTAGE
    assert state.state == "58"

    state = hass.states.get("sensor.test_printer_photo_black_ink")
    assert state
    assert state.attributes.get(ATTR_ICON) == "mdi:water"
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) is PERCENTAGE
    assert state.state == "98"

    state = hass.states.get("sensor.test_printer_cyan_ink")
    assert state
    assert state.attributes.get(ATTR_ICON) == "mdi:water"
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) is PERCENTAGE
    assert state.state == "91"

    state = hass.states.get("sensor.test_printer_yellow_ink")
    assert state
    assert state.attributes.get(ATTR_ICON) == "mdi:water"
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) is PERCENTAGE
    assert state.state == "95"

    state = hass.states.get("sensor.test_printer_magenta_ink")
    assert state
    assert state.attributes.get(ATTR_ICON) == "mdi:water"
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) is PERCENTAGE
    assert state.state == "73"

    state = hass.states.get("sensor.test_printer_uptime")
    assert state
    assert state.attributes.get(ATTR_ICON) == "mdi:clock-outline"
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) is None
    assert state.state == "2019-11-11T09:10:02+00:00"

    entry = entity_registry.async_get("sensor.test_printer_uptime")
    assert entry
    assert entry.unique_id == "cfe92100-67c4-11d4-a45f-f8d027761251_uptime"


async def test_disabled_by_default_sensors(
    hass: HomeAssistant,
    init_integration: MockConfigEntry,
) -> None:
    """Test the disabled by default IPP sensors."""
    registry = er.async_get(hass)

    state = hass.states.get("sensor.test_printer_uptime")
    assert state is None

    entry = registry.async_get("sensor.test_printer_uptime")
    assert entry
    assert entry.disabled
    assert entry.disabled_by is er.RegistryEntryDisabler.INTEGRATION


async def test_missing_entry_unique_id(
    hass: HomeAssistant,
    mock_config_entry: MockConfigEntry,
    mock_ipp: AsyncMock,
) -> None:
    """Test the unique_id of IPP sensor when printer is missing identifiers."""
    mock_config_entry.unique_id = None
    mock_config_entry.add_to_hass(hass)

    await hass.config_entries.async_setup(mock_config_entry.entry_id)
    await hass.async_block_till_done()

    registry = er.async_get(hass)

    entity = registry.async_get("sensor.test_printer")
    assert entity
    assert entity.unique_id == f"{mock_config_entry.entry_id}_printer"
