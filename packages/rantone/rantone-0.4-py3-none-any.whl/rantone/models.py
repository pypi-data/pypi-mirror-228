class Models:

    def __init__(self):
        pass

    def fit(self, model, X_train, y_train, X_test, y_test):

        model.compile(loss=self.keras.losses.categorical_crossentropy,
                      optimizer='adam', metrics=['accuracy'])
        # validation_split=.3
        return model.fit(X_train, y_train, epochs=3, batch_size=32, validation_data=(X_test, y_test))

    def performance(self, model,  X_test, y_test):
        return model.evaluate(X_test, y_test)

    def predict(self, model, test_images):
        return model.predict(test_images)

    def save_weight(self, model, name):
        model.save_weights('name.h5')

    def save_model(self, model, name):
        model.save('model_dropout')

    def load_model(self, models):
        return models.load_model('model_dropout')
