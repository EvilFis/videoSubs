from app import *
import unittest
import json

# python -m unittest -v file.py

class TestApp(unittest.TestCase):
    
    def setUp(self) -> None:
        """
        Функция предобработки кода
        """
        return super().setUp()


    def tearDown(self) -> None:
        """
        Какие дейсвия необходимо выполнить после тестирования
        """
        return super().tearDown()


    def test_append_zero_time(self):
        # check type data
        self.assertEqual(type(append_zero_time(15)), str)
        self.assertEqual(type(append_zero_time(5)), str)
        self.assertEqual(type(append_zero_time(15.5)), str)
        self.assertEqual(type(append_zero_time(5.135)), str)

        # check result integer
        self.assertEqual(append_zero_time(5), "05")
        self.assertEqual(append_zero_time(10), "10")

        # check result float
        self.assertEqual(append_zero_time(1.15), "01.15")
        self.assertEqual(append_zero_time(10.98), "10.98")


    def test_time_filter(self):

        data = {
            "data_int": [15, 78, 11_745, 40_545, 92_942],
            "data_float": [15.189, 78.741, 11_745.23, 40_545.47, 92_942.985],
            "res_int": ["00:00:15:00", "00:01:18:00", "03:15:45:00", "11:15:45:00", "25:49:02:00"],
            "res_float": ["00:00:15:189", "00:01:18:741", "03:15:45:230", "11:15:45:470", "25:49:02:985"],
        }

        if len(data["data_int"]) != len(data["res_int"]) and len(data["data_float"]) != len(data["res_float"]):
            raise RuntimeError("The length of the input data does not match the output data")

        # check type data
        self.assertEqual(type(time_filter(15.15)), str)
        self.assertEqual(type(time_filter(78)), str)

        # check result int
        for i in range(len(data["data_int"])):
            self.assertEqual(time_filter(data["data_int"][i]), data["res_int"][i])

        # check result float
        for i in range(len(data["data_float"])):
            self.assertEqual(time_filter(data["data_float"][i]), data["res_float"][i])


    def test_audio_to_text_google(self):

        path='./test/src/audio.wav'
        offset_start = [0.660, 230.71]
        offset_end = [2.460, None]
        result=["hi this is Mark", "okay great job I'll see you next time take it easy by"] 

        if len(offset_start) != len(offset_end):
            raise RuntimeError("The length of the input data does not match the output data")

        for i in range(len(offset_start)):
            self.assertEqual(audio_to_text_google(
                path=path,
                offset_start=offset_start[i],
                offset_end=offset_end[i]
            ), result[i])


if __name__ == "__main__":
    unittest.main()
