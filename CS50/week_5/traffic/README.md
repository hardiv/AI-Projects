My first course of action for this project was to try and construct a neural network similar to the one in the source 
code, i.e. 

- an input layer
- one hidden layer
- an output layer

However, it was clear that this kind of NN wouldn't work very well for this task, and this was backed up by the 27% 
accuracy of the network. So, I decided to add in a few more hidden layers and take a look at how that would go. I also 
used some different activation functions like tanh and added in a dropout layer. This time, the accuracy had actually
dropped down to 2%, leaving me very confused. 

I realised what I was missing: some convolution, in order to allow the NN to actually look for features in the image
rather than just look at each pixel and try and figure out what the image is on a larger scale. So I added in 3 
convolutional and 3 2x2 pooling layers before the input layer, and changed my activation function for the
hidden layer from softmax to relu, and that seemed to do the rick, getting me to 97.04% accuracy. I experimented with
adding more hidden layers, but this didn't really affect the accuracy much (to 97.09%).
