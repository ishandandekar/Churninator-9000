import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder,
    LabelEncoder,
    FunctionTransformer,
    OrdinalEncoder,
)
import numpy as np

CAT_COLS = [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
]
NUM_COLS = ["tenure", "MonthlyCharges", "TotalCharges"]
TARGET = ["Churn"]
SEED = 69420

df = pd.read_csv(
    "./data/WA_Fn-UseC_-Telco-Customer-Churn.csv", usecols=CAT_COLS + NUM_COLS + TARGET
)
df.TotalCharges = df.TotalCharges.replace(to_replace=" ", value="0")


def custom_combiner(feature, category):
    return str(feature) + "_" + type(category).__name__ + "_" + str(category)


# Assuming you have a DataFrame named df and the column lists: CAT_COLS_LE, NUM_COLS, CAT_COLS_OHE

CAT_COLS_OHE = ["PaymentMethod", "Contract", "InternetService"]
CAT_COLS_LE = list(set(CAT_COLS) - set(CAT_COLS_OHE))

# Step 1: Create individual transformers
scaler = StandardScaler().set_output(transform="pandas")
encoder_ohe = OneHotEncoder(feature_name_combiner=custom_combiner)
encoder_oe = OrdinalEncoder().set_output(transform="pandas")
converter = FunctionTransformer(
    lambda x: pd.to_numeric(x, errors="coerce"), validate=False
)

# Step 2: Create a list of transformer tuples
transformers = [
    ("numerical", scaler, NUM_COLS),
    ("categorical_ohe", encoder_ohe, CAT_COLS_OHE),
    ("categorical_le", encoder_oe, CAT_COLS_LE),
    ("totalcharges_conversion", converter, ["TotalCharges"]),
]

# Step 3: Create the ColumnTransformer
column_transformer = ColumnTransformer(transformers)

# Step 4: Apply the transformation to the DataFrame
# df_trans = column_transformer.fit_transform(X=df, y=None)

# One hot encoding
X_ohe_ = df[CAT_COLS_OHE]
print(f"Previously --> {X_ohe_.shape}")
print(f"Previously type --> {type(X_ohe_)}")
encoder_ohe.fit(X_ohe_)
X_ohe__trans_ = encoder_ohe.transform(X_ohe_)
X_ohe__trans_df_: pd.DataFrame = pd.DataFrame(
    X_ohe__trans_.toarray(), columns=encoder_ohe.get_feature_names_out()
)
print(f"Now --> {X_ohe__trans_df_.shape}")
print(f"Now type --> {type(X_ohe__trans_df_)}")
print(f"Now cols --> {X_ohe__trans_df_.columns}", end="\n\n")

print("##" * 6, end="\n\n")

# Label encoding
print(CAT_COLS_LE)
X_oe_ = df[CAT_COLS_LE]
print(f"Previously --> {X_oe_.shape}")
print(f"Previously type --> {type(X_oe_)}")
encoder_oe.fit(X_oe_)
X_oe__trans_ = encoder_oe.transform(X_oe_)
print(f"Now --> {X_oe__trans_.shape}")
print(f"Now type --> {type(X_oe__trans_)}")
print(f"Now cols --> {X_oe__trans_.columns}", end="\n\n")

print("##" * 6, end="\n\n")

# Scaling num cols
# TODO: Add code for scaling numerical columns