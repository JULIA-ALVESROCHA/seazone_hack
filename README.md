Link para o vídeo: https://drive.google.com/file/d/1044q9RjTdzGl2FWiPFj1qRW-E46S2RrM/view?usp=sharing

link para Transcrição: https://drive.google.com/file/d/1aO7TpE8jVwnTrmm2PfUL0n3ciE0cnmS6/view?usp=sharing
# Itapema Investment Screen — Seazone Hackathon 2026

A decision system, not a notebook: it turns five raw CSVs into a ranked buy list with
stated assumptions, confidence intervals and an assumption sweep.

**Headline:** buy compact 2-bedroom apartments (60–72 m², two suítes, sleeps 5–6) in
**Morretes / Tabuleiro dos Oliveiras** around R$680k–850k asking (median of the segment:
R$790k), plus a smaller 2BR beach-band sleeve (Meia Praia) as liquidity insurance.
Expected unlevered net cash yield **6.2%** under professional (Seazone) operation (11.6% gross),
payback 16.1 years; up to **9.1%** on disciplined listing-level selection. The internal
hypothesis — *compact studios/1BR in Centro* — is **rejected**: no studios exist on the sale
market, 1BR is 2.0% of listed apartments, Centro shows no revenue premium once distance-to-sea
and unit size are controlled, and 1BR carries the highest price per m² in the city.

## Run

Everything below is reproducible from this repo alone (paths resolve to `data/` and `output/`
relative to the repo root; override with `ITAPEMA_DATA` / `ITAPEMA_OUT`):

```bash
pip install pandas numpy scipy scikit-learn matplotlib
python src/01_airbnb_demand.py       # availability panel + booking curve + price model (+ weekly series)
python src/02_sale_market.py         # VivaReal cleaning, de-duplication, geography normalisation
python src/03_spatial.py             # data-derived coastline, distance to sea, KD-tree competition
python src/04_investment_model.py    # segment-level yields under explicit assumptions
python src/05_drivers_hypothesis.py  # revenue drivers + the Centro/compact hypothesis test
python src/06_screening.py           # listing-level revenue prediction and screening
python src/07_robustness.py          # bootstrap CIs + 2,187-combination assumption sweep
python src/07b_distance.py           # distance-to-sea gradient on both sides of the market
python src/08_decision.py            # controlled tests, deployable capital, buy list, cases
python src/09_portfolio.py           # quality-adjusted screen + R$20M allocation
python src/11_guest_segments.py      # guest segments + opportunity matrix
python src/stress_test.py            # robustness probes of the recommendation
python src/10_presentation.py        # charts + executive deck (reads only output/)
```

Outputs land in `output/`; the written recommendation is `docs/recomendacao.html`.

## The three methodological choices that matter

**1. `Price_AV` is an availability file, not a price file.** A row exists only when a night is
bookable, so a missing (listing, stay-date) inside a capture window is an unavailable night.
That makes occupancy observable rather than assumed — but availability seen 90 days out
overstates final availability. With three captures (6, 7 and 20 Jan 2025) the same stay-date
is seen at two lead times, which identifies a booking curve. We fit
`logit P(available) = listing + stay-date + lead` over 209,846 listing-nights and project
every listing to a 3-day lead. Nights at 0–2 days lead are excluded: that drop is the
platform's booking cut-off, not demand.

**2. Airbnb has capacity but no floor area; VivaReal has floor area but no capacity.**
The two sides are bridged by rank-preserving quantile matching inside each
(zone × bedrooms) cell, so a unit in the 70th area percentile inherits the 70th-percentile
capacity of comparable Airbnb units.

**3. VivaReal has no coordinates.** Its `suburb` field is finer than the Airbnb mesh
(it splits Meia Praia into Andorinha / Castelo Branco), so zones are normalised to a common
taxonomy and Meia Praia is split by a data-derived coastline: the eastern envelope of the
listing point cloud, smoothed and densified, with distance computed by KD-tree. Ad text is
mined for explicit "N metros do mar" claims. The residual location uncertainty is the
largest single source of error and is stress-tested directly in `07b_distance.py` and
`09_portfolio.py`.

## Assumptions (all in `output/assumptions.json`, all swept in `07_robustness.py`)

| Parameter | Base | Swept |
|---|---|---|
| Lead time treated as final availability | 3 days | 2–10 |
| Share of unavailable nights that are paid bookings | 0.90 | 0.80–1.00 |
| Host share of the displayed nightly price | 0.90 | 0.85–1.00 |
| May–Sep RevPAN vs observed April | 0.50 | 0.35–0.65 |
| Negotiation discount off asking price | 7% | 0–12% |
| Closing costs (ITBI, deed, registry) | 5% | — |
| STR furnishing | R$1,200/m² | R$800–1,800 |
| Management fee | 20% of booking revenue | 15–25% |
| Utilities/consumables per occupied night | R$45 | R$30–65 |
| Maintenance reserve | 0.5% of value p.a. | — |

Annualisation factor implied by the seasonality assumption: **2.47×** the observed 105-night window.

## Two yield concepts — and which one is the headline

There are two defensible "net yield" numbers per segment, and the deck is explicit about both:

- **Market-revenue view** (median existing host, `segments_micro_zone.csv`): Morretes 2BR ≈ **4.0%** net.
  This is what you should earn by buying a building as-is. It is not an attractive asset yield.
- **Professional-operator view** (Seazone-operated counterfactual, `segment_yields_ci.csv`): Morretes 2BR ≈ **6.2%** net,
  Tabuleiro 2BR ≈ 6.8%, Morretes 3BR ≈ 7.8%.

**The thesis is the service, not the building.** The 6.2% headline *requires* running the units
like the top professional hosts (the model scores every sale unit at the 75th-percentile listing
quality). If Seazone planned to buy-and-hold without operating, the honest number to carry is the
~4.0% market view.

## What the data cannot support

Eight months of the year are unobserved. Transaction prices are unobserved (asking prices only).
Capital appreciation and income tax are excluded. Only 1,005 of 4,441 Airbnb listings carry
calendar data, and that subset skews professional — so absolute occupancy is likely flattered
even after the 10% owner-block haircut. Morretes 3BR rests on only 10 Airbnb comparables — which
is why it is flagged as higher-yield-but-thinner and the 2BR cells (51 comparables, 827 listings
ready) anchor the recommendation rather than the higher-scoring 3BR.

## Stress tests (see `output/logs/log_stress.txt`)

The recommendation survives every probe that can be run from the existing outputs:

| Probe | Result vs base (Morretes 2BR 6.2%) |
|---|---|
| Cheap tail excluded (asking ≥ R$550k) | 6.1% — unchanged ordering |
| Strict band only (R$600k–900k) | Morretes 2BR 6.3%; cheap orla 2BR improves (value within sleeve) |
| Morretes 3BR removed (thin cell) | Tabuleiro 6.8% leads, Morretes 2BR 6.2% holds |
| Median host (non-operator) revenue | 3.6% — the market view, ~half the operator view |
| Conservative corner assumptions | 2.6% — still leads, but this is the floor |
| Revenue +30% / −25% on all cells | Ordering unchanged; no large/orla cell jumps |
| Distance stress (07b): off-beach stock 2×−3× further | sleeve crosses at ~2.5× with pessimistic elasticity |

The one force that can invert the order is *geography*: if the off-beach sale stock is
systematically farther from the sea than its Airbnb comparables, Morretes' revenue is overstated.
That is exactly why the recommendation carries a Meia Praia 2BR sleeve (≈50 basis points of
yield as insurance) and why the sleeve is a *sleeve*, not the core.

---

## Camada de apresentação e camada de demanda

```bash
python src/11_guest_segments.py   # segmentos de hóspede + matriz de oportunidades
python src/10_presentation.py     # gráficos matplotlib + deck executivo
```

`10_presentation.py` lê apenas `output/` — não recalcula nada. Roda de novo depois de qualquer
mudança acima e o deck se reconstrói sozinho, com os números atualizados. Cada gráfico declara
uma regra de relevância e só entra se ela disparar contra os resultados; textos podem ser
revisados sem tocar em código criando `presentation/overrides.json`
(ex.: `{"slides": {"0": {"headline": "Nova manchete"}}}`).

Deck em [`docs/apresentacao.html`](docs/apresentacao.html) — 11 lâminas, navegação por teclado
(←/→, `G` índice, `N` notas do apresentador, `P` PDF). Todos os gráficos têm fundo branco.

**Quem é o hóspede (camada de demanda).** Não observamos hóspedes: observamos como cada unidade é
configurada e a demanda que essa configuração alcança — preferência revelada, não persona.
Quatro segmentos, todos com padrão de demanda distinto:

| Segmento | Anúncios | Hóspedes | Diária | Ocupação | Receita/ano |
|---|---|---|---|---|---|
| Alto padrão e frente-mar | 120 | 8 | R$ 1.221 | 75% | R$ 176 mil |
| Grupos e amigos | 217 | 8 | R$ 683 | 85% | R$ 108 mil |
| Famílias | 407 | 6 | R$ 554 | 83% | R$ 87 mil |
| Casais e escapadas curtas | 167 | 4 | R$ 499 | 70% | R$ 70 mil |

E dois segmentos **descartados com evidência**: viagem de negócios aparece em 1,9% dos anúncios e
estadia mensal em 0,1%. A diária de sexta e sábado é igual à de meio de semana em praticamente toda
a cidade — a demanda é de semana inteira de férias, não de escapada de fim de semana.

A cadeia completa está em `output/opportunity_matrix.csv`:
**2 dorm compacto → Morretes → família de 5–6 em semana de férias → ocupação de 77% → R$ 71 mil/ano
→ 6,2% líquido.**

---

## Entrega (hackathon)

- Recomendação por escrito: [`docs/recomendacao.html`](docs/recomendacao.html) e [`RECOMENDACAO.md`](RECOMENDACAO.md)
- Log de uso de IA: pasta [`ai-log/`](ai-log/)
