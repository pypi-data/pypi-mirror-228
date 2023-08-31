def prop_per_x(x, count):
    import pandas as pd
    """
    Compute the proportion of the counts for each value of x
    """
    df = pd.DataFrame({
        'x': x,
        'count': count
    })
    prop = df['count']/df.groupby('x')['count'].transform('sum')
    return prop

def bar_pct_plot(df, category, fill):
    import pandas as pd
    from plotnine import ggplot, geom_bar, geom_label, aes, after_stat
    from fav_plots.bars import prop_per_x
    import matplotlib.pyplot as plt

    graph = (ggplot(df, aes('factor(category)', fill='factor(fill)'))
    + geom_bar(position='fill')
    + geom_label(
        aes(label=after_stat('prop_per_x(x, count) * 100')),
        stat='count',
        position='fill',
        format_string='{:.1f}%',
        size=9,
    )
    )
    graph.draw()
    plt.show()

