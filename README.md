# Banco de doações de sangue

Uma interface para a base de conhecimento prolog da questão 7 da lista 3 da matéria de Paradigmas de Linguagens de Programação - 2024/2 na UFAM.

## Como executar
**Importante:** O script foi criado com Python 3.12 e SWI-Prolog 9.3.15, não garanto que funcione com versões anteriores

1. Instale Python.
2. Instale [SWI-Prolog](https://www.swi-prolog.org/download/devel)
3. Instale wxPython: `pip install wxPython`.
4. Instale pyswip: `pip install pyswip`.
5. Execute o script: `python main.py`.
6. Selecione a aba `Consultar` para fazer as consultas, `Tabela de Compatibilidade` para a lista de compatibilidade disponibilizada na lista, ou `Banco de Dados` para uma tabela listando todas as pessoas e seus atributos na base de conhecimento.
7. Na aba `Consultar`, selecione a opção que você quer em uma das ComboBoxes, e clique no respectivo botão abaixo da ComboBox. Somente um botão pode ser ativado de cada vez, e ativar um botão limpa a seleção de todas as comboboxes não relacionadas ao botão.
