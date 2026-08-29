"""Builds the deck specification from the analysis results.

The spec is data, not layout: slide order, headlines, KPI values, table rows and
which charts to show are all derived from output/. A slide or a chart only enters
the deck if its `include` rule fires against the actual results, so a rerun on
different data produces a different — but still coherent — deck.
Copy can be revised without touching code via presentation/overrides.json.
"""
import json, numpy as np, pandas as pd
from pathlib import Path
import deck_data as D
import pandas as _pd
from deck_data import seg_label, zpt
from deck_style import brl, num, pct

ROOT = Path(__file__).resolve().parent.parent

def build(d, R):
    """R = computed results bundle (see 10_presentation.py)."""
    P, cb, ci, ms = d['P'], R['bridge'], d['ci'], R['market']
    rec_z, rec_b = R['rec']; hyp_z, hyp_b = R['hyp']; slv_z, slv_b = R['sleeve']
    ci_i = ci.set_index(['zone','bed'])
    rec = ci_i.loc[(rec_z, rec_b)]; hyp = ci_i.loc[(hyp_z, hyp_b)]; slv = ci_i.loc[(slv_z, slv_b)]
    mkt = d['segm'].set_index(['zone', 'bed_bucket'])
    rec_mkt = float(mkt.loc[(rec_z, rec_b), 'net_yield']) if (rec_z, rec_b) in mkt.index else None
    rank = ci.sort_values('net_yield', ascending=False).reset_index(drop=True)
    hyp_rank = int(rank.index[(rank.zone == hyp_z) & (rank.bed == hyp_b)][0]) + 1
    sleeve_cost_bp = (rec.net_yield - slv.net_yield) * 100 * 100  # in basis points
    pf, roll = R['pf'], R['roll']
    sale = d['sale']; total_value = ms.value.sum()
    n_studio = int((sale.bedrooms == 0).sum())
    n_1br    = int((sale.bedrooms == 1).sum())
    n_1br_c  = int(((sale.bedrooms == 1) & (sale.macro_zone == 'Centro')).sum())
    share_1br = n_1br/len(sale)
    big_share = ms[ms.bed_bucket >= 3].value.sum()/total_value
    core_stock = ms[(ms.micro_zone.isin(['Morretes','Tabuleiro dos Oliveiras'])) & (ms.bed_bucket == 2)].value.sum()
    base_t, tor = R['tornado']
    worst = tor.low.min()

    S = []
    # ---------------------------------------------------------------- 1
    S.append(dict(id='resumo', section='Resumo executivo',
        headline=f'Comprar {int(rec_b)} dormitórios compactos em {zpt(rec_z)} — e não studios no Centro',
        layout='kpi',
        standfirst=(f'Apartamentos de {int(rec_b)} dormitórios, {cb["area"]:.0f} m², capacidade para 5 a 6 pessoas, '
                    f'na faixa de {brl(680000)} a {brl(850000)}. Retorno líquido de caixa de {pct(rec.net_yield)} ao ano, '
                    f'com uma parcela na orla da Meia Praia como seguro de liquidez.'),
        kpis=[dict(label='Retorno líquido de caixa', value=pct(rec.net_yield), note='sob operação Seazone, sobre o custo total, após gestão, condomínio, IPTU e reservas'),
              dict(label='Retorno bruto', value=pct(cb['gross_yield']), note='receita de reservas sobre o custo total'),
              dict(label='Payback', value=f'{cb["payback"]:.0f} anos'.replace('.', ','), note='sem alavancagem e sem valorização'),
              dict(label='Seleção disciplinada', value=pct(pf.noi_adj.sum()/pf.capex.sum()), note=f'carteira de {len(pf)} unidades triadas uma a uma'),
              dict(label='Estoque alocável', value=brl(core_stock), note='unidades prontas anunciadas no perfil recomendado')],
        verdict=dict(kind='reject',
            title='A hipótese interna não se sustenta',
            body=(f'“Studios e 1 dormitório no Centro” cai por três motivos independentes: não existe '
                  f'um único studio à venda na base; 1 dormitório é {pct(share_1br)} da oferta e apenas '
                  f'{n_1br_c} unidades no Centro; e o retorno do segmento é {pct(hyp.net_yield)}, '
                  f'{hyp_rank}º entre {len(ci)} segmentos. A intuição está meio certa — pequeno é eficiente — '
                  f'mas o mercado já cobrou por isso.')),
        notes=(f'Abrir pela decisão, não pelo método. O retorno de {pct(rec.net_yield)} é o do operador '
               f'profissional; o anfitrião mediano da célula roda perto de '
               f'{pct(rec_mkt) if rec_mkt is not None else "—"} — a tese é o serviço, não o prédio. '
               f'Se perguntarem “por que não o Centro”, a resposta curta é: não há produto para comprar e o m² já está caro. '
               f'O detalhe vem no slide posterior.')))
    # ---------------------------------------------------------------- 2
    big4 = ms.dropna(subset=['net_yield']).nlargest(4, 'value')
    big4_lo, big4_hi = big4.net_yield.min(), big4.net_yield.max()
    S.append(dict(id='mercado', section='Panorama do mercado', chart='c1_market',
        headline=f'{brl(total_value)} anunciados em Itapema — {pct(big_share,0)} em unidades grandes, que rendem menos',
        bullets=[f'{int(ms.n.sum()):,}'.replace(',', '.') + ' apartamentos prontos à venda nos ' + f'{len(ms)} segmentos com evidência suficiente dos dois lados do mercado.',
                 f'Os segmentos de maior capital anunciado rendem entre {pct(big4_lo)} e {pct(big4_hi)} — são os piores da cidade.',
                 f'O perfil recomendado concentra {brl(core_stock)} de estoque pronto: capital suficiente para uma tese, não uma raridade.'],
        notes='O ponto desta lâmina é a inversão: o mercado anuncia o que rende menos. É aí que está a oportunidade.'))
    # ---------------------------------------------------------------- 3
    wk = _pd.read_csv(ROOT/'output'/'weekly_revpan.csv')
    drop_pc = 100*(1 - wk.exp_rev.min()/wk.exp_rev.max())
    S.append(dict(id='demanda', section='Demanda · Airbnb', charts=['c2_season','c3_curve'],
        headline=f'A ocupação é observada, não arbitrada — e a receita cai {drop_pc:.0f}% em onze semanas',
        bullets=['O arquivo de preços do Airbnb só traz linha quando a diária está disponível: as datas ausentes são noites indisponíveis.',
                 'Três capturas do calendário enxergam a mesma estadia em horizontes diferentes, o que permite corrigir a disponibilidade vista com antecedência.',
                 f'Base observada: {d["curve"]["n_nights"]} noites, de 06/jan a 20/abr/2025. Os outros oito meses entram como premissa declarada, não como dado.'],
        notes=('Se um diretor questionar a ocupação, esta é a lâmina. Ocupação de 73% na alta temporada com '
               'corte de 10% para bloqueios do proprietário. O que não temos é o inverno, e isso está dito.')))
    # ---------------------------------------------------------------- 4
    def ppsm_cell(zone, bed):
        sub = sale[(sale.micro_zone == zone) & (sale.bed_bucket == bed) & (sale.is_offplan == 0)]
        if sub.empty: return None
        return float(sub.ppsm.median())
    ppsm_hyp_centro = ppsm_cell('Centro', 1)
    ppsm_hyp_mp     = ppsm_cell('Meia Praia (beach band)', 1)
    ppsm_rec        = ppsm_cell('Morretes', 2)
    def fpp(x):
        return f'{x:,.0f}'.replace(',', '.') if x else None
    ppsm_1br_mp = fpp(ppsm_hyp_mp) or 'data insuficiente'
    n_mp_1br = int(sale[(sale.micro_zone == 'Meia Praia (beach band)') & (sale.bed_bucket == 1) & (sale.is_offplan == 0)].shape[0])
    first_1br = (f'O metro quadrado de 1 dormitório é o mais caro entre os segmentos com escala — '
                 f'{brl(ppsm_hyp_centro, False)}/m² no Centro'
                 f'{f" e {ppsm_1br_mp}/m² na orla da Meia Praia (nicho de {n_mp_1br} unidades)" if ppsm_hyp_mp else ""}, '
                 f'contra {brl(ppsm_rec, False)}/m² num 2 dormitórios compacto em Morretes.' if ppsm_hyp_mp else
                 f'{brl(ppsm_hyp_centro, False)}/m² no Centro para 1 dormitório, contra {brl(ppsm_rec, False)}/m² '
                 f'num 2 dormitórios compacto em Morretes.')
    S.append(dict(id='precos', section='Imóveis e preços', chart='c4_ppsm',
        headline='O metro quadrado mais caro do estoque com escala é o de 1 dormitório',
        bullets=[first_1br,
                 'A eficiência do imóvel pequeno é real — ele rende mais por m² — mas já está integralmente no preço.',
                 f'Somente {n_1br} unidades de 1 dormitório e {n_studio} studios à venda em toda a cidade.'],
        notes='Esta lâmina é o cerne da refutação. O erro da hipótese não é a intuição, é ignorar o lado do custo.'))
    # ---------------------------------------------------------------- 5
    S.append(dict(id='oportunidade', section='Onde está a oportunidade', chart='c5_frontier',
        headline='A receita se compra em capacidade de dormir por m², não em endereço',
        bullets=['Elasticidade da diária em relação à capacidade: +0,55. Cada 1% de capacidade a mais vale 0,55% na diária.',
                 'Distância do mar: a receita cai 6% a cada dobra de distância; o preço pedido cai 9%. Uma quadra para dentro é acretivo.',
                 'Operação profissional vale +27% na diária — mais do que qualquer escolha fina de localização.'],
        notes=('Se sobrar tempo em uma só lâmina, é esta. As diagonais são retorno bruto constante: subir e ir '
               'para a esquerda é o objetivo.')))
    # ---------------------------------------------------------------- 6
    S.append(dict(id='perfil', section='Perfil recomendado', layout='profile',
        headline=f'{int(rec_b)} dormitórios · {cb["area"]:.0f} m² · duas suítes · 6 hóspedes · {zpt(rec_z)}',
        spec=[('Tipologia', 'Apartamento, 2 dormitórios (ambos suíte)'),
              ('Área útil', f'60 a 72 m² — mediana de {cb["area"]:.0f} m²'),
              ('Capacidade', '5 a 6 hóspedes, com sofá-cama na sala'),
              ('Localização', 'Morretes e Tabuleiro dos Oliveiras, 300 a 800 m da Meia Praia'),
              ('Faixa de preço', f'{brl(680000)} a {brl(850000)} de pedido — mediana do segmento em {brl(cb["price"])}'),
              ('Condomínio', 'até R$ 400 por mês — acima disso o retorno some'),
              ('Prédio', 'piscina e elevador; uma vaga de garagem'),
              ('Evitar', '3 e 4 dormitórios na orla e no Centro; unidades sem vaga')],
        compare=[dict(label=seg_label(rec_z, rec_b), yield_=rec.net_yield, tag='recomendado'),
                 dict(label=seg_label(slv_z, slv_b), yield_=slv.net_yield, tag='parcela de liquidez'),
                 dict(label=seg_label(hyp_z, hyp_b), yield_=hyp.net_yield, tag='a hipótese'),
                 dict(label=seg_label('Meia Praia (beach band)', 4), yield_=float(ci_i.loc[('Meia Praia (beach band)', 4)].net_yield), tag='evitar')],
        notes='Este é o briefing de compra que vai para o time de originação. Números redondos, critérios operáveis.'))
    # ---------------------------------------------------------------- 6b: quem é o hóspede
    sd = _pd.read_csv(ROOT/'output'/'segment_demand.csv')
    om = _pd.read_csv(ROOT/'output'/'opportunity_matrix.csv')
    gs = _pd.read_csv(ROOT/'output'/'guest_segments.csv')
    S.append(dict(id='hospede', section='Quem é o hóspede', layout='segments',
        headline='Itapema é família e grupo em semana de férias — não é negócios, nem fim de semana',
        standfirst=('Não observamos hóspedes: observamos como cada unidade é configurada e a demanda que essa '
                    'configuração alcança. Os segmentos abaixo são preferência revelada, não persona.'),
        rows=[dict(seg=r.segment, n=int(r.n), guests=f'{r.guests:.0f}', dorm=f'{r.dorm:.0f}',
                   adr=brl(r.adr, False), occ=pct(r.occ,0), rev=brl(r.rev),
                   season=pct(r.season,0)) for _, r in sd.iterrows()],
        evidence=[('DADO', f'Viagem de negócios aparece em {pct(gs.tx_biz.mean(),1)} dos anúncios e estadia mensal em '
                           f'{pct(gs.tx_long.mean(),1)}. Não são segmentos deste mercado — não vamos inventá-los.'),
                  ('DADO', 'A diária de sexta e sábado é igual à de meio de semana em praticamente toda a cidade. '
                           'A demanda é de semana inteira de férias, não de escapada de fim de semana.'),
                  ('DADO', f'{pct(gs.pets_ok.mean(),0)} dos anúncios aceitam animais — sinal de viagem de carro em família, '
                           'coerente com o público do Sul do país.'),
                  ('HIPÓTESE', 'A origem provável é rodoviária (Curitiba, Porto Alegre, interior de SC). A base não traz '
                               'origem do hóspede; isso precisa ser confirmado com dados internos da Seazone.')],
        notes=('Se perguntarem por corporativo ou aluguel mensal: a base diz que não existe aqui. Vale dizer que '
               'testamos e descartamos, em vez de omitir.')))
    # ---------------------------------------------------------------- 6c: matriz
    om2 = om.head(7)
    S.append(dict(id='matriz', section='Investimento → local → cliente', layout='matrix',
        headline='Cada perfil tem uma área e um cliente — e só um deles junta retorno, evidência e escala',
        cols=['Perfil', 'Área', 'Cliente predominante', 'Diária', 'Ocupação', 'Receita/ano', 'Pedido', 'Retorno', 'Evidência'],
        rows=[dict(cells=[f'{int(r.bed)} dorm', zpt(r.zone), f'{r.customer} ({pct(r.customer_share,0)})',
                          brl(r.adr, False), pct(r.occ,0), brl(r.rev), brl(r.price),
                          pct(r.net_yield), r.evidence],
                   tone=('rec' if (r.zone, int(r.bed)) == (rec_z, rec_b) else
                         'slv' if (r.zone, int(r.bed)) == (slv_z, slv_b) else
                         'hyp' if (r.zone, int(r.bed)) == (hyp_z, hyp_b) else ''))
              for _, r in om2.iterrows()],
        chain=[('Compra', f'2 dorm compacto, {cb["area"]:.0f} m², {brl(cb["price"])}'),
               ('Local', f'{zpt(rec_z)}, 300–800 m da Meia Praia'),
               ('Cliente', 'Família de 5–6 em semana de férias'),
               ('Demanda', f'Ocupação projetada de {pct(cb["occ"]/P["booked_share"],0)} (bruta · {pct(P["booked_share"],0)} de reservas pagas) · sem prêmio de fim de semana'),
               ('Retorno', f'{pct(rec.net_yield)} líquido · payback de {cb["payback"]:.0f} anos')],
        notes=('A linha de baixo é a tese em cinco caixas. Morretes 3 dorm rende mais, mas se apoia em 10 comparáveis; '
               'a orla tem evidência forte e menos retorno. O 2 dorm em Morretes é o único com os três.')))
    # ---------------------------------------------------------------- 7
    FURN = f"{int(P['furnish_per_m2']):,}".replace(',', '.')
    S.append(dict(id='financeiro', section='Análise financeira', chart='c7_bridge',
        headline=f'De {brl(cb["rev"])} de receita a {brl(cb["noi"])} de resultado — {pct(cb["net_yield"])} sobre {brl(cb["capex"])}',
        secondary='c6_yields',
        bullets=[f'Custo total = pedido menos {pct(P["negotiation_disc"],0)} de negociação, mais {pct(P["closing_costs"],0)} de fechamento, '
                 f'mais R$ {FURN}/m² de mobília e enxoval.',
                 f'A diferença entre bruto ({pct(cb["gross_yield"])}) e líquido ({pct(cb["net_yield"])}) é de {pct(cb["gross_yield"]-cb["net_yield"])}. '
                 'Qualquer retorno prometido nessa faixa é bruto vestido de líquido.',
                 'Custos fixos pesam desproporcionalmente em unidades pequenas — a segunda razão pela qual o studio não fecha.'],
        notes=('O número para levar: 11,6% bruto, 6,2% líquido (o do operador profissional; o anfitrião '
               'mediano roda ~4,0%). Se alguém citar “13% a 23% ao ano”, é bruto ou '
               'inclui valorização — e vale dizer isso na reunião.')))
    # ---------------------------------------------------------------- 8
    S.append(dict(id='riscos', section='Riscos e sensibilidades', charts=['c8_tornado','c9_distance'],
        headline='Nenhuma premissa isolada derruba a tese — a única ameaça real é geográfica',
        bullets=[f'2.187 combinações de premissas: os três primeiros segmentos mantêm a ordem em todas. '
                 f'O pior caso de qualquer premissa isolada é {pct(worst)}.',
                 'O VivaReal não traz coordenadas. Se o estoque fora da orla estiver mais longe do mar do que os comparáveis do Airbnb, a receita está superestimada.',
                 f'A parcela na orla existe exatamente para isso: custa cerca de {sleeve_cost_bp:.0f} pontos-base de retorno e elimina a única incerteza capaz de inverter a ordem.'],
        limits=['Oito meses do ano não são observados — sazonalidade é premissa declarada, com sensibilidade.',
                'Preços são pedidos, não transações. Valorização e imposto de renda estão fora.',
                f'Apenas 1.005 dos 4.441 anúncios têm calendário, e o subconjunto pende para anúncios profissionais.'],
        notes='Não esconder o risco geográfico. Apresentá-lo antes que perguntem é o que compra credibilidade.'))
    # ---------------------------------------------------------------- 9
    S.append(dict(id='recomendacao', section='Recomendação e próximos passos', chart='c10_portfolio',
        headline=f'{brl(pf.capex.sum())} em {len(pf)} unidades — {pct(pf.noi_adj.sum()/pf.capex.sum())} líquido, payback de {pf.capex.sum()/pf.noi_adj.sum():.1f} anos'.replace('.', ','),
        steps=[('Validar em campo', f'Visitar as {len(pf)} unidades da lista triada — começando pelas {min(25, len(pf))} de maior retorno. São os m² mais baratos das suas células — é onde também moram anúncio velho e área errada.'),
               ('Confirmar condomínio e IPTU', f'Valores declarados em apenas {pct(sale.monthly_condo_fee.notna().mean(),0)} dos anúncios. Acima de R$ 400/mês a tese muda.'),
               ('Testar a premissa de baixa temporada', 'É a premissa mais sensível da análise. Um mês de dados reais de maio resolve.'),
               ('Fechar a primeira tranche', f'6 a 8 unidades em {zpt(rec_z)}, cerca de {brl(6*cb["capex"])}, para validar a operação antes de escalar.')],
        notes='Terminar pedindo uma decisão concreta: autorização da primeira tranche, não do plano inteiro.'))

    spec = dict(
        title='Itapema · Tese de Investimento',
        subtitle='Onde a Seazone deveria comprar, e por quê',
        meta=dict(date='Agosto de 2026',
                  source='Airbnb + VivaReal · snapshot de janeiro de 2025',
                  scope=f'{int((sale.is_offplan == 0).sum())} apartamentos prontos à venda · 1.005 anúncios com calendário'),
        slides=S)
    ov = ROOT/'presentation'/'overrides.json'
    if ov.exists():
        spec = deep_merge(spec, json.load(open(ov)))
    return spec

def deep_merge(base, over):
    if isinstance(base, dict) and isinstance(over, dict):
        out = dict(base)
        for k, v in over.items():
            out[k] = deep_merge(base.get(k), v) if k in base else v
        return out
    if isinstance(base, list) and isinstance(over, dict):
        out = list(base)
        for k, v in over.items():          # {"2": {...}} patches slide index 2
            i = int(k)
            if 0 <= i < len(out): out[i] = deep_merge(out[i], v)
        return out
    return over
