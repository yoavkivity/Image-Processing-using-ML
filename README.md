
###Image-Processing-using-ML
Overview
This project automates the process of preparing images for laser engraving on wood blocks. It uses a machine learning model to predict optimal image adjustment parameters, improving clarity, sharpness, and contrast for high-quality engraving.

Project Components
1. adjust_image_ratio.py
This script crops the original image to a fixed aspect ratio based on the size of the wooden block.

2. calc_and_filter_best_results.py
Uses the ML model to predict parameters for image adjustments, filters out bad results, and saves the best images with a preview on a BIRCH wood background.

3. image_fine_tuning.py (Optional)
Allows fine-tuning of the predicted parameters to achieve the best engraving quality.

4. manual_picker.py
Displays preview images side by side, letting you choose the best one. The selected image is then loaded into LaserGRBL for engraving (LaserGRBL must be installed separately).

5. train_ml_module.py
Trains the ML model by rating 20 variations of an image with different parameters, allowing the model to learn and predict optimal settings for future images.

Parameters Predicted by the ML Model
Sharpness Alpha, Beta, Gamma: Controls image sharpness.
Gamma Correction: Adjusts image brightness and tone.
Label: Ranks image quality (Very Bad to Very Good).
Filter Strength/Template Window/Search Window/Clip Limit: Controls noise reduction and smoothing.
How to Run
Install Dependencies:

bash
Copy code
pip install pandas numpy scikit-learn xgboost tkinter
Run Scripts:

Run adjust_image_ratio.py to crop the image.
Run calc_and_filter_best_results.py for parameter prediction and previews.
Optionally, fine-tune with image_fine_tuning.py.
Use manual_picker.py to select the best image for engraving.
To train the model, run train_ml_module.py.
Laser Engraving: After selecting an image, the script opens LaserGRBL for engraving.

Training the Model
Provide labeled data by rating image variations to train the ML model. The model learns to predict the best parameters for future images.

