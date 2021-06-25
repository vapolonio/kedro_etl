# kedro_etl

## Overview

Esse é um projeto desenvolvido com [Kedro](https://kedro.readthedocs.io)
O projeto realiza o download de um arquivo em `xls` realiza a conversão para `ods` em seguida faz a limpeza de dados e o salva particionado no diretorio `data/03_primary/etl_raizen`.
(./dataflow.png)

## Instanciando o projeto com kedro

Para criar o ambiente de kedro com o conda utilize os seguintes comandos:
`conda create -n test-etl-env`
`conda activate test-etl-env`
`conda install -c conda-forge kedro -y`
`pip install kedro-docker`

Construindo a imagem docker:
`kedro docker build`
`kedro docker run`

#### Validando
Utilize o comando `kedro docker jupyter lab` para iniciar um jupyter lab, acessando o notebook `notebooks/validacao.ipynb` os dados foram carregados para um dataframe onde o resultado pode ser validado.

Utilize o comando para validar o dataflow resultante
`kedro docker cmd --docker-args="-p=4141:4141" kedro viz --host=0.0.0.0`