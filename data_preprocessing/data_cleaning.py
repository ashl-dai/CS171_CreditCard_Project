from ucimlrepo import fetch_ucirepo
import pandas as pd

def clean_data(drop_duplicates: bool = True):
    # fetch the data
    credit_card_data = fetch_ucirepo(id=350)

    X = credit_card_data.data.features.copy()
    y = credit_card_data.data.targets.copy()
    
    # rename the cols
    X.columns = [
        "LIMIT_BAL",
        "SEX",
        "EDUCATION",
        "MARRIAGE",
        "AGE",
        "PAY_1",
        "PAY_2",
        "PAY_3",
        "PAY_4",
        "PAY_5",
        "PAY_6",
        "BILL_AMT1",
        "BILL_AMT2",
        "BILL_AMT3",
        "BILL_AMT4",
        "BILL_AMT5",
        "BILL_AMT6",
        "PAY_AMT1",
        "PAY_AMT2",
        "PAY_AMT3",
        "PAY_AMT4",
        "PAY_AMT5",
        "PAY_AMT6",
    ]
    y.columns = ["default_payment_next_month"]

    # Group 0, 5, 6 into 4
    X["EDUCATION"] = X["EDUCATION"].replace({0: 4, 5: 4, 6: 4})

    # remove duplicates
    df = pd.concat([X, y], axis=1)
    duplicate_count = df.duplicated().sum()
    if drop_duplicates and duplicate_count > 0:
        df = df.drop_duplicates().reset_index(drop=True)

    X_clean = df.drop(columns=["default_payment_next_month"])
    y_clean = df["default_payment_next_month"]
    
    # change type to category
    categorical_cols = [
        "SEX",
        "EDUCATION",
        "MARRIAGE",
        "PAY_1",
        "PAY_2",
        "PAY_3",
        "PAY_4",
        "PAY_5",
        "PAY_6",
    ]
    for col in categorical_cols:
        X_clean[col] = X_clean[col].astype("category")

    return X_clean, y_clean