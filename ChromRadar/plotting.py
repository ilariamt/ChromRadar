
# SPIDER PLOT COLORATO DI ANNA    
def spider_plot(data, category, genesets, color_fill=False, save=None, dpi=300):
    import matplotlib.pyplot as plt
    import numpy as np
    from math import pi
    import scanpy.plotting._utils
    import pandas as pd

    if category + "_colors" not in data.uns.keys():
        scanpy.plotting._utils.add_colors_for_categorical_sample_annotation(data, category)

    # Associates cluster categories to palette generated automatically by scanpy
    cluster2color = {cl:col for cl,col in zip(data.obs[category].cat.categories, data.uns[f"{category}_colors"])}

    term2plot = genesets.keys()

    # Spiderplot
    # This has requirement the gsea
    index = []
    df = []
    term2plot = genesets.keys()
    for cl in data.uns['gsea'].keys():
        index.append(cl)
        df.append([data.uns['gsea'][cl]['results'][term]['es'] for term in term2plot])
    df = pd.DataFrame(df, columns=term2plot, index=pd.Index(index, name='Cluster'))
    df = (df+1).divide((df+1).sum(axis=1), axis=0)
    # number of variable
    categories=df.columns.values.tolist()
    N = len(categories)
    # number of panels (subjects or clusters)
    subjects = df.index.values.tolist()
    npanels = len(subjects)
    ncol = np.ceil(np.sqrt(npanels))
    ncol=int(ncol)
    fig = plt.figure(figsize=(5*ncol, 5*ncol))
    c=1
    for p in range(npanels):
        # Initialise the spider plot
        ax = plt.subplot(ncol, ncol, c, polar=True)
        c+=1
        # We are going to plot the first line of the data frame.
        # But we need to repeat the first value to close the circular graph:
        values=df.iloc[p,:].values.flatten().tolist()
        values += values[:1]
        values
        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]
        idx = np.argmax(values)
        ax.plot(angles[idx], values[idx], 'ro')


        # Draw ylabels
        ax.set_rlabel_position(90)
        # Plot data
        
        # Fill area
        
        if color_fill:
            ax.plot(angles, values, linewidth=1, linestyle='solid', color=cluster2color[subjects[p]])
            ax.fill(angles, values, 'b', alpha=0.1, color=cluster2color[subjects[p]])
        else:
            ax.plot(angles, values, linewidth=1, linestyle='solid')
            ax.fill(angles, values, 'b', alpha=0.1)
            
        ax.set_title(f"Cluster_{subjects[p]}")
        # Draw one axe per variable + add labels labels yet
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=12)


    plt.tight_layout()
    if save:
        plt.savefig(save, dpi=dpi)
    plt.show()


# SPIDER PLOT GLOBALE DI ANNA
def spider_plot_global(data, category, genesets, linewidth=1, fill=True, save=None, dpi=300):
    import matplotlib.pyplot as plt
    import numpy as np
    from math import pi
    import scanpy.plotting._utils
    import pandas as pd

    if category + "_colors" not in data.uns.keys():
        scanpy.plotting._utils.add_colors_for_categorical_sample_annotation(data, category)

    # Associates cluster categories to palette generated automatically by scanpy
    cluster2color = {cl:col for cl,col in zip(data.obs[category].cat.categories, data.uns[f"{category}_colors"])}

    term2plot = genesets.keys()

    # Spiderplot
    # This has requirement the gsea
    index = []
    df = []
    term2plot = genesets.keys()
    for cl in data.uns['gsea'].keys():
        index.append(cl)
        df.append([data.uns['gsea'][cl]['results'][term]['es'] for term in term2plot])
    df = pd.DataFrame(df, columns=term2plot, index=pd.Index(index, name='Cluster'))
    df = (df+1).divide((df+1).sum(axis=1), axis=0)
    # number of variable
    categories=df.columns.values.tolist()
    N = len(categories)
    # number of panels (subjects or clusters)
    subjects = df.index.values.tolist()
    npanels = len(subjects)



    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(5,5))
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    idx = np.where(df.values == np.max(df.values))
    #rticklabel=np.round(np.arange(0, round(df.values.flatten()[idx],2)+0.05, 0.05),2)
    ax.plot(angles[idx[1][0]],df.values[idx]) #'ro'
#     plt.draw()
#     labelsY = [np.round(float(item.get_text()),2) for item in ax.get_yticklabels()]

#     # # Draw ylabels
#     ax.set_yticklabels(labelsY,fontsize=8) #fontweight='bold')


    ax.set_rlabel_position(90)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=12)
    #ax.set_yticklabels([]) #to remove radial labels 


    for p in range(npanels):
        values=df.iloc[p,:].values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=linewidth, linestyle='solid', color=cluster2color[subjects[p]])
        if fill:
            # Fill area
            ax.fill(angles, values, 'b', alpha=0.1, color=cluster2color[subjects[p]])

    
    plt.tight_layout()
    if save:
        plt.savefig(save, dpi=dpi)
    plt.show()
