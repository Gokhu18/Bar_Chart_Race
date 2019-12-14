from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as img
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation
import pandas as pd
import random

# Read Dataset
usecols = [0]
usecols.extend(list(range(4,65)))
df = pd.read_csv("Population_Dataset.csv", usecols=usecols, header = 0)

# Generate Random Color for Color Column in Dataset
def randomColorGenerate(dfColumn):
    color = "#%06x" % random.randint(0, 0xFFFFFF)
    if color in dfColumn.values.astype(str):
        randomColorGenerate(dfColumn)
    else:
        return color

# Fill colors in Color Column for NaN values
for i in df.index:
    color = randomColorGenerate(df['Color'])
    df['Color'] = df['Color'].fillna(color,limit = 1)

#print(df.head())

# Extract years
years = df.columns[1:-2]

# Draw Bar Chart
fig, ax = plt.subplots(figsize=(14,6))

def drawChart(Currentyear):
    df.sort_values(by = str(Currentyear), ascending = False, inplace=True)
    ax.clear()
    
    country = df.iloc[:,0].head(10)
    population = df[str(Currentyear)].head(10)
    colors = df['Color'].head(10)
    imagesPath = df['ImagesPath'].head(10)

    ax.barh(country, population, align='center', color = colors)   

    # Axis Configuration
    ax.invert_yaxis()
    plt.box(False)
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.tick_params(axis='x', colors='#777777', labelsize=10)
    ax.set_yticks([])

    dx = population.max() / 40

    for i,(cn,p,iP) in enumerate(zip(country,population,imagesPath)):
        ax.text(p-dx, i+.15, cn, color = "#ffffff", size=10, weight=600, ha='right', va='bottom')
        ax.text(p+dx, i, f"{p:,.0f}",  size=10, ha='left',  va='center')
        # Figure
        flag = img.imread(str(iP))
        imagebox = OffsetImage(flag, zoom=0.15)
        ab = AnnotationBbox(imagebox, (p, i),bboxprops =dict(edgecolor='#000000',color='#000000',boxstyle="square,pad=0.1"))
        ax.add_artist(ab)

    
    ax.text(1, 0.4, Currentyear, transform=ax.transAxes, size=40, ha='right', weight=800)

    ax.text(0, 1.15, 'The most populous cities in the world from 1960 to 2018',
                transform=ax.transAxes, size=24, weight=600, ha='left', va='top')

# end drawChart function

drawChart(1960)

# Save Figure
# plt.savefig("Bar_Char_Race_pic.png", dpi = 500)

plt.show()


# If you want to enable animation then remove below comment
"""
# Animation
# Call the animator	 
animator = FuncAnimation(fig, drawChart, frames=years, interval=50, repeat = False)
# Save Animation
Writer = animation.writers['ffmpeg']
writer = Writer(fps=29, metadata=dict(artist='Khalid'))
animator.save("BarAnimation.mp4", writer = writer, dpi = 500)
plt.show()"""

# Done