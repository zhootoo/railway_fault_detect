from keras.layers import Masking,Embedding,LSTM,Dropout,Dense
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
PATH = 'D:/WorkSpace/PyCharm/Dalang/data/current/'
def get_data():
    y = []
    X = []
    for filename1 in os.listdir(PATH):
        for filename2 in os.listdir(PATH+filename1):
            data = pd.read_excel(PATH+filename1+'/'+filename2)
            x_temp = data.values.tolist()
            scaler = MinMaxScaler()
            X.append(scaler.fit_transform(x_temp))
            y.append(filename1)
    X = pad_sequences(X,padding='post',value=-1.,dtype='float32')
    y = to_categorical(y)
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)
    return X_train,X_test,y_train,y_test


def train_lstm(x_train,y_train,x_test,y_test):
    print('正在构建模型...')
    model = Sequential()
    model.add(Masking(mask_value=-1,input_shape=(299,3)))
    model.add(LSTM(50))
    model.add(Dense(25,activation='tanh'))
    model.add(Dense(7,activation='softmax'))
    print ('Compiling the Model...')
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',metrics=['accuracy'])
    history = model.fit(x_train, y_train,validation_data=(X_test,y_test), epochs=50,batch_size=20,verbose=1)
    score = model.evaluate(x_test, y_test)
    print(score)
    return history

def plot_train(history):
    fig = plt.figure()#新建一张图
    plt.plot(history.history['acc'],label='training acc')
    plt.plot(history.history['val_acc'],label='val acc')
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(loc='lower right')
    fig = plt.figure()
    plt.plot(history.history['loss'],label='training loss')
    plt.plot(history.history['val_loss'], label='val loss')
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(loc='upper right')
    plt.show()
if __name__=='__main__':
    X_train,X_test,y_train,y_test = get_data()
    history = train_lstm(X_train,y_train,X_test,y_test)
    plot_train(history)
