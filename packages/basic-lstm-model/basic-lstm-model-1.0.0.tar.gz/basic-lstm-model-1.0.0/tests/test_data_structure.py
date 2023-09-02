import pandas as pd
from lstm_model.config.core import config
from lstm_model.processing.pipe_needs import ReestructuraLSM

def test_data_structure(sample_input_data):
    # Given
    transformer = ReestructuraLSM(config.model_config.ventana)

    assert len(sample_input_data.shape)==2, "Wrong loaded data."

    # When
      # Basic transformations.
    features = config.model_config.features
    sample_input_data['fecha'] = pd.to_datetime(sample_input_data[features[0]],format='%d.%m.%Y %H:%M:%S.%f')
    sample_input_data[f'precio_EURUSD'] = sample_input_data[features[1]]

      # NULOS
      # For the null values we will take the preceed value.
    sample_input_data['precio_EURUSD'] = sample_input_data['precio_EURUSD'].fillna(method='ffill')
      # Except when we do not have a preceed value, then we will take the next value.
    sample_input_data['precio_EURUSD'] = sample_input_data['precio_EURUSD'].fillna(method='bfill')

      # Select columns.
    sample_input_data = sample_input_data[['fecha','precio_EURUSD']]
    sample_input_data.set_index('fecha',inplace=True)

    subject = transformer.transform(sample_input_data.values)

    # Then
    assert len(subject.shape) == 3, "Bad shape for the LSTM."