import pandas as pd
from pathlib import Path
import joblib

from lstm_model.config.core import DATASET_DIR, TRAINED_MODEL_DIR, config
from lstm_model.pipeline import LSTM_pipe
from lstm_model import __version__ as _version

def entrenando_pipe():
    # Define parameters.
    ventana = config.model_config.ventana
    #n_features = config.n_features
    #epochs = config.epochs
    corte_fecha = config.model_config.corte_fecha
    corte_train_test = config.model_config.corte_train_test
    features = config.model_config.features
    file_name = config.app_config.data_file

    # Read.
    data1 = pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"), usecols = features)

    # Basic transformations.
    data1['fecha'] = pd.to_datetime(data1[features[0]],format='%d.%m.%Y %H:%M:%S.%f')
    data1['precio_EURUSD'] = data1[features[1]]

    # Select records from 2013 onwards.
    data1 = data1[(data1['fecha'].dt.year*100+data1['fecha'].dt.month)>corte_fecha]

    # Temporal order.
    data1.sort_values('fecha',inplace=True)

    # NULOS
    # For the null values we will take the preceed value.
    data1['precio_EURUSD'] = data1['precio_EURUSD'].fillna(method='ffill')
    # Except when we do not have a preceed value, then we will take the next value.
    data1['precio_EURUSD'] = data1['precio_EURUSD'].fillna(method='bfill')

    # Target and TRAIN/TEST.
    X_train=data1[(data1['fecha'].dt.year*100+data1['fecha'].dt.month)< corte_train_test][['fecha','precio_EURUSD']]
    X_test =data1[(data1['fecha'].dt.year*100+data1['fecha'].dt.month)>=corte_train_test][['fecha','precio_EURUSD']]
    y_train=data1[(data1['fecha'].dt.year*100+data1['fecha'].dt.month)< corte_train_test][['fecha','precio_EURUSD']].rename(columns={'precio_EURUSD':'target'})
    y_train['target'] = y_train['target'].shift(-1).fillna(method='ffill')
    y_test =data1[(data1['fecha'].dt.year*100+data1['fecha'].dt.month)>=corte_train_test][['fecha','precio_EURUSD']].rename(columns={'precio_EURUSD':'target'})
    y_test['target'] = y_test['target'].shift(-1).fillna(method='ffill')

    y_train = y_train['target'].values
    y_test= y_test['target'].values

    y_train = y_train[ventana-1:len(y_train) ]
    y_test = y_test[ventana-1:len(y_test) ]

    X_train.set_index('fecha',inplace=True)
    X_test.set_index('fecha',inplace=True)

    # PIPELINE.
    LSTM_pipe.fit(X_train,y_train)

    # SAVE THE QUEE ejm... the pipeline.
    # Save the trained Pipe, overwrite the previous.
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
    save_path = TRAINED_MODEL_DIR / save_file_name

    # Removing the previous.
    for ficheros in TRAINED_MODEL_DIR.iterdir():
        if ficheros.name not in [save_file_name]+["__init__.py"]:
            ficheros.unlink()
    # Saving
    joblib.dump(LSTM_pipe, save_path)

if __name__ == "__main__":
    entrenando_pipe()