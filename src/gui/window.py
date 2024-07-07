from copy import deepcopy
from typing import Any

from PySide6.QtWidgets import QMainWindow, QWidget
from PySide6.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvas  # type: ignore
from matplotlib.figure import Figure

from ..algorithm.param import Param, ParamError
from .param_ui import Ui_Form
from .window_ui import Ui_MainWindow


class OneLineEditWidget(QWidget):
    __type: type

    def __init__(self, name: str, type: type, value: Any = None):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.label.setText(name)
        self.__type = type
        self.set_value(value)

    def get_name(self):
        return self.ui.label.text()

    def set_value(self, value):
        if not value:
            self.ui.lineEdit.setText("")
        else:
            self.ui.lineEdit.setText(str(value))

    def get_value(self):
        value_str = self.ui.lineEdit.text()
        if value_str == "":
            return None
        return self.__type(self.ui.lineEdit.text())


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
        error = {}
        widgets = [
            self.layout().itemAt(i).widget() for i in range(self.layout().count())
        ]
        for widget in widgets:
            try:
                name = widget.get_name()  # type: ignore
                value = widget.get_value()  # type: ignore
                self.__params[name].set_value(value)
            except Exception as e:
                error[widget.get_name()] = e  # type: ignore
        if error:
            raise ParamError(error)


class MainWindow(QMainWindow):
    __aboveFigureCanvas: FigureCanvas
    __belowFigureCanvas: FigureCanvas
    __params_widget: ParamsWidget

    def __init__(self):
        def print_param(params: dict[str, Param]):
            for name, param in params.items():
                print(name, param.get_value())

        super().__init__()
        self.ui = Ui_MainWindow()
        self.__init_ui()
        self.ui.setParamButton.clicked.connect(
            lambda: print_param(self.__params_widget.get_params())
        )
        self.ui.resetParamButton.clicked.connect(
            self.__params_widget.reset_params_widget
        )

    def __init_ui(self):
        self.ui.setupUi(self)
        self.__aboveFigureCanvas = FigureCanvas()
        self.__belowFigureCanvas = FigureCanvas()
        self.__params_widget = ParamsWidget()
        self.ui.centerVerticalLayout.replaceWidget(
            self.ui.aboveFigure, self.__aboveFigureCanvas
        )
        self.ui.centerVerticalLayout.replaceWidget(
            self.ui.belowFigure, self.__belowFigureCanvas
        )
        self.ui.rightVerticalLayout.replaceWidget(
            self.ui.paramWidget, self.__params_widget
        )

        def check_positive(value):
            if value <= 0:
                raise ParamError("Value must be positive")

        params = {
            "param1": Param(int, 1, [check_positive]),
            "param2": Param(str, "test"),
            "param3": Param(float, 1.0, [check_positive]),
        }
        self.__params_widget.set_params_widget(params)
