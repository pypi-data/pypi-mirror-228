import math

import numpy as np
import pandas as pd
from lstm_model.config.core import config
from lstm_model.predict import make_prediction


def test_make_prediction(sample_input_data):
    # Given
    #expected_first_prediction_value = 113422
    expected_no_predictions = 69030

    # When
          # Basic transformations.
#    features = config.model_config.features
#    sample_input_data['fecha'] = pd.to_datetime(sample_input_data[features[0]],format='%d.%m.%Y %H:%M:%S.%f')
#    sample_input_data[f'precio_EURUSD'] = sample_input_data[features[1]]

      # NULOS
      # For the null values we will take the preceed value.
#    sample_input_data['precio_EURUSD'] = sample_input_data['precio_EURUSD'].fillna(method='ffill')
      # Except when we do not have a preceed value, then we will take the next value.
#    sample_input_data['precio_EURUSD'] = sample_input_data['precio_EURUSD'].fillna(method='bfill')

      # Select columns.
#    sample_input_data = sample_input_data[['fecha','precio_EURUSD']]
#    sample_input_data.set_index('fecha',inplace=True)

    result = make_prediction(input_data=sample_input_data)

    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions, list), "Las predicciones deberíar estar en una lista."
    print(type(predictions[0]))
    assert isinstance(predictions[0], np.float32), "Las predicciones deberían ser de tipo float."
    #assert result.get("errors") is None
    assert len(predictions) == expected_no_predictions, f"Las predicciones deben tenr una longitud de {expected_no_predictions}"
    #assert math.isclose(predictions[0], expected_first_prediction_value, abs_tol=100)