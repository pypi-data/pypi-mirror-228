'''Model Performance'''
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, precision_recall_curve, auc
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd



def plotModelMetrics(model, x_tst, y_tst,  title= '', binary= False, plot = True):
    '''
    old name : lgbm_metrics_plot
    '''
    if len(title)>0:
        print(title)

    print('Model accuracy {:.4f}'.format(model.score(x_tr,y_tr)))
    if binary == True:
        y_hat = model.predict(x_tst)
        y_hat = [1 if i>0 else i for i in y_hat ]
        y_tst = [1 if i>0 else i for i in y_tst ]
    else:
        y_hat = model.predict(x_tst)

    report = metrics.classification_report(y_tst, y_hat, output_dict=True)
    if plot:
        print('Classification Report')
        print(metrics.classification_report(y_tst,y_hat))
        
        if binary == False:
            print('Confsion Matrix')
            metrics.plot_confusion_matrix(model,x_tst,y_tst,cmap='Blues_r')
        else:
            plotConfusionMatrix_binary(y_tst, y_hat, plot_title = 'Confsion Matrix')
    return report

def plotConfusionMatrix_binary(y_tst, y_hat, plot_title = ''):
    cf_matrix = confusion_matrix(y_tst, y_hat)

    ax = sns.heatmap(cf_matrix, annot=True, cmap='Blues', fmt='g')

    ax.set_title(plot_title)
    ax.set_xlabel('\nPredicted Values')
    ax.set_ylabel('Actual Values ')
    ax.xaxis.set_ticklabels(['False','True'])
    ax.yaxis.set_ticklabels(['False','True'])

    ## Display the visualization of the Confusion Matrix.
    plt.show()


def plotPrecisionRecallCurve_binary(model, x, y, return_plot = True):
    '''
    old name : plotPrecisionRecallCurve
    '''
    y_score = model.predict_proba(x)
    pr, tpr, th = precision_recall_curve(y, y_score[:,1])
    pr_re_auc = auc(tpr, pr)
    pr = [0] + list(pr) 
    tpr = [1] + list(tpr)
    plt.plot(pr, tpr, label = 'Pr-Recall Curve (area = %0.2f)'% pr_re_auc)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('recall')
    plt.ylabel('precision')
    plt.legend(loc="lower left")
    plt.show()
    
    if return_plot:
        fig = plt.gcf()
        return fig

def createSubplotsGrid(num_plots):
        """
        Creates a grid of subplots with 3 columns.
        
        :param num_plots: Total number of subplots required.
        :return: Figure and array of axes.
        """
        num_rows = -(-num_plots // 4)  # Calculate the number of rows required. This is equivalent to ceiling division.
        fig, axs = plt.subplots(num_rows, 4, figsize=(10, 3*num_rows)) # 12 width, 4 height for each row
        return fig, axs

def plotPrecisionRecallCurve_multiclass(model, x_test, y_test, return_plot = False):

    pr, tpr, roc_auc = dict(), dict(), dict()
    import pandas as pd
    y_score = model.predict_proba(x_test)
    y = pd.get_dummies(y_test, prefix='typ')
    fig, axs = createSubplotsGrid(y.shape[1])

    for i in range(y.shape[1]):
        pr[i], tpr[i], _ = precision_recall_curve(y.iloc[:, i], y_score[:, i])
        roc_auc[i] = auc( tpr[i], pr[i])
    for i in range(y.shape[1]):
            y_vals = [0] + list(pr[i])
            x_vals = [1] + list(tpr[i])
            # Get the axis for current plot. 
            # Since axs can be 1D (if only 1 row) or 2D, we handle both cases.
            if axs.ndim == 1:
                ax = axs[i]
            else:
                ax = axs[i//3, i%3]
            ax.plot(x_vals, y_vals,)
            ax.plot([1, 0], [1, 0], 'k--')
            ax.set_xlim([0.0, 1.0])
            ax.set_ylim([0.0, 1.05])
            ax.set_xlabel('Recall')
            ax.set_ylabel('Precision')
            ax.set_title('ROC curve for label {} (area = {})'.format(i, round(roc_auc[i],2)), fontsize=9)
        # Hide any unused axes
    total_axes = axs.size
    for j in range(i+1, total_axes):
        if axs.ndim == 1:
            axs[j].axis('off')
        else:
            axs[j//3, j%3].axis('off')
    plt.tight_layout() 

    if return_plot:
        return fig

