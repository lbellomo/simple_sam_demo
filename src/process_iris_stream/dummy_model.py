from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


class Model:
    """Create a dummy model"""

    def __init__(self):
        """Train a logistic regression with the iris data
        (with all the features and categories) with a random seed."""
        random_state = 42
        iris = load_iris()

        X = iris["data"]
        y = iris["target"]
        self.target_names = iris["target_names"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=random_state
        )

        self.clf = LogisticRegression()
        self.clf.fit(X_train, y_train)

    def predict(self, X):
        """Wrapper for the predict sklearn method."""
        y = self.clf.predict(X)
        return self.target_names[y].tolist()
