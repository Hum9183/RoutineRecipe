# -*- coding: utf-8 -*-
from PySide2.QtGui import QDoubleValidator
from PySide2.QtWidgets import QLineEdit, QWidget

from ..enums import PortType
from ..node_data import NodeDataModel
from ..nodedata.string_data import StringData


class StringModel(NodeDataModel):
    name = 'StringModel'
    caption = 'String'
    caption_visible = True
    num_ports = {
        PortType.input: 0,
        PortType.output: 1,
    }
    data_type = {
        PortType.output: {
            0: StringData.data_type,
        },
    }

    def __init__(self, style=None, parent=None):
        super().__init__(style=style, parent=parent)
        self.__string: str = ''
        self._number = None

        self._line_edit = QLineEdit()
        self._line_edit.setValidator(QDoubleValidator())
        self._line_edit.setMaximumSize(self._line_edit.sizeHint())
        self._line_edit.textChanged.connect(self.on_text_edited)
        self._line_edit.setText("test")

    def out_data(self, port_index):
        return StringData(self.__string)

    @property
    def number(self):
        return self._number

    def save(self) -> dict:
        """Add to the JSON dictionary to save the state of the NumberSource"""
        doc = super().save()
        if self._number:
            doc['number'] = self._number.number
        return doc

    # def restore(self, state: dict):
    #     'Restore the number from the JSON dictionary'
    #     try:
    #         value = float(state["number"])
    #     except Exception:
    #         ...
    #     else:
    #         self._number = DecimalData(value)
    #         self._line_edit.setText(self._number.number_as_text())

    def embedded_widget(self) -> QWidget:
        """The number source has a line edit widget for the user to type in"""
        return self._line_edit

    def on_text_edited(self, string: str):
        """
        Line edit text has changed

        Parameters
        ----------
        string : str
        """
        try:
            string = self._line_edit.text()
        except ValueError:
            self._data_invalidated.emit(0)
        else:
            self.__string = string
            self.data_updated.emit(0)


#
# class NumberSourceDataModel(NodeDataModel):
#     name = "NumberSource"
#     caption_visible = False
#     num_ports = {PortType.input: 0,
#                  PortType.output: 1,
#                  }
#     port_caption = {'output': {0: 'Result'}}
#     data_type = DecimalData.data_type
#
#     def __init__(self, style=None, parent=None):
#         super().__init__(style=style, parent=parent)
#         self._number = None
#         self._line_edit = QLineEdit()
#         self._line_edit.setValidator(QDoubleValidator())
#         self._line_edit.setMaximumSize(self._line_edit.sizeHint())
#         self._line_edit.textChanged.connect(self.on_text_edited)
#         self._line_edit.setText("0.0")
#
#     @property
#     def number(self):
#         return self._number
#
#     def save(self) -> dict:
#         'Add to the JSON dictionary to save the state of the NumberSource'
#         doc = super().save()
#         if self._number:
#             doc['number'] = self._number.number
#         return doc
#
#     def restore(self, state: dict):
#         'Restore the number from the JSON dictionary'
#         try:
#             value = float(state["number"])
#         except Exception:
#             ...
#         else:
#             self._number = DecimalData(value)
#             self._line_edit.setText(self._number.number_as_text())
#
#     def out_data(self, port: int) -> NodeData:
#         '''
#         The data output from this node
#
#         Parameters
#         ----------
#         port : int
#
#         Returns
#         -------
#         value : NodeData
#         '''
#         return self._number
#
#     def embedded_widget(self) -> QWidget:
#         'The number source has a line edit widget for the user to type in'
#         return self._line_edit
#
#     def on_text_edited(self, string: str):
#         '''
#         Line edit text has changed
#
#         Parameters
#         ----------
#         string : str
#         '''
#         try:
#             number = float(self._line_edit.text())
#         except ValueError:
#             self._data_invalidated.emit(0)
#         else:
#             self._number = DecimalData(number)
#             self.data_updated.emit(0)
