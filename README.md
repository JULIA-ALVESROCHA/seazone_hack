**🎥 Vídeo (3 min):** `COLE-AQUI-O-LINK-DO-GOOGLE-DRIVE`

# Itapema — Onde a Seazone deveria comprar

**Hackathon Jovens Talentos AI Builder 2026 · Julia Alves Rocha**

> **Resposta curta:** comprar **apartamentos compactos de 2 dormitórios (60–72 m², duas suítes,
> capacidade 5–6 pessoas) em Morretes e Tabuleiro dos Oliveiras** — a faixa de 300–800 m atrás da
> Meia Praia — na janela de preço de **R$ 680 mil a R$ 850 mil**, com uma parcela menor na orla da
> Meia Praia para liquidez de revenda.
>
> **Yield líquido de caixa 6,4% a.a.** (11,7% bruto), payback de 15,7 anos, sem alavancagem e sem
> valorização. Com seleção disciplinada listing a listing, até **9,7%**.
>
> **A hipótese interna — "studios/1 dormitório no Centro" — é rejeitada.** Não existe um único studio
> à venda na base. Apartamentos de 1 dormitório são 2,0% da oferta (16 unidades no Centro). O Centro
> não tem prêmio de receita quando se controla distância do mar e tamanho da unidade. E o metro
> quadrado de 1 dormitório é o mais caro da cidade.

---

## Como rodar

```bash
pip install pandas numpy scipy scikit-learn

python src/01_airbnb_demand.py       # painel de disponibilidade + curva de reserva + modelo de preço
python src/02_sale_market.py         # limpeza VivaReal, deduplicação, normalização de bairros
python src/03_spatial.py             # linha de costa derivada dos dados, distância do mar, KD-tree
python src/04_investment_model.py    # economia por segmento sob premissas explícitas
python src/05_drivers_hypothesis.py  # drivers de receita + teste da hipótese Centro/compacto
python src/06_screening.py           # previsão de receita e triagem listing a listing
python src/07_robustness.py          # bootstrap + varredura de 2.187 combinações de premissas
python src/07b_distance.py           # gradiente de distância do mar nos dois lados do mercado
python src/08_decision.py            # testes controlados, capital alocável, lista de compra
python src/09_portfolio.py           # triagem ajustada por qualidade + alocação de R$ 20 milhões
```

Saídas em `output/` (logs completos de cada etapa em `output/logs/`).
**Recomendação escrita e gráficos: [`docs/recomendacao.html`](docs/recomendacao.html)** — abra no navegador.
Versão em texto: [`RECOMENDACAO.md`](RECOMENDACAO.md). Log de uso de IA: [`ai-log/`](ai-log/).

---

## As três decisões de método que sustentam o resultado

**1. `Price_AV` é um arquivo de disponibilidade, não de preço.**
Existe uma linha apenas quando a diária está disponível — então uma data ausente dentro da janela
de captura é uma **noite indisponível**. Isso torna a ocupação observável em vez de arbitrada.
Mas disponibilidade vista com 90 dias de antecedência superestima a disponibilidade final. Como há
três capturas (6, 7 e 20/jan/2025), a mesma data de estadia aparece em dois horizontes diferentes,
o que **identifica uma curva de reserva**. Ajustamos
`logit P(disponível) = listing + data + antecedência` sobre 209.846 noites-listing e projetamos todo
mundo para 3 dias de antecedência. Antecedências de 0 a 2 dias são descartadas: aquela queda é o
corte de reserva da plataforma, não demanda.

**2. O Airbnb tem capacidade e não tem área; o VivaReal tem área e não tem capacidade.**
Os dois lados são ligados por **pareamento de quantis** dentro de cada célula (zona × dormitórios):
uma unidade no percentil 70 de área herda a capacidade do percentil 70 dos anúncios comparáveis.

**3. O VivaReal não tem coordenadas.**
O campo `suburb` dele é mais fino que o do Airbnb (separa Andorinha e Castelo Branco de Meia Praia),
então normalizamos as duas taxonomias e dividimos a Meia Praia com uma **linha de costa derivada dos
próprios dados** — o envelope leste da nuvem de pontos dos anúncios, suavizado e densificado, com
distância calculada por KD-tree. O texto dos anúncios também é minerado atrás de "N metros do mar".
Essa incerteza de localização é a maior fonte de erro do trabalho e é testada diretamente em
`src/07b_distance.py`. *(Atenção: Jardim Praia Mar fica ~1,2 km do mar apesar do nome — não pode ser
somado à faixa de orla.)*

---

## O mecanismo econômico

| Driver | Efeito | IC 95% |
|---|---|---|
| Capacidade de hóspedes (log) | **+0,55** na diária | +0,47 … +0,65 |
| Operação profissional | **+27%** na diária | +21% … +34% |
| Nota de avaliação (por ponto) | +0,27 | +0,12 … +0,47 |
| Distância do mar (log km) | −0,090 na receita | e.p. 0,015 |
| Estar no Centro | +2,9% | −6,7% … +13,1% |
| Ser compacto (studio/1 dorm) | +6,0% | −6,1% … +22,3% |
| Centro × compacto | **−7,2%** | −21,3% … +8,2% |

A receita é comprada em **capacidade de dormir por metro quadrado**, não em endereço. E o mercado de
venda desconta distância do mar mais rápido (−9% por dobra) do que o mercado de locação penaliza
(−6% por dobra) — por isso uma quadra para dentro é acretivo, não dilutivo.

Um detalhe que vale registrar: a **ocupação é praticamente inexplicável** (R² = 0,10) enquanto o
preço é bem explicado (R² = 0,37). Em Itapema todo mundo enche no verão; operadores se diferenciam
na diária, não em noites vendidas. Anúncios profissionais rodam ocupação *menor* e receita bem maior.

---

## Premissas (todas em `output/assumptions.json`, todas varridas em `07_robustness.py`)

| Parâmetro | Base | Varredura |
|---|---|---|
| Antecedência tratada como disponibilidade final | 3 dias | 2–10 |
| Fração das noites indisponíveis que são reservas pagas | 0,90 | 0,80–1,00 |
| Fração da diária exibida que fica com o anfitrião | 0,90 | 0,85–1,00 |
| RevPAN mai–set vs abril observado | 0,50 | 0,35–0,65 |
| Desconto de negociação sobre o pedido | 7% | 0–12% |
| Custos de fechamento (ITBI, escritura, registro) | 5% | — |
| Mobília e enxoval para temporada | R$ 1.200/m² | R$ 800–1.800 |
| Taxa de administração | 20% da receita | 15–25% |
| Consumo por noite ocupada | R$ 45 | R$ 30–65 |
| Reserva de manutenção | 0,5% do valor a.a. | — |

Fator de anualização implícito: **2,47×** a janela observada de 105 noites.

**Robustez:** em 2.187 combinações de premissas, Morretes 3 dorm fica em 1º lugar em *todas*,
Tabuleiro 2 dorm em 2º e Morretes 2 dorm em 3º. O Centro 1 dorm nunca passa do 6º lugar.

---

## O que os dados **não** sustentam

- **Oito meses do ano não são observados.** O calendário vai de 06/jan a 20/abr/2025. Qualquer número
  anual depende de uma premissa de sazonalidade declarada — mostramos a sensibilidade em vez de escondê-la.
- **Preços de transação não são observados.** O VivaReal traz preço pedido.
- **Valorização e imposto de renda estão fora.** Todo yield aqui é yield de caixa.
- **Só 1.005 dos 4.441 anúncios do Airbnb têm calendário**, e esse subconjunto pende para anúncios
  profissionais — a ocupação absoluta provavelmente está superestimada mesmo após o corte de 10%
  para bloqueios do proprietário.
- **Morretes 3 dorm e Tabuleiro 2 dorm se apoiam em 10 e 12 comparáveis** do Airbnb. A célula
  Morretes 2 dorm (51 comparáveis, 827 unidades à venda) é a mais sólida entre as de alto retorno,
  e é ela que ancora a recomendação — não a de maior yield.
