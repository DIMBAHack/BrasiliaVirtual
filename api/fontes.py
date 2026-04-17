from files.fileManagement import fileArrumadoAnalisar
from database.configDB import ConfigDB
import os
from dotenv import load_dotenv



class Fontes:
    def __init__(self):
        self.file = fileArrumadoAnalisar.chuncking()

