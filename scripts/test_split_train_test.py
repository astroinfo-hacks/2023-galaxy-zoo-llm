import unittest
import split_train_test

class TestSplitTrainTest(unittest.TestCase):

    def setUp(self):
        # Test data
        self.test_data = [
            {
                "id": "1",
                "value": "test1"
            },
            {
                "id": "2",
                "value": "test2"
            },
            {
                "id": "3",
                "value": "test3"
            }
        ]

    def test_split_data(self):
        # Test case 1: 67% split
        train_data, test_data = split_train_test.split_data(self.test_data, 0.67)
        # Assert that the data was split correctly
        self.assertEqual(len(train_data), 2)
        self.assertEqual(len(test_data), 1)

        # Test case 2: 50% split
        train_data, test_data = split_train_test.split_data(self.test_data, 0.5)
        # Assert that the data was split correctly
        self.assertEqual(len(train_data), 1)
        self.assertEqual(len(test_data), 2)


if __name__ == '__main__':
    unittest.main()
