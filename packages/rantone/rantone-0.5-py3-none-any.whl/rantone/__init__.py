from rantone.datasets import Datasets
from rantone.utils import Utils
from rantone.visuals import Visuals
from rantone.models import Models

class Rantone(Datasets, Utils, Visuals, Models) :

    def __init__(self, keras, matplotlib): 
        self.keras = keras
        self.plt = matplotlib
        