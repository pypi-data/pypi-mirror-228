def scatter_box(data1, data2, metric):
    """This function create boxplot to compare the metric in two datasets

    Args:
        data1 (pandas DataFrame): The first dataframe
        data2 (pandas DataFrame): The second dataframe
        metric (str): The name of the metric column to compare.
    
    Return:
        ax (Axes): The Axes object containing the boxplot.
    """
    import seaborn as sns
    import matplotlib.pyplot as plt
    plt.figure(figsize=(8,8))
    ax = sns.boxplot(data = [data1[metric],data2[metric]],
                palette = 'colorblind',
                showfliers = False,
                boxprops=dict(alpha=.3)
                )
    sns.stripplot(data = [data1[metric],data2[metric]],
                palette = 'colorblind',
                alpha = 1,
                jitter = True)                
    ax.set_title(f"comparison on {metric}", fontsize=16)
    plt.show()

    return ax
