from rantone.datasets import Datasets
from rantone.utils import Utils
from rantone.visuals import Visuals


class Decitone(Datasets, Utils, Visuals) :

    def __init__(self, keras, matplotlib): 
        self.keras = keras
        self.plt = matplotlib
        