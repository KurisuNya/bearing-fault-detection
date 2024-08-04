from copy import deepcopy
from typing import Any

from PySide6.QtWidgets import QVBoxLayout, QWidget

from ..algorithm.param import Param, ParamError, ParamType
from .param_ui import Ui_Form


class OneLineEditWidget(QWidget):
    __type: ParamType

    def __init__(self, name: str, type: ParamType, value: Any = None):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.label.setText(name)
        self.__type = type
        self.set_value(value)

    def get_name(self):
        return self.ui.label.text()

    def set_value(self, value):
        if value is None:
            self.ui.lineEdit.setText("")
        else:
            self.ui.lineEdit.setText(self.__type.to_string(value))

    def get_value(self):
        return self.__type.to_value(self.ui.lineEdit.text())


class ParamsWidget(QWidget):
    __params: dict[str, Param]

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

    def set_params_widget(self, params: dict[str, Param]):
        self.__params = params
        self.__delete_params_widget()
        self.__set_params_widget()

    def reset_params_widget(self):
        self.__delete_params_widget()
        self.__set_params_widget()

    def __delete_params_widget(self):
        layout = self.layout()
        for i in range(layout.count()):
            layout.itemAt(i).widget().deleteLater()

    def __set_params_widget(self):
        layout = self.layout()
        for name, param in self.__params.items():
            layout.addWidget(
                OneLineEditWidget(
                    name,
                    param.get_type(),
                    param.get_value(),
                )
            )

    def get_params(self):
        try:
            self.__update_params()
            return deepcopy(self.__params)
        finally:
            self.reset_params_widget()

    def __update_params(self):
        widgets_count = self.layout().count()
        widgets = [self.layout().itemAt(i).widget() for i in range(widgets_count)]
        error = {}
        for widget in widgets:
            try:
                name = widget.get_name()  # type: ignore
                value = widget.get_value()  # type: ignore
                self.__params[name].set_value(value)
            except Exception as e:
                error[widget.get_name()] = e  # type: ignore
        if error:
            raise ParamError(error)
