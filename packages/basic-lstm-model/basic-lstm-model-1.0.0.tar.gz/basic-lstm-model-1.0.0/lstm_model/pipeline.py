from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler
from lstm_model.processing import pipe_needs
from lstm_model.config.core import config

LSTM_pipe = Pipeline([
    # === SCALING ===
    ('Normalization the data with Robust Scaler', RobustScaler()),

    # === RE-STRUCTURE ===
    ('Fit the data to the LSTM input structure', pipe_needs.ReestructuraLSM(config.model_config.ventana)),

    # === MODEL ===
    ('LSTM Model', pipe_needs.ModeloLSM(config.model_config.ventana,
                                        config.model_config.n_features,
                                        config.model_config.epochs))
])