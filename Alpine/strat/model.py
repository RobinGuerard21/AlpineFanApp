import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, OneHotEncoder
import plotly.express as px

df = pd.read_csv("tyrelife.csv")
df.dropna(inplace=True)

X = df[['Distance']]
y = df['Time']

encoder = OneHotEncoder()
encoded = encoder.fit_transform(df[['Team', 'Compound', 'Track']])
X = pd.concat([X, pd.DataFrame(data = encoded.toarray(),columns = encoder.get_feature_names_out())], axis=1)

poly_reg = make_pipeline(
    PolynomialFeatures(),
    LinearRegression()
)

param_grid = {
    'polynomialfeatures__degree': [2, 3, 4],
    'linearregression__fit_intercept': [True, False]
}

grid_search = GridSearchCV(poly_reg, param_grid, cv=5)
grid_search.fit(X, y)

print("Best hyperparameters:", grid_search.best_params_)
print("Best score:", grid_search.best_score_)