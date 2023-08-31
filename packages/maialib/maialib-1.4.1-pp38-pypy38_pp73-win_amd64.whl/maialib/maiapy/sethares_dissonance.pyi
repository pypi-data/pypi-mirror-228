import plotly.graph_objects as go
import pandas as pd
from _typeshed import Incomplete
from maialib import maiacore as mc
from typing import List, Tuple

def plotSetharesDissonanceCurve(base_freq: int = ..., numPartials: int = ..., r_low: int = ..., r_high: float = ..., n_points: int = ..., amplVec: Incomplete | None = ...) -> Tuple[go.Figure, List[float], List[float]]: ...
def plotScoreSetharesDissonance(score: mc.Score, **kwargs) -> Tuple[go.Figure, pd.DataFrame]: ...
