# Gamma-Ray-Burst Light-Curve-Reconstruction (LCR) Using-Bi-Directional-LSTM
This repository holds the source code for predicting missing points of GRB Light Curves Using Bi-Directional LSTM. It also holds the results generated via code for various classes of GRBs taken from SWIFT XRT.

# Hyperparameters Used And Their Values Achieved Through Experimentation

![Hyperparameters](https://github.com/AmitShukla2808/Prediction-Of-GRB-Light-Curves-Using-Bi-Directional-LSTM/assets/77337715/26f888a5-4169-4b00-be06-90ccbd14efad)



# Results In Comparison To Other Algorithms
![Total Comparison](https://github.com/AmitShukla2808/Prediction-Of-GRB-Light-Curves-Using-Bi-Directional-LSTM/blob/main/Tables/Comparison%20Table.png)

# Error Fraction and % Decrease in uncertainty of flux values for GRBs belonging to Break Bump and Bump Flare Category
![Break Bump and Bump Flare LCR](https://github.com/AmitShukla2808/Prediction-Of-GRB-Light-Curves-Using-Bi-Directional-LSTM/blob/main/Tables/Break%20Bump%20and%20Bump%20Flare%20LCR.png)


# Sample Plots Generated Using Bi-LSTM Light Curve Reconstruction

![Good GRB 050607 LCR](https://github.com/AmitShukla2808/Prediction-Of-GRB-Light-Curves-Using-Bi-Directional-LSTM/blob/main/Reconstructed%20GRB%20Light%20Curves/Good%20GRB%20050607%20LCR.png)

![Break Bump GRB 050803 LCR](https://github.com/AmitShukla2808/Prediction-Of-GRB-Light-Curves-Using-Bi-Directional-LSTM/blob/main/Reconstructed%20GRB%20Light%20Curves/Break%20Bump%20GRB%20050803%20LCR.png)

![Bump Flare GRB 140709A LCR](https://github.com/AmitShukla2808/Prediction-Of-GRB-Light-Curves-Using-Bi-Directional-LSTM/blob/main/Reconstructed%20GRB%20Light%20Curves/Bump%20Flare%20GRB%20140709A%20LCR.png)

![Double Break Bump GRB 060219](https://github.com/AmitShukla2808/Prediction-Of-GRB-Light-Curves-Using-Bi-Directional-LSTM/blob/main/Reconstructed%20GRB%20Light%20Curves/060219%20Double%20break.png)


# Cleaning Of SWIFT XRT Files
The source SWIFT XRT files can be directly used in their raw and unprocessed form with the above code. The raw file first undergoes cleaning process by using the swiftxrt_clean module/python script whose source code and implementation has also been given and mentioned in the repository itself. This cleaned file is then fed to the code for further processing.
