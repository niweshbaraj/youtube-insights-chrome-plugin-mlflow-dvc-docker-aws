import pandas as pd

def select_clean_comment_column(X):
    """Extracts the 'clean_comment' column from DataFrame input for vectorizer."""
    if isinstance(X, pd.DataFrame):
        return X["clean_comment"]
    return X
