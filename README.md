Link para o vídeo: https://drive.google.com/file/d/1044q9RjTdzGl2FWiPFj1qRW-E46S2RrM/view?usp=sharing

link para Transcrição: https://drive.google.com/file/d/1aO7TpE8jVwnTrmm2PfUL0n3ciE0cnmS6/view?usp=sharing

# Itapema Investment Screen — Seazone Hackathon 2026

Um sistema de decisão, não um notebook: ele transforma cinco CSVs brutos em uma lista ranqueada de imóveis para compra, com premissas declaradas, intervalos de confiança e uma análise de sensibilidade das premissas.

**Destaque:** comprar apartamentos compactos de 2 quartos (60–72 m², duas suítes, acomodando 5–6 pessoas) em **Morretes / Tabuleiro dos Oliveiras**, na faixa de R$680k–850k de preço anunciado (mediana do segmento: R$790k), além de uma parcela menor de imóveis de 2 quartos na faixa litorânea (Meia Praia) como seguro de liquidez.

Yield líquido de caixa esperado, sem alavancagem, de **6,2%** sob operação profissional (Seazone) (11,6% bruto), payback de 16,1 anos; chegando a **9,1%** com uma seleção disciplinada em nível de anúncio.

A hipótese interna — *studios compactos/1BR no Centro* — é **rejeitada**: não existem studios no mercado de venda, 1BR representa 2,0% dos apartamentos anunciados, o Centro não apresenta prêmio de receita quando controlamos por distância até o mar e tamanho da unidade, e 1BR possui o maior preço por m² da cidade.

## Execução

Tudo abaixo é reproduzível apenas a partir deste repositório (os caminhos apontam para `data/` e `output/` relativos à raiz do repositório; substitua usando `ITAPEMA_DATA` / `ITAPEMA_OUT` quando necessário):

```bash
pip install pandas numpy scipy scikit-learn matplotlib
python src/01_airbnb_demand.py       # painel de disponibilidade + curva de reservas + modelo de preço (+ série semanal)
python src/02_sale_market.py         # limpeza do VivaReal, deduplicação, normalização geográfica
python src/03_spatial.py             # linha costeira derivada dos dados, distância até o mar, competição por KD-tree
python src/04_investment_model.py    # yields por segmento sob premissas explícitas
python src/05_drivers_hypothesis.py  # fatores de receita + teste da hipótese Centro/compacto
python src/06_screening.py           # previsão e triagem de receita em nível de anúncio
python src/07_robustness.py          # intervalos de confiança por bootstrap + análise de 2.187 combinações de premissas
python src/07b_distance.py           # gradiente de distância até o mar nos dois lados do mercado
python src/08_decision.py            # testes controlados, capital disponível para investimento, lista de compra, cenários
python src/09_portfolio.py           # triagem ajustada por qualidade + alocação de R$20M
python src/11_guest_segments.py      # segmentos de hóspedes + matriz de oportunidades
python src/stress_test.py            # testes de robustez da recomendação
python src/10_presentation.py        # gráficos + apresentação executiva (lê apenas output/)
```

Os resultados são gerados em `output/`; a recomendação escrita está em `docs/recomendacao.html`.

## As três escolhas metodológicas que mais importam

**1. `Price_AV` é um arquivo de disponibilidade, não um arquivo de preço.** Uma linha existe apenas quando uma noite está disponível para reserva; portanto, uma ausência de (listing, stay-date) dentro de uma janela de captura representa uma noite indisponível.

Isso torna a ocupação observável, em vez de presumida — mas a disponibilidade observada com 90 dias de antecedência superestima a disponibilidade final. Com três capturas (6, 7 e 20 de janeiro de 2025), a mesma stay-date é observada em dois lead times diferentes, o que permite identificar uma booking curve.

Ajustamos `logit P(available) = listing + stay-date + lead` em 209.846 listing-nights e projetamos cada listing para um lead de 3 dias. Noites com lead de 0–2 dias são excluídas: essa queda representa o booking cut-off da plataforma, e não a demanda.

**2. Airbnb possui capacidade, mas não possui área útil; VivaReal possui área útil, mas não possui capacidade.**

Os dois lados são conectados por rank-preserving quantile matching dentro de cada célula `(zone × bedrooms)`, de modo que uma unidade no percentil 70 de área recebe a capacidade correspondente ao percentil 70 de unidades comparáveis do Airbnb.

**3. VivaReal não possui coordenadas.** O campo `suburb` é mais detalhado do que a malha do Airbnb (ele divide Meia Praia em Andorinha / Castelo Branco), então as zonas são normalizadas para uma taxonomia comum e Meia Praia é dividida por uma linha costeira derivada dos dados: o envelope leste da nuvem de pontos dos anúncios, suavizado e densificado, com a distância calculada por KD-tree.

O texto dos anúncios é analisado em busca de afirmações explícitas como "N metros do mar". A incerteza residual de localização é a maior fonte individual de erro e é testada diretamente em `07b_distance.py` e `09_portfolio.py`.

## Premissas (todas em `output/assumptions.json`, todas testadas em `07_robustness.py`)

| Parâmetro                                              | Base                       | Testado     |
| ------------------------------------------------------ | -------------------------- | ----------- |
| Lead time tratado como disponibilidade final           | 3 dias                     | 2–10        |
| Parcela de noites indisponíveis que são reservas pagas | 0.90                       | 0.80–1.00   |
| Parcela do anfitrião sobre a diária exibida            | 0.90                       | 0.85–1.00   |
| RevPAN de maio–setembro vs abril observado             | 0.50                       | 0.35–0.65   |
| Desconto de negociação sobre o preço anunciado         | 7%                         | 0–12%       |
| Custos de fechamento (ITBI, escritura, registro)       | 5%                         | —           |
| Mobiliário STR                                         | R$1.200/m²                 | R$800–1.800 |
| Taxa de gestão                                         | 20% da receita de reservas | 15–25%      |
| Utilidades/consumíveis por noite ocupada               | R$45                       | R$30–65     |
| Reserva para manutenção                                | 0.5% do valor a.a.         | —           |

Fator de anualização implícito pela premissa de sazonalidade: **2,47×** a janela observada de 105 noites.

## Dois conceitos de yield — e qual é o principal

Existem dois números defensáveis de "net yield" por segmento, e o deck deixa ambos explícitos:

* **Visão de receita de mercado** (anfitrião existente mediano, `segments_micro_zone.csv`): Morretes 2BR ≈ **4,0%** líquido.
  É o que você ganharia comprando um imóvel e mantendo-o como está. Não é um yield de ativo atrativo.

* **Visão de operador profissional** (contrafactual operado pela Seazone, `segment_yields_ci.csv`): Morretes 2BR ≈ **6,2%** líquido, Tabuleiro 2BR ≈ 6,8%, Morretes 3BR ≈ 7,8%.

**A tese está no serviço, não no imóvel.** O destaque de 6,2% *exige* operar as unidades como os melhores anfitriões profissionais (o modelo atribui a cada unidade à venda uma qualidade de anúncio no percentil 75).

Se a Seazone planejasse comprar e manter os imóveis sem operar, o número mais honesto a considerar seria a visão de mercado de ~4,0%.

## O que os dados não conseguem sustentar

Oito meses do ano não são observados. Preços de transação não são observados (apenas preços anunciados). Valorização de capital e imposto de renda são excluídos.

Apenas 1.005 de 4.441 anúncios do Airbnb possuem dados de calendário, e esse subconjunto é mais profissional — portanto, a ocupação absoluta provavelmente está superestimada mesmo após o desconto de 10% para bloqueios do proprietário.

Morretes 3BR se baseia em apenas 10 comparáveis do Airbnb — por isso é sinalizado como um segmento de maior yield, porém mais limitado. As células de 2BR (51 comparáveis, 827 listings prontos) sustentam a recomendação, em vez do 3BR com pontuação mais alta.

## Testes de estresse (veja `output/logs/log_stress.txt`)

A recomendação sobrevive a todos os testes que podem ser executados a partir dos resultados existentes:

| Teste                                                                  | Resultado vs base (Morretes 2BR 6,2%)                                   |
| ---------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Exclusão da cauda barata (preço anunciado ≥ R$550k)                    | 6,1% — ordenação inalterada                                             |
| Apenas faixa estrita (R$600k–900k)                                     | Morretes 2BR 6,3%; 2BR barato da orla melhora (valor dentro da parcela) |
| Remoção do Morretes 3BR (célula limitada)                              | Tabuleiro 6,8% lidera, Morretes 2BR 6,2% permanece                      |
| Receita do anfitrião mediano (não operador)                            | 3,6% — visão de mercado, ~metade da visão do operador                   |
| Premissas conservadoras de cenário extremo                             | 2,6% — ainda lidera, mas este é o piso                                  |
| Receita +30% / −25% em todas as células                                | Ordenação inalterada; nenhuma célula grande/orla salta                  |
| Estresse de distância (07b): estoque fora da praia 2×–3× mais distante | parcela cruza em ~2,5× com elasticidade pessimista                      |

A única força capaz de inverter a ordem é a *geografia*: se o estoque de imóveis à venda fora da praia estiver sistematicamente mais distante do mar do que seus comparáveis no Airbnb, a receita de Morretes estará superestimada.

É exatamente por isso que a recomendação inclui uma parcela de 2BR em Meia Praia (≈50 pontos-base de yield como seguro) e por que essa parcela é uma *sleeve*, não o núcleo da estratégia.

---

## Camada de apresentação e camada de demanda

```bash
python src/11_guest_segments.py   # segmentos de hóspedes + matriz de oportunidades
python src/10_presentation.py     # gráficos matplotlib + apresentação executiva
```

`10_presentation.py` lê apenas `output/` — não recalcula nada. Execute novamente depois de qualquer mudança acima e o deck será reconstruído automaticamente, com os números atualizados.

Cada gráfico declara uma regra de relevância e só é incluído caso essa regra seja acionada pelos resultados; os textos podem ser revisados sem alterar o código criando `presentation/overrides.json` (ex.: `{"slides": {"0": {"headline": "Nova manchete"}}}`).

Deck em [`docs/apresentacao.html`](docs/apresentacao.html) — 11 lâminas, navegação por teclado (←/→, `G` índice, `N` notas do apresentador, `P` PDF). Todos os gráficos têm fundo branco.

**Quem é o hóspede (camada de demanda).** Não observamos os hóspedes diretamente: observamos como cada unidade é configurada e a demanda que essa configuração consegue alcançar — preferência revelada, não persona.

Quatro segmentos, todos com padrões de demanda distintos:

| Segmento                  | Anúncios | Hóspedes | Diária   | Ocupação | Receita/ano |
| ------------------------- | -------- | -------- | -------- | -------- | ----------- |
| Alto padrão e frente-mar  | 120      | 8        | R$ 1.221 | 75%      | R$ 176 mil  |
| Grupos e amigos           | 217      | 8        | R$ 683   | 85%      | R$ 108 mil  |
| Famílias                  | 407      | 6        | R$ 554   | 83%      | R$ 87 mil   |
| Casais e escapadas curtas | 167      | 4        | R$ 499   | 70%      | R$ 70 mil   |

E dois segmentos **descartados com evidência**: viagens de negócios aparecem em 1,9% dos anúncios e estadias mensais em 0,1%.

A diária de sexta e sábado é igual à de meio de semana em praticamente toda a cidade — a demanda é de semanas inteiras de férias, não de escapadas de fim de semana.

A cadeia completa está em `output/opportunity_matrix.csv`:

**2 dorm compacto → Morretes → família de 5–6 em semana de férias → ocupação de 77% → R$ 71 mil/ano → 6,2% líquido.**

---

## Entrega (hackathon)

* Recomendação por escrito: [`docs/recomendacao.html`](docs/recomendacao.html) e [`RECOMENDACAO.md`](RECOMENDACAO.md)
* Log de uso de IA: pasta [`ai-log/`](ai-log/)
* Link para o vídeo: https://drive.google.com/file/d/1044q9RjTdzGl2FWiPFj1qRW-E46S2RrM/view?usp=sharing
* Link para a transcrição: https://drive.google.com/file/d/1aO7TpE8jVwnTrmm2PfUL0n3ciE0cnmS6/view?usp=sharing
