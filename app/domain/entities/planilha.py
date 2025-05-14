class Planilha():
    def __init__(self, cpf, nome, dataUpload, size, id = None):
        self.id = id
        self.cpf = cpf
        self.nome = nome 
        self.dataUpload =  dataUpload
        self.size = size
