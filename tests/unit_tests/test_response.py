from datetime import date, datetime

import pytest

from argenta.command import InputFlags
from argenta.command.flag.models import InputFlag
from argenta.data_bridge import DataBridge
from argenta.response.entity import EMPTY_INPUT_FLAGS, Response
from argenta.response.status import ResponseStatus


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def data_bridge() -> DataBridge:
    """Create a new DataBridge instance for each test"""
    return DataBridge()


# ============================================================================
# Tests for DataBridge - basic data operations
# ============================================================================


def test_databridge_update_stores_basic_data(data_bridge: DataBridge) -> None:
    """Test basic data update functionality"""
    test_data = {"key1": "value1", "key2": "value2"}
    data_bridge.update(test_data)
    assert data_bridge.get_all() == test_data


def test_databridge_update_stores_datetime_objects(data_bridge: DataBridge) -> None:
    """Test updating data with datetime objects"""
    test_datetime = datetime(2024, 1, 15, 10, 30, 45)
    test_data = {"created_at": test_datetime, "name": "test"}
    data_bridge.update(test_data)

    result = data_bridge.get_all()
    assert result["created_at"] == test_datetime
    assert result["name"] == "test"


def test_databridge_multiple_updates_merge_data(data_bridge: DataBridge) -> None:
    """Test multiple update calls merge data"""
    first_data = {"key1": "value1"}
    second_data = {"key2": "value2"}
    data_bridge.update(first_data)
    data_bridge.update(second_data)
    assert len(data_bridge.get_all()) == 2


# ============================================================================
# Tests for DataBridge - data retrieval
# ============================================================================


def test_databridge_get_all_returns_empty_dict_initially(data_bridge: DataBridge) -> None:
    """Test get_all returns empty dict when no data"""
    assert data_bridge.get_all() == {}


def test_databridge_get_by_key_retrieves_correct_values(data_bridge: DataBridge) -> None:
    """Test get_by_key retrieves correct value"""
    test_data = {"key1": "value1", "key2": date(2024, 1, 1)}
    data_bridge.update(test_data)
    assert data_bridge.get_by_key("key1") == "value1"
    assert data_bridge.get_by_key("key2") == date(2024, 1, 1)


def test_databridge_get_by_key_returns_none_for_missing_key(data_bridge: DataBridge) -> None:
    """Test get_by_key returns None for nonexistent key"""
    test_data = {"key1": "value1"}
    data_bridge.update(test_data)
    assert data_bridge.get_by_key("nonexistent") is None


# ============================================================================
# Tests for DataBridge - data deletion
# ============================================================================


def test_databridge_clear_all_removes_all_data(data_bridge: DataBridge) -> None:
    """Test clear_all removes all data"""
    data_bridge.update({"key": "value"})
    assert data_bridge.get_all() != {}
    data_bridge.clear_all()
    assert data_bridge.get_all() == {}


def test_databridge_delete_by_key_removes_specific_key(data_bridge: DataBridge) -> None:
    """Test delete_by_key removes specific key"""
    test_data = {"key1": "value1", "key2": "value2"}
    data_bridge.update(test_data)
    data_bridge.delete_by_key("key1")
    result = data_bridge.get_all()
    assert "key1" not in result
    assert "key2" in result


def test_databridge_delete_by_key_raises_error_for_missing_key(data_bridge: DataBridge) -> None:
    """Test delete_by_key with nonexistent key raises KeyError"""
    with pytest.raises(KeyError):
        data_bridge.delete_by_key("nonexistent_key")


# ============================================================================
# Tests for Response - initialization
# ============================================================================


def test_response_initializes_with_status_and_empty_flags() -> None:
    """Test basic Response initialization"""
    response = Response(ResponseStatus.ALL_FLAGS_VALID)
    assert response.status == ResponseStatus.ALL_FLAGS_VALID
    assert response.input_flags == EMPTY_INPUT_FLAGS


def test_response_initializes_with_status_and_input_flags() -> None:
    """Test Response initialization with input flags"""
    input_flags = InputFlags([InputFlag('test', input_value='value', status=None)])
    response = Response(ResponseStatus.INVALID_VALUE_FLAGS, input_flags)
    assert response.status == ResponseStatus.INVALID_VALUE_FLAGS
    assert response.input_flags == input_flags


# ============================================================================
# Tests for Response - status types
# ============================================================================


def test_response_accepts_all_status_types() -> None:
    """Test Response with different status types"""
    statuses = [
        ResponseStatus.ALL_FLAGS_VALID,
        ResponseStatus.UNDEFINED_FLAGS,
        ResponseStatus.INVALID_VALUE_FLAGS,
        ResponseStatus.UNDEFINED_AND_INVALID_FLAGS
    ]
    for status in statuses:
        response = Response(status)
        assert response.status == status
