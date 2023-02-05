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
    def __init__(self, string_connection, dataframe_carros, dataframe_montadoras) -> None:
        self.dataframe_carros = dataframe_carros
        self.dataframe_montadoras = dataframe_montadoras
        self.conector_local = MongoConnector(string_connection)
        self.collection_carros = self.conector_local.return_collection('carros')
        self.collection_montadoras = self.conector_local.return_collection('montadoras')
        self.collection_carros.drop()
        self.collection_montadoras.drop()
    def inserir_carros(self) -> None:
        carros = DadosCarro(dataframe=self.dataframe_carros)
        self.collection_carros = self.conector_local.return_collection('carros')
        carros.insert_mongo(self.conector_local)
        
        
    def inserir_montadoras(self) -> None:
        montadoras = DadosMontadora(dataframe=self.dataframe_montadoras)
        self.collection_montadoras = self.conector_local.return_collection('montadoras')
        montadoras.insert_mongo(self.conector_local)
    

    def gerar_agregacao(self) -> None:
        # Realizar a agregação para fazer o relacionamento
        pipeline = pipeline = [
                            {"$lookup": {
                            "from": "montadoras",
                            "localField": "Montadora",
                            "foreignField": "Montadora",
                            "as": "Montadoras"
                            }},
                            {"$unwind": "$Montadoras"},
                            {"$addFields": {"País": "$Montadoras.País"}},
                            
                            
                            ]
        result = self.collection_carros.aggregate(pipeline)

        result_lista = list(result)
        print(result_lista)
        # Converter o resultado para um DataFrame do Pandas
        result_df = pd.DataFrame(result_lista)
        print(result_df)
        self.conector_local.db.carros.drop()
        self.conector_local.db.carros.insert_many(result_df.to_dict(orient="records"))
        with open("agregacao.js", "w") as f:
            json.dump(pipeline, f)
    
    def run(self) -> None:
        self.inserir_carros()
        self.inserir_montadoras()
        self.gerar_agregacao()
        self.conector_local.close_connection()
