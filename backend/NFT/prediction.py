import numpy as np
import sentiment as stm
import train as train

def predict(input):
    try:
        model = load_model('DogeTest1.h5')
        prediction = model.predict(input)
        return prediction
    except:
        print("Invalid input.")

#newModel = load_model('test1.h5')
testInput = np.array([0,5,0.2,-0.9,0.7,0])
p = predict(testInput)
print(p)
