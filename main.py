from classes import DataFrameObject, DadosCarro, DadosMontadora, MongoConnector, Executor
import pandas as pd

dataframe_carros_input = pd.DataFrame(
    {
                    'Carro':['Onix',
                            'Polo',
                            'Sandero',
                            'Fiesta',
                            'City'
                            ],
                    'Cor':['Prata',
                           'Branco',
                           'Prata',
                           'Vermelho',
                           'Preto'
                           ],
                    'Montadora':['Chevrolet',
                                 'Volkswagen',
                                 'Renault',
                                 'Ford',
                                 'Honda'
                                 ]
                    }
                                      )

dataframe_montadoras_input = pd.DataFrame({'Montadora':['Chevrolet',
                                                        'Volkswagen',
                                                        'Renault',
                                                        'Ford',
                                                        'Honda'
                                                        ],
                                           'País':['EUA',
                                                   'Alemanha',
                                                   'França',
                                                   'EUA',
                                                   'Japão'
                                                   ]
                                           }
                                          )

if __name__ == "__main__":
    Executor("mongodb://localhost:27017/",
             dataframe_carros_input,
             dataframe_montadoras_input).run()
