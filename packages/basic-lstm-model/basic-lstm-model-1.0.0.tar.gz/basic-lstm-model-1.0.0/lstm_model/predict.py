#import typing as t

#import numpy as np
import pandas as pd

from lstm_model import __version__ as _version
from lstm_model.config.core import config
from lstm_model.processing.data_manager import load_pipeline

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_price_pipe = load_pipeline(file_name=pipeline_file_name)


def make_prediction(
    *,
    input_data: pd.DataFrame,
) -> dict:
    """Make a prediction using a saved model pipeline."""

    data = pd.DataFrame(input_data)
          # Basic transformations.
    features = config.model_config.features
    data['fecha'] = pd.to_datetime(data[features[0]],format='%d.%m.%Y %H:%M:%S.%f')
    data['precio_EURUSD'] = data[features[1]]

      # NULOS
      # For the null values we will take the preceed value.
    data['precio_EURUSD'] = data['precio_EURUSD'].fillna(method='ffill')
      # Except when we do not have a preceed value, then we will take the next value.
    data['precio_EURUSD'] = data['precio_EURUSD'].fillna(method='bfill')

      # Select columns.
    data = data[['fecha','precio_EURUSD']]
    data.set_index('fecha',inplace=True)


    results = {"predictions": None, "version": _version}

    predictions = _price_pipe.transform(
        X=data#[config.model_config.features]
        )
    results = {
        "predictions": list(predictions.flatten()),#[np.exp(pred) for pred in predictions],  # type: ignore
        "version": _version
        }

    return results