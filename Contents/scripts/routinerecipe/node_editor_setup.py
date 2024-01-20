# -*- coding: utf-8 -*-
from .nodeeditor.data_model_registry import DataModelRegistry
from .nodeeditor.flow_scene import FlowScene
from .nodeeditor.flow_view import FlowView
from .nodeeditor.enums import PortType
from .nodeeditor.nodedatamodels.print_model import PrintModel
from .nodeeditor.nodedatamodels.start_model import StartModel
from .nodeeditor.nodedatamodels.string_model import StringModel


def setup(app):
    registry = DataModelRegistry()
    registry.register_model(StartModel, category='systems')
    registry.register_model(PrintModel, category='cmds')
    registry.register_model(StringModel, category='variables')
    scene = FlowScene(registry=registry)

    connection_style = scene.style_collection.connection

    # Configure the style collection to use colors based on data types:
    connection_style.use_data_defined_colors = True

    view = FlowView(scene)
    view.resize(800, 600)

    start_node = scene.create_node(StartModel)
    print_node = scene.create_node(PrintModel)
    string_node = scene.create_node(StringModel)

    scene.create_connection(
        start_node[PortType.output][0],
        print_node[PortType.input][0],
    )
    scene.create_connection(
        string_node[PortType.output][0],
        print_node[PortType.input][1],
    )

    return scene, view
