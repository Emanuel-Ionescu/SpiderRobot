import pandas as pandas
import matplotlib.pyplot as plt
import numpy as np

raw_data = pandas.read_excel("servo_data.xlsx")
# Strip whitespace from column names
raw_data.columns = raw_data.columns.str.strip()

data = {}

servos_names = [f"Servo{i}" for i in range(12)]

for servo in servos_names:
    data[servo] = {"duty": [], "angle": [], "m":0, "b":0}

for servo in servos_names:
    for idx, el in enumerate(raw_data[servo]):
        if el == el:
            data[servo]["duty"].append(idx + 1)
            data[servo]["angle"].append(el)
    
    if len(data[servo]["duty"]) == 0:
        del data[servo]
        continue
    
    data[servo]["m"] = float(np.polyfit(np.array(data[servo]["duty"]), np.array(data[servo]["angle"]), 1)[0])
    data[servo]["b"] = float(np.polyfit(np.array(data[servo]["duty"]), np.array(data[servo]["angle"]), 1)[1])


for servo in data.keys():
    plt.figure()
    
    duty_array = np.array(data[servo]["duty"])
    angle_array = np.array(data[servo]["angle"])
    fitted_values = data[servo]["m"] * duty_array + data[servo]["b"]
    residuals = np.abs(angle_array - fitted_values)
    
    for i in range(len(duty_array)):
        if residuals[i] > 5:
            plt.plot([duty_array[i], duty_array[i]], [angle_array[i], fitted_values[i]], "r-")
            plt.text(duty_array[i], angle_array[i], f"{residuals[i]:.2f}", color="r")

        elif residuals[i] > 2.5:
            plt.plot([duty_array[i], duty_array[i]], [angle_array[i], fitted_values[i]], "y-")
            plt.text(duty_array[i], angle_array[i], f"{residuals[i]:.2f}", color="y")
        
    
    plt.plot(data[servo]["duty"], data[servo]["angle"], label=servo, marker=".")
    plt.plot(duty_array, fitted_values, label=servo+" fit")
    plt.legend()
    plt.tight_layout()
    plt.show()

    print(data[servo])
    print()
