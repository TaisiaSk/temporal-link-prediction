from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve

import matplotlib.pyplot as plt


def prediction(data: tuple) -> float:
    X, y = data

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
    logreg = LogisticRegression()
    logreg.fit(X_train, y_train)

    pred = logreg.predict(X_test)[:,1]

    auc = roc_auc_score(y_test, pred)
    fpr, tpr, thresholds = roc_curve(y_test, pred)

    plt.figure()
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % auc)
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Probability')
    plt.ylabel('True Positive Probability')
    plt.title('Receiver operating characteristic (ROC)')
    plt.legend(loc="lower right")
    plt.show()

    return auc