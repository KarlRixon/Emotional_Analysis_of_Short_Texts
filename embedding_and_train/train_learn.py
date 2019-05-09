from keras.models import Sequential
from keras.layers.embeddings import Embedding

def main():
    model = Sequential()
    model.add(Embedding())

if __name__ == "__main__":
    main()