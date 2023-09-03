### USAGE
---
#### Beautify Your Plot

First of all, you need to import the package:

```python
from pymeili import beautifyplot as bplt
```    
Then, you can use the function `beautifyplot` to beautify your plot. Unlike `matplotlib.pyplot`, you don't need to create a figure and axes object. When you begin to plot, set the figsize to initialize your canvas by using `initplot` function. For instance:

```python
from pymeili import beautifyplot as bplt
bplt.initplot(figsize=(10, 5))
```
You can set up the theme of your plot in the same function, the theme style can be 'default' or 'dark'. For instance, if you want to create a subplot with dark theme, you can use the code below:

```python
from pymeili import beautifyplot as bplt
subplot = bplt.initsubplots(2, 1, figsize=(10, 6), style='dark')
```
where nrows=2, ncols=1 in this case.

Now, you can plot your data in your canvas. For instance, if you want to plot a line chart, you can use the code below:

```python
# import the packages
from pymeili import beautifyplot as bplt
import numpy as np

# set the x and y axis data
x = np.linspace(0, 2*np.pi, 100)
y = np.linspace(0, 2*np.pi, 100)

# plot the line chart
bplt.initplot(figsize=(10, 5), style='default')
bplt.plot(x, np.sin(x), label='sin')
bplt.plot(x, np.cos(x), label='cos')
bplt.title('test')
bplt.xtick(np.linspace(0, 2*np.pi, 5), ['0', 'pi/2', 'pi', '3pi/2', '2pi'])
bplt.ytick(np.linspace(-1, 1, 5), ['1', '0.5', '0', '-0.5', '-1'])
bplt.xlabel('x')
bplt.ylabel('y')
bplt.legend()
bplt.spines()
bplt.twinx()
bplt.grid()
bplt.show()
bplt.savefig('test_1.png')
bplt.clf()
```
More functions are waiting for you to explore, and most syntax are similar to `matplotlib.pyplot`
For instance, if you want to plot a contourf chart, you can use the code below:

```python
# import the packages
from pymeili import beautifyplot as bplt
import numpy as np

# set the x and y axis data
x = np.linspace(0, 2*np.pi, 100)
y = np.linspace(0, 2*np.pi, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) + np.cos(Y)

# plot the contourf chart
subplot = bplt.initsubplots(2, 1, figsize=(8, 5))
subplot[0].righttitle('test')
subplot[0].spines()
subplot[1].contourf(X, Y, Z)
subplot[1].title('test1')
subplot[1].xlabel('x')
subplot[1].ylabel('y')
subplot[1].righttitle('test2')
subplot[1].spines()
subplot[1].twinx()
subplot.suptitle('test3')
bplt.savefig('test_2.png', dpi=300)
bplt.clf()
```
Another example, if you want to plot the map, you can use function `Basemap` like the code below:

```python
# import the packages
from pymeili import beautifyplot as bplt

# plot the map
bplt.initplot(figsize=(18, 6), style='d') # style='d' means dark theme as well
map = bplt.Basemap(lat_0=0, lon_0=195, llcrnrlat=-15, urcrnrlat=15, llcrnrlon=90, urcrnrlon=300, resolution='l')
map.drawparallels(np.arange(-15., 15., 5.), labels=[0, 0, 0, 0], fontsize=10, linewidth=0.3, alpha=0.2)
map.drawmeridians(np.arange(90., 300., 5.), labels=[0, 0, 0, 0], fontsize=10, linewidth=0.3, alpha=0.2)
map.fillcontinents()
map.drawrivers()
bplt.axhline(-5, color='2', linewidth=3.5)
bplt.xlabel('Longitude', fontsize=14)
bplt.ylabel('Latitude', fontsize=14)
bplt.spines()
bplt.xticks([90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 240, 255, 270, 285, 300], ['90°E', '105°E', '120°E', '135°E', '150°E', '165°E', '180°', '165°W', '150°W', '135°W', '120°W', '105°W', '90°W', '75°W', '60°W'])
bplt.yticks([-15, -10, -5, 0, 5, 10, 15], ['15°S', '10°S', '5°S', '0°', '5°N', '10°N', '15°N'])
bplt.lefttitle('FIGURE 1', fontsize=15)
bplt.righttitle('Maritime Continent Zone', fontsize=15)
bplt.savefig('test_3.png', dpi=300)
```







You can find out that the syntax will be more simple and clear. Enjoy it!

In your code, when the system does not find the font file, it will raise an error. You can use the function `redirectfontfolder` to redirect the font folder which contains the font file. For instance: if you have moved the font file to the folder `C:\Users\Username\AppData\Local\Programs\Python\Python311\Lib\site-packages\pymeili`, you can use the code below:

```python
from pymeili import beautifyplot as bplt

path = 'C:\\Users\\Username\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\pymeili'
bplt.redirectfontfolder(path)
```
By the way, if you do not know the default fontpath, try to use the function below:

```python
from pymeili import beautifyplot as bplt

bplt.inspectfontfolder()
```
The system will print the default fontpath in your terminal.




#### Beautify Your Terminal Text

First of all, you need to import the package:

```python
from pymeili import beautifyterminal as btml
```    
Then, you can use the function `bprint` to beautify your terminal text. For instance:

```python
from pymeili import beautifyterminal as btml
from pymeili import beautifyterminal.bprint as bp

bp('Hello World', bg.CYAN, fg.BOLD, end=' ')
```
add the `bg` (background) or `fg` (foreground) color to your output text. To know which style you can use, try to use the function below:

```python
from pymeili import beautifyterminal as btml

btml.inspectfg()

btml.inspectbg()
```
Very simple, right? Enjoy it!