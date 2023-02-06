import streamlit as st
from classes import Executor
import pandas as pd


input_carro = pd.DataFrame({'Carro': None,
                'Cor': None,
                'Montadora': None
                }, index = [])


carro_carro = st.text_input('Modelo do carro')
carro_cor = st.text_input('Cor')
carro_montadora = st.text_input('Nome da montadora')

input_carro = pd.DataFrame({'Carro': carro_carro,
                'Cor': carro_cor,
                'Montadora': carro_montadora
                }, index = [0])
        


input_montadora = pd.DataFrame({'Montadora': None,
                'País': None
                }, index = [0])



montadora_pais = st.text_input('País')
montadora_montadora = st.text_input('Montadora')


input_montadora['País'] = montadora_pais
input_montadora['Montadora'] = montadora_montadora


opcao = st.radio('Selecione a opção desejada:', ['Registrar carro', 'Registrar montadora', 'Registrar ambos'])

carro_bool = False
montadora_bool = False
string_registro = None

if opcao == 'Registrar carro':
    carro_bool = True
    string_registro = 'Carro registrado'

elif opcao == 'Registrar montadora':
    montadora_bool = True
    string_registro = 'Montadora registrada'

else:
    carro_bool= True
    montadora_bool = True
    string_registro = 'Carro e Montadora registrados'

if st.button('Registrar Dado'):
        Executor("mongodb://localhost:27017/",
                input_carro,
                input_montadora,
                clear=False).run(carros=carro_bool, montadoras=montadora_bool)
        st.success(string_registro)
        
