import os
from unittest import TestCase, mock
from broadband_cost import BroadBandCost


class TestApplicationController(TestCase):

    def setUp(self):
        cabinet_cost = 1000
        verge_cost = 50
        road_cost = 100
        chamber_cost = 200
        port_cost = 100
        self.broad_band_cost_obj = BroadBandCost(cabinet_cost, verge_cost, road_cost, chamber_cost, port_cost)

    @mock.patch.dict(os.environ, {"POT_COST_CALCULATE_DYNAMIC": "False"})
    def test_final_cost(self):
        result = self.broad_band_cost_obj.final_cost()
        message = "First value and response are not equal !"
        # firstValue = 42200
        firstValue = 133800
        self.assertEqual(os.environ["POT_COST_CALCULATE_DYNAMIC"], "False")
        self.assertEqual(firstValue, result, message)

    @mock.patch.dict(os.environ, {"POT_COST_CALCULATE_DYNAMIC": "True"})
    def test_final_cost_with_dynamic_pot_val(self):
        cabinet_cost = 1200
        verge_cost = 40
        road_cost = 80
        chamber_cost = 200
        port_cost = 20
        band_cost_obj = BroadBandCost(cabinet_cost, verge_cost, road_cost, chamber_cost, port_cost)
        result = band_cost_obj.final_cost()
        message = "First value and response are not equal !"
        firstValue = 52400

        self.assertEqual(firstValue, result, message)


if __name__ == '__main__':
    import unittest

    unittest.main()
