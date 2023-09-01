from __future__ import annotations

import logging
import typing as t

import pandas as pd

from sarus.dataspec_wrapper import (
    IGNORE_WARNING,
    DataSpecVariant,
    DataSpecWrapper,
)
from sarus.typing import SPECIAL_WRAPPER_ATTRIBUTES
from sarus.utils import (
    create_lambda_op,
    create_method,
    register_ops,
    sarus_init,
    sarus_method,
    sarus_property,
)

logger = logging.getLogger(__name__)
from typing import (
    Any,
    Callable,
    Dict,
    Hashable,
    Iterable,
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

import numpy.typing as npt
import shap
from pandas._typing import Axes
from scipy.sparse import spmatrix
from shap import Explainer


class Explanation(DataSpecWrapper[shap.Explanation]):
    @sarus_init("shap.SHAP_EXPLANATION")
    def __init__(
        self,
        values: Union[npt.ArrayLike, spmatrix],
        base_values: Optional[Union[npt.ArrayLike, spmatrix]] = None,
        data: Optional[Union[npt.ArrayLike, spmatrix]] = None,
        display_data: Optional[Dict[str, npt.ArrayLike]] = None,
        instance_names: Optional[List[str]] = None,
        feature_names: Optional[List[str]] = None,
        output_names: Optional[List[str]] = None,
        output_indexes: Optional[List[int]] = None,
        lower_bounds: Optional[Union[npt.ArrayLike, spmatrix]] = None,
        upper_bounds: Optional[Union[npt.ArrayLike, spmatrix]] = None,
        error_std: Optional[Union[npt.ArrayLike, spmatrix]] = None,
        main_effects: Optional[Union[npt.ArrayLike, spmatrix]] = None,
        hierarchical_values: Optional[Union[npt.ArrayLike, spmatrix]] = None,
        clustering: Optional[Union[npt.ArrayLike, spmatrix]] = None,
        compute_time: Optional[float] = None,
    ):
        ...

    @sarus_property("shap.SHAP_VALUES")
    def values(self):
        ...

    @sarus_property("shap.SHAP_SUM")
    def sum(self):
        ...
