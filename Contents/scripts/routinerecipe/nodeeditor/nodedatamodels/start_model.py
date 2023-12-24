# -*- coding: utf-8 -*-
from ..enums import PortType
from ..node_data import NodeDataModel
from ..nodedata.flow_data import FlowData


class StartModel(NodeDataModel):
    name = 'StartModel'
    caption = 'start'
    caption_visible = True
    num_ports = {
        PortType.input: 0,
        PortType.output: 1,
    }
    data_type = {
        PortType.output: {
            0: FlowData.data_type,
        },
    }

    def out_data(self, port_index):
        return FlowData()

    def set_in_data(self, node_data, port):
        ...

    def embedded_widget(self):
        ...
