# src/model/model_building.py

import numpy as np
import pandas as pd
import os
import pickle
import yaml
import logging
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import lightgbm as lgb

from ..utils.pipeline_utils import select_clean_comment_column 

# logging configuration
logger = logging.getLogger('model_building')
logger.setLevel('DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')

file_handler = logging.FileHandler('model_building_errors.log')
file_handler.setLevel('ERROR')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


def load_params(params_path: str) -> dict:
    """Load parameters from a YAML file."""
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
        logger.debug('Parameters retrieved from %s', params_path)
        return params
    except FileNotFoundError:
        logger.error('File not found: %s', params_path)
        raise
    except yaml.YAMLError as e:
        logger.error('YAML error: %s', e)
        raise
    except Exception as e:
        logger.error('Unexpected error: %s', e)
        raise


def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        df.fillna('', inplace=True)  # Fill any NaN values
        logger.debug('Data loaded and NaNs filled from %s', file_path)
        return df
    except pd.errors.ParserError as e:
        logger.error('Failed to parse the CSV file: %s', e)
        raise
    except Exception as e:
        logger.error('Unexpected error occurred while loading the data: %s', e)
        raise


def train_tfidf_lgbm(X_train: np.ndarray, y_train: np.ndarray, max_features: int, ngram_range: tuple, learning_rate: float, max_depth: int, n_estimators: int) -> Pipeline:
    """Builds, Trains and returns a TF-IDF + LightGBM scikit-learn Pipeline."""
    try:
        best_model_pipeline = Pipeline([
            ('selector', FunctionTransformer(select_clean_comment_column, validate=False)),
            ('tfidf', TfidfVectorizer(max_features=max_features, ngram_range=ngram_range)),
            ('lgbm', lgb.LGBMClassifier(
                objective='multiclass',
                num_class=3,
                metric="multi_logloss",
                is_unbalance=True,
                class_weight="balanced",
                reg_alpha=0.1,  # L1 regularization
                reg_lambda=0.1,  # L2 regularization
                learning_rate=learning_rate,
                max_depth=max_depth,
                n_estimators=n_estimators
            ))
        ])
        best_model_pipeline.fit(X_train, y_train)
        logger.debug('TF-IDF + LightGBM model training completed')
        return best_model_pipeline
    except Exception as e:
        logger.error('Error during TF-IDF + LightGBM model training: %s', e)
        raise


def save_model(model, file_path: str) -> None:
    """Save the trained model to a file."""
    try:
        with open(file_path, 'wb') as file:
            pickle.dump(model, file)
        logger.debug('Model saved to %s', file_path)
    except Exception as e:
        logger.error('Error occurred while saving the model: %s', e)
        raise


def get_root_directory() -> str:
    """Get the root directory (two levels up from this script's location)."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../../'))


def main():
    try:
        # Get root directory and resolve the path for params.yaml
        root_dir = get_root_directory()

        # Load parameters from the root directory
        params = load_params(os.path.join(root_dir, 'params.yaml'))

        max_features = params['model_building']['max_features']
        ngram_range = tuple(params['model_building']['ngram_range'])
        learning_rate = params['model_building']['learning_rate']
        max_depth = params['model_building']['max_depth']
        n_estimators = params['model_building']['n_estimators']

        # Load the preprocessed training data from the interim directory
        train_data = load_data(os.path.join(root_dir, 'data/interim/train_processed.csv'))

        X_train = train_data['clean_comment'].values

        y_train = train_data['category'].values

        # Train the TFIDF with LightGBM model pipeline using hyperparameters from params.yaml
        best_model_pipeline = train_tfidf_lgbm(X_train, y_train, max_features, ngram_range, learning_rate, max_depth, n_estimators)

        # Save the trained model in the root directory
        save_model(best_model_pipeline, os.path.join(root_dir, 'tfidf_lgbm_model.pkl'))

    except Exception as e:
        logger.error('Failed to complete the feature engineering and model building process: %s', e)
        print(f"Error: {e}")


if __name__ == '__main__':
    main()