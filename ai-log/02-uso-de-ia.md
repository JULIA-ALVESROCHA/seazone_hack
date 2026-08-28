# Onde a IA entrou — e onde não entrou

## Onde entrou

| Etapa | O que a IA fez | O que foi mantido |
|---|---|---|
| Perfilagem | Explorou a estrutura dos cinco arquivos, chaves, joins, duplicatas, valores impossíveis | A leitura de que `Price_AV` é um arquivo de disponibilidade — origem de tudo |
| Modelagem | Escreveu o painel de disponibilidade, o modelo de efeitos fixos da curva de reserva, o modelo de preço, o modelo de receita | Os nove scripts em `src/`, reproduzíveis |
| Geografia | Derivou a linha de costa como envelope leste da nuvem de pontos e calculou distâncias por KD-tree | `src/03_spatial.py` |
| Ponte entre bases | Propôs o pareamento de quantis área ↔ capacidade | `src/06_screening.py` |
| Redação | Escreveu o README, a recomendação e este log | Revisados linha a linha |

## Onde **não** entrou — e por quê

**Nenhuma chamada de LLM está no caminho numérico.** Todo número deste repositório sai de código
determinístico e auditável:

- **A fórmula de retorno é Python puro**, com cada premissa nomeada em `output/assumptions.json`.
  Um analista da Seazone precisa poder discordar de uma premissa e rodar de novo — não interrogar
  um modelo de linguagem.
- **A curva de reserva é uma regressão logística com efeitos fixos**, não uma estimativa pedida a
  um modelo. A antecedência de corte (3 dias) foi escolhida olhando os dados brutos de
  disponibilidade no dia da captura, não por julgamento textual.
- **A varredura de 2.187 combinações de premissas é um produto cartesiano em `itertools`**. É o
  tipo de trabalho em que um LLM só adicionaria custo e variância.
- **Nenhum dado foi inventado.** Onde a base não sustenta uma resposta — oito meses do ano, preços
  de transação, valorização, localização exata dos anúncios de venda — está escrito que não sustenta.
  As premissas de sazonalidade estão declaradas como premissas, com sensibilidade.

## A regra que guiou a divisão

A IA foi usada onde havia **ambiguidade estruturada** — ler o formato de um arquivo, propor uma
ponte entre duas bases incompatíveis, escrever código, redigir. Não foi usada onde havia
**aritmética com consequência de negócio**. Um yield de 6,4% precisa ser rastreável até uma linha
de código; um resumo bonito não substitui isso.

O sinal de maturidade que este projeto quer dar não é "usamos IA em tudo". É: **sabemos exatamente
onde uma regra determinística é melhor do que um modelo, e escolhemos a regra.**
