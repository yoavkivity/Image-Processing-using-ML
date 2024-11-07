
**_Image-Processing-using-ML_**
__Overview_

_This project automates the process of preparing images for laser engraving on wood blocks. It uses a machine learning model to predict optimal image adjustment parameters, improving clarity, sharpness, and contrast for high-quality engraving._


**Project Components**
**_1. adjust_image_ratio.py_**

_This script crops the original image to a fixed aspect ratio based on the size of the wooden block_.![crop_image](https://github.com/user-attachments/assets/bfbfa50b-1f88-47bc-9675-591bfd863247)


**_2. calc_and_filter_best_results.py_**

_Uses the ML model to predict parameters for image adjustments, filters out bad results, and saves the best images with a preview on a BIRCH wood background_.


**_3. manual_picker.py_**

_Displays preview images side by side, letting you choose the best one. The selected image is then loaded into LaserGRBL for engraving (LaserGRBL must be installed separately)_.![pick_best_preview](https://github.com/user-attachments/assets/ba543494-a8a7-4a82-8342-b7327eb84278)



**_4. image_fine_tuning.py (Optional)_**

_Allows fine-tuning of the predicted parameters to achieve the best engraving quality_.![fine_tuning](https://github.com/user-attachments/assets/3c96c243-1cb8-4dcd-b451-7a937f6fa2ca)

![comparision](https://github.com/user-attachments/assets/665bb7d1-1e75-44a4-865d-0c38b375ed0c)
![output](https://github.com/user-attachments/assets/8af60485-a693-4cea-be2c-63b9dc362774)


**_5. train_ml_module.py_**

_Trains the ML model by rating 20 variations of an image with different parameters, allowing the model to learn and predict optimal settings for future images_.



**_Parameters Predicted by the ML Model_**

**Sharpness Alpha, Beta, Gamma**: Controls image sharpness.
**Gamma Correction**: Adjusts image brightness and tone.
**Label**: Ranks image quality (Very Bad to Very Good).
**Filter Strength/Template Window/Search Window/Clip Limit**: Controls noise reduction and smoothing.

_How to Run_
Install Dependencies:


INSTALL LIBS: pip install pandas numpy scikit-learn xgboost tkinter

**Run Scripts:**
Run adjust_image_ratio.py to crop the image.
Run calc_and_filter_best_results.py for parameter prediction and previews.
Optionally, fine-tune with image_fine_tuning.py.
Use manual_picker.py to select the best image for engraving.
To train the model, run train_ml_module.py.
Laser Engraving: After selecting an image, the script opens LaserGRBL for engraving.

**Training the Model**
Provide labeled data by rating image variations to train the ML model. The model learns to predict the best parameters for future images.
