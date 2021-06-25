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
Utilize o comando `kedro docker jupyter lab` para iniciar um jupyter.
O arquivo `notebooks/validacao.ipynb` carrega os dados resultantes para um dataframe onde o resultado pode ser validado.