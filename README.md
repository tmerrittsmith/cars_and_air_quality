## Counting cars and Air quality

I've been interested in open data for a while, and [Newcastle City Council](https://www.netraveldata.co.uk/) has combined forces with the [University] (https://urbanobservatory.ac.uk/) here to do some interesting things.

Specifically, there's an air quality monitor and a cctv traffic camera near a local primary school. This got me wondering: is it possible to see a relation between changes in air quality and the number of cars on the road. 

The problem is not straightforward, and of course correlation doesn't imply causation, but the results are quite nice. Along the way, I learnt a bit about object detection using the FasteR-CNN model, pretrained on the COCOv3 dataset.


Here's a plot of the two results over time:
![](air_quality_plot.png "Air quality plot")


and here's a GIF (which I generated using [gifsicle](https://www.lcdf.org/gifsicle/):

![](chilli_road_counting_cars.gif)

I used google colab to do the heavy lifting, you can see the notebook [here](https://colab.research.google.com/drive/13ifhi58oW9rgJ9IIUnRywjTGD_DUir0J?usp=sharing)

The script to download images from the cctv api is in this repo. I had trouble setting up the listener, so ended up just checking the api for a new update every so often.
