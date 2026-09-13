import matplotlib.pyplot as plt
import numpy as np

def plot_residuals(y_test, preds):
    """Plot residuals to evaluate regression."""
    residuals = y_test - preds
    fig, axes = plt.subplots(1, 2, figsize=(15, 3))

    axes[0].scatter(np.arange(residuals.shape[0]), residuals)
    axes[0].set(xlabel='Observation', ylabel='Residual')

    residuals.plot(kind='kde', ax=axes[1])
    axes[1].set_xlabel('Residual')

    plt.suptitle('Residuals')
    return axes