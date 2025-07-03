import pandas as pd
import numpy as np


def select_clean_comment_column(X):

    if isinstance(X, pd.DataFrame):
        return X["clean_comment"]
    elif isinstance(X, pd.Series):
        return X
    elif isinstance(X, list):
        return pd.Series(X)
    elif isinstance(X, np.ndarray):
        return pd.Series(X)
    else:
        raise ValueError(f"Unsupported input type: {type(X)}")
