# Log da sessão de análise

**Ferramenta:** Claude (Cowork), com execução de código Python no ambiente da sessão.
**Papel da IA:** engenharia de dados, modelagem, e redação. Todas as decisões de método e de
negócio foram revisadas e são defendidas aqui explicitamente.

---

## Ponto de partida — e uma correção logo no início

Antes do enunciado do desafio existir, eu tinha preparado um dossiê estratégico sobre a Seazone que
concluía por um produto chamado FAROL — uma camada de IA para a rede de franqueados. Quando o
enunciado real chegou (uma **decisão de investimento imobiliário em Itapema**), esse dossiê deixou
de ser a resposta. Foi mantido como contexto de negócio e descartado como direção. Registro isso
porque a tentação de encaixar um trabalho pronto num enunciado diferente é o erro mais caro
disponível aqui.

Instrução dada explicitamente à IA no começo: *"não siga cegamente o dossiê nem minhas sugestões
anteriores. Trate como hipóteses. Se os dados mostrarem uma direção melhor, mude a recomendação e
explique por quê."*

---

## Etapa 1 — Perfilagem antes de qualquer modelo

Primeira pergunta feita aos dados, antes de escolher qualquer técnica: **o que cada arquivo é de
verdade?**

A descoberta que definiu todo o resto veio de olhar a estrutura de `Price_AV_Itapema.csv`:

- 118.839 linhas, mas apenas **1.005 dos 4.441 anúncios** aparecem.
- Três datas de captura (06, 07 e 20/jan/2025), cada uma olhando ~90 noites à frente.
- A contagem de anúncios disponíveis por data de estadia **sobe** de 21 em 06/jan para 627 em abril.

Isso não é um arquivo de preços. É um **arquivo de disponibilidade**: só existe linha quando a
diária está livre. Datas ausentes dentro da janela são noites indisponíveis. Ou seja, **ocupação é
observável** — não precisa ser arbitrada. Essa leitura vale mais do que qualquer modelo que viesse
depois.

Também ficou registrado no mesmo passo o que *não* dá para fazer: o calendário cobre 105 noites de
janeiro a abril. Oito meses do ano não existem na base. Qualquer número anual depende de uma
premissa declarada.

## Etapa 2 — A curva de reserva

Disponibilidade vista com 90 dias de antecedência superestima a disponibilidade final. Como a mesma
data de estadia aparece em duas capturas diferentes, dá para medir quanto uma noite enche em 13 dias
— e daí identificar a curva inteira.

Modelo: `logit P(disponível) = anúncio + data + antecedência`, ajustado em 209.846 noites-anúncio.

Detalhe que quase virou erro: a curva desaba entre 3 e 0 dias de antecedência (−1,1 em log-odds).
Olhando os dados brutos, a disponibilidade no próprio dia da captura é de 2,8% a 3,6% — isso é o
corte de reserva da plataforma, não demanda de última hora. Projetar para antecedência 0 dava
**ocupação média de 87%**, implausível. Projetando para 3 dias: 73%. Adotamos 3 dias, com
sensibilidade de 2 a 10 dias na varredura de premissas.

Validação: a ocupação modelada sobe monotonicamente com o número de avaliações do anúncio
(0,47 para anúncios sem avaliação → 0,80 para anúncios com mais de 30). Não é prova, é consistência.

## Etapa 3 — Três erros que apareceram e o que cada um custou

**Erro 1 — li um coeficiente por quilômetro como se fosse elasticidade.**
Numa primeira regressão, a distância do mar entrava em quilômetros, não em log. O coeficiente
−0,512 virou, na minha leitura, "−46% de receita por dobra de distância". Reestimando com a
especificação certa (log-log, produto mantido constante): a elasticidade real é **−0,090** na
receita e **−0,139** no preço pedido. Isso **inverteu** o teste de estresse: com −0,46, ir para
dentro destruía o retorno e a orla vencia; com −0,090, o mercado de venda desconta distância mais
rápido do que o de locação penaliza, e ir uma quadra para dentro passa a ser acretivo. A conclusão
central do trabalho depende dessa correção.

**Erro 2 — confiei no nome de um bairro.**
"Jardim Praia Mar" foi inicialmente agrupado na faixa de orla da Meia Praia. As coordenadas dos
anúncios do Airbnb mostram que ele fica a ~1,2 km do mar. Corrigido, o yield da orla caiu de 6,7%
para 5,8% e três anúncios saíram do topo da lista de compra. Nome de bairro não é geolocalização.

**Erro 3 — a primeira lista de compra premiava erro de cadastro.**
O ranking bruto por yield trouxe anúncios de R$ 350 mil para 55 m² em Morretes — metade do preço
mediano do segmento. Podem ser barganhas reais, mas também podem ser anúncio velho, área errada ou
preço de "a partir de". Foram adicionados dois filtros: descarte de outliers de preço/m² dentro da
própria célula, e um deságio de receita para unidades anunciadas abaixo dos seus comparáveis
(se o mercado precifica 30% abaixo, parte disso é atributo que também derruba a diária). O resultado
final é apresentado como **lista de visitas, não ordem de compra**.

## Etapa 4 — O teste da hipótese

Antes de calcular retorno, uma pergunta mais simples: **o produto existe?**
Zero studios entre 6.796 apartamentos à venda. 136 unidades de 1 dormitório (2,0%), 16 no Centro.
Isso encerra a hipótese por restrição de escala antes de qualquer discussão de retorno.

Depois, com controles: o efeito "Centro" e o efeito "compacto" têm intervalos de confiança que
cruzam zero, e a interação Centro × compacto — exatamente o termo que a hipótese precisaria — sai
**negativa**.

E o achado que explica tudo: o 1 dormitório de fato ganha mais por metro quadrado, **e custa mais
por metro quadrado**. A eficiência é real e já está no preço.

## Etapa 5 — Robustez antes de conclusão

2.187 combinações das sete premissas que mais importam. A ordem dos três primeiros segmentos não
muda em nenhuma delas. Isso, e não um R² melhor, é o que autoriza escrever a recomendação.

Escolha final consciente: a recomendação âncora **não** é o segmento de maior yield
(Morretes 3 dorm, 7,9%, mas apenas 10 comparáveis do Airbnb), e sim Morretes 2 dorm — 6,4% com
51 comparáveis e 827 unidades à venda. Evidência mais espessa e capital alocável de verdade valem
mais do que 150 pontos-base num segmento fino.
