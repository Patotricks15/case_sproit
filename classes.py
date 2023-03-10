import pandas as pd
from pymongo import MongoClient
import json



class MongoConnector:
    def __init__(self, connection_string:str) -> None:
        self.client = MongoClient(connection_string)
        self.db = self.client["database"]
    def return_collection(self, collection_name:str):
        self.collection = self.db[collection_name]
        return self.collection
    def close_connection(self):
        self.client.close()

class DadosObject:
    def __init__(self, collection, dataframe:pd.DataFrame) -> None:
        self.collection = collection
        self.dataframe = dataframe
    def insert_mongo(self, mongo_connector:MongoConnector):
        records = self.dataframe.to_dict(orient="records")
        mongo_connector.collection.insert_many(records)

class DadosCarro(DadosObject):
    def __init__(self, dataframe:pd.DataFrame) -> None:
        super().__init__(collection = 'carros', dataframe=dataframe)
    def insert_mongo(self, mongo_connector):
        super().insert_mongo(mongo_connector)

class DadosMontadora(DadosObject):
    def __init__(self, dataframe:pd.DataFrame) -> None:
        super().__init__(collection = 'montadoras', dataframe=dataframe)
    def insert_mongo(self, mongo_connector):
        super().insert_mongo(mongo_connector)
        

class Executor:
    def __init__(self, string_connection:str, dataframe_carros:pd.DataFrame, dataframe_montadoras:pd.DataFrame, clear:bool=False) -> None:
        self.dataframe_carros = dataframe_carros
        self.dataframe_montadoras = dataframe_montadoras
        self.conector_local = MongoConnector(string_connection)
        self.collection_carros = self.conector_local.return_collection('carros')
        self.collection_montadoras = self.conector_local.return_collection('montadoras')
        if clear == True:
            self.collection_carros.drop()
            self.collection_montadoras.drop()
        else:
            pass
    def inserir_carros(self) -> None:
        carros = DadosCarro(dataframe=self.dataframe_carros)
        self.collection_carros = self.conector_local.return_collection('carros')
        carros.insert_mongo(self.conector_local)
        
        
    def inserir_montadoras(self) -> None:
        montadoras = DadosMontadora(dataframe=self.dataframe_montadoras)
        self.collection_montadoras = self.conector_local.return_collection('montadoras')
        montadoras.insert_mongo(self.conector_local)
    

    def gerar_agregacao(self) -> None:
        # Realizar a agrega????o para fazer o relacionamento
        pipeline_nova_collection = [
                            {"$lookup": {
                            "from": "montadoras",
                            "localField": "Montadora",
                            "foreignField": "Montadora",
                            "as": "Montadoras"
                            }},
                            {"$unwind": "$Montadoras"},
                            {"$addFields": {"Pa??s": "$Montadoras.Pa??s"}},
                                        {"$group": {
                            "_id": "$Montadoras.Pa??s",
                            "Carros": {"$push": "$$ROOT"}
                            }}
                            ]
        result = self.collection_carros.aggregate(pipeline_nova_collection)
        result_lista = list(result)
        # Converter o resultado para um DataFrame do Pandas
        result_df = pd.DataFrame(result_lista)
        self.conector_local.db.pa??s.drop()
        self.conector_local.db.pa??s.insert_many(result_df.to_dict(orient="records"))
        with open("agregacao_collection_pa??s.js", "w") as f:
            json.dump(pipeline_nova_collection, f)
        
        pipeline_carros = [
                            {"$lookup": {
                            "from": "montadoras",
                            "localField": "Montadora",
                            "foreignField": "Montadora",
                            "as": "Montadoras"
                            }},
                            {"$unwind": "$Montadoras"},
                            {"$addFields": {"Pa??s": "$Montadoras.Pa??s"}}

                            ]
        result = self.collection_carros.aggregate(pipeline_carros)
        result_lista = list(result)
        # Converter o resultado para um DataFrame do Pandas
        result_df = pd.DataFrame(result_lista)
        self.conector_local.db.carros.drop()
        self.conector_local.db.carros.insert_many(result_df.to_dict(orient="records"))
        with open("agregacao_carros.js", "w") as f:
            json.dump(pipeline_carros, f)
            
    def run(self, carros:bool=True, montadoras:bool=True) -> None:
        if carros:
            self.inserir_carros()
        if montadoras:
            self.inserir_montadoras()
        self.gerar_agregacao()
        self.conector_local.close_connection()