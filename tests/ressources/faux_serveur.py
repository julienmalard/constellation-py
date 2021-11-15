import os
import sys

from constellationPy.serveur import Serveur as ServeurOriginal

dir_serveur = os.path.join(os.path.split(__file__)[0], "_serveur.py")


class Serveur(ServeurOriginal):
    """
    Un faux serveur pour simplifier le processus de test du client.
    """

    def __init__(soimême, port=None):
        super().__init__(port, autoinstaller=False, exe=[sys.executable, dir_serveur])
