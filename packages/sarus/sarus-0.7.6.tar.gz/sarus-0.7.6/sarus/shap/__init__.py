"""Sarus Pandas package documentation."""
from shap import (
    bar_plot,
    decision_plot,
    dependence_plot,
    embedding_plot,
    force_plot,
    group_difference_plot,
    image_plot,
    monitoring_plot,
    multioutput_decision_plot,
    partial_dependence_plot,
    save_html,
    summary_plot,
    text_plot,
    waterfall_plot,
)

from sarus.utils import register_ops

from .explainers import Additive as AdditiveExplainer
from .explainers import *
from .explainers import Explainer
from .explainers import GPUTree as GPUTreeExplainer
from .explainers import Kernel as KernelExplainer
from .explainers import Linear as LinearExplainer
from .explainers import Partition as PartitionExplainer
from .explainers import Permutation as PermutationExplainer
from .explainers import Sampling as SamplingExplainer
from .explainers import Tree as TreeExplainer
from .Explanation import *
from .maskers import *
from .plots import *
from .utils import *

register_ops()
