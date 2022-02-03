import pandas as pd
from sklearn.preprocessing import LabelEncoder
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from keras.utils.np_utils import to_categorical
from sklearn.preprocessing import OneHotEncoder

df = pd.read_csv('./dataset/tweet_sentiment.csv')

vocabSize = 2000
tokenizer = Tokenizer(num_words = vocabSize, split=' ')
clean_tweets = df['cleaned_tweets'].astype(str) # specifying the field datatype
tokenizer.fit_on_texts(clean_tweets.values)
X_train = tokenizer.texts_to_sequences(clean_tweets)
X_train = pad_sequences(X_train, maxlen = 50, padding = 'pre', truncating = 'pre')

le = LabelEncoder()
y_train = le.fit_transform(df['sentiment'])
y_train = y_train.reshape(-1, 1)

enc = OneHotEncoder(handle_unknown='ignore')
enc.fit(y_train)
y_train = enc.transform(y_train).toarray()
print(y_train)
# print("X_train\n")
# print(X_train)
# print(X_train.shape, y_train.shape)


# LSTM model
lstm_out = 128

model = Sequential()
model.add(Embedding(input_dim = vocabSize, output_dim=16, input_length = 50))
model.add(SpatialDropout1D(0.4))
model.add(LSTM(lstm_out, dropout = 0.2, recurrent_dropout = 0.2))
model.add(Dense(3, activation = 'softmax'))
print(model.summary())
model.compile(loss = 'categorical_crossentropy', optimizer = 'adam', metrics = ['accuracy'])


# fit training model
batchSize = 64
print(X_train.shape, y_train.shape)
model.fit(X_train, y_train, epochs = 4, batch_size = batchSize, verbose = 1)

model.save('./built_model/lstm_model')
# new_model = tf.keras.models.load_model('saved_model/my_model')  # Load model