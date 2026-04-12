import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder, StandardScaler
from xgboost import XGBClassifier

NUMERIC_FEATURES = [
    "engine_temp",
    "brake_wear_pct",
    "battery_voltage",
    "tire_pressure",
    "chain_tension",
    "image_brightness",
    "image_contrast",
    "image_edge_density",
    "image_dark_ratio",
    "image_red_ratio",
    "image_green_ratio",
    "image_blue_ratio",
    "image_embedding_mean",
    "image_embedding_std",
    "image_embedding_max",
    "image_embedding_l2",
    "ambient_temp",
]

CATEGORICAL_FEATURES = ["smoke_detected", "abnormal_noise"]


def cast_to_string(X):
    return X.astype(str)


def build_pipeline() -> Pipeline:
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("cast", FunctionTransformer(cast_to_string, validate=False)),
            ("imputer", SimpleImputer(strategy="most_frequent", fill_value="missing")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )

    model = XGBClassifier(
        use_label_encoder=False,
        eval_metric="mlogloss",
        n_estimators=100,
        max_depth=4,
        random_state=42,
        verbosity=0,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", model),
        ]
    )
    return pipeline
