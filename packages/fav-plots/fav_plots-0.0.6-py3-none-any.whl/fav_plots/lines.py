def show_facet_line():
    
    from plotnine import ggplot, geom_point, aes, stat_smooth, facet_wrap
    from plotnine.themes import theme_minimal
    from plotnine.scales import scale_color_manual
    from fav_plots.utils import custom_colors
    from plotnine.data import mtcars
    import matplotlib.pyplot as plt

    graph = (ggplot(mtcars, aes('wt', 'mpg', color='factor(gear)'))
    + geom_point()
    + stat_smooth(method='lm', se = False)
    + facet_wrap('gear')
    + theme_minimal()
    + scale_color_manual(values = custom_colors())
    )
    
    graph.draw()
    plt.show()

def draw_facet_line(df, x, y, facet):
    
    from plotnine import ggplot, geom_point, aes, stat_smooth, facet_wrap
    from plotnine.themes import theme_minimal
    from plotnine.scales import scale_color_manual
    from fav_plots.utils import custom_colors
    from plotnine.data import mtcars
    import matplotlib.pyplot as plt
    
    graph = (ggplot(df, aes(x, y, fill = facet))
    + geom_point()
    + stat_smooth(method='lm', se = False)
    + facet_wrap(facet)
    + theme_minimal()
    + scale_color_manual(values = custom_colors())
    )
    
    graph.draw()
    plt.show()