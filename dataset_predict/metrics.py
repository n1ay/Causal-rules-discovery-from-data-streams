from sklearn.metrics import confusion_matrix
import numpy as np

def get_metrics(true, pred):
    cm = confusion_matrix(true, pred)

    FP = np.mean(cm.sum(axis=0) - np.diag(cm))
    FN = np.mean(cm.sum(axis=1) - np.diag(cm))
    TP = np.mean(np.diag(cm))
    TN = np.mean(cm.sum() - (FP + FN + TP))

    Pos = TP+FN
    Neg = TN+FP

    TPR = TP/Pos #recall
    TNG = TN/Neg
    FPR = 1 - TNG

    ACC = (TP+TN)/(Pos+Neg)

    precision = TP/(TP+FP)
    F1=2*(TPR*precision)/(TPR+precision)

    return [ACC, TPR, FPR, precision, TPR, F1]

def print_metrics(metrics):
    print("Accuracy: {0[0]}, TP Rate: {0[1]}, FP Rate: {0[2]}, Precision: {0[3]}, Recall: {0[4]}, F1-Score: {0[5]}\n".format(metrics))

def get_metrics_mean(true, pred):
    metrics = np.array([])
    for i in range(len(true)):
        metrics = np.concatenate((metrics, get_metrics(true[i], pred[i])), axis=0)

    metrics = metrics.reshape(len(true), 6)

    #return (ACC, TPR, FPR, precision, TPR, F1)
    return np.mean(metrics, axis=0)