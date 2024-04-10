# Projeto Tatooshop

Este é o repositório do projeto Tatooshop, desenvolvido como parte do curso de Software Project.

## Como rodar o ambiente

Para rodar o ambiente, siga estas instruções:

* Certifique-se de ter o Docker instalado em sua máquina.

* Execute o seguinte comando para iniciar o ambiente usando o Docker Compose:

    ```
    docker-compose up
    ```

* Após qualquer atualização no código, execute o seguinte comando para desligar o ambiente:

    ```
    docker-compose down
    ```

* Após fazer as atualizações necessárias no código, execute novamente o comando para iniciar o ambiente:

    ```
    docker-compose up
    ```

* Se você precisar fazer alterações no banco de dados, adicione o código de criação da sua tabela no final do arquivo `init.sql`. Por exemplo:

    ```sql
    CREATE TABLE nome_tabela(
        campos da tabela
    );
    ```

Isso é tudo! Agora você pode começar a trabalhar no projeto Tatooshop.
