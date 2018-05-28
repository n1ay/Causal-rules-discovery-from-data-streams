from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score, f1_score
import numpy as np

def get_metrics(true, pred):
    ACC = accuracy_score(true, pred)
    precision = precision_score(true, pred, average='weighted')
    recall = recall_score(true, pred, average='weighted')
    F1 = f1_score(true, pred, average='weighted')

    return [ACC, precision, recall, F1]

def print_metrics(metrics):
    print("Accuracy: {0[0]}, Precision: {0[1]}, Recall: {0[2]}, F1-Score: {0[3]}\n".format(metrics))

def get_metrics_full(true, pred, mean=True):
    metrics = np.array([])
    for i in range(len(true)):
        metrics = np.concatenate((metrics, get_metrics(true[i], pred[i])), axis=0)

    metrics = metrics.reshape(len(true), 4)

    if mean:
        return np.mean(metrics, axis=0)
    else:
        return metrics