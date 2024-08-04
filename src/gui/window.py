from copy import deepcopy
from typing import Any, Callable

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import QComboBox, QDialog, QMainWindow, QMessageBox
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ..algorithm.param import Param, ParamError
from .param import ParamsWidget
from .window_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    __aboveFigureCanvas: FigureCanvas
    __belowFigureCanvas: FigureCanvas
    __params_widget: ParamsWidget

    __client: int | None
    __magnet_distance: int = 1

    __client_change_hook: Callable[[int | None], Any]
    __algorithm_change_hook: Callable[[str], Any]
    __backend_calculation_hook: Callable[[bool], Any]
    __stop_calculation_hook: Callable[[bool], Any]
    __above_figure_change_hook: Callable[[str], Any]
    __below_figure_change_hook: Callable[[str], Any]

    def __init__(
        self,
        client_change_hook: Callable[[int | None], Any] = lambda client_id: None,
        algorithm_change_hook: Callable[[str], Any] = lambda algorithm_name: None,
        backend_calculation_hook: Callable[[bool], Any] = lambda state: None,
        stop_calculation_hook: Callable[[bool], Any] = lambda state: None,
        above_figure_change_hook: Callable[[str], Any] = lambda figure_name: None,
        below_figure_change_hook: Callable[[str], Any] = lambda figure_name: None,
        magnet_distance: int = 1,
    ):

        super().__init__()
        self.ui = Ui_MainWindow()
        self.__client = None
        self.__magnet_distance = magnet_distance
        self.__client_change_hook = client_change_hook
        self.__algorithm_change_hook = algorithm_change_hook
        self.__backend_calculation_hook = backend_calculation_hook
        self.__stop_calculation_hook = stop_calculation_hook
        self.__above_figure_change_hook = above_figure_change_hook
        self.__below_figure_change_hook = below_figure_change_hook

        self.__init_ui()
        self.__connect()

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

    def __connect(self):
        self.ui.clientComboBox.currentIndexChanged.connect(
            self.__on_client_change,
        )
        self.ui.algorithmComboBox.currentIndexChanged.connect(
            self.__on_algorithm_change
        )
        self.ui.stopAlgorithmButton.clicked.connect(
            self.__on_stop_calculation_click,
        )
        self.ui.backendCheckBox.stateChanged.connect(
            self.__on_backend_state_change,
        )
        self.ui.aboveFigureComboBox.currentIndexChanged.connect(
            self.__on_above_figure_change
        )
        self.ui.belowFigureComboBox.currentIndexChanged.connect(
            self.__on_below_figure_change
        )
        self.ui.setParamButton.clicked.connect(
            self.__on_params_change_button_click,
        )
        self.ui.resetParamButton.clicked.connect(
            self.__params_widget.reset_params_widget
        )

    # event handlers
    def __on_client_change(self, index: int):
        self.__temporally_disable_right_panel(1500)

        if index == -1:
            self.__set_client(None)
            return
        client_id = self.ui.clientComboBox.itemData(index)
        self.__set_client(client_id)

    def __on_algorithm_change(self, index: int):
        if index == -1:
            return
        self.__algorithm_change_hook(self.ui.algorithmComboBox.itemText(index))

    def __temporally_disable_right_panel(self, msec: int):
        def disable_all():
            self.ui.rightVerticalLayoutWidget.setEnabled(False)

        def enable_all():
            self.ui.rightVerticalLayoutWidget.setEnabled(True)
            timer.stop()

        timer = QTimer()
        timer.timeout.connect(enable_all)
        disable_all()
        timer.start(msec)

    def __on_stop_calculation_click(self):
        if self.ui.stopAlgorithmButton.text() == "暂停算法":
            self.ui.stopAlgorithmButton.setText("继续算法")
            self.__stop_calculation_hook(True)
        else:
            self.ui.stopAlgorithmButton.setText("暂停算法")
            self.__stop_calculation_hook(False)

    def __on_backend_state_change(self, state: bool):
        self.__backend_calculation_hook(state)

    def __on_above_figure_change(self, index: int):
        if index == -1:
            self.__set_above_figure(Figure())
            return
        figure_name = self.ui.aboveFigureComboBox.itemText(index)
        self.__set_above_figure(self.ui.aboveFigureComboBox.itemData(index))
        self.__above_figure_change_hook(figure_name)

    def __on_below_figure_change(self, index: int):
        if index == -1:
            self.__set_below_figure(Figure())
            return
        figure_name = self.ui.belowFigureComboBox.itemText(index)
        self.__set_below_figure(self.ui.belowFigureComboBox.itemData(index))
        self.__below_figure_change_hook(figure_name)

    def __on_params_change_button_click(self):
        try:
            params = self.__params_widget.get_params()
            self.__params_change_hook(params)
        except ParamError as e:
            self.__show_params_error(e)

    def __show_params_error(self, error: ParamError):
        errors = eval(str(error))
        msg = "请检查参数, 错误信息如下:\n"
        for name, e in errors.items():
            msg += f"{name}: {e}\n"
        self.msg_box = QMessageBox()
        self.msg_box.setWindowModality(Qt.WindowModality.NonModal)
        self.msg_box.setWindowTitle("参数错误")
        self.msg_box.setIcon(QMessageBox.Icon.Critical)
        self.msg_box.setText(msg)
        self.msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.msg_box.show()

    # hooks setters
    def set_client_change_hook(self, hook: Callable[[int | None], Any]):
        self.__client_change_hook = hook

    def set_algorithm_change_hook(self, hook: Callable[[str], Any]):
        self.__algorithm_change_hook = hook

    def set_stop_calculation_hook(self, hook: Callable[[bool], Any]):
        self.__stop_calculation_hook = hook

    def set_backend_calculation_hook(self, hook: Callable[[bool], Any]):
        self.__backend_calculation_hook = hook

    def set_above_figure_change_hook(self, hook: Callable[[str], Any]):
        self.__above_figure_change_hook = hook

    def set_below_figure_change_hook(self, hook: Callable[[str], Any]):
        self.__below_figure_change_hook = hook

    def set_params_change_hook(self, hook: Callable[[dict[str, Param]], Any]):
        self.__params_change_hook = hook

    # setters
    def set_msg(self, msg: str, scroll_to_bottom: bool = False):
        check_distance = (
            self.ui.msgPlainTextEdit.verticalScrollBar().maximum()
            - self.ui.msgPlainTextEdit.verticalScrollBar().value()
            < MainWindow.__magnet_distance
        )
        if scroll_to_bottom or check_distance:
            self.ui.msgPlainTextEdit.setPlainText(msg)
            self.ui.msgPlainTextEdit.verticalScrollBar().setValue(
                self.ui.msgPlainTextEdit.verticalScrollBar().maximum()
            )
        else:
            value = self.ui.msgPlainTextEdit.verticalScrollBar().value()
            self.ui.msgPlainTextEdit.setPlainText(msg)
            self.ui.msgPlainTextEdit.verticalScrollBar().setValue(value)

    def set_stop_calculation_state(self, state: bool):
        if state:
            self.ui.stopAlgorithmButton.setText("继续算法")
        else:
            self.ui.stopAlgorithmButton.setText("暂停算法")

    def set_stop_calculation_button(self, state: bool):
        self.ui.stopAlgorithmButton.setEnabled(state)

    def set_backend_calculation_state(self, state: bool):
        self.ui.backendCheckBox.setChecked(state)

    def set_backend_calculation_checkbox(self, state: bool):
        self.ui.backendCheckBox.setEnabled(state)

    def set_figure_combo_box(
        self,
        figures: dict[str, Figure],
        above_figure_name: str,
        below_figure_name: str,
        reset: bool = False,
    ):
        def check_names(figures: dict[str, Figure], names: list[str]) -> bool:
            new_names = set(figures.keys())
            old_names = set(names)
            return new_names == old_names

        def get_names(combo_box: QComboBox) -> list[str]:
            return [combo_box.itemText(i) for i in range(combo_box.count())]

        def reset_combo_box(
            combo_box: QComboBox,
            figures: dict[str, Figure],
            figure_name: str,
        ):
            combo_box.clear()
            for name in figures.keys():
                combo_box.addItem(name, figures[name])
            combo_box.setCurrentIndex(combo_box.findText(figure_name))

        def update_combo_box(
            combo_box: QComboBox,
            figures: dict[str, Figure],
            figure_name: str,
            old_figure_name: str,
        ):
            for name in figures.keys():
                combo_box.setItemData(combo_box.findText(name), figures[name])
            if old_figure_name != figure_name:
                combo_box.setCurrentIndex(combo_box.findText(figure_name))

        if check_names(figures, get_names(self.ui.aboveFigureComboBox)) and not reset:
            update_combo_box(
                self.ui.aboveFigureComboBox,
                figures,
                above_figure_name,
                self.ui.aboveFigureComboBox.currentText(),
            )
            self.__refresh_above_figure()
        else:
            reset_combo_box(self.ui.aboveFigureComboBox, figures, above_figure_name)

        if check_names(figures, get_names(self.ui.belowFigureComboBox)) and not reset:
            update_combo_box(
                self.ui.belowFigureComboBox,
                figures,
                below_figure_name,
                self.ui.belowFigureComboBox.currentText(),
            )
            self.__refresh_below_figure()
        else:
            reset_combo_box(self.ui.belowFigureComboBox, figures, below_figure_name)

    def clear_figure_combo_box(self):
        self.ui.aboveFigureComboBox.clear()
        self.ui.belowFigureComboBox.clear()

    def set_algorithm_combo_box(self, algorithms: list[str], algorithm: str):
        self.ui.algorithmComboBox.currentIndexChanged.disconnect()
        self.ui.algorithmComboBox.clear()
        self.ui.algorithmComboBox.addItems(algorithms)
        self.ui.algorithmComboBox.setCurrentIndex(
            self.ui.algorithmComboBox.findText(algorithm)
        )
        self.ui.algorithmComboBox.currentIndexChanged.connect(
            self.__on_algorithm_change
        )

    def clear_algorithm_combobox(self):
        self.ui.algorithmComboBox.clear()

    def set_result_label(self, label: str):
        self.ui.resultLabel.setText(label)

    def set_params(self, params: dict[str, Param]):
        self.__params_widget.set_params_widget(params)

    def clear_params(self):
        self.__params_widget.set_params_widget({})

    def add_client(self, client_id: int, client_name: str):
        self.ui.clientComboBox.addItem(client_name, client_id)

    def remove_client(self, client_id: int):
        index = self.ui.clientComboBox.findData(client_id)
        self.ui.clientComboBox.removeItem(index)
        self.__set_to_last_client()

    def __set_to_last_client(self):
        count = self.ui.clientComboBox.count()
        if count == 0:
            self.__set_client(None)
        else:
            self.ui.clientComboBox.setCurrentIndex(count - 1)

    def __set_client(self, client_id: int | None):
        if not client_id == self.__client:
            self.__client = client_id
            self.__client_change_hook(client_id)

    def __refresh_above_figure(self):
        self.__set_above_figure(self.ui.aboveFigureComboBox.currentData())

    def __refresh_below_figure(self):
        self.__set_below_figure(self.ui.belowFigureComboBox.currentData())

    def __set_above_figure(self, figure: Figure):
        self.__aboveFigureCanvas.figure = deepcopy(figure)
        self.__set_figure_size(
            self.__aboveFigureCanvas.figure,
            self.__aboveFigureCanvas,
        )
        self.__aboveFigureCanvas.draw_idle()

    def __set_below_figure(self, figure: Figure):
        self.__belowFigureCanvas.figure = deepcopy(figure)
        self.__set_figure_size(
            self.__belowFigureCanvas.figure,
            self.__belowFigureCanvas,
        )
        self.__belowFigureCanvas.draw_idle()

    def __set_figure_size(self, figure: Figure, canvas: FigureCanvas):
        size = canvas.size()
        pixel_ratio = canvas.device_pixel_ratio
        dpi = figure.dpi
        w = size.width() * pixel_ratio
        h = size.height() * pixel_ratio
        figure.set_size_inches(w / dpi, h / dpi, forward=False)
