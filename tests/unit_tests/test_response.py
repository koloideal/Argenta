import unittest
from datetime import date, datetime

from argenta.data_bridge import DataBridge
from argenta.command.flag.models import InputFlag
from argenta.command.flag.flags.models import InputFlags
from argenta.response.entity import EMPTY_INPUT_FLAGS, Response
from argenta.response.status import ResponseStatus


class TestDataBridge(unittest.TestCase):
    def setUp(self):
        """Create a new DataBridge instance for each test"""
        self.data_bridge = DataBridge()

    def test_update_data_basic(self):
        """Test basic data update functionality"""
        test_data = {"key1": "value1", "key2": "value2"}
        self.data_bridge.update(test_data)
        self.assertEqual(self.data_bridge.get_all(), test_data)

    def test_update_data_with_datetime(self):
        """Test updating data with datetime objects"""
        test_datetime = datetime(2024, 1, 15, 10, 30, 45)
        test_data = {"created_at": test_datetime, "name": "test"}
        self.data_bridge.update(test_data)

        result = self.data_bridge.get_all()
        self.assertEqual(result["created_at"], test_datetime)
        self.assertEqual(result["name"], "test")

    def test_update_data_multiple_calls(self):
        """Test multiple update calls merge data"""
        first_data = {"key1": "value1"}
        second_data = {"key2": "value2"}
        self.data_bridge.update(first_data)
        self.data_bridge.update(second_data)
        self.assertEqual(len(self.data_bridge.get_all()), 2)

    def test_get_data_empty(self):
        """Test get_all returns empty dict when no data"""
        self.assertEqual(self.data_bridge.get_all(), {})

    def test_clear_data(self):
        """Test clear_all removes all data"""
        self.data_bridge.update({"key": "value"})
        self.assertNotEqual(self.data_bridge.get_all(), {})
        self.data_bridge.clear_all()
        self.assertEqual(self.data_bridge.get_all(), {})

    def test_delete_from_data(self):
        """Test delete_by_key removes specific key"""
        test_data = {"key1": "value1", "key2": "value2"}
        self.data_bridge.update(test_data)
        self.data_bridge.delete_by_key("key1")
        result = self.data_bridge.get_all()
        self.assertNotIn("key1", result)
        self.assertIn("key2", result)

    def test_delete_from_data_nonexistent_key(self):
        """Test delete_by_key with nonexistent key raises KeyError"""
        with self.assertRaises(KeyError):
            self.data_bridge.delete_by_key("nonexistent_key")

    def test_get_by_key(self):
        """Test get_by_key retrieves correct value"""
        test_data = {"key1": "value1", "key2": date(2024, 1, 1)}
        self.data_bridge.update(test_data)
        self.assertEqual(self.data_bridge.get_by_key("key1"), "value1")
        self.assertEqual(self.data_bridge.get_by_key("key2"), date(2024, 1, 1))
        self.assertIsNone(self.data_bridge.get_by_key("nonexistent"))


class TestResponse(unittest.TestCase):
    def test_response_initialization_basic(self):
        """Test basic Response initialization"""
        response = Response(ResponseStatus.ALL_FLAGS_VALID)
        self.assertEqual(response.status, ResponseStatus.ALL_FLAGS_VALID)
        self.assertEqual(response.input_flags, EMPTY_INPUT_FLAGS)

    def test_response_initialization_with_flags(self):
        """Test Response initialization with input flags"""
        input_flags = InputFlags([InputFlag('test', input_value='value', status=None)])
        response = Response(ResponseStatus.INVALID_VALUE_FLAGS, input_flags)
        self.assertEqual(response.status, ResponseStatus.INVALID_VALUE_FLAGS)
        self.assertEqual(response.input_flags, input_flags)

    def test_response_status_types(self):
        """Test Response with different status types"""
        statuses = [
            ResponseStatus.ALL_FLAGS_VALID,
            ResponseStatus.UNDEFINED_FLAGS,
            ResponseStatus.INVALID_VALUE_FLAGS,
            ResponseStatus.UNDEFINED_AND_INVALID_FLAGS
        ]
        for status in statuses:
            with self.subTest(status=status):
                response = Response(status)
                self.assertEqual(response.status, status)


if __name__ == '__main__':
    unittest.main()