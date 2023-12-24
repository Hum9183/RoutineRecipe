# -*- coding: utf-8 -*-
from ..enums import PortType
from ..node_data import NodeDataModel, NodeData
from ..nodedata.flow_data import FlowData
from ..nodedata.string_data import StringData


class PrintModel(NodeDataModel):
    name = 'PrintModel'
    caption = 'print'
    caption_visible = True
    num_ports = {
        PortType.input: 2,
        PortType.output: 1,
    }
    data_type = {
        PortType.input: {
            0: FlowData.data_type,
            1: StringData.data_type,
        },
        PortType.output: {
            0: FlowData.data_type,
        }
    }

    def __init__(self, style=None, parent=None):
        super().__init__(style=style, parent=parent)
        self.__node_data: StringData = None

    def set_in_data(self, node_data: NodeData, port):
        self.__node_data = node_data
        self.data_updated.emit(0)

    def embedded_widget(self):
        ...

    def source_code(self) -> str:  # add
        text: str = self.__node_data.string
        return f'print(\'{text}\')'
