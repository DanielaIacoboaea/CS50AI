# CS50AI Neural Networks Project - Traffic 

The purpose of this document is to describe the *experimentation process* of using **TensorFlow**  
to build a **Convolutional neural network** to classify traffic signs based on an image of those signs.

##### Abreviations used: 
* **Convolutional Layer** - *Conv-Layer*
* **Max-pooling Layer** - *Max-Layer*
* **Hidden Layer** - *Hidden-Layer*
* **Training data set** - *Train-Set*
* **Testing data set** - *Test-Set*

---

### What did you try?
    
I tried to figure out what setting of the parameters works best in terms of **accuracy** and **loss** for both  
the *Train-Set* and for the *Test-Set*, keeping in mind the computational **time** as well:

* I started with **1** *Conv-Layer* and **1** *Max-Layer* and worked towards getting the best option for  
the number of *units* in the *Hidden-Layer* and the number of *Hidden-Layers* in the neural network
* The purpose was, by extracting the features maps only once and resizing the images only once, check what  
settings for the *Hidden-Layer* can lead to a good performance
* After finding parameters that perform better for the hidden layer, I tried adding more *Hidden-Layers* with   different number of units for each layer 
* Also I tried adjusting the *Dropout* rate between 0.2 and 0.6 for the *Hidden-Layer*  
* After that I tried extracting more feature maps and reducing the images even further by adding another *Conv-Layer*  
and another *Max-Layer* 
* Also tried to change pooling-size from (2,2) to (3,3) and have different sizes between layers
* The variations in *units* for the *Hidden-Layer* used:
    * 8, 16, 32, 64, 128 and 256
    * used only one layer of each with different parameters for the *Conv-Layers*
    * used variations of up to 3 hidden layers with different number of units for each *Hidden-Layer*:  
    
    e.g: (32, 64), (32, 64, 128), (64, 128, 256), (64, 64)
* The variations in the number of training *filters* for the *Conv-Layer*:
    * 32, 64, 128
    * used from 1 - 3 layers with different paratemers settings
* At first I didn't add any Dropout to the *Conv-Layers*, but then I found that this layers can have a *Dropout* rate  
as well and tried using smaller *Dropout* rates for them

    
### What worked well?

As the number of *units* increased in the *Hidden-Layer*, the accuracy started improving significantly.  

Having at least 2 layers of *Conv-Layer* increased **accuracy**, but if the number of *units* in the *Hidden-Layer*  
was small, it wasn't enough to boost the **accuracy** on their own.  

By contrast, removing a *Conv-Layer* when the number of *units* in the *Hidden-Layer* is large enough,  
resulted in performance drop.

Having only one *Hidden-Layer* performed best, adding multiple *Hidden-Layers* did not improve **accuracy** and  
**loss** significantly.   
But maybe ths depends on the size of the data as well, in this case, the number of images   
was relatively small(500). More *Hidden-Layers* might perform better for a larger data set.

Adding a smaller *Dropout* Rate of 0.2 to each of the *Conv-Layer* increased performance and allows for a higher  
*Dropout* rate in the *Hidden-Layer*: e.g 0.5.


### What didn’t work well?

Increasing the number of filters in the *Conv-Layer* and the number of *Conv-Layers* did not improve performance  
when the number of units in the *Hidden-Layer* was bellow 128.  
Keeping a high Dropout rate of 0.5 - 0.6 in *Hidden-Layers* with number of *units* less than 128 lead to poor  
accuracy results in the *Train-Set*. I assume this is bacause it had fewer units to train on. 

Due to the fact that the images are small (30*30), when trying to set a higher pooling-size, the size of the image   
decreased rapidly, so the best setting was of (2,2) for the *Max-Layers* to allow it to be used multiple times (max of 3 times).


### What did you notice?

Having a smaller *Dropout* rate for the *Hidden-Layer* lead to increased **accuracy** in the *Train-Set*, but at the same time this leads to overfitting.  

For e.g a 64 units *Hidden-Layer* with *Dropout* rate 0.2 performed a lot better than with a 0.5 *Dropout* rate.
So a way of making the data more resilient before reaching the *Hidden-Layer* or *Hidden-Layers* was needed.

Adding more *Conv-Layers* increases the computational *time*.

If the *Conv-Layers* is kept to one, having more *Hidden-Layers*(e.g 64 and 128 units) that perform well, does not increase the performance.  

Changing the number of units between different layers increased performance.  
For e.g: having a *Conv-Layer* with 32 filters and the next one with 64 filters.  

---

### Conclusion:

Starting from this **accuracy** and **loss** results for the first setting of parameters:

* 1 *Conv-Layer* and 1 *Max-Layer* 
* 8 units for the *Hidden-Layer*
* **Accuracy**: **5%**

>**Epoch 1/10**  
>500/500 [==============================] - 3s 5ms/step - loss: 3.6827 - accuracy: 0.0532  
>**Epoch 10/10**  
>500/500 [==============================] - 2s 5ms/step - loss: 3.4932 - accuracy: 0.0569  
>**Test set**  
>333/333 - 1s - loss: 3.5049 - **accuracy: 0.0555** - 533ms/epoch - 2ms/step


After going throught the logic described above with different values for the parameters of *Conv-Layers*, *Max-Layers*, *Hidden-Layers*, *Dropout* rates, and throught different numbers of layers, it turns out that:
* 1 *Hidden-Layer* of 128 units and *Dropout* 0.5 performs best  
* 2 *Conv-Layer* with *Dropout* 0.2 and different filters settings (32 and 64) 
* 2 *Max-Layers* with pool size (2, 2) 
* Can get us to:  
    * An **accuracy** up to **93%** for the *Train-Set* and an **accuracy** of **98%** for *Test-Set*.
    
> **Epoch 1/10**  
> 500/500 [==============================] - 5s 9ms/step - loss: 2.3923 - accuracy: 0.3475   
> **Epoch 10/10**    
> 500/500 [==============================] - 6s 11ms/step - loss: 0.1986 - accuracy: 0.9352  
> **Test set**  
333/333 - 1s - loss: 0.0612 - accuracy: 0.9842 - 1s/epoch - 3ms/step

---
##### As a side note, without the screen recorder each training sessions runs in avg 6-7 sec and with the screen recorder running (for the youtube video), each session runs for 14-15 sec on avg
