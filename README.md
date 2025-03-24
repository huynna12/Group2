# Line-following
1. How the Grayscale Sensors Work

Your robot uses three grayscale sensors to detect the line. These sensors read the intensity of reflected light, which is converted into grayscale values:
	•	Higher values → White (background) - usually above 1400
	•	Lower values → Black (line)        - usually below 1400 

The relationship between the grayscale values and the detected color depends on the threshold values you set.

2. Threshold Logic Explained

The robot interprets the sensor readings into black (1) and white (0) based on the thresholds you configure:
	•	A[0] > threshold → 0 → White (background)
	•	A[0] < threshold → 1 → Black (line)
	•	The same logic applies to the middle and right sensors.

 For example, THRESHOLDS = [1400, 1400, 1400]  # [left, middle, right]
              gm_val_list = [802, 1480, 1450]
---> _state[1, 0, 0] ---> slightly goe to the left to get back on track
