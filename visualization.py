

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
import numpy as np
from matplotlib import cm

#https://randalolson.com/2014/06/28/how-to-make-beautiful-data-visualizations-in-python-with-matplotlib/

def set_color(color):

    if color == 'tab20':
        # These are the "Tableau 20" colors as RGB.  
        colors = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),  
                     (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),  
                     (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),  
                     (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),  
                     (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)] 


        # Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.  
        for i in range(len(colors)):  
            r, g, b = colors[i]  
            colors[i] = (r / 255., g / 255., b / 255.)  
    
    if color == 'neon':
        colors = [(8,247,254),  (254,83,187), (245,211,0), (0,255,65), (148,103,189), (255,0,0)]
        for i in range(len(colors)):  
            r, g, b = colors[i]  
            colors[i] = (r / 255., g / 255., b / 255.) 

        
    mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=colors)
    
    return colors
    
def make_figure(caption_source="caption_source", caption_notes = 'caption_notes', title = 'title', title_below = 'title_below', figsize = (16, 10)):
 
    f, ax = plt.subplots(figsize=figsize)
    
    plt.text(0, -0.14, "Data source: " + caption_source + 
           "\nContact: orn.hjartarson@gmail.com"  
           "\n" + caption_notes, fontsize=10, transform = ax.transAxes)

    remove_stuff(ax)
    
    plt.text(0.5, 1, s = title, fontsize = 20, transform = ax.transAxes, ha = "center")
    plt.text(0.5, 0.97, color = 'grey', s = title_below, fontsize = 14, transform = ax.transAxes, ha="center")

    ax.set_xlabel("")
    ax.set_ylabel("")
    
    set_color(color = 'tab20')

    return ax
    
    
def plot_it(df_plot, ax, highlight_col = [], unit = 'McD', grid = []):
    
    if highlight_col:
        dim_cols = [x for x in df_plot.columns if x not in  highlight_col]
        df_plot[dim_cols].plot(ax=ax, alpha=1, ls='-', lw=2, legend = False)
        df_plot[highlight_col].plot(ax=ax, lw=2.5, legend = False)
    else:
        df_plot.plot(ax=ax,  lw=2, kind='line', legend = False, rot=0, alpha = 1)
        #df_plot.plot(ax=ax,  lw=1, kind='line', legend = False, color = 'black')
    
    
    max_y = df_plot.max().max()
    min_y = df_plot.min().min()
    min_x = df_plot.index[0]
    max_x = df_plot.index[-1]
    
    ax.set_xlim([min_x, max_x])
    ylim = ax.get_ylim()
    
    plt.yticks([])
    plt.xticks([])
    
    for tick in grid:
        plt.text(min_x, tick, str(int(round(tick, 0))) + unit + " ", fontsize = 16, ha = "right", alpha = 1)
        ax.axhline(tick, ls="dashed", lw = 2, color = "black", alpha = 0.1, zorder = 99)
        #ax.plot([min_x, max_x], [50, 50], transform = ax.transAxes)
    
    if True:
        for tick in ['2019','2020', '2021', '2022']:
            plt.text(tick, ylim[0], tick, fontsize = 14, ha = "center", va='top', alpha = 1, rotation=0)
            ax.axvline(tick, ls="dashed", lw = 2, color = "black", alpha = 0.1, zorder = 99)
    
    #ax.text(x=-0.05, size = 16, y=0.5, s = "["+unit+"]", transform = ax.transAxes, rotation = 'vertical')
    
    
    return ax


def remove_stuff(ax):
    # Remove the plot frame lines. They are unnecessary chartjunk.  

    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(True)  
    ax.spines["right"].set_visible(False)  
    ax.spines["left"].set_visible(True)  
    
    # Ensure that the axis ticks only show up on the bottom and left of the plot.  
    # Ticks on the right and top of the plot are generally unnecessary chartjunk.  
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()  
   
    
    #plt.yticks(range(0, 91, 10), [str(x) + "%" for x in range(0, 91, 10)], fontsize=14)  
    plt.yticks(fontsize=14)  
    plt.xticks(fontsize=14)
    
    ax.set_ylabel("", fontsize=16)
    ax.set_xlabel("")
    ax.set_label("")
    #plt.yticks([])
    #plt.xticks([])
    
    
    # Remove the tick marks; they are unnecessary with the tick lines we just plotted.  
    #plt.tick_params(axis="both", which="both", bottom="off", top="off", left="off", right="off") 
    

def put_legend_below(ax, ncol=3):
	# Shrink current axis's height by 10% on the bottom
	box = ax.get_position()
	ax.set_position([box.x0, box.y0 + box.height * 0.1,
					 box.width, box.height * 0.9])

	# Put a legend below current axis
	ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
			  fancybox=False, shadow=False, ncol=ncol, prop={'size': 13})


def put_legend_right(ax, df_plot, color = 'tab20'):

    color = set_color(color = color)
    ylim = ax.get_ylim()
    # LEGEND END OF LINE
    for rank, column in enumerate(df_plot.columns):

        y_pos = (df_plot[column].dropna().values[-1] - ylim[0])/(ylim[1] - ylim[0])

        if column == 'Transport':
            y_pos -= 0.01
        elif column == "Water/Heating Plant":
            y_pos += 0.01  
        elif column == "Electricity":
            y_pos += 0.0
        elif column == "":  
            y_pos -= 0.25  
        
        
        plt.text(1, y_pos, s = " " + str(column), fontsize=16, color=color[rank], transform = ax.transAxes)


def set_monthly_ticks(ax):

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', '']
    plt.xticks(np.linspace(0,365,13), months)
