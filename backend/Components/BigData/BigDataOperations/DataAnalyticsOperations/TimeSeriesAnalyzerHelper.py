import pandas as pd
import numpy as np
from typing import Dict, Any
from statsmodels.tsa.seasonal import seasonal_decompose


def analyze_time_series(data: pd.Series, freq: int = 1) -> Dict[str, Any]:
    try:
        result = seasonal_decompose(data, model='additive', period=freq)
        trend = result.trend.dropna().tolist()
        seasonal = result.seasonal.dropna().tolist()
        resid = result.resid.dropna().tolist()

        return {
            "trend": trend,
            "seasonal": seasonal,
            "residual": resid
        }
    except Exception as e:
        return {"error": str(e)}