from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt

from features_collector import features_to_matrix


def prediction(data: tuple, data_name: str) -> float:
    y, X = data

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # # Variant without standartization
    # logreg = LogisticRegression(max_iter=10000,  n_jobs=-1, random_state=42)
    # logreg.fit(X_train, y_train)
    # pred = logreg.predict_proba(X_test)[:,1]

    # Variant with standartization data
    pipe = make_pipeline(StandardScaler(), 
                         LogisticRegression(max_iter=10000,  n_jobs=-1, random_state=42))
    pipe.fit(X_train, y_train)
    pred = pipe.predict_proba(X_test)[:,1]

    auc = roc_auc_score(y_test, pred)
    fpr, tpr, thresholds = roc_curve(y_test, pred)

    plt.figure()
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % auc)
    plt.fill_between(fpr, tpr, color='#ddeeff')
    plt.plot([0, 1], [0, 1], 'r--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Probability')
    plt.ylabel('True Positive Probability')
    plt.title(f'{data_name.capitalize()} dataset')
    plt.legend(loc="lower right")

    # Uncomment to save plot
    # plt.savefig(f'{data_name}.png')

    plt.show()

    return auc


############################################################################################


# Testing

# dataset = {'file_name' : 'email.tsv', 'timestamp_col' : 3, 'number_of_lines_to_skip' : 1, 'filter' : 26}
# data = features_to_matrix(dataset)
# print(prediction(data, dataset['file_name'].split('.')[0]))