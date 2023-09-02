import numpy as np
import pandas as pd
from sklearn import metrics
import os
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display

from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from imblearn.over_sampling import ADASYN
from imblearn.over_sampling import SVMSMOTE
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    recall_score,
    confusion_matrix,
    precision_score,
)
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
    mean_absolute_percentage_error,
)


# 2. Función para eliminar columnas si tienen más del 70% de nan o sustituir por el valor medio si los nan son menos del 20%.
def eliminar_nan(df):
    for i in df.columns:
        if df[i].isnull().sum() / len(df[i]) > 0.7:
            df.drop([i], axis=1, inplace=True)
        elif (df[i].isnull().sum() / len(df[i]) < 0.2) & (df[i].dtypes != object):
            df[i].fillna(df[i].mean(), inplace=True)
        else:
            pass
    return df


# 5. Función para aplicar un modelo. Dependiendo de ser de regresión o clasificación, saca las métricas correspondientes.


def aplicar_modelo(dataframe_val, dataframe_test, model, model_type, target_name):
    X = dataframe_val.drop([target_name], axis=1)
    y = dataframe_val[target_name]
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model.fit(X_train, y_train)
    prediction = model.predict(X_val)

    X_test = dataframe_test.drop([target_name], axis=1)
    y_test = dataframe_test[target_name]
    y_pred = model.predict(X_test)

    if model_type == "classification":
        c_matrix = confusion_matrix(y_test, y_pred, normalize="true")
        import seaborn as sns

        sns.heatmap(c_matrix, annot=True)
        plt.xlabel("Predicted")
        plt.ylabel("Actual")

        print("TRAIN")

        print("Accuracy score:", round((accuracy_score(y_val, prediction)), 4))
        print("Precision:", round((precision_score(y_val, prediction)), 4))
        print("Recall:", round((recall_score(y_val, prediction)), 4))
        print("F1 Score:", round((f1_score(y_val, prediction)), 4))

        print("TEST")

        print("Accuracy score:", round((accuracy_score(y_test, y_pred)), 4))
        print("Precision:", round((precision_score(y_test, y_pred)), 4))
        print("Recall:", round((recall_score(y_test, y_pred)), 4))
        print("F1 Score:", round((f1_score(y_test, y_pred)), 4))

    elif model_type == "regression":
        print("TRAIN")

        print("MAE:", round((metrics.mean_absolute_error(y_val, prediction)), 4))
        print("MSE:", round((metrics.mean_squared_error(y_val, prediction)), 4))
        print("RMSE:", round(np.sqrt(metrics.mean_squared_error(y_val, prediction)), 4))

        print("TEST")

        print("MAE:", round(metrics.mean_absolute_error(y_test, y_pred)), 4)
        print("MSE:", round(metrics.mean_squared_error(y_test, y_pred)), 4)
        print("RMSE:", round(np.sqrt(metrics.mean_squared_error(y_test, y_pred)), 4))

    return


# 8. Sacar el archivo .pkl de un modelo


def convertir_pickle(model_filename, df, model, target_name):
    # Ruta completa del archivo .py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Cambio del directorio de trabajo al directorio del archivo .py
    os.chdir(script_dir)
    X = df.drop([target_name], axis=1)
    y = df[target_name]
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model.fit(X_train, y_train)
    model_path = os.path.join(script_dir, model_filename)
    pickle.dump(model, open(model_path, "wb"))
    return


# 12. Función para balancear el dataset

"""Esta función sirve para balancear un dataframe utilizando técnicas de oversampling o undersampling. Los algoritmos utilizados pueden ser
RandomOverSampler()
RandomUnderSampler()
ADASYN()
SVMSMOTE()"""


def balancear_datos(df, model, target_name):
    X = df.drop([target_name], axis=1)
    y = df[target_name]
    X_bal, y_bal = model.fit_resample(X, y)
    df_bal = pd.DataFrame(X_bal)
    df_bal[target_name] = y_bal
    df_bal.reset_index(inplace=True, drop=True)

    return df_bal


# 23. Función para representar gráficamente las métricas de los modelos, bien de regresión o clasificación


def calcular_metricas(
    dataframe_val, dataframe_test, model_list, model_type, target_name
):
    resultados = []  # Lista para almacenar los resultados de cada modelo

    X = dataframe_val.drop([target_name], axis=1)
    y = dataframe_val[target_name]
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    X_test = dataframe_test.drop([target_name], axis=1)
    y_test = dataframe_test[target_name]

    for model in model_list:
        if isinstance(model, PolynomialFeatures):
            poly_feats = model
            poly_feats.fit(X)
            X_poly = poly_feats.transform(X)
            X_train, X_val, y_train, y_val = train_test_split(
                X_poly, y, test_size=0.2, random_state=12
            )
            model_linear = LinearRegression()
            model_linear.fit(X_train, y_train)
            prediction = model_linear.predict(X_val)
            X_poly_test = poly_feats.transform(X_test)
            y_pred = model_linear.predict(X_poly_test)
        else:
            model.fit(X_train, y_train)
            prediction = model.predict(X_val)
            y_pred = model.predict(X_test)
        y_test = dataframe_test[target_name]

        if model_type == "classification":
            accuracy = round(accuracy_score(y_test, y_pred), 4)
            precision = round(precision_score(y_test, y_pred), 4)
            recall = round(recall_score(y_test, y_pred), 4)
            F1 = round(f1_score(y_test, y_pred), 4)

            # Almacenar los resultados en un diccionario
            resultados.append(
                {
                    "Modelo": str(model),
                    "Accuracy": accuracy,
                    "Precision": precision,
                    "Recall": recall,
                    "F1 Score": F1,
                }
            )

        if model_type == "regression":
            MAE = round(metrics.mean_absolute_error(y_test, y_pred), 4)
            MAPE = round(metrics.mean_absolute_percentage_error(y_test, y_pred), 4)
            MSE = round(metrics.mean_squared_error(y_test, y_pred), 4)
            RMSE = round(np.sqrt(metrics.mean_squared_error(y_test, y_pred)), 4)
            # Almacenar los resultados en un diccionario
            resultados.append(
                {
                    "Modelo": str(model),
                    "MAE": MAE,
                    "MAPE": MAPE,
                    "MSE": MSE,
                    "RMSE": RMSE,
                }
            )

    df_resultados = pd.DataFrame(resultados)
    return df_resultados


def representacion_grafica(metrica):
    df_resultados = calcular_metricas(
        dataframe_val, dataframe_test, model_list, model_type, target_name
    )
    sns.swarmplot(data=df_resultados, x="Modelo", y=metrica)
    plt.xticks(rotation=45, ha="right")
    display(df_resultados)
    return plt.show()
