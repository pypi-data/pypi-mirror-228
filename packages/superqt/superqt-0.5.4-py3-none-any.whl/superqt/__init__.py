"""superqt is a collection of Qt components for python."""
from importlib.metadata import PackageNotFoundError, version
from typing import TYPE_CHECKING, Any

try:
    __version__ = version("superqt")
except PackageNotFoundError:
    __version__ = "unknown"

if TYPE_CHECKING:
    from .spinbox._quantity import QQuantity

from .collapsible import QCollapsible
from .combobox import QEnumComboBox, QSearchableComboBox
from .elidable import QElidingLabel, QElidingLineEdit
from .selection import QSearchableListWidget, QSearchableTreeWidget
from .sliders import (
    QDoubleRangeSlider,
    QDoubleSlider,
    QLabeledDoubleRangeSlider,
    QLabeledDoubleSlider,
    QLabeledRangeSlider,
    QLabeledSlider,
    QRangeSlider,
)
from .spinbox import QLargeIntSpinBox
from .utils import QMessageHandler, ensure_main_thread, ensure_object_thread

__all__ = [
    "ensure_main_thread",
    "ensure_object_thread",
    "QDoubleRangeSlider",
    "QCollapsible",
    "QDoubleSlider",
    "QElidingLabel",
    "QElidingLineEdit",
    "QEnumComboBox",
    "QLabeledDoubleRangeSlider",
    "QLabeledDoubleSlider",
    "QLabeledRangeSlider",
    "QLabeledSlider",
    "QLargeIntSpinBox",
    "QMessageHandler",
    "QQuantity",
    "QRangeSlider",
    "QSearchableComboBox",
    "QSearchableListWidget",
    "QSearchableTreeWidget",
]


def __getattr__(name: str) -> Any:
    if name == "QQuantity":
        from .spinbox._quantity import QQuantity

        return QQuantity
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
