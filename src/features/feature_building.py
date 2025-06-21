# src/model/model_building.py

import numpy as np
import pandas as pd
import os
import pickle
import yaml
import logging
from sklearn.feature_extraction.text import TfidfVectorizer

# logging configuration
logger = logging.getLogger('feature_building')
logger.setLevel('DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')

file_handler = logging.FileHandler('feature_building_errors.log')
file_handler.setLevel('ERROR')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


def get_root_directory() -> str:
    """Get the root directory (two levels up from this script's location)."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(current_dir, '../../'))


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


def apply_tfidf(train_data: pd.DataFrame, max_features: int, ngram_range: tuple) -> tuple:
    """Apply TF-IDF with ngrams to the data."""
    try:
        vectorizer = TfidfVectorizer(max_features=max_features, ngram_range=ngram_range)

        X_train = train_data['clean_comment'].values
        y_train = train_data['category'].values

        # Perform TF-IDF transformation
        X_train_tfidf = vectorizer.fit_transform(X_train)

        logger.debug(f"TF-IDF transformation complete. Train shape: {X_train_tfidf.shape}")

        # Save the vectorizer in the root directory
        with open(os.path.join(get_root_directory(), 'tfidf_vectorizer.pkl'), 'wb') as f:
            pickle.dump(vectorizer, f)

        logger.debug('TF-IDF applied with trigrams and data transformed')
    except Exception as e:
        logger.error('Error during TF-IDF transformation: %s', e)
        raise


def main():
    try:
        # Get root directory and resolve the path for params.yaml
        root_dir = get_root_directory()

        # Load parameters from the root directory
        params = load_params(os.path.join(root_dir, 'params.yaml'))
        max_features = params['feature_building']['max_features']
        ngram_range = tuple(params['feature_building']['ngram_range'])

        # Load the preprocessed training data from the interim directory
        train_data = load_data(os.path.join(root_dir, 'data/interim/train_processed.csv'))
        test_processed_data = load_data(os.path.join(root_dir, 'data/interim/test_processed.csv'))

        # Apply TF-IDF feature engineering on training data
        apply_tfidf(train_data, max_features, ngram_range)
        logger.info('Feature engineering completed successfully.')

    except Exception as e:
        logger.error('Failed to complete the feature engineering building process: %s', e)
        print(f"Error: {e}")


if __name__ == '__main__':
    main()