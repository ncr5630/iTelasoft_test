# -*- coding: utf-8 -*-
# !/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals
import os, shutil
import json
import string
import networkx as nx
from benedict import benedict
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DATA_PATH = os.environ.get("DATA_PATH")
POT_COST_CALCULATE_DYNAMIC = os.environ.get("POT_COST_CALCULATE_DYNAMIC")


class BroadBandCost:
    def __init__(self, cabinet_cost, verge_cost, road_cost, chamber_cost, port_cost) -> None:
        self.cabinet_cost = cabinet_cost
        self.verge_cost = verge_cost
        self.road_cost = road_cost
        self.chamber_cost = chamber_cost
        self.port_cost = port_cost
        self.data_path = DATA_PATH


    @staticmethod
    def parse(text):
        try:
            return json.loads(text)
        except ValueError as e:
            return None

    def final_cost(self) -> float:
        """

        :rtype: float
        """
        point_cost = self.get_total_point_cost()
        cable_cost = self.get_total_cable_cost()
        return point_cost + cable_cost

    def get_total_point_cost(self) -> float:
        point_cost = 0

        data = self.read_data()

        record_data = [
            {"key": "Cabinet", "item_cost": self.cabinet_cost},
            {"key": "Chamber", "item_cost": self.chamber_cost}]

        if POT_COST_CALCULATE_DYNAMIC in [False, "false", "False", 0]:
            record_data.append({"key": "Pot", "item_cost": self.port_cost})
        else:

            point_cost += self.get_total_port_cost_with_variable_rate(data)

        for item in record_data:
            key = item.get("key")
            cost = item.get("item_cost")
            if key and cost:
                point_cost += self.get_point_cost(key, cost, data)

        return point_cost


    def get_total_cable_cost(self) -> float:
        record_data = [
            {"material": "verge", "item_cost": self.verge_cost},
            {"material": "road", "item_cost": self.road_cost}]
        cable_cost = 0
        data = self.read_data()
        for item in record_data:
            key = item.get("material", None)
            cost = item.get("item_cost", None)
            if key and cost:
                cable_cost += self.get_item_cable_cost(key, cost, data)

        return cable_cost

    @staticmethod
    def get_point_cost(node_key, cost, data_obj) -> float:
        records = 0
        for item in data_obj.get("nodes", []):
            record = item.get('data', None)
            if record == node_key:
                records += 1
        item_tot_cost = records * cost

        return item_tot_cost

    @staticmethod
    def get_item_cable_cost(material, item_cost, data_obj) -> float:

        tot_length = 0
        for item in data_obj.get("edges", []):
            item_data = benedict(item)
            record = item_data["data"]["material"] if "data.material" in item_data else None
            if record == material:
                length = item_data["data"]["length"] if "data.length" in item_data else 0
                tot_length += length
        item_length_cost = tot_length * item_cost

        return item_length_cost

    def read_data(self) -> string:
        cwd = os.getcwd()
        for filename in os.listdir(cwd + "/" + self.data_path):
            with open(cwd + "/" + self.data_path + '/' + filename) as f:
                data = f.read()
                if self.parse(data):
                    return self.parse(data)
                else:
                    print("Not Json %s " % filename)
                    return False


    def get_total_port_cost_with_variable_rate(self, data) -> float:
        start_id = 'A'
        get_all_pots_ids = self.get_all_pot_ids("Pot", data)
        total_length = 0
        for item in get_all_pots_ids:
            end_id = item
            step_data_list = self.graphml_data_read(start_id, end_id)
            length_pairs = self.convert_continues_length_pairs(step_data_list)
            for single_pair in length_pairs:
                length = self.get_id_pairs_actual_length(data, single_pair)
                total_length += length
        return total_length*self.port_cost

    def get_id_pairs_actual_length(self, data_obj, pair_val=list()):
        '''

        :param pair_val:
        :param data_obj:
        :return:
        if par_val ['B','F']
            then Pot length 20m
        '''


        pair_length = 0
        for item in data_obj.get("edges", []):
            record_data = []
            item_data = benedict(item)
            source = item.get('source', None)
            target = item.get('target', None)
            record_data.append(source)
            record_data.append(target)
            record_data.sort()
            pair_val.sort()

            if record_data == pair_val:
                pair_length = item["data"]["length"] if "data.length" in item_data else 0
                break
        return pair_length

    def get_all_pot_ids(self, node_key,data_obj):
        '''

            :param node_key: ie Pot
            :param data_obj:
            :return: all Pot ids
            ie: ['B','C','D','E']
        '''
        ids = list()
        for item in data_obj.get("nodes", []):
            record = item.get('data', None)
            id_val = item.get('id', None)
            if record == node_key and id_val:
                ids.append(id_val)

        return ids


    def convert_continues_length_pairs(self, data=list) -> list:
        '''

            :param data:
            :return:
            return given list continues items pairs
            ie data=['A', 'F', 'B']
            return [['A','F'],['F','B']]
        '''
        list_pairs = list()
        for first, second in zip(data, data[1:]):
            list_pairs.append([first, second])
        return list_pairs


    def graphml_data_read(self, start, end):
        """
            :param start:
            :param end:
            :return: path['A']['B'] ie. ['A', 'F', 'B']
            read problem.graphml file using networkx lib and return path for given start and end point
        """
        return_val = None
        try:
            G = nx.read_graphml('problem.graphml')
            path = dict(nx.all_pairs_dijkstra_path(G))
            return_val = path[start][end]
        except Exception as error:
            raise error

        return return_val



