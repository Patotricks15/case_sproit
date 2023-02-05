# case_sproit



## classes.py
Esse script Python executa várias tarefas para gerenciar dados armazenados em um banco de dados MongoDB.


![classes](https://github.com/Patotricks15/case_sproit/blob/main/classes.png)


O código começa definindo as classes que vão gerenciar os dados

* **MongoConnector**: esta classe se conecta a um banco de dados MongoDB usando uma string de conexão e fornece métodos para retornar uma collection específica e fechar a conexão.
* **DadosObject**: Esta é uma classe base que recebe uma collection e um dataframe do pandas como entrada e possui um método para inserir dados no MongoDB.
* **DadosCarro** e **DadosMontadora**: Essas classes herdam da classe **DadosObject** e especificam o nome da collection para os dados.

Por fim, é defina a classe **Executor**, que é responsável por executar as tarefas desejadas.

A classe possui os seguintes métodos:
* **inserir_carros**: Insere dados do dataframe_carros na collection "carros" do MongoDB.
* **inserir_montadoras**: Insere dados do dataframe_montadoras na collection "montadoras" do MongoDB.
* **gerar_agregacao**: Realiza uma operação de agregação no banco de dados MongoDB para relacionar os dados das coleções "carros" e "montadoras" e salva o resultado em uma nova collection "carros".
* O método **run** chama os métodos para inserir os dados, executar a agregação e fechar a conexão.
