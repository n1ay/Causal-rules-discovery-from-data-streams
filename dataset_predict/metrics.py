from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score, f1_score
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def get_metrics(true: pd.DataFrame, pred: pd.DataFrame):
    ACC = accuracy_score(true, pred)
    precision = precision_score(true, pred, average='weighted')
    recall = recall_score(true, pred, average='weighted')
    F1 = f1_score(true, pred, average='weighted')

    return [ACC, precision, recall, F1]


def print_metrics(metrics):
    print("Accuracy: {0[0]}, Precision: {0[1]}, Recall: {0[2]}, F1-Score: {0[3]}\n".format(metrics))


def get_metrics_full(true: pd.DataFrame, pred: pd.DataFrame, mean=True):
    metrics = np.array([])
    for i in range(len(true)):
        metrics = np.concatenate((metrics, get_metrics(true[i], pred[i])), axis=0)

    metrics = metrics.reshape(len(true), 4)

    if mean:
        return np.mean(metrics, axis=0)
    else:
        return metrics


def plot(true, pred, title):
    x = range(len(true))
    fig = plt.figure()
    plt.plot(x, true.values.flatten().tolist(), label='Ground truth values', color='green')
    plt.plot(x, pred.values.flatten().tolist(), label='Predicted values', color='purple')
    plt.title(title)
    plt.xlabel('Index')
    plt.ylabel('Value')
    lgd = plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), fancybox=True, shadow=True, ncol=2)
    fig.savefig(title+'.pdf', dpi=600, format='pdf', bbox_extra_artists=(lgd,), bbox_inches='tight')
    print('Plot has been saved to '+title+'.pdf')
    #plt.show()


def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    fig.savefig(title+'_cm.pdf', dpi=600, format='pdf')
    print('Confusion matrix has been saved to '+title+'_cm.pdf')
    #plt.show()
    return ax

def present_results(true, pred, title):
    classes = list(set(true.iloc[:, 0].unique()).union(set(pred.iloc[:, 0].unique())))
    print_metrics(get_metrics(true, pred))
    plot(true, pred, title)
    plot_confusion_matrix(true, pred, classes, normalize=True, title=title)
