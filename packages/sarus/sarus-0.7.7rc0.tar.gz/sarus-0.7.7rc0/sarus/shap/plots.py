from sarus.utils import register_ops

try:
    from shap.plots import *
except ModuleNotFoundError:
    pass  # error message in sarus_data_spec.typing

from shap.plots import (
    bar,
    beeswarm,
    benchmark,
    decision,
    embedding,
    force,
    group_difference,
    heatmap,
    image,
    image_to_text,
    initjs,
    monitoring,
    partial_dependence,
    scatter,
    text,
    violin,
    waterfall,
)

register_ops()
