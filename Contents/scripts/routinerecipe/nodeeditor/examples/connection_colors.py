# -*- coding: utf-8 -*-
import sys
import logging

from PySide2 import QtWidgets

from ..node_data import NodeData, NodeDataModel, NodeDataType
from ..data_model_registry import DataModelRegistry
from ..flow_scene import FlowScene
from ..flow_view import FlowView
from ..enums import PortType


class MyNodeData(NodeData):
    data_type = NodeDataType(id='MyNodeData', name='My Node Data')


class SimpleNodeData(NodeData):
    data_type = NodeDataType(id='SimpleData', name='Simple Data')


class NaiveDataModel(NodeDataModel):
    name = 'NaiveDataModel'
    caption = 'Caption'
    caption_visible = True
    num_ports = {PortType.input: 2,
                 PortType.output: 2,
                 }
    data_type = {
        PortType.input: {
            0: MyNodeData.data_type,
            1: SimpleNodeData.data_type
        },
        PortType.output: {
            0: MyNodeData.data_type,
            1: SimpleNodeData.data_type
        },
    }

    def out_data(self, port_index):
        if port_index == 0:
            return MyNodeData()
        elif port_index == 1:
            return SimpleNodeData()

    def set_in_data(self, node_data, port):
        ...

    def embedded_widget(self):
        ...


def main(app):
    registry = DataModelRegistry()
    registry.register_model(NaiveDataModel, category='My Category')
    scene = FlowScene(registry=registry)

    connection_style = scene.style_collection.connection

    # Configure the style collection to use colors based on data types:
    connection_style.use_data_defined_colors = True

    view = FlowView(scene)
    view.setWindowTitle("Connection (data-defined) color example")
    view.resize(800, 600)

    node_a = scene.create_node(NaiveDataModel)
    node_b = scene.create_node(NaiveDataModel)

    scene.create_connection(node_a[PortType.output][0],
                            node_b[PortType.input][0],
                            )

    scene.create_connection(node_a[PortType.output][1],
                            node_b[PortType.input][1],
                            )

    return scene, view, [node_a, node_b]


def main_start():
    logging.basicConfig(level='DEBUG')
    app = QtWidgets.QApplication.instance()
    scene, view, nodes = main(app)
    view.show(dockable=True)
    sys.exit()
    app.exec_()
