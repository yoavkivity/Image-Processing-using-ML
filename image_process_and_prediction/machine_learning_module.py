import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error
import xgboost as xgb
from sklearn.ensemble import GradientBoostingRegressor
from image_process_and_prediction import image_process, files_operations

# load and prepare the data
data = pd.read_excel(files_operations.get_path("DATA_WITH_INSIGHTS"))

# define target variables
targets = ['Sharpness Alpha', 'Sharpness Beta', 'Sharpness Gamma', 'Gamma Correction', 'Clip Limit',
           'Filter Strength', 'Template Window', 'Search Window']

# define columns to remove
columns_to_remove = ['Serial', 'File Name', 'A+B', 'A+B-correction', 'Correction-clip*100', 'Label', 'alpha-clip*1000']

# remove specified columns
data = data.drop(columns=columns_to_remove, errors='ignore')

# Separate features and targets
X = data.drop(targets, axis=1)
y = data[targets]

# Handle missing values
imputer = SimpleImputer(strategy='mean')
X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define and train the models
best_params = {
    'Sharpness Alpha': {'colsample_bytree': 1.0, 'learning_rate': 0.2, 'max_depth': 5, 'n_estimators': 200,
                        'subsample': 0.9},
    'Sharpness Beta': {'colsample_bytree': 0.9, 'learning_rate': 0.1, 'max_depth': 3, 'n_estimators': 300,
                       'subsample': 0.8},
    'Sharpness Gamma': {'learning_rate': 0.01, 'max_depth': 7, 'n_estimators': 100},
    'Gamma Correction': {'colsample_bytree': 0.9, 'learning_rate': 0.2, 'max_depth': 3, 'n_estimators': 300,
                         'subsample': 0.8},
    'Filter Strength': {'learning_rate': 0.01, 'max_depth': 3, 'n_estimators': 100},
    'Template Window': {'learning_rate': 0.01, 'max_depth': 3, 'n_estimators': 100},
    'Search Window': {'learning_rate': 0.01, 'max_depth': 3, 'n_estimators': 100},
    'Clip Limit': {'learning_rate': 0.1, 'max_depth': 3, 'n_estimators': 300}
}

models = {}
for target in targets:
    if target in ['Sharpness Alpha', 'Sharpness Beta', 'Gamma Correction']:
        models[target] = xgb.XGBRegressor(random_state=42, **best_params[target])
    else:
        models[target] = GradientBoostingRegressor(random_state=42, **best_params[target])

    # For each target, we train on all previous targets plus the original features
    X_train_target = pd.concat([X_train, y_train[targets[:targets.index(target)]]], axis=1)
    models[target].fit(X_train_target, y_train[target])


# create prediction function
def predict_targets(input_data, alpha_values):
    results = []

    for alpha in alpha_values:
        prediction = {'Sharpness Alpha': alpha}
        input_scaled = scaler.transform(input_data)
        temp_input = pd.DataFrame(input_scaled, columns=X.columns)

        for target in targets[1:]:  # skip 'Sharpness Alpha' as it's given
            if target == 'Sharpness Beta':
                temp_input['Sharpness Alpha'] = alpha
            elif target == 'Sharpness Gamma':
                temp_input['Sharpness Beta'] = prediction['Sharpness Beta']
            elif target == 'Gamma Correction':
                temp_input['Sharpness Gamma'] = prediction['Sharpness Gamma']
            elif target == 'Clip Limit':
                temp_input['Gamma Correction'] = prediction['Gamma Correction']
            elif target == 'Filter Strength':
                temp_input['Clip Limit'] = prediction['Clip Limit']
            elif target == 'Template Window':
                temp_input['Filter Strength'] = prediction['Filter Strength']
            elif target == 'Search Window':
                temp_input['Template Window'] = prediction['Template Window']

            prediction[target] = models[target].predict(temp_input)[0]

        results.append(prediction)
    return results


# evaluate the model
mae_scores = {}
for target in targets:
    X_test_target = pd.concat([X_test, y_test[targets[:targets.index(target)]]], axis=1)
    y_pred = models[target].predict(X_test_target)
    mae = mean_absolute_error(y_test[target], y_pred)
    mae_scores[target] = mae

# print("MAE scores:")
# print(json.dumps(mae_scores, indent=2))

def calc_new_image_data():
    average_alpha_values = [3.5, 4.02, 4.48, 4.76, 5, 5.56, 6, 7.11, 7.75]
    alpha_values = np.arange(3.5, 7.6, 0.1)
    alpha_values = list(set(alpha_values) | set(average_alpha_values))
    new_data = image_process.process_missing_data(files_operations.read_file(files_operations.get_path("IMAGE_PATH")))
    predictions = predict_targets(new_data, alpha_values)

    print("\nPredictions:")
    FULL_PRED = []
    for i, pred in enumerate(predictions):
        FULL_PRED.append(pred)

    print(FULL_PRED)
    return FULL_PRED
