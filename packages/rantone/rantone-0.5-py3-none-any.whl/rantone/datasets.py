class Datasets:

    def __init__(self):
        pass

    def fashionMNIST(self):
        return self.keras.datasets.fashion_mnist.load_data()


    def cifar10(self):
        return self.keras.datasets.cifar10.load_data()