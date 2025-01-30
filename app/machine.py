from pandas import DataFrame
from sklearn.svm import SVC
import joblib
from datetime import datetime
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler


class Machine:
    """Machine learning model for classification using Support Vector Machines with oversampling and undersampling.

    :arg:
        name (str): Name of the model.
        model (SVC): Support Vector Machines model.
        oversampling (SMOTE): Oversampling technique for handling imbalanced classes.
        undersampling (RandomUnderSampler): Undersampling technique for handling imbalanced classes.
        timestamp (str): Timestamp when the model was initialized.
    """

    def __init__(self, df: DataFrame):
        """Constructor method that takes in a DataFrame, extracts the target variable and selected feature columns,
        applies oversampling and undersampling techniques to the data, fits a Support Vector Machine model,
        and stores the timestamp of model creation for reference.

        :arg:
            df (DataFrame): Input dataframe containing the training data.
        """
        target = df["Rarity"]
        features = df[["Level", "Health", "Energy", "Sanity"]]

        self.name = "Support Vector Machines"
        self.model = SVC(random_state=42,
                         probability=True,
                         decision_function_shape='ovo',
                         C=7,
                         kernel='rbf',
                         gamma=0.1)

        self.oversampling = SMOTE(sampling_strategy='auto', random_state=42)
        self.undersampling = RandomUnderSampler(random_state=42)

        # Apply oversampling to the features and target
        features_resampled, target_resampled = self.oversampling.fit_resample(features, target)
        # Apply undersampling to the features and target
        features_resampled, target_resampled = self.undersampling.fit_resample(features_resampled, target_resampled)

        self.model.fit(features_resampled, target_resampled)
        self.timestamp = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    def __call__(self, feature_basis: DataFrame):
        """Makes predictions using the trained Support Vector Machines model.

        :arg:
            feature_basis (DataFrame): Input DataFrame containing the features for prediction

        :return:
            tuple: Prediction and confidence of the prediction
        """
        prediction = self.model.predict(feature_basis)[0]  # Access the first (and only) prediction
        if feature_basis.shape[0] == 1:  # Single prediction case
            confidence = self.model.predict_proba(feature_basis)[0].max()  # Access the first prediction's confidence
        else:
            confidence = self.model.predict_proba(feature_basis).max(axis=1)  # Multiple rows
        return prediction, float(confidence)

    def save(self, filepath: str):
        """ Saves the machine learning model to the specified filepath using joblib.
        The model is serialized using joblib.dump() to the specified filepath. Serialization allows the model
        to be saved in a file format that can be later loaded and used for predictions or further analysis.

        :arg:
            filepath (str): Filepath where the model will be saved.
        """
        joblib.dump(self, filepath)

    @staticmethod
    def open(filepath: str):
        """Loads the saved machine learning model from a file using joblib.
        The model is deserialized using joblib.load() from the specified filepath. Deserialization allows the model
        to be loaded from a saved file and used for predictions or further analysis.

        :arg:
            filepath (str): Filepath from where the model will be loaded.
        """
        return joblib.load(filepath)

    def info(self):
        """Returns information about the Machine object.

        :return:
            str: Information about the name of the trained model and the timestamp.
        """
        nl = "<br>"
        return f"Base Model:{self.name}{nl}Timestamp:{self.timestamp}"