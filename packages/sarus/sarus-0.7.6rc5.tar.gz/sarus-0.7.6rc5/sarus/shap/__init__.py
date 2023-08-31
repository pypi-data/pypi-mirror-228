"""Sarus Pandas package documentation."""
from sarus.utils import register_ops

from .explainers import *
from .Explanation import *
from .plots import *
from .maskers import *
from .utils import *

from shap import (
    bar_plot,
    summary_plot,
    decision_plot,
    multioutput_decision_plot,
    embedding_plot,
    force_plot,
    save_html,
    group_difference_plot,
    image_plot,
    monitoring_plot,
    partial_dependence_plot,
    dependence_plot,
    text_plot,
    waterfall_plot,
)

from .explainers import Additive as AdditiveExplainer
from .explainers import Explainer
from .explainers import GPUTree as GPUTreeExplainer
from .explainers import Kernel as KernelExplainer
from .explainers import Linear as LinearExplainer
from .explainers import Partition as PartitionExplainer
from .explainers import Permutation as PermutationExplainer
from .explainers import Sampling as SamplingExplainer
from .explainers import Tree as TreeExplainer

register_ops()
