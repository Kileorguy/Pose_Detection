# Pose_Detection

## Installation

This guide demonstrates how to install the library using Anaconda. Feel free to use another tool if you prefer. Feel free to change the environment name too if you prefer, in this case I will be using "Pose_Detection"

1. Open Command Prompt from the root folder 

2. Create an Anaconda environment with Python 3.10.x:  
   ```bash
   conda create -n Pose_Detection python=3.10
3. Activate the anaconda environment
    ```bash
   conda activate Pose_Detection
4. Install the libraries based on requirements.txt
    ```bash
    pip install -r requirements.txt
## PreProcessing

- Convert to RGB : because mediapipe input image is RGB so the image must be in RGB order.
- Image Augmentation : Enhancing the dataset by generating additional images through flipping, rotating, and stretching. This helps address the issue of a limited original dataset.
- Landmark Detection : Detecting the human sekeletal structure so it can be trained through SVM. The detail can be seen in the picture below :

![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/937b0b22-b87b-4650-916e-b035c9ae2141/8d289e92-7a33-40eb-bced-436eeaca2da8/image.png)

In the code, only 23-28 are selected.

- Calculate knee degree : Uses numpy arctan2 formula to calculate the degree of both knee and adding it to the dataset.
- Convert to CSV

## Modeling

- Read CSV : Read from previously generated CSV
- Check duplicates and NA values
- Remove Outliers : This process uses the interquartile method, which removes the data under the lower bound (Q1 - 1.5 * IQR) and above the upper bound (Q3 + 1.5 * IQR). This method is used to prevent anomalous data from mediapipe from being used in training.
- Train SVM with Gridsearch : Grid search is used for hyperparameter so it could search for the best parameter.

## Testing

- Open Video : Uses opencv to load the video.
- Extract each frame.
- Landmark Detection : To detect the skeletal structure like previously in the preprocessing method.
- Calculate Knee Degree : To calculate the degree of both knee in the video.
- Change to tabular data : Convert the data into pandas DataFrame format so it can be used for prediction.
- Predict using SVM : This will return between Standing, Half Lunge, or Full Lunge.

## Weakness

This model is not able to predict correctly if the person is standing facing forward because the data mostly consists of a person standing facing to the side, not the front.

## Application Demo
<!-- ![Image](https://github.com/Kileorguy/Review_Analyzer_RAG/blob/main/Documentation/Website.png?raw=true)
[Demo Video Here](https://www.youtube.com/watch?v=qA8o_w6GvJg) -->



