import matplotlib.pyplot as plt

import json
 
# Opening JSON file
f = open('sample.json')
 
# returns JSON object as 
# a dictionary
data = json.load(f)
 
acc = data['acc']
val_acc = data['top_k_categorical_accuracy']
# Closing file
f.close()

epochs = range(1, len(acc) + 1)

plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

# plt.plot(epochs, loss, 'bo', label='Training loss')
# plt.plot(epochs, val_loss, 'b', label='Validation loss')
# plt.title('Training and validation loss')
# plt.legend()

plt.show()