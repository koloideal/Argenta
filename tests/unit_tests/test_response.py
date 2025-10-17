import unittest
from datetime import datetime, date
from typing import Any

from argenta.response.entity import Response, DataBridge, EMPTY_INPUT_FLAGS
from argenta.response.status import ResponseStatus
from argenta.command.flag.flags.models import InputFlags
from argenta.command.flag import InputFlag


class TestDataBridge(unittest.TestCase):
    def setUp(self):
        """Clear data before each test"""
        DataBridge.clear_data()

    def tearDown(self):
        """Clear data after each test"""
        DataBridge.clear_data()

    def test_update_data_basic(self):
        """Test basic data update functionality"""
        test_data = {"key1": "value1", "key2": "value2"}
        DataBridge.update_data(test_data)
        self.assertEqual(DataBridge.get_data(), test_data)

    def test_update_data_with_datetime(self):
        """Test updating data with datetime objects"""
        test_datetime = datetime(2024, 1, 15, 10, 30, 45)
        test_data = {"created_at": test_datetime, "name": "test"}
        DataBridge.update_data(test_data)
        
        result = DataBridge.get_data()
        self.assertEqual(result["created_at"], test_datetime)
        self.assertEqual(result["name"], "test")

    def test_update_data_with_date(self):
        """Test updating data with date objects"""
        test_date = date(2024, 1, 15)
        test_data = {"birth_date": test_date, "active": True}
        DataBridge.update_data(test_data)
        
        result = DataBridge.get_data()
        self.assertEqual(result["birth_date"], test_date)
        self.assertEqual(result["active"], True)

    def test_update_data_multiple_calls(self):
        """Test multiple update_data calls merge data"""
        first_data = {"key1": "value1", "date1": date(2024, 1, 1)}
        second_data = {"key2": "value2", "date2": datetime(2024, 2, 1, 12, 0)}
        
        DataBridge.update_data(first_data)
        DataBridge.update_data(second_data)
        
        result = DataBridge.get_data()
        self.assertEqual(len(result), 4)
        self.assertEqual(result["key1"], "value1")
        self.assertEqual(result["key2"], "value2")
        self.assertEqual(result["date1"], date(2024, 1, 1))
        self.assertEqual(result["date2"], datetime(2024, 2, 1, 12, 0))

    def test_update_data_overwrites_existing_keys(self):
        """Test that update_data overwrites existing keys"""
        initial_data = {"key": "old_value", "date": date(2024, 1, 1)}
        updated_data = {"key": "new_value", "date": date(2024, 2, 1)}
        
        DataBridge.update_data(initial_data)
        DataBridge.update_data(updated_data)
        
        result = DataBridge.get_data()
        self.assertEqual(result["key"], "new_value")
        self.assertEqual(result["date"], date(2024, 2, 1))

    def test_get_data_empty(self):
        """Test get_data returns empty dict when no data"""
        result = DataBridge.get_data()
        self.assertEqual(result, {})

    def test_clear_data(self):
        """Test clear_data removes all data"""
        test_data = {"key": "value", "timestamp": datetime.now()}
        DataBridge.update_data(test_data)
        
        # Verify data exists
        self.assertNotEqual(DataBridge.get_data(), {})
        
        # Clear and verify
        DataBridge.clear_data()
        self.assertEqual(DataBridge.get_data(), {})

    def test_delete_from_data(self):
        """Test delete_from_data removes specific key"""
        test_data = {
            "key1": "value1", 
            "key2": "value2",
            "created_at": datetime(2024, 1, 1, 10, 0)
        }
        DataBridge.update_data(test_data)
        
        # Delete one key
        DataBridge.delete_from_data("key1")
        
        result = DataBridge.get_data()
        self.assertEqual(len(result), 2)
        self.assertNotIn("key1", result)
        self.assertIn("key2", result)
        self.assertIn("created_at", result)

    def test_delete_from_data_nonexistent_key(self):
        """Test delete_from_data with nonexistent key raises KeyError"""
        test_data = {"existing_key": "value"}
        DataBridge.update_data(test_data)
        
        with self.assertRaises(KeyError):
            DataBridge.delete_from_data("nonexistent_key")


class TestResponse(unittest.TestCase):
    def setUp(self):
        """Clear data before each test"""
        DataBridge.clear_data()

    def tearDown(self):
        """Clear data after each test"""
        DataBridge.clear_data()

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

    def test_response_inherits_databridge_functionality(self):
        """Test that Response inherits DataBridge methods"""
        response = Response(ResponseStatus.ALL_FLAGS_VALID)
        test_data = {"message": "hello", "timestamp": datetime.now()}
        
        # Test update_data
        response.update_data(test_data)
        result = response.get_data()
        self.assertEqual(result["message"], "hello")
        self.assertIsInstance(result["timestamp"], datetime)

    def test_response_data_passing_with_dates(self):
        """Test passing date and datetime objects through Response"""
        response = Response(ResponseStatus.ALL_FLAGS_VALID)
        
        current_time = datetime.now()
        today = date.today()
        
        date_data = {
            "current_datetime": current_time,
            "current_date": today,
            "custom_datetime": datetime(2024, 3, 15, 14, 30, 0),
            "custom_date": date(2023, 12, 25),
            "metadata": {"created": current_time, "updated": today}
        }
        
        response.update_data(date_data)
        retrieved_data = response.get_data()
        
        # Verify datetime objects are preserved
        self.assertEqual(retrieved_data["current_datetime"], current_time)
        self.assertEqual(retrieved_data["current_date"], today)
        self.assertEqual(retrieved_data["custom_datetime"], datetime(2024, 3, 15, 14, 30, 0))
        self.assertEqual(retrieved_data["custom_date"], date(2023, 12, 25))
        
        # Verify nested datetime objects
        self.assertEqual(retrieved_data["metadata"]["created"], current_time)
        self.assertEqual(retrieved_data["metadata"]["updated"], today)

    def test_response_data_persistence_across_instances(self):
        """Test that data persists across different Response instances"""
        # First response instance
        response1 = Response(ResponseStatus.ALL_FLAGS_VALID)
        test_datetime = datetime(2024, 1, 1, 12, 0, 0)
        response1.update_data({"session_start": test_datetime})
        
        # Second response instance
        response2 = Response(ResponseStatus.UNDEFINED_FLAGS)
        retrieved_data = response2.get_data()
        
        # Data should persist
        self.assertEqual(retrieved_data["session_start"], test_datetime)

    def test_response_data_complex_date_scenarios(self):
        """Test complex scenarios with date/datetime handling"""
        response = Response(ResponseStatus.ALL_FLAGS_VALID)
        
        # Create complex data structure with various date formats
        complex_data = {
            "user": {
                "name": "John Doe",
                "birth_date": date(1990, 5, 15),
                "last_login": datetime(2024, 1, 15, 10, 30, 45),
                "preferences": {
                    "timezone": "UTC",
                    "date_format": "%Y-%m-%d",
                    "created_at": datetime(2023, 1, 1, 0, 0, 0)
                }
            },
            "events": [
                {"name": "login", "timestamp": datetime(2024, 1, 15, 10, 30, 45)},
                {"name": "logout", "timestamp": datetime(2024, 1, 15, 18, 45, 30)},
            ],
            "dates_list": [
                date(2024, 1, 1),
                date(2024, 1, 2),
                date(2024, 1, 3)
            ]
        }
        
        response.update_data(complex_data)
        retrieved_data = response.get_data()
        
        # Verify all date/datetime objects are correctly preserved
        self.assertEqual(retrieved_data["user"]["birth_date"], date(1990, 5, 15))
        self.assertEqual(retrieved_data["user"]["last_login"], datetime(2024, 1, 15, 10, 30, 45))
        self.assertEqual(retrieved_data["user"]["preferences"]["created_at"], datetime(2023, 1, 1, 0, 0, 0))
        
        # Verify dates in lists
        self.assertEqual(len(retrieved_data["events"]), 2)
        self.assertEqual(retrieved_data["events"][0]["timestamp"], datetime(2024, 1, 15, 10, 30, 45))
        self.assertEqual(retrieved_data["events"][1]["timestamp"], datetime(2024, 1, 15, 18, 45, 30))
        
        # Verify date list
        self.assertEqual(len(retrieved_data["dates_list"]), 3)
        self.assertEqual(retrieved_data["dates_list"][0], date(2024, 1, 1))
        self.assertEqual(retrieved_data["dates_list"][1], date(2024, 1, 2))
        self.assertEqual(retrieved_data["dates_list"][2], date(2024, 1, 3))

    def test_response_clear_data_functionality(self):
        """Test clearing data functionality through Response"""
        response = Response(ResponseStatus.ALL_FLAGS_VALID)
        
        # Add some data with dates
        response.update_data({
            "timestamp": datetime.now(),
            "date": date.today(),
            "message": "test"
        })
        
        # Verify data exists
        self.assertNotEqual(response.get_data(), {})
        
        # Clear data
        response.clear_data()
        
        # Verify data is cleared
        self.assertEqual(response.get_data(), {})

    def test_response_delete_specific_date_data(self):
        """Test deleting specific date-related data"""
        response = Response(ResponseStatus.ALL_FLAGS_VALID)
        
        # Add mixed data
        test_data = {
            "start_date": date(2024, 1, 1),
            "end_date": date(2024, 12, 31),
            "created_at": datetime.now(),
            "name": "test_session"
        }
        response.update_data(test_data)
        
        # Delete specific date field
        response.delete_from_data("start_date")
        
        result = response.get_data()
        self.assertNotIn("start_date", result)
        self.assertIn("end_date", result)
        self.assertIn("created_at", result)
        self.assertIn("name", result)

    def test_response_status_types(self):
        """Test Response with different status types"""
        statuses = [
            ResponseStatus.ALL_FLAGS_VALID,
            ResponseStatus.UNDEFINED_FLAGS,
            ResponseStatus.INVALID_VALUE_FLAGS,
            ResponseStatus.UNDEFINED_AND_INVALID_FLAGS
        ]
        
        for status in statuses:
            response = Response(status)
            response.update_data({"timestamp": datetime.now(), "status_test": True})
            
            self.assertEqual(response.status, status)
            self.assertIn("timestamp", response.get_data())
            self.assertIn("status_test", response.get_data())


if __name__ == '__main__':
    unittest.main()