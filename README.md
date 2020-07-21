# Deep Leaning Based Data Augmentation Method and Signature Verification System for Offline Handwritten Signature

Verify authenticity of offline handwritten signatures according to the writer dependent approach through digital image processing and neural networks.

There are offline signature examples of two individuals named 0115 and 129 from the databases listed below in the Data folder. In addition, the signature samples reconstructed with the proposed data augmentation method are in the data folder.

We couldn't upload trained weights here because there is a 100MB file limit on GitHub. You can download pre-trained weight from **[HERE](http://mutluyapici.com/wp-content/uploads/2017/09/M0115_weight.h5)** 

# Step By Step Usage
      
   1- Download all files and folders.
   
   2- If you want to see performance of the system, download pre-trained weight from **[HERE](http://mutluyapici.com/wp-content/uploads/2017/09/M0115_weight.h5)**
  .Then move the file in /data/Mimza_0115 directory.
   
   3- Run all codes in **loadData.py**
   
   4- Run all codes in **loadModel.py**
   
   5- Run the required codes in **trainAndAnalysis.py**  according to the your plans
    

# Built with

    Keras
    Tensorflow

# Requirements

    Python 3.6.0
    Numpy
    Keras 2.2.0
    Tensorflow
    h5py 2.9.0
        

# Dataset

The dataset used was gotten from the GPDS and MCYT signature databases. More details are available to the links below.

**[More Information About GPDSsyntheticSignature Dataset](http://www.gpds.ulpgc.es/downloadnew/download.htm)**

**[More Information About MCYT-75 Dataset](http://atvs.ii.uam.es/atvs/mcyt75so.html)**

# Accuracy

The model acheived an accuracy of 98.06% F1 Score and 2.58% EER with 10 Genuine samples on the MCYT signature dataset. 
