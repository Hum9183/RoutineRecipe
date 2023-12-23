# -*- coding: utf-8 -*-
from ..node_data import NodeData, NodeDataType


class StringData(NodeData):
    data_type = NodeDataType(id='StringData', name='String')

    def __init__(self, string: str):
        self.string: str = string
