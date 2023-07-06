from pandas import read_csv as read
from sklearn.model_selection import train_test_split as train
from sklearn.ensemble import RandomForestClassifier
from tkinter import messagebox as mb

class NeuralNetwork:
    def __init__(self):
        try:
            path = "training.csv"
            data = read(path, delimiter=",")
            data.head()
            self.X = data.values[::, 1:11]
            self.y = data.values[::, 11:12]
            self.clf = RandomForestClassifier(n_estimators=100, n_jobs=-1)
        except OSError as error:
            mb.showinfo("No training dataset", "File training.csv doesn`t exist")

    def training(self):
        X = self.X
        y = self.y
        clf = self.clf
        X_train, X_test, y_train, y_test = train(X, y, test_size=0.6)
        clf.fit(X_train, y_train.ravel())
        accuracy = clf.score(X_test, y_test)
        print('Accuracy: ' + str(accuracy))
        return accuracy

    def prediction(self):
        self.training()
        clf = self.clf
        path_test = "account.csv"
        data_test = read(path_test, delimiter=",")
        data_test.head()
        row_test = data_test.values[::, 1:11]
        predicted = clf.predict(row_test)
        result = predicted[0]
        return result

    def __str__(self, result):
        result = self.result
        return result