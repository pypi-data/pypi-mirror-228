class Utils:

    def __init__(self):
        pass

    def to_categorical(self, data):
        return self.keras.utils.to_categorical(data)


    def to_scale(self, data):
        return data.astype('float32') / 255.0

    def summary(self, model):
        return model.summary()