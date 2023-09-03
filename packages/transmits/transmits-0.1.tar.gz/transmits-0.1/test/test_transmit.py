import unittest
from transmit import Transmit

class DataTransmit(unittest.TestCase):

    def test_data_transmission(self):
        biu = Transmit()
        biu.to.data1 = 5
        self.assertEqual(biu.me.data1, 5)

if __name__ == '__main__':
    unittest.main()
