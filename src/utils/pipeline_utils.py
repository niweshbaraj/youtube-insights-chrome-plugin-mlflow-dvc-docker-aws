import pandas as pd

def select_clean_comment_column(X):
    """Returns a 1D Series or list of clean_comment values."""
    if isinstance(X, pd.DataFrame):
        return X["clean_comment"]  # returns all rows
    elif isinstance(X, pd.Series):
        return X
    elif isinstance(X, list):
        return pd.Series(X)
    else:
        raise ValueError("Unsupported input type")
