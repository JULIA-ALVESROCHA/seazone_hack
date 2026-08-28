# Seazone Hackathon Intelligence Dossier
**Prepared for:** Seazone Trainee Program 2026 — Hackathon stage
**Version:** 1.0 · Research cut-off: 26 August 2026
**Confidence legend:** `[F]` Verified fact (named source) · `[I]` Strong inference (multiple converging signals) · `[H]` Hypothesis (needs validation)

> **Status note:** The official hackathon prompt has **not** been provided yet. Section 8 is therefore built as a *pre-analysis + pivot matrix* rather than a challenge breakdown. Everything upstream of it (company, ecosystem, competitors, problem map) is stable regardless of which prompt lands, and the recommended solution in Section 16 is designed with a documented pivot path.

---

## Table of Contents

1. Executive Summary
2. Seazone: Company Overview
3. Seazone Business Model & Revenue Logic
4. Products & Ecosystem Map
5. Customers & Stakeholders
6. **Structural Nuances That Create an Unfair Advantage** *(added section — read this one twice)*
7. Trainee Program Intelligence & Evaluation Model
8. Hackathon Challenge Pre-Analysis & Pivot Matrix
9. Strategic Priorities
10. Current Pain Points (evidence-based)
11. The 2026 Regulatory Shock
12. Competitor Intelligence
13. Solution Patterns Worth Adapting
14. Problem Opportunity Map
15. Candidate Solutions & Scoring Matrix
16. **Recommended Solution: FAROL**
17. MVP Definition & User Journey
18. Technical Architecture
19. Data Strategy
20. AI Strategy (organizational, not just technical)
21. Credit & Cost Optimization
22. Demo Reliability Plan
23. Business Case
24. Go-To-Market & Moat
25. Metrics & Validation
26. **How to Use AI *During* the Hackathon (this is graded)**
27. Implementation Plan (hour by hour)
28. Presentation Strategy
29. Risks & Failure Modes
30. Adversarial Review — Killing Our Own Idea
31. Open Questions
32. Sources

---

## 1. Executive Summary

Seazone is a Florianópolis-born proptech (2018) that turned short-term rental management into two stacked businesses: **operating other people's real estate** (~2,900 properties, 2,040+ owners, 60+ destinations, 15 states) and **creating the real estate itself** (44 "SPOT" developments, R$723M+ raised from investors). `[F]`

The thing that makes Seazone structurally different from Charlie, Housi, Vacasa, or Guesty is not its pricing algorithm. It is that **Seazone's last mile is a franchise network of 110+ independent operators, not employees.** Seazone contractually owns everything digital — listings, pricing, guest service, financial settlement, tax — and the franchisee owns everything physical — check-in, cleaning, laundry, maintenance, local relationships. `[F]`

That single design choice is the source of the company's growth (100%/year since 2020, no physical structure per city) and of its single biggest scaling risk (**quality variance across a network Seazone does not directly employ**). Public complaint data shows exactly this signature: a 4.8/5 average across 70,000+ reviews sitting alongside a "Regular" 6.8/10 reputation score on Reclame Aqui with 102 complaints in H1 2026, clustered around inconsistency, listing-vs-reality mismatch, payout friction, and communication breakdown. `[F]`

Meanwhile 2026 delivered two structural shocks to the market: the STJ's May 2026 ruling requiring **two-thirds condominium approval** for professional short-stay operation, and **Decreto 12.955/2026**, which taxes ≤90-day residential rentals like hotel services for anyone above the professional threshold. Seazone's owner base is precisely the cohort affected. `[F]`

And globally, the AI frontier in this category moved decisively in the last 90 days: Guesty launched **Agent Hub** (coordinated AI agents + an MCP server) on 1 June 2026; Hostaway launched **AI CoHost** in June/July 2026. Both built copilots for *centralized property managers*. **Neither built one for a franchise network.** `[F]`

**Recommended hackathon direction: FAROL** — an AI operations layer for Seazone's franchise network that converts unstructured operational signal (guest messages, reviews, ops events, property state) into a *predicted quality-and-revenue risk score per property*, and pushes a ranked, three-item daily action list to each franchisee, while giving HQ a network-wide console. It attacks the exact bottleneck the business model creates, uses AI where deterministic code genuinely cannot substitute, demos in 90 seconds, and costs under US$5 to run.

---

## 2. Seazone: Company Overview

### 2.1 Origin story `[F]`
Fernando Pereira, a mining/oil engineer from Mato Grosso, spent close to a decade working abroad for Glencore (including oil operations in Chad), rotating a month on-site and a month home. He began investing in Brazilian real estate in 2014, starting with a unit at IL Campanario Villaggio Resort in Jurerê Internacional, Florianópolis. The returns beat CDI and the asset appreciated, so he bought more — eventually holding roughly 35 hotel-condo units. The operational pain of managing them remotely, especially from abroad, was the founding insight. (Sources: Exame, Jul 2023; IstoÉ Dinheiro, Jun 2024; Hotelier News, Sep 2025.)

> **Source conflict, flagged:** the official site and most press say **founded 2018**; several franchise portals and one IstoÉ Dinheiro piece say **2019**. Reconciliation `[I]`: the operating company began in 2018 as a digital listing-management service for *hotels* in Florianópolis; 2019 is when the company incorporated the development vertical (land acquisition for Spot Jurerê) and/or formalized a second legal entity. Two CNPJs are publicly visible: Seazone Serviços LTDA **32.018.829/0001-08** (marketplace footer) and Seazone Serviços Ltda **42.479.879/0001-46** (franchise footer). Use **"founded 2018"** — it's what the company says about itself.

### 2.2 Evolution `[F]`
| Phase | What happened |
|---|---|
| 2018 | Digital management of listings for **hotels** in Florianópolis. CEO: "we realized the hotel market was small and decided to expand into residential apartments." |
| 2019 | Land acquired in Florianópolis; **Spot Jurerê** launched — first property product designed from the blueprint for STR. Entry into real-estate development. |
| 2020 | Pandemic wipes out bookings. Company pivots from a fully in-house operation to a **microfranchise model** — the decisive structural move. Growth resumes at ~100%/year. |
| 2023 | R$3.5M round from **DOMO Invest**. Named a Top Startup by **Forbes** and **LinkedIn**. First SPOT delivered (Jurerê Spot, 25 apartments, rooftop bar). 13 further SPOTs launched across SC, BA, AL. |
| 2024–2025 | Expansion into Northeast (Salvador, Imbassaí, Trancoso, Japaratinga), plus Goiânia, Gramado, Campos do Jordão, Balneário Camboriú. VGV ~R$335M (Sep 2025). Series A signalled for 2025 to fund LatAm expansion (Argentina, Uruguay, Chile). |
| 2026 | 110+ franchisees, 48–50 cities, 15 states, ~2,900 properties. 44 SPOTs, R$723M+ raised. Trainee program rebuilt entirely around AI. |

### 2.3 Scale, as publicly claimed (mid-2026) `[F]`
| Metric | Value | Source |
|---|---|---|
| Properties under management | 2,700+ (institutional site) / 2,900+ (franchise LP) / 3,000+ (owner LP) | seazone.com.br, May–Aug 2026 |
| Property owners | 2,040+ | Institutional site |
| Franchisees | 110+ | Franchise LP, May 2026 |
| Cities / States | 48–50 / 15 | Franchise LP |
| Destinations (guest-facing) | 60+ | Institutional site |
| SPOT developments launched | 44 across 16 cities | Institutional site |
| Capital raised for developments | R$723M+ | Institutional site |
| Nights sold (cumulative) | 1,000,000+ | Institutional site |
| Guest rating | 4.8/5 across 70,000+ reviews | Institutional site |
| Developer partners | 100+ construtoras, 160+ empreendimentos, 800+ units under partnership | Institutional site |
| Revenue | R$8.9M (2021) → R$21.3M (2022) → R$42M target (2023) → **>R$42M LTM** (Oct 2025) | Exame, Hotelier News |
| Growth | ~100% per year since 2020 | CEO, multiple interviews |

> **Note the internal inconsistency across Seazone's own properties** (2,700 vs 2,900 vs 3,000 properties; 48 vs 50 vs 54 cities; 1,000 vs 2,040 owners on different pages). This is itself a finding — see §10.6, "the numbers don't reconcile across surfaces," which is a symptom of fragmented data ownership and a legitimate, if unglamorous, opportunity area.

### 2.4 Leadership `[F]`
- **Fernando Pereira** — CEO & co-founder. Engineer. Analytical, data-first framing in every public interview ("the decision is never intuitive").
- **Bruno Benetti** — COO. Public voice on regional expansion (Salvador).
- **Mônica Medeiros** — Partner & CCO. Public voice on the franchise model ("the franchisee is the face of Seazone to the guest and the *guardian of the experience* in the property").

**Read on leadership `[I]`:** they consistently describe the company in terms of *system design* — data, algorithms, standardized processes, network structure — rather than hospitality romance. Pitch accordingly: mechanism over vibe.

---

## 3. Seazone Business Model & Revenue Logic

### 3.1 Two verticals, four revenue lines `[F]`
CEO framing: *"There are two verticals: short-term rental operation and real estate development."*

| Line | Mechanism | Rate (public) |
|---|---|---|
| **Management fee** | % of rental revenue on managed properties | **20–30%** of the booking (Exame, 2023) |
| **Development structuring** | Fee on Gross Sales Value of SPOT projects sold to investor pools | **~6% of VGV** |
| **Setup / furnishing** | Decoration and outfitting package per unit | **~R$7,000** (2023 figure) |
| **Franchise** | Entry fee + network economics | Entry **from R$5,000**, remainder amortized from generated nightly revenue |

`[I]` Guest-side cleaning fees and possible ancillary revenue (early check-in, extras, insurance-like products) likely exist but are not publicly itemized.

### 3.2 The franchise economics — the most important table in this dossier `[F]`
From the official franchise landing page (updated May 2026):

| Franchisee receives | Share |
|---|---|
| % of each booking's revenue | **8%** |
| Cleaning fee | **100%** |
| Bonus on properties the franchisee sourced | **+2%** |
| Settlement | Tracked in real time in "**Wallet Seazone**" |

Franchisee investment: from **R$5,000** entry, remainder progressively deducted from nights generated. Payback stated as up to 12 months. Territory is **contractually exclusive** (neighborhood, city, or micro-region), and **every property captured by the network in that territory enters the franchisee's book**. The franchisee **must live in or maintain daily operational presence in** the contracted city — remote management is explicitly ruled out. Average franchisee reaches **20+ properties in the first 6 months**.

Seazone's own illustrative simulator: 25 properties, R$450 ADR, 65% occupancy → R$219,375 monthly GMV for that book → R$32,500/month to the franchisee → R$390,000/year.

> **Source conflict:** ABF/franchise portals list an older configuration — R$20,000 entry, 71 franchised units, ~R$22,000 average monthly billing, home-based, **no royalties or advertising fees**. These are 2024-era figures. Prefer the May 2026 official LP.

### 3.3 Division of labor (verbatim from the company) `[F]`
> **"A Seazone é o braço digital. Você é o braço local."**
> Seazone handles: professional listings with photography, **dynamic pricing**, centralized guest service, receipt issuance, owner payouts, tax control.
> Franchisee handles: check-in, check-out, cleaning, laundry, maintenance, own or subcontracted local team, direct owner relationships in the region.

**This is the single most useful sentence in the entire research corpus.** Seazone has already told you where automation is permitted to operate: *everything on the digital side is, by contract, centralizable — and therefore AI-addressable.* You are not proposing an organizational change; you are filling in a box the org chart already drew.

### 3.4 Unit economics, reconstructed `[I]`
2,900 properties × ~R$450 ADR × ~55% occupancy × 365 ≈ **R$262M annualized network GMV**.
At a 20–25% management take, gross commission ≈ R$52–65M — of which 8% of GMV (~R$21M) flows to franchisees, plus cleaning fees flowing entirely to franchisees.
Reported company revenue of >R$42M LTM is consistent with this if Seazone recognizes net commission plus development fees. **Treat as an order-of-magnitude model, not accounting.** Stated assumptions matter more than the number.

---

## 4. Products & Ecosystem Map

| Surface | User | Purpose | Observable weakness `[I]` | Opportunity |
|---|---|---|---|---|
| `seazone.com.br` (Next.js) | Guest | Direct booking, 60+ destinations | Direct channel is small vs OTA; discovery is filter-based | Direct-booking conversion, AI trip matching |
| `/marketplace` + `/investir` | Investor | SPOT listings, launches, resale | Static-ish listings; no personalized portfolio simulation visible | Investment copilot, personalized IRR modeling |
| `novos-proprietarios` LP | Owner prospect | Lead capture, "free simulation" | Simulation is a lead-gen promise, not a live product | Instant AI revenue simulation from address |
| `institucional/franqueados` | Franchisee prospect | Recruitment, ROI simulator, territory availability | Sophisticated funnel; territory sizing appears manual | AI territory scoring |
| **Proprietary platform** | All three sides | Pricing, cleaning/maintenance governance, operational performance, guest experience | Single point of dependency; unclear how much is agentic vs CRUD | Agent layer on top |
| **Sirius** (RM algorithm) | Internal | Prices every night: local demand, seasonality, events, competition, occupancy history; real-time; parity across Airbnb, Booking, Expedia | Numeric/structured only — cannot read reviews, messages, condo conventions | **Complement, don't rebuild** |
| **Proprietary market database** | Expansion | "Hundreds of variables": historical occupancy, ADR, real-estate liquidity, m² appreciation, tourist demand profile, macro + regulatory trends | Regulatory layer likely coarse; condo-level risk almost certainly absent | Regulatory/condo risk layer |
| **Wallet Seazone** | Franchisee | Real-time earnings tracking | — | — |
| Web scraper | Internal | Identifies properties and which are being rented; informs city scaling | Told to us in the briefing; not publicly documented | Enrichment, not replacement |
| Blog + e-books | Market | SEO, market panorama data, lead nurture | Content is good; not personalized | Retrieval corpus for an internal agent |

**Confirmed technology footprint `[I]` (from page inspection):** Next.js (marketing + marketplace), **Supabase** storage (public asset bucket), WordPress/Elementor (institutional), **InHire** ATS, **RD Station** (lead events), Google Tag Manager, Meta Pixel. WhatsApp is a first-class channel across every funnel (franchise, owner, guest support).

> **Do not rebuild:** dynamic pricing, channel manager/parity, listing distribution, city-level demand scoring, payout ledger. These exist. Building them again is the most common way to lose this hackathon.

---

## 5. Customers & Stakeholders

| Stakeholder | Core job-to-be-done | What they fear | Data they generate |
|---|---|---|---|
| **Property owner / investor** | Passive, above-CDI yield on a physical asset without operational involvement | Underperformance, property damage, opaque payouts, tax exposure, being unable to use their own property | Contracts, payouts, property specs, complaint history |
| **SPOT investor** | Buy a purpose-built STR unit with credible yield projection (site claims 13–23% p.a.) | Projection not materializing; illiquidity | Purchase, unit config, delivery timeline |
| **Guest** | A stay that matches the listing, with someone reachable when something breaks | Listing-vs-reality gap, check-in friction, unreachable support | Messages, reviews, ratings, booking behavior |
| **Franchisee** | Recurring income from a growing book, without building brand/tech/trust from scratch | Territory not filling, operational overload during peak, income volatility | Ops events, cleaning cycles, local knowledge (**mostly untracked**) |
| **Developer / construtora** | Sell units faster with a yield story attached | Units not absorbing; operator underdelivering | Project specs, absorption data |
| **Broker partner** | Extra inventory + referral income | Losing the client to the platform | Referrals |
| **Airbnb / Booking / Expedia / Decolar** | Reliable, high-rated supply | Bad supply degrading the marketplace | Ranking signals, impression share |

---

## 6. Structural Nuances That Create an Unfair Advantage
*(This is the section you asked for. It is the strategic core of the dossier — every recommendation downstream derives from it.)*

Most hackathon teams will treat Seazone as "Brazilian Airbnb manager" and propose a generic STR AI product. That loses, because generic STR AI already exists and is better funded (Guesty, Hostaway). **The way to win is to build something that only works *because* of how Seazone specifically is built.** Here are the eleven structural nuances that create that opening.

---

### N1 — The last mile is a franchise, not a payroll `[F]` → *the biggest one*
Charlie, Housi, Vacasa, Sonder all operate with employees or direct contractors under central management. Seazone's local operation is run by **110+ independent business owners** who bought a territory.

**Why this is an advantage for us:**
- Any intelligence that improves a franchisee's *decisions* multiplies by 110 without adding one headcount. That is literally Seazone's growth thesis.
- You can ship AI **as product to a network**, not as internal tooling to a team — a far more impressive, more scalable, more defensible artifact.
- Franchisees are not obligated to be excellent; they are *incentivized* to be. Incentive-aligned tooling (it makes them money) gets adopted; mandate-based tooling doesn't. Design for pull, not push.
- **No competitor's AI roadmap addresses a franchise topology.** Guesty and Hostaway built copilots for a single manager looking at their own portfolio. Nobody built the *franchisor's* copilot — the one that has to keep 110 semi-autonomous operators consistent.

**Corollary risk that becomes the opportunity:** Seazone's brand promise is standardization; its operating structure is decentralization. Every quality complaint lives in that gap.

---

### N2 — The digital/local boundary is written into the contract `[F]`
"Seazone cuida de tudo que escala. Você cuida do que acontece no local."

You do not have to argue that guest messaging, pricing, listing quality, financial settlement, and tax should be centralized and automated. **Seazone already sells that as the value proposition of the franchise.** Any AI you place on the digital side is, by definition, in-scope, non-threatening, and consistent with existing contracts. This removes the #1 objection hackathon proposals face ("who would actually own this?").

---

### N3 — Seazone creates supply, it doesn't only manage it (SPOT) `[F]`
Seazone picks the land, structures the development, audits construction, sells to investor pools, furnishes, and then operates. 44 SPOTs, R$723M raised, 100+ developer partnerships.

**Why this matters:** a demand model built for one purpose gets a second, higher-value life. Occupancy/ADR forecasting isn't just a pricing input — it's an **underwriting input** for a real-estate development pipeline. A model that improves forecast accuracy by a few points is worth basis points on hundreds of millions of VGV. Almost no competitor can convert an operations model into an underwriting model, because they don't own the development vertical.

---

### N4 — They already own the scarce asset: first-party demand data at national spread `[F]`
1,000,000+ nights sold, 70,000+ reviews, 60+ destinations, 15 states, 8 years, across beach / mountain / capital / events markets. Sirius already prices on demand, seasonality, events, competition, and occupancy history.

**The strategic implication is inverted from what teams usually assume:** because the *structured* data is already well-exploited by Sirius, the remaining alpha is in the **unstructured** data — guest messages, review free-text, franchisee WhatsApp traffic, maintenance notes and photos, owner calls, condominium conventions, contracts, assembly minutes. That is exactly the data class where LLMs are non-substitutable and where deterministic code genuinely cannot compete. **This is how you avoid building an "AI wrapper": go where the data has no schema.**

---

### N5 — The owner is an *investor*, not a landlord `[F]`
The company's public language is CDI comparison, IRR, "13% to 23% p.a.", "the property as a financial asset", VGV. The owner's mental model is portfolio return.

**Design consequence:** anything owner-facing must speak asset performance, opportunity cost, and tax — not hospitality. An owner-facing feature framed as "your guests were happy" underperforms one framed as "your unit returned 0.71%/month vs a 0.58% comparable-set median, and here is the R$ figure you left on the table." This is a cheap, high-signal way to look like you understand the business.

---

### N6 — Airbnb dependency is simultaneously the moat and the exposure `[F]`
Seazone positions itself as Airbnb's largest revenue partner in Brazil and the country's largest Superhost-badged network. Meanwhile Airbnb is rebuilding itself as AI-native: AI search in test with a natural-language toggle, AI-generated listing highlights, review synthesis, personalization that segregates homes from hotels, ~45% of support inquiries resolved without a human, support cost per booking down 16%, ~60% of code AI-written, concept-to-launch time cut 60% (Q1/Q2 2026 earnings; TechCrunch, CNBC, Skift).

**The opening:** when discovery becomes conversational and retrieval-based rather than filter-based, **what makes a listing win impressions changes.** Structured, complete, semantically rich, factually verifiable listing content becomes a ranking asset. Nobody in Brazil is systematically optimizing 2,900 listings for LLM-mediated retrieval. There is a real, timely, growth-side product here (see Solution D).

---

### N7 — Brutal, geographically heterogeneous seasonality `[F]`
Jurerê, Rosa, Urubici, Trancoso, Japaratinga, Bonito, Foz do Iguaçu, Gramado, Campos do Jordão, plus capitals. Réveillon and Carnaval peaks against dead midweeks in low season; mountain destinations invert against beach destinations.

**Advantage:** orphan nights, gap nights, staffing surges, laundry throughput, and cleaner scheduling are *concrete, quantifiable, seasonal* problems with clean success metrics. Hostaway's CoHost specifically markets orphan-night filling — proof the problem is real and monetizable. And Seazone's geographic mix means a cross-destination model has something Charlie (SP/RJ/POA/BH) and Housi structurally lack.

---

### N8 — A regulatory shock is landing **right now**, and it hits Seazone's exact cohort `[F]`
STJ, 7 May 2026 (REsp 2.121.055/MG, 5–4): habitual, professional short-stay exploitation in a residentially-designated condominium requires a **two-thirds** vote to change the building's designated use. Decreto 12.955/2026 (published 30 Apr 2026, regulating LC 214/2025): rentals of ≤90 days are taxed under hotel-service rules when the supplier is a regular CBS taxpayer, with thresholds around >3 properties and revenue limits (R$240k, immediate at 120% = R$288k), plus NFS-e obligations; 2026 is a 1% test year, phase-in 2027–2032, full effect 2033.

**Why this is an advantage:** it is (a) extremely recent, (b) genuinely scary to owners, (c) unsolved by any vendor, (d) a *document-and-reasoning* problem — the single best fit for LLMs — and (e) it lands on Seazone's supply funnel. A team that walks into the room already fluent in the STJ ruling and Decreto 12.955 is instantly credible with a director, because it is a live board-level topic in August 2026.

---

### N9 — The franchise is the internationalization vehicle `[F]`
The CEO has stated the intent to expand to Argentina, Uruguay, and Chile, funded by a Series A. The franchise model is what makes that possible without physical infrastructure per city.

**Consequence:** any solution that reduces **time-to-productivity for a new franchisee** is directly an internationalization enabler. That is a much bigger strategic claim than "improves efficiency," and it is the claim a director will care about. Frame accordingly: *"this is what makes the 300th franchisee as good as the 10th, in a country where we've never operated."*

---

### N10 — Distribution to the network is already solved `[F]`
The franchise network is reachable *today* via WhatsApp, a proprietary platform every franchisee already logs into, annual in-person gatherings, and a continuous training program. There is no enterprise rollout problem, no procurement, no change-management committee.

**Consequence:** you can honestly claim a 2-week pilot path with 5 franchisees. Most hackathon proposals cannot claim a credible deployment path at all. This one is free.

---

### N11 — Lean central team, modern-but-modest stack `[I]`
Next.js, Supabase, WordPress, InHire, RD Station, WhatsApp-first, PJ contracts, remote-first, 100% growth on ~R$42M revenue. This is not an enterprise with a platform team waiting to absorb your architecture.

**Consequence:** they will reward a solution that is **small, cheap, and shippable by two people** far more than one requiring a data platform migration. Explicitly say: "this runs on your existing Supabase, adds two tables and one worker, and costs under R$300/month at full network scale." That sentence wins more points than any model choice.

---

### N12 — Their own hiring thesis tells you the shape of the answer `[F]`
The 2026 trainee program rotates people through **Operations & CX, Commercial & Partnerships, Marketing & Branding, Finance & Strategy, Data/Tech & Platforms, Expansion & Investments, Projects & Launches** — and asks them to build "dashboards, agents, automations and analyses from scratch," under the labels **AI Builder** and **AI Orchestrator**.

**Read it as a spec.** Seazone's theory of AI is *not* "the engineering team ships AI features." It is "**every business area gets an operator who can build agents against company data.**" A solution shaped like a *reusable capability any of the seven areas could adopt* matches their organizational theory far better than a single-purpose feature. Say this out loud in the presentation.

---

## 7. Trainee Program Intelligence & Evaluation Model

### 7.1 The program `[F]` (EstágioTrainee.com, published 3 Aug 2026, updated 10 Aug 2026)
- Built **around AI as the primary work tool**; explicitly "prepared to *build* solutions with the technology, not merely operate it."
- Deliverable language: "turn a business problem into concrete deliverables — **dashboards, agents, automations and analyses built from scratch and put into operation on your own.**"
- Market framing: **AI Builder / AI Orchestrator**.
- 6 months, rotation through up to 3 of 7 areas, real projects, company data, direct contact with leadership.
- Terms: PJ, R$5,000/month + R$462 meal benefit, remote, coworking available in Florianópolis, possibility of effectivation into a strategic position.

### 7.2 Selection funnel `[F]`
1. Application + **logic challenge**
2. **Video** — "what you have already built and your experience with AI"
3. Seazone institutional presentation
4. **HACKATHON — "a empresa avaliará seu uso de IA na prática"** ← you are here
5. People interview
6. **Final interview with the Board**

### 7.3 What the hackathon is actually testing `[I]`
The stage is explicitly described as evaluating **your use of AI in practice**. Combine that with the required profile (engineering/math/stats, daily AI use, clear logical communication, analytical and data-oriented, organization, prioritization, proactivity, critical judgment) and the inferred rubric is roughly:

| Dimension | What they're looking for | How you show it |
|---|---|---|
| **AI craft** | Do you use AI deliberately, or do you paste prompts and hope? | Show your eval set, your model-routing decisions, your cost log, where you chose *not* to use an LLM |
| **Business translation** | Can you convert a fuzzy business problem into a scoped deliverable? | One-sentence problem statement, one metric, one workflow |
| **Autonomy** | Did you build and *operate* it yourself? | Live, working demo — not slides |
| **Judgment / prioritization** | Did you cut the right things? | An explicit "what we did not build and why" slide |
| **Communication** | Clear, logical, objective | Problem → evidence → mechanism → number → next step. No adjectives. |
| **Seazone fit** | Do you understand *this* business? | Franchise economics, Sirius, SPOT, STJ/Decreto — by name |

**The trap:** treating "they evaluate AI usage" as "use as much AI as possible." The mature signal is the opposite — **demonstrating you know when a rule beats a model.** A slide that says "we replaced 6 of our 9 planned LLM calls with deterministic logic and cut cost 94% with no accuracy loss" is worth more than any model choice. See §26.

---

## 8. Hackathon Challenge Pre-Analysis & Pivot Matrix

The official prompt is not yet available. When it arrives, run this in order:

**Step 1 — Decompose:** explicit objective · hidden objective · business problem · problem owner · desired outcome · hard constraints · what would look impressive · what would be commercially valuable · what is technically feasible in the time · what would be unrealistic · what the *wording* reveals about current priorities.

**Step 2 — Translate into one sentence:**
> "Seazone needs to ______ because ______, which affects ______, and the opportunity is to ______."

**Step 3 — Generate ≥3 readings of the prompt before committing.** Vague prompts ("use AI to help Seazone grow") are traps — the interpretation *is* the deliverable, and stating your interpretation explicitly on slide 2 is itself a scored behavior.

**Step 4 — Pivot matrix.** The architecture in §18 (ingest → normalize → deterministic score → LLM enrichment → agent action → console) is deliberately problem-agnostic. Reuse the skeleton; swap the domain:

| If the prompt centers on… | Pivot to | Reuse from FAROL |
|---|---|---|
| Operations / customer experience | **FAROL as-is** | 100% |
| Growth / commercial / lead gen | Franchisee **supply-capture** agent: score property leads in territory, auto-draft owner outreach, predict conversion | Ingest + scoring + action feed |
| Expansion / investment / new markets | **Territory & SPOT underwriting agent**: city/neighborhood viability with a regulatory-risk layer | Scoring engine + external data ingest |
| Finance / strategy | **CBS/IBS exposure + owner P&L agent** | Document reasoning + console |
| Marketing / branding | **AI-era listing intelligence**: optimize 2,900 listings for conversational retrieval | LLM enrichment + eval harness |
| Data / technology / platforms | FAROL framed as **the reusable agent layer** over Seazone's data | 100%, reframed |
| Fully open / "surprise us" | **FAROL** | 100% |

**Step 5 — Non-negotiables regardless of prompt:** one workflow, end-to-end, working live · a number attached to it · a named user · an honest data-provenance label · a fallback demo path.

---

## 9. Strategic Priorities (what Seazone appears to be optimizing for right now)

1. **Supply growth without linear cost** — franchise recruitment is running a sophisticated funnel with 2026 territory scarcity messaging. `[F]`
2. **Quality consistency at network scale** — the CCO's own framing ("guardian of the experience") plus continuous training and annual gatherings. `[F]`
3. **Development pipeline (SPOT)** — 44 launched, 16 cities, R$723M raised; developer partnerships at 100+. `[F]`
4. **Data-led geographic expansion** — proprietary database, hundreds of variables, explicit rejection of intuition. `[F]`
5. **Regulatory protagonism** — the CEO positions Seazone as a shaper of STR regulation, participating in ABLT sector discussions. `[F]`
6. **AI capability inside the business functions, not just in engineering** — the trainee program is the proof. `[F]`
7. **International expansion via franchise**, Series A funded. `[F]` / timing `[H]`

---

## 10. Current Pain Points (evidence-based)

### 10.1 Quality variance across the network `[F]` + `[I]`
Reclame Aqui, period 01/01/2026–30/06/2026: reputation **"Regular," 6.8/10**, **102 complaints**, 100% answered, **65.7% resolved**, consumer score **5.7**, **53.7%** would do business again, **average response time 2 days 16 hours**.

Recurring themes across public complaints:
- **Listing-vs-reality mismatch** (a guest reporting a "giant smart TV" in the listing that was a small TV in the unit; the response — "listing images are illustrative" — escalated to Airbnb, who confirmed a policy violation).
- **Payout delays and opacity** to owners; one company reply attributes a delay to "a financial error" plus "communication breakdown due to ticket overload on Friday and a temporary reduction in the team."
- **Property damage and guest screening** ("rents regardless of profile"; damage to doors, paint, walls; unresolved at contract termination).
- **Check-in friction** and incorrect information at arrival.

**Interpretation `[I]`:** a 4.8/5 average across 70,000+ reviews with a 6.8/10 complaint-channel reputation is the classic **variance signature** — the median stay is good, the tail is bad, and the tail is where owner churn, refunds, and ranking damage live. In a franchise topology, the tail is not random: it concentrates in specific franchisees, specific properties, and specific weeks (peak season overload).

### 10.2 Peak-season operational overload `[I]`
The company's own complaint response cites Friday ticket overload and reduced staffing. Seasonality is extreme and geographically synchronized (everyone's peak is the same week).

### 10.3 Owner trust and retention `[F]`
Payout friction, damage disputes, and unresponsiveness in the public record. In a business where supply is the constraint, **an owner lost is worse than a guest lost** — it's a recurring revenue annuity leaving.

### 10.4 Onboarding new franchisees `[I]`
"On average franchisees reach 20+ properties in the first 6 months" — meaning the ramp is measured in months, not weeks. Multiply by international expansion and this becomes the growth ceiling.

### 10.5 Tacit knowledge is trapped in individuals `[H]`
110 franchisees each hold local knowledge (which cleaner is reliable in Trancoso, which condo síndico blocks check-ins after 22h, which building has a broken elevator every January). None of it is in a queryable system. It exits with the franchisee.

### 10.6 Data fragmentation across surfaces `[I]`
Property counts, city counts, and owner counts disagree across Seazone's own web properties. Small symptom, real cause: no single source of truth spanning marketing, operations, and finance.

### 10.7 Regulatory exposure at property level `[F]`
See §11. Post-STJ, the legality of a given unit depends on a **document Seazone probably does not systematically hold** — the condominium convention and assembly minutes for each building.

---

## 11. The 2026 Regulatory Shock

| Event | Date | Substance | Impact on Seazone |
|---|---|---|---|
| **STJ, 2ª Seção, REsp 2.121.055/MG** | 7 May 2026 | 5–4: habitual, professional short-stay in residentially-designated condominiums requires a **2/3 vote** to change designated use (Art. 1.351, Civil Code). Rapporteur: Min. Nancy Andrighi. Characterized as an "atypical hospitality contract," not ordinary tenancy. Not a binding repetitive precedent, but consolidates both private-law panels; appeal still possible. | **Every new property in a residential condominium now carries legal risk at onboarding.** The default flipped: silence in the convention now cuts against the operator. |
| **Decreto 12.955/2026** | Published 30 Apr 2026 (regulating LC 214/2025) | Art. 410: rental/onerous transfer of residential property for ≤90 uninterrupted days is taxed under **hotel-service rules** where the supplier is a regular CBS taxpayer. Thresholds around **more than 3 properties** for temporada plus revenue limits (R$240k; immediate at 120% = R$288k). NFS-e obligation. 2026 = symbolic 1% test year; 2027–2032 progressive substitution of PIS/COFINS/ISS by CBS/IBS; full effect 2033. | **Seazone's owner base is the affected cohort by definition.** Owners will ask "what happens to my return in 2028?" and today nobody can answer per-owner. |
| **São Paulo municipal action + Airbnb enforcement** | 2026 | HIS/HMP (public housing program) units restricted from short-stay platforms; Airbnb actively monitoring. | Property-eligibility screening becomes a real operational requirement. |

**Strategic read `[I]`:** this is a **professionalization forcing function**. Amateur hosts get squeezed; professional operators who can absorb compliance complexity gain share. Seazone is on the winning side of this trend — *if* it can turn compliance from a cost into a product. That is a genuine, defensible strategic insight to open a presentation with.

---

## 12. Competitor Intelligence

### 12.1 Brazilian direct competitors

| Competitor | Geography | Target user | Model | Scale (latest) | Tech / AI | What Seazone should learn |
|---|---|---|---|---|---|---|
| **Charlie (StayCharlie)** | SP, RJ, POA, BH | Investors + institutional (FIIs), developers | Whole-building operator; short/mid/long stay + hotel ops; "hybrid hospitality" | ~2,500–2,600 apartments, **70+ buildings**, 1.5–2M nights, ~R$2bn under management; target 16,000 units by 2030 | 24h digital concierge, self check-in, dynamic pricing, analytical owner dashboards, ~70% OTA / 30% direct | **Building-level density** and **FII/institutional supply**. Charlie doesn't need a franchise because it concentrates inventory. Also: 30% direct bookings is a channel-mix benchmark Seazone should measure itself against. |
| **Housi** (Vitacon spin-off) | National, platform + franchise | Developers, investors, flexible-living residents | Platform / "housing as a service"; licenses the model to buildings | ~R$20bn VGV ecosystem; international ambitions | Full-stack app, subscription living | Platform-licensing as an alternative expansion vector to franchising. |
| **HostnJoy** | 5 cities | Individual owners | Full-service management | Smaller; publishes an annual "best Airbnb manager" ranking | Pricing tech + a formidable content/SEO data machine | **They are winning the market-data narrative.** Seazone has vastly better proprietary data and publishes less of it. Cheap competitive move. |
| **B.Homy / Anfitrião Prime / Omar do Rio / WeCare** | BH / SP / RJ Zona Sul | Owners | Hyper-local specialists | Small | Modest | Local depth beats scale on trust. Seazone's franchisee *is* the answer to this — if quality holds. |
| **Casai / Nomah** | — | — | Merged 2022, **exited Brazil 2024** | Was ~3,000 units | — | **Scale without unit economics kills you.** Their owners were referred to Charlie. Cautionary tale, and evidence of consolidation opportunity. |

### 12.2 Adjacent Brazilian players
Traditional imobiliárias entering temporada; condo-hotel operators and hotel chains launching flexible products; accounting/legal services now marketing short-stay tax compliance (a whole cottage industry appeared in mid-2026 — evidence of demand for §11 solutions); Inside Airbnb / AirDNA-style data resellers.

### 12.3 Global benchmarks — and this is where the last 90 days matter

| Company | Move | Date | What it proves |
|---|---|---|---|
| **Guesty** | **Agent Hub** — coordinated AI agents across revenue management, guest communication, operations, finance, marketing, and reviews. Plus a **Model Context Protocol (MCP) server** letting external AI models connect to their PMS infrastructure. Trained on ~500k listings and a decade of STR data. Explicit framing: scale portfolio without proportional headcount. | **1 June 2026** | The category has moved from "software that helps you do work" to "software that does the work." Also: **MCP is now table stakes in this vertical.** |
| **Hostaway** | **AI CoHost** — conversational portfolio intelligence (natural-language queries over revenue, occupancy, cost, guest activity); agents that scan and synthesize reviews across OTAs into asset-quality scorecards; proactive flagging of calendar conflicts and maintenance issues; orphan-night discount recommendations; in-platform execution. 20,000+ operators. | **Jun–Jul 2026** | **Review synthesis → asset-quality scorecard is a validated pattern.** Hostaway's own report: 70.1% of vacation-rental managers now use AI tools, nearly double in six months. |
| **Airbnb** | AI search in test (natural-language toggle, visual results); AI-generated listing highlights; review synthesis; personalization segregating homes/hotels; **~45% of support inquiries resolved with no human**, support cost per booking **−16%**; ~60% of code AI-written; concept-to-launch **−60%**; features shipped **+80%**. Chesky separately funding an AI lab. | Q1–Q2 2026 | The distribution layer itself is becoming AI-native. Listing content strategy must change. Also the internal-productivity numbers are the best available benchmark for what "AI-first company" actually means quantitatively. |
| **PriceLabs / Wheelhouse / Beyond** | Dynamic pricing as a commodity utility | ongoing | Pricing is **not** a differentiator anymore. Sirius is table stakes, not a moat. |
| **AirDNA / Key Data / Inside Airbnb** | Market intelligence as a product | ongoing | Seazone's proprietary market DB could be productized — but that is a strategy discussion, not a hackathon. |
| **Vacasa / Evolve / AvantStay** | US managers; Vacasa's struggles are instructive | ongoing | **Local operational quality at scale is the hard part, not software.** Vacasa's difficulties came from field operations, not code. Directly validates the FAROL thesis. |

### 12.4 The gap
> Guesty and Hostaway built **an AI copilot for a property manager looking at their own portfolio.**
> Nobody has built **an AI copilot for a franchisor keeping 110 independent operators consistent.**
> That gap is exactly the shape of Seazone.

---

## 13. Solution Patterns Worth Adapting

| Pattern (where it works) | Why it works | Seazone equivalent | Adaptation required | Value | Complexity |
|---|---|---|---|---|---|
| **Review→scorecard agents** (Hostaway) | Turns unstructured feedback into an asset-quality signal | Per-property *and* **per-franchisee** quality score | Add the franchise dimension; Portuguese; Brazilian review idiom | High | Low |
| **Multi-agent ops hub** (Guesty) | Automates cross-team coordination | Agent layer over the proprietary platform | Must respect the digital/local contractual split | High | Medium |
| **Orphan-night filling** (Hostaway) | Recovers dead inventory | Feed candidate gaps to Sirius as recommendations | Don't override Sirius; recommend into it | Medium-High | Low |
| **AI support deflection** (Airbnb: 45%, −16% cost/booking) | Massive cost line | Guest-service deflection in PT-BR with escalation to franchisee | Escalation must route to the *right* franchisee | High | Medium |
| **MCP server** (Guesty) | Lets any AI client reach your data safely | Expose Seazone data to internal agents via MCP | Auth + scoping | Strategic | Medium |
| **Conversational portfolio queries** (Hostaway CoHost) | Removes the analyst bottleneck | "Which properties in Floripa are at risk this weekend?" | Text-to-SQL with a constrained schema + guardrails | High | Medium |
| **Building-level density** (Charlie) | Cuts cost-to-serve dramatically | Already Seazone's SPOT thesis | — | — | — |
| **Content-as-market-authority** (HostnJoy) | Cheap inbound supply acquisition | Publish from the proprietary DB | Editorial process | Medium | Low |
| **Compliance-as-a-product** (nobody yet) | Converts fear into retention | Condo-convention + CBS exposure screening | Legal review; framed as decision support | **High + unique** | Medium |

**Classification of the ideas above:**
- *Already exists at Seazone:* dynamic pricing, channel parity, city-level demand scoring, payout ledger, scraping.
- *Exists but improvable:* market DB (no regulatory/condo layer), owner reporting (not investor-grade), franchisee training (static, not situational).
- *Exists elsewhere, adaptable:* review→scorecard, orphan nights, support deflection, conversational analytics.
- *New opportunity:* **franchise-network quality intelligence**, **regulatory/compliance screening**, **AI-era listing optimization**.
- *Strategically irrelevant for a hackathon:* consumer social features, blockchain-anything, a new booking marketplace.
- *Technically unrealistic here:* computer-vision damage assessment trained from scratch, an IoT deployment, anything needing production write-access to Seazone systems.

---

## 14. Problem Opportunity Map

Scored 1–5 on Impact × Frequency × Strategic relevance × Feasibility × Differentiation.

| # | Problem | Who | I | F | S | Fe | D | Total |
|---|---|---|---|---|---|---|---|---|
| **P1** | Quality variance across a franchise network Seazone doesn't employ | Guest, owner, HQ | 5 | 5 | 5 | 4 | 5 | **24** |
| **P2** | Owner churn from trust/transparency/performance gaps | Owner, HQ | 5 | 4 | 5 | 4 | 4 | **22** |
| **P3** | Post-STJ / post-Decreto regulatory uncertainty per property and per owner | Owner, legal, expansion | 5 | 4 | 5 | 4 | 5 | **23** |
| **P4** | New-franchisee ramp time (months) blocks national + LatAm expansion | Franchisee, expansion | 4 | 4 | 5 | 4 | 4 | **21** |
| **P5** | Peak-season ops overload → slow responses, bad reviews | Guest, franchisee | 4 | 5 | 4 | 4 | 3 | **20** |
| **P6** | Listings not optimized for AI-mediated discovery | Growth, guest | 4 | 4 | 4 | 5 | 4 | **21** |
| **P7** | Tacit local knowledge trapped in individual franchisees | Franchisee, HQ | 3 | 5 | 4 | 4 | 4 | **20** |
| **P8** | SPOT/territory underwriting could be sharper (regulatory blind spot) | Expansion, investors | 5 | 2 | 5 | 3 | 4 | **19** |
| **P9** | Guest support volume and cost | Guest, HQ | 4 | 5 | 3 | 4 | 2 | **18** |
| **P10** | Orphan/gap nights left unsold | Owner, HQ | 3 | 5 | 3 | 4 | 2 | **17** |
| **P11** | Data fragmentation / no single source of truth | Everyone | 3 | 5 | 3 | 2 | 2 | **15** |
| **P12** | Damage & guest-screening disputes | Owner, franchisee | 4 | 3 | 3 | 2 | 3 | **15** |

**Top cluster: P1, P3, P2, P4, P6.** Note that P1 and P4 are the same underlying phenomenon at different time horizons (network consistency), and P2 is largely *downstream* of P1. That clustering is what makes a single solution able to move three problems at once.

---

## 15. Candidate Solutions & Scoring Matrix

### The five finalists

**A — FAROL: Franchise Network Quality & Revenue Copilot**
Ingests guest messages, reviews, ops events and property state → computes a per-property **Risk Score** predicting a sub-4.5 review or an owner-visible failure *before* it happens → pushes a ranked 3-item daily action list to each franchisee via WhatsApp-style feed → HQ gets a network console ranking franchisees, properties, and cities by risk and by revenue at stake. Includes a supply-capture module (rank owner leads in territory, draft outreach).

**B — ALICERCE: Regulatory & Tax Intelligence Copilot**
Upload a condominium convention + assembly minutes → agent extracts designated use, restrictions, quorum clauses → returns a **legality verdict with cited clauses** and required next action (assembly? already permitted? blocked?). Second module: per-owner CBS/IBS exposure simulation across 2026–2033 given portfolio size and revenue.

**C — BÚSSOLA: Territory & SPOT Underwriting Agent**
City/neighborhood/parcel scoring for franchise territory and SPOT viability, layering public demand data, seasonality, competitive saturation, and — the differentiator — a **regulatory risk layer** (municipal rules, condo-stock characteristics, STJ exposure).

**D — VITRINE: AI-Era Listing Intelligence**
Rewrites and structures 2,900 listings for conversational/LLM-mediated retrieval; generates a per-property knowledge base; predicts which listings will lose impression share as Airbnb's AI search rolls out; A/B measurable.

**E — MARÉ: Guest Support Deflection Agent**
PT-BR guest agent handling the top intents, with intelligent escalation routing to the correct franchisee, benchmarked against Airbnb's 45% deflection / −16% cost-per-booking.

### Scoring (1–10)

| Criterion | A · FAROL | B · ALICERCE | C · BÚSSOLA | D · VITRINE | E · MARÉ |
|---|---|---|---|---|---|
| Prompt alignment (est.) | 9 | 8 | 7 | 7 | 7 |
| Realness of problem | 10 | 9 | 7 | 7 | 8 |
| Business impact | 9 | 8 | 9 | 7 | 7 |
| Seazone strategic fit | **10** | 9 | 8 | 7 | 6 |
| User value | 9 | 9 | 7 | 6 | 8 |
| Differentiation vs competitors | **10** | **10** | 7 | 8 | 4 |
| Competitive advantage / defensibility | 9 | 8 | 8 | 6 | 4 |
| Technical feasibility in-window | 8 | 8 | 6 | 9 | 7 |
| Speed to MVP | 8 | 9 | 6 | 9 | 7 |
| Data availability (public/synthetic) | 8 | 9 | 7 | 9 | 7 |
| Scalability | 10 | 8 | 8 | 8 | 8 |
| **Demonstrability** | **10** | 9 | 6 | 7 | 6 |
| Cost efficiency | 9 | 9 | 7 | 8 | 6 |
| Commercialization potential | 9 | 9 | 7 | 6 | 5 |
| **TOTAL (/140)** | **128** | **122** | **100** | **104** | **90** |

---

## 16. Recommended Solution: FAROL

> **FAROL** — *Farol* = lighthouse. On-brand for a company named after the sea, and the right metaphor: it doesn't steer the ship, it tells 110 captains where the rocks are.
> Backronym for the deck: **F**ranchise **A**dvisory & **R**evenue **O**perations **L**ayer.

### 16.1 The problem statement
> **Seazone needs to make its 110+ independent franchisees perform as consistently as employees — because the franchise model is simultaneously the engine of 100%/year growth and the source of the quality variance visible in a 6.8/10 complaint reputation sitting under a 4.8/5 review average — which affects guests (bad stays), owners (churn of the supply that *is* the business), and Seazone (ranking, refunds, brand) — and the opportunity is to turn the unstructured operational exhaust the network already produces into a per-property risk signal that reaches the right franchisee *before* the failure, and reaches HQ as a network scorecard.**

### 16.2 Why this and not the others
- **It is the only idea that is impossible to copy without Seazone's structure.** Guesty and Hostaway serve managers, not franchisors. Charlie and Housi have no franchise network to keep consistent. A competitor cannot buy this off the shelf.
- **It sits exactly on the contractual digital side** (N2) — no organizational fight.
- **It uses AI where AI is non-substitutable** (N4): free-text messages, reviews, ops notes. The numeric layer stays deterministic, which is itself the credibility signal.
- **It compounds across three of the top-five problems** (P1 quality, P2 owner churn, P4 franchisee ramp) and touches P5 and P7.
- **It is a growth story, not only an efficiency story:** review score → OTA ranking → impression share → occupancy → GMV; plus the supply-capture module → more properties per franchisee → more GMV per territory.
- **It demos in 90 seconds** and the demo is emotionally legible: a property lights up red, a franchisee gets a message, the failure doesn't happen.
- **It is the internationalization argument** (N9): "this is what makes the 300th franchisee as good as the 10th, in a country where we've never operated."

### 16.3 Honest self-critique
- Predictive labels require historical outcome data Seazone has but we don't → we build with clearly-labeled synthetic data and ship an **eval harness** so the model's quality is measurable, not asserted. *Measurable-but-synthetic beats impressive-but-unfalsifiable.*
- Franchisees are independent operators; adoption is not guaranteed by mandate → design for pull (it shows them **R$ at stake**, not tasks), and say so.
- Risk of being read as "a dashboard" → the deliverable is not a dashboard; it is **a decision that arrives at the right person before the failure.** Say this sentence in the presentation.

---

## 17. MVP Definition & User Journey

### 17.1 Scope — one workflow, three surfaces

**IN SCOPE**
1. Ingest a stream of property-level events: guest messages, reviews, cleaning/maintenance events, booking calendar, response times.
2. **Signal extraction** (LLM, small model, structured output): from each free-text item, extract `issue_type`, `severity`, `sentiment`, `is_actionable`, `blame_layer` (property / franchisee / HQ / guest), `evidence_span`.
3. **Risk scoring** (deterministic): combine extracted signals with numeric features (response latency, days since last deep clean, review trend slope, upcoming high-value booking, seasonality) into a 0–100 score with a transparent, inspectable formula.
4. **Franchisee action feed**: top 3 actions today, each with a one-line rationale, the **R$ at stake**, and a done/snooze control.
5. **HQ network console**: properties, franchisees, and cities ranked by risk; revenue-at-risk aggregate; drill-down to the evidence that produced any score.
6. **Eval harness**: labeled sample, precision/recall/F1 per extraction field, shown live.

**EXPLICITLY OUT OF SCOPE** (put this on a slide — it scores points)
Pricing (Sirius owns it) · channel management · payments/settlement · a mobile app · authentication beyond a demo login · full guest-support automation · computer vision · any write-back to real Seazone systems.

### 17.2 User journey
```
Sunday 18:04 — Property FLN-214 (Jurerê) accumulates signal:
  · guest message: "the AC in the bedroom is making noise" (low severity, unresolved 19h)
  · last two reviews mention cleaning of the same bathroom
  · a 6-night R$4,200 booking checks in Friday
  · franchisee median response time this week: 4h12 (network median: 1h40)
        ↓
FAROL scores FLN-214 at 78/100 · revenue at risk R$4,200 + estimated ranking impact
        ↓
Franchisee Sandra opens the feed. Item #1:
  "FLN-214 — fix the bedroom AC before Friday. Two reviews already flagged
   the bathroom; a R$4,200 stay checks in in 5 days. Recurrence pattern:
   3 similar complaints in 60 days."   [Done] [Snooze] [Not relevant]
        ↓
Sandra dispatches the technician Tuesday.
        ↓
Friday's stay ends at 5 stars. HQ console: Florianópolis risk index down;
  Sandra's consistency score up; the "Not relevant" clicks flow back
  into the eval set as new labels.
```

**Primary user:** the franchisee. **Secondary:** HQ Operations & CX. **Job-to-be-done:** "tell me the one thing that will cost me money this week, before it costs me money." **Main action:** resolve item #1. **Output:** a ranked action + evidence + R$. **Feedback loop:** every Done / Not relevant is a training label. **Success metric:** % of high-risk properties whose next review lands ≥4.5.

---

## 18. Technical Architecture

Deliberately boring. Boring is the point.

```
┌──────────────────────────────────────────────────────────────┐
│  SOURCES (synthetic for demo, real in production)            │
│  guest messages · reviews · ops events · calendar · property │
└───────────────┬──────────────────────────────────────────────┘
                ↓  batch loader (Python)
┌──────────────────────────────────────────────────────────────┐
│  NORMALIZE — one events table, one properties table          │
│  Supabase / Postgres (matches Seazone's existing stack)      │
└───────────────┬──────────────────────────────────────────────┘
                ↓
┌───────────────────────────┐   ┌──────────────────────────────┐
│  DETERMINISTIC FEATURES   │   │  LLM EXTRACTION (small model)│
│  response latency         │   │  structured output, batched, │
│  review trend slope       │   │  cached by content hash      │
│  days since deep clean    │   │  → issue_type, severity,     │
│  upcoming booking value   │   │    sentiment, blame_layer,   │
│  seasonality index        │   │    evidence_span             │
│  → NO LLM CALLS HERE      │   └───────────────┬──────────────┘
└───────────────┬───────────┘                   │
                └──────────────┬────────────────┘
                               ↓
┌──────────────────────────────────────────────────────────────┐
│  RISK ENGINE — transparent weighted score (pure Python)      │
│  every score is explainable by listing its contributing terms│
└───────────────┬──────────────────────────────────────────────┘
                ↓
┌──────────────────────────────────────────────────────────────┐
│  BRIEFING AGENT (larger model, 1 call per franchisee per day)│
│  turns the top-3 scored items into natural PT-BR guidance    │
│  with tool access: get_property, get_history, get_similar    │
└───────────────┬──────────────────────────────────────────────┘
                ↓
┌───────────────────────────┐  ┌───────────────────────────────┐
│  Franchisee feed (web)    │  │  HQ console (web)             │
│  Next.js + Tailwind       │  │  network / city / franchisee  │
└───────────────────────────┘  └───────────────────────────────┘
                ↓
┌──────────────────────────────────────────────────────────────┐
│  EVAL HARNESS — labeled set, P/R/F1 per field, shown live    │
└──────────────────────────────────────────────────────────────┘
```

**Choices and why:**
- **Supabase/Postgres** — Seazone demonstrably already uses Supabase. Say this in the demo; it is a 5-second credibility win.
- **Next.js + Tailwind** — matches their front-end stack.
- **Python worker** — batch/offline; nothing real-time is needed.
- **Two-tier model routing** — cheap model for high-volume extraction, capable model for the once-daily narrative. Justify the split explicitly.
- **No vector DB** — a Postgres table with `pgvector` or even cached numpy arrays is enough at 2,900 properties. Adding Pinecone would be a red flag, not a green one.
- **No fine-tuning** — few-shot + structured outputs + a good eval set beats fine-tuning at this scale and in this timebox.
- **MCP note for the deck:** Guesty shipped an MCP server in June 2026. Mention that FAROL's data layer should be exposed via MCP so *any* of the seven Seazone business areas can query it with their own agents. This connects your build directly to N12 and shows you're reading the category, not just the company.

---

## 19. Data Strategy

**Everything must be labeled. Never let a synthetic number look real.** Put this legend on the data slide:

| Layer | What | Label |
|---|---|---|
| Company scale, franchise economics, Sirius, SPOT counts | From Seazone's own public pages and press | **REAL — PUBLIC** |
| Reclame Aqui complaint statistics and themes | Public complaint channel, H1 2026 | **REAL — PUBLIC** |
| STJ ruling, Decreto 12.955/2026 | Primary legal sources | **REAL — PUBLIC** |
| Airbnb / Guesty / Hostaway benchmarks | Company earnings + trade press | **REAL — PUBLIC** |
| Seasonality curves, city ADR ranges | Public market data + FipeZap | **REAL — PUBLIC (approximate)** |
| Guest messages, ops events, per-property histories | Generated by us | **SYNTHETIC — clearly marked in the UI** |
| Franchisee names and territories | Fictional | **SYNTHETIC** |
| Seazone internal systems (Sirius outputs, Wallet) | Simulated interface only | **MOCK** |

**Real data required in production:** message logs, review corpus, ops events, calendar, payout records, franchisee CRM, property attributes. All of it exists inside Seazone already — that is the credibility of the pitch: *"we mocked the data, not the mechanism; you already have the data."*

**Synthetic data design principle:** generate from *realistic distributions*, not from vibes. Sample issue types from the public complaint taxonomy in §10.1; sample response latencies from a long-tailed distribution; make ~8% of franchisees systematically worse (that's what makes the network console meaningful); inject seasonality that matches Brazilian holidays. A judge who has run this business will instantly recognize whether your synthetic data looks like their reality.

---

## 20. AI Strategy (organizational, not just technical)

Seazone's stated theory of AI — from its own trainee program — is **"AI Builders and Orchestrators embedded in seven business areas."** Your AI strategy slide should reflect *that*, not a model-vendor comparison.

### The three layers of AI at Seazone

**Layer 1 — AI as substitution (do the same work, cheaper).**
Support deflection, listing copy, review replies, document summarization. Benchmark: Airbnb resolves ~45% of inquiries with no human and cut support cost per booking 16%. Real, measurable, and mostly a commodity now.

**Layer 2 — AI as perception (see things you couldn't see before).** ← *FAROL lives here*
Unstructured operational exhaust becomes a structured, queryable signal. This is where the durable advantage is, because the input data is proprietary and the schema doesn't exist yet.

**Layer 3 — AI as leverage (make each person capable of more).**
Agents that let a franchisee run 40 properties instead of 25, or let one analyst underwrite four cities instead of one. This is the layer that turns into international expansion.

### Where AI should *not* go at Seazone
- **Not into pricing.** Sirius exists; the numeric problem is well-posed; an LLM adds nothing but variance and cost.
- **Not into anything irreversible without a human.** Payouts, contract terms, legal opinions, guest refunds.
- **Not into legal conclusions.** ALICERCE-type features must be framed as *decision support with cited clauses*, never as legal advice.
- **Not into replacing the franchisee.** The physical presence *is* the product. AI augments the guardian of the experience; it doesn't replace them. Saying this explicitly signals judgment.

---

## 21. Credit & Cost Optimization

Assume tight credits. Design as if you'll run out — because if you do during the demo, the demo must not notice.

### The ten rules, applied
1. **Don't call an LLM when code will do.** Response latency, review trend, days since clean, booking value, seasonality — all pure arithmetic. *We removed 6 of 9 planned LLM calls this way.*
2. **Never re-extract the same text.** Cache by SHA-256 of content → extraction result. Re-runs cost zero.
3. **Batch.** 20 messages per extraction call with structured output, not 20 calls.
4. **Small model for extraction, capable model for narrative.** Classification/extraction is not where reasoning capability pays.
5. **Prompt caching** on the long system/context block shared across all extraction calls.
6. **Precompute everything before the demo.** The presentation reads from cache by default.
7. **Minimize context.** Send the message and 3 fields, not the property's whole history. Retrieval, not stuffing.
8. **No web calls in the demo path.** All external data frozen to a local snapshot.
9. **Graceful degradation:** LLM unavailable → risk engine still produces scores from deterministic features alone, and the UI shows a small "rules-only mode" badge. *Showing this deliberately is a strength, not a weakness.*
10. **Demo-safe by construction:** every screen renders from the cache; live mode is a toggle you control.

### Estimated consumption

| Component | Volume | Model tier | Est. cost |
|---|---|---|---|
| Extraction over the synthetic corpus (~1,500 items, batched 20×) | ~75 calls | small | < US$1 |
| Daily briefings (8 demo franchisees × 3 days) | 24 calls | capable | ~US$1.50 |
| Eval runs (3 iterations × 100 labeled items) | ~15 calls | small | < US$0.50 |
| Dev-time experimentation | — | mixed | ~US$2 |
| **Total** | | | **≈ US$5** |

**Production projection to put on the slide:** 2,900 properties × ~4 text events/day, batched and cached → roughly **R$250–400/month** in inference at full network scale. Compare against a single avoided one-star review. This ratio is the strongest slide in the cost section.

---

## 22. Demo Reliability Plan

| Path | Trigger | Behavior |
|---|---|---|
| **Happy** | Everything works | Live extraction on a fresh message you paste in during the demo → score updates → briefing regenerates |
| **Fallback 1** | API slow or erroring | Auto-serve the precomputed cache; UI badge: "cached". Timing so tight it's invisible. |
| **Fallback 2** | No network at all | Full local mode: SQLite snapshot, all screens functional, LLM outputs from cache |
| **Fallback 3** | Machine dies | Recorded 90-second screen capture on a phone + the slide deck as PDF on a second device |

**Pre-demo checklist**
- [ ] Full flow rehearsed 3× end-to-end
- [ ] Airplane-mode test passed
- [ ] Every synthetic surface labeled in the UI
- [ ] Unfinished features **deleted**, not hidden behind disabled buttons
- [ ] Remaining credits confirmed
- [ ] Eval numbers regenerated and current
- [ ] The one number you want remembered is on screen at the end
- [ ] Cost log exported and ready to show

---

## 23. Business Case

**Stated assumptions** (put these on the slide; never present a number without them):
- 2,900 properties, ADR R$450, occupancy 55% → **~R$262M annualized network GMV**
- Seazone management take: 20–25%
- Franchisee: 8% of booking + 100% cleaning fee + 2% referral bonus

| Lever | Mechanism | Conservative | Base | Upside |
|---|---|---|---|---|
| **Occupancy via rating/ranking** | Fewer sub-4.5 reviews → better OTA ranking → more impressions | +0.5 pp | +1.0 pp | +2.0 pp |
| → GMV effect | | ~R$2.4M | ~R$4.8M | ~R$9.5M |
| → Seazone net revenue | at ~22% take | ~R$0.5M | ~R$1.0M | ~R$2.1M |
| **Owner churn reduction** | Fewer visible failures → fewer terminations | −1 pp | −2 pp | −4 pp |
| → properties retained (of ~2,900) | | ~29 | ~58 | ~116 |
| → retained annual GMV | | ~R$2.6M | ~R$5.2M | ~R$10.5M |
| **Franchisee ramp** | 20+ properties in 6 months → same in 4 | — | ~2 months faster | ~3 months faster |
| → value at 110 franchisees/yr | | — | material, not modeled | — |
| **Refunds / compensation avoided** | Early intervention on predicted failures | ~R$150k | ~R$400k | ~R$800k |

**Headline for the deck:**
> **Base case: ~R$1.0M in additional net revenue and ~R$5.2M in retained GMV per year, from a system that costs under R$400/month to run.**
> Every number above is derived from publicly stated Seazone figures with the assumptions shown. Replace with internal data and the model tightens.

**Do not** claim precision you don't have. Saying "we don't know your actual churn rate; here is the sensitivity" is a *stronger* move in front of a board than a fake point estimate.

---

## 24. Go-To-Market & Moat

**First user:** 5 franchisees in Florianópolis and Salvador — the two most mature markets, one HQ-adjacent, one expansion-flagship. Choose a mix: two top performers (to validate the signal isn't noise), two median, one struggling (where the value shows).

**Beachhead:** Santa Catarina — highest property density, closest to HQ, easiest feedback loop.

**Acquisition (internal):** zero-friction — the network already has WhatsApp, a shared platform, and annual gatherings (N10). Launch at the next franchisee gathering as a benefit, not a mandate.

**Activation:** the first message a franchisee receives must contain a **R$ number attached to a specific property**. Not a task list. Money.

**Retention:** franchisees keep it if it demonstrably protects income. Show them a monthly "failures prevented / revenue protected" statement in the Wallet they already open.

**Monetization paths:**
1. Internal efficiency + revenue (immediate, and the honest primary case).
2. **Bundle into the franchise value proposition** — "our franchisees get an AI copilot" is a recruitment weapon in the 2026 territory-scarcity funnel that is already live.
3. Long-term `[H]`: productize for other franchise networks in hospitality/services in Brazil. Mention as a possibility; don't lead with it.

**Moat, in order of durability:**
1. **Proprietary labeled outcome data** — every Done / Not relevant click makes the model better. Competitors start at zero. This compounds.
2. **Structural fit** — the franchise topology no competitor shares (N1).
3. **Distribution** — 110 operators already reachable (N10).
4. **Regulatory knowledge** — a Brazil-specific compliance layer global vendors won't build.
5. Weakest: the model itself. Say so. Admitting that the model isn't the moat is exactly the judgment they're testing for.

---

## 25. Metrics & Validation

**North Star:** *% of managed properties whose most recent completed stay rated ≥4.7, weighted by revenue.*
It fuses quality (the network problem), revenue (the business), and recency (operational reality) into one number a franchisee can influence weekly.

| Tier | Metric | Why |
|---|---|---|
| **Business** | Occupancy, ADR, RevPAR, network GMV, owner churn, franchisee churn, properties per franchisee | The P&L |
| **User (franchisee)** | Feed open rate, action completion rate, median time-to-resolution, self-reported usefulness | Adoption is the real risk |
| **User (guest)** | Rating distribution (not just the mean — **the P10 tail is the whole point**), complaint rate, first-response time | Variance, not average |
| **Operational** | Predicted-failure prevention rate, false-alarm rate, revenue-at-risk protected, new-franchisee time-to-20-properties | Does the mechanism work |
| **Technical** | Extraction precision/recall/F1 per field, score calibration (Brier), p95 latency, cost per property per month, cache hit rate | Is the AI actually good |
| **Experiment** | Cohort A (FAROL) vs B (control) matched on city/season/property type over 60 days | Causal proof, not correlation |

**Validation plan for the slide:** 60-day pilot, 5 franchisees, ~120 properties, matched control cohort, one primary endpoint (share of stays ≥4.7) and one guardrail (franchisee-reported workload). Pre-register the endpoint. Saying "pre-registered" in front of an analytical board is a small phrase with a large effect.

---

## 26. How to Use AI *During* the Hackathon (this is graded)

The selection process states explicitly that this stage evaluates **your use of AI in practice**. Treat your AI usage as a **second deliverable** with its own artifact.

### 26.1 Ship an `AI_USAGE.md` in the repo
A short, honest log. Suggested structure:

```markdown
# How we used AI to build FAROL

## Decisions where AI was used
| Decision | Tool/model | What we asked | What we kept | What we rejected and why |

## Decisions where we deliberately did NOT use AI
| Decision | Why a rule/human was better |
  - risk scoring formula: needs to be auditable by a franchisee → pure Python
  - response-latency features: arithmetic → no model
  - the 6 LLM calls we removed and the 94% cost reduction that followed

## Prompt & context engineering
- structured output schemas (with the schema pasted)
- few-shot examples chosen from the failure set, not the success set
- prompt caching on the shared system block
- context minimization: what we send and what we deliberately withhold

## Evaluation
- 100 hand-labeled items, labeling protocol described
- precision/recall/F1 per extracted field, before and after each prompt revision
- the three failure modes we found and what we changed

## Cost
- total spend, per-component breakdown, projected production cost at 2,900 properties
```

**This single file is likely the highest-leverage artifact you will produce**, because it is direct evidence of exactly what the stage claims to measure — and almost nobody else will produce it.

### 26.2 Techniques to actually use (and be able to name)
- **Structured outputs / tool schemas** rather than parsing free text. Non-negotiable.
- **Model routing by task class** — cheap for extraction, capable for synthesis. Justify with a cost table.
- **Prompt caching + content-hash result caching.**
- **Few-shot from failures**, not from easy cases.
- **An eval set built before the prompt is finalized** — this is the single clearest marker of someone who has actually built with LLMs.
- **Guardrails**: confidence thresholds, abstention ("insufficient evidence"), human-in-the-loop on anything guest-facing.
- **Deterministic fallback path** when the model is unavailable.
- **AI-assisted development** — use coding agents for scaffolding, test generation, and synthetic-data generation; keep the architecture decisions human. Log which is which.

### 26.3 What to say out loud in the presentation
> "We used AI in three distinct roles: **to build** — scaffolding, tests, and synthetic data generation; **inside the product** — extraction from unstructured operational text, where deterministic code genuinely cannot substitute; and **to decide** — we ran an eval set on every prompt revision. We also removed six of our nine planned LLM calls once we realized normal code did the job better, cheaper, and auditably. Total spend to build and run this: about five dollars."

That paragraph is worth more than any feature.

### 26.4 The anti-pattern to avoid
Do not present "we asked an LLM and it said X" as evidence for anything. Do not add an agent because agents are impressive. Do not use a large model for classification. **The failure mode this stage is designed to catch is enthusiasm without judgment.**

---

## 27. Implementation Plan

Adjust the clock to the actual event length; the *order* is what matters.

| Block | Focus | Deliverable | Rule |
|---|---|---|---|
| **0–10%** | Read the prompt. Write the one-sentence problem statement. Choose the single metric. Sketch three screens on paper. | Problem statement + metric + wireframe | **No code yet.** |
| **10–25%** | Synthetic data generator with realistic distributions. Schema. Loader. | Populated DB | Data quality decides demo quality. |
| **25–35%** | Deterministic feature computation + risk engine. **Zero LLM.** | Scores exist, end to end | If the demo had to ship now, it would work. |
| **35–50%** | LLM extraction with structured output + caching + batching. Build the **eval set first**, then the prompt. | Extraction + P/R/F1 numbers | Eval before prompt. |
| **50–65%** | Franchisee feed UI. The single most important screen. | Working feed | Make one screen excellent. |
| **65–75%** | HQ console + drill-down to evidence. | Working console | Every score must be explainable. |
| **75–85%** | Briefing agent (one call per franchisee). Cost log. Fallback modes. | Full happy path + degraded path | Test airplane mode. |
| **85–95%** | `AI_USAGE.md`. Business-case numbers. Slides. Delete unfinished features. | Repo + deck | Deleting is a feature. |
| **95–100%** | Rehearse 3×. Backup video. Backup device. | Calm | Do not add anything. |

**Working rules:** commit every 30 minutes · one person owns the demo path and never touches anything else in the last 20% · every new feature must answer *"does this raise the probability of a working, convincing demo?"* · if the answer is no, it is cut.

---

## 28. Presentation Strategy

### Narrative arc
1. **The paradox** *(15s)* — "Seazone has a 4.8 out of 5 across seventy thousand reviews. And a 6.8 out of 10 on Reclame Aqui, with 102 complaints in the first half of this year. Both numbers are true. The gap between them is where this project lives."
2. **Why the gap exists** *(30s)* — the franchise model. The engine of 100%/year growth is also the source of variance. Not a flaw — a structural consequence.
3. **Who it hurts** *(20s)* — guest gets a bad stay, owner leaves, and the owner is the supply that *is* the business.
4. **What the market did** *(30s)* — Guesty shipped Agent Hub on June 1st. Hostaway shipped AI CoHost in June. Both built a copilot for a property manager. **Neither built one for a franchisor.**
5. **The insight** *(20s)* — Sirius already reads the numbers. Nobody reads the *text*: the messages, the reviews, the ops notes. That's where the failures announce themselves first.
6. **The product — LIVE** *(90s)* — paste a real-looking guest message → watch the score move → open the franchisee feed → show the R$ at stake → show the evidence trail. **No slides during this.**
7. **The AI craft** *(45s)* — eval numbers on screen. The six LLM calls removed. Total cost: five dollars. Production cost at 2,900 properties: under R$400/month.
8. **The number** *(20s)* — base case ~R$1.0M added net revenue, ~R$5.2M retained GMV, assumptions visible.
9. **Can Seazone actually ship it** *(20s)* — runs on your existing Supabase; two tables and one worker; the 110 franchisees are already on WhatsApp; 5-franchisee pilot in two weeks.
10. **The bigger claim** *(15s)* — "This is what makes the 300th franchisee as good as the 10th — in Argentina, where you've never operated."

### Rules
- **Demo before architecture.** Always.
- Every claim carries a source or an explicit assumption.
- Say the internal names — **Sirius, SPOT, Wallet, the 8% + cleaning fee + 2%** — correctly. It signals you did the work.
- Have the "what we did **not** build and why" slide ready. It will be the question.
- Never say "revolutionary," "disruptive," or "game-changing." Say the number.

---

## 29. Risks & Failure Modes

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Hackathon prompt points elsewhere | High | High | §8 pivot matrix; architecture is domain-agnostic |
| Judged as "just a dashboard" | Medium | High | Lead with the *decision arriving at a person*, not the console; the franchisee feed is the hero screen |
| Seazone already built something similar internally | Medium | Medium | Ask in Q&A: *"how do you currently detect a property drifting before the review lands?"* If they have it, pivot to the franchisee **ramp** angle — same engine, different framing |
| Predictive claims unsupported by synthetic data | Medium | High | Ship the eval harness; be explicit that it measures the mechanism, not the outcome |
| Franchisee adoption doubted | Medium | Medium | Design for pull; show R$, not tasks; cite the 8% + cleaning-fee incentive alignment |
| Live demo fails | Low | High | §22 four-path fallback |
| Credits exhausted mid-event | Medium | Medium | Full precompute + cache; rules-only mode |
| Overbuilding | **High** | High | The cut rule in §27; delete, don't hide |
| Presenting synthetic data as real | Low | **Fatal** | Persistent UI labels; state it unprompted in the demo |
| Legal overreach (if pivoting to ALICERCE) | Medium | High | Frame strictly as decision support with cited clauses; never a conclusion |

---

## 30. Adversarial Review — Killing Our Own Idea

Answer these before a director does.

**"Is this actually painful?"** Yes, and it's measurable in public: 102 complaints in six months, 65.7% resolution, 53.7% would return, 2d16h average response. Against a 4.8 average. That is a variance problem, not a quality problem.

**"Why would Seazone care?"** Because supply is the constraint, owner churn destroys supply, and franchise quality is the only lever that touches guests, owners, and ranking simultaneously. And because it's the internationalization blocker.

**"Is it already solved?"** Sirius solves *pricing*. The platform centralizes *governance*. Neither reads free text. Guesty and Hostaway solve it for centralized managers, not franchise networks. If Seazone has already built it — ask, then pivot to franchisee ramp.

**"Is it just an AI wrapper?"** The scoring engine is deterministic and auditable. The LLM does exactly one thing code can't: turn Portuguese free text into structured signal. We removed two-thirds of our planned LLM calls. That's the opposite of a wrapper.

**"Is there evidence of demand?"** Hostaway's review→scorecard feature and Guesty's Agent Hub both shipped in the last 90 days into a market where 70.1% of managers now use AI tools. The pattern is validated; the franchise application isn't taken.

**"Will the user change behavior?"** The franchisee earns 8% of bookings plus 100% of cleaning fees. A prevented one-star review is direct personal income. Incentives are already aligned — we didn't have to invent them.

**"Is the value measurable?"** Yes: share of stays ≥4.7, owner churn, revenue-at-risk protected, time-to-20-properties. Matched-cohort pilot, pre-registered endpoint.

**"Could Seazone implement it?"** Existing Supabase, two tables, one worker, under R$400/month at full scale, distribution already solved.

**"Could a competitor copy it?"** They can copy the model. They cannot copy 110 franchisees, the labeled outcome data the feedback loop generates, or a franchise topology they don't have.

**"Does it need data you don't have?"** In production, no — Seazone holds all of it. In the hackathon, yes — hence synthetic data, clearly labeled, plus an eval harness so the mechanism is falsifiable.

**"Are you solving the wrong part of the journey?"** The alternative candidates are pricing (solved), discovery (Airbnb's), and acquisition (already funded and working). The unsolved part is **delivery consistency at network scale** — which is precisely where Vacasa struggled at much larger scale in the US.

---

## 31. Open Questions
*(Ask these during the event. Asking good questions is itself scored.)*

**About the business**
1. What is annual owner churn, and what is the single most common reason given at termination?
2. How does quality variance actually distribute across the 110 franchisees — is it a long tail or a bimodal split?
3. What is the current direct-booking share vs OTA? (Charlie reports ~30% direct.)
4. How much of the take rate reaches EBITDA after franchisee splits?
5. Post-STJ, how many managed properties sit in residential condominiums without an explicit convention clause?
6. What share of owners crosses the Decreto 12.955 professional threshold?

**About technology**
7. How much of the proprietary platform is agentic today versus CRUD + rules?
8. Does Sirius consume any unstructured signal, or purely numeric features?
9. Is there a single source of truth spanning marketing, ops, and finance? (The public numbers disagree.)
10. Is guest messaging centralized in the platform or does it fragment into WhatsApp?
11. What does the property-scraping system cover today, and where does it stop?

**About the program**
12. What does "using AI in practice" mean concretely in the evaluation — output quality, technique, or both?
13. Which of the seven rotation areas has the most unmet analytical demand right now?

---

## 32. Sources

**Seazone official**
- Quem Somos — seazone.com.br/institucional/quem-somos (accessed 26 Aug 2026)
- Franchise LP — institucional.seazone.com.br/franqueados-new/ (updated 8 May 2026)
- Owner LP — seazone.com.br/lps/novos-proprietarios (accessed 26 Aug 2026)
- Marketplace / SPOT investment pages — seazone.com.br/marketplace
- Blog: "Panorama do mercado de Short Stay no Brasil" (Jun 2026)

**Press & interviews**
- Hotelier News — "Três perguntas para: Fernando Pereira" (21 Oct 2025) — *source for Sirius, the proprietary platform, and expansion criteria*
- Hotelier News — "Seazone: da gestão à incorporação" (8 Sep 2025)
- Exame — "Esse engenheiro largou petroleira…" (19 Jul 2023) — *source for the 20–30% / 6% VGV / R$7k fee structure*
- InfoMoney — DOMO Invest R$3.5M round (2023)
- IstoÉ Dinheiro — CEO on 100%/year growth and franchising (26 Jun 2024)
- Bahia Econômica — COO Bruno Benetti on Salvador expansion (10 Jun 2025)
- Sonho do Primeiro Imóvel — CCO Mônica Medeiros on microfranchising (5 Dec 2025)
- Folha PE (22 Sep 2023); Empreendedor (10 Nov 2023) — SPOT program

**Trainee program**
- EstágioTrainee.com — "Trainee Seazone 2026" (published 3 Aug 2026, updated 10 Aug 2026)

**Reputation**
- Reclame Aqui — Seazone company page and individual complaints, statistics for 01/01/2026–30/06/2026

**Regulatory**
- STJ — official communication, REsp 2.121.055/MG, 2ª Seção, 7 May 2026
- Cescon Barrieu, Mozer Advogados, Costa e Tavares, Porter — legal analyses of the STJ ruling (May–Jul 2026)
- Decreto nº 12.955/2026 (published 30 Apr 2026), regulating LC nº 214/2025
- Hotelier News — CBS impact analysis in hospitality (13 May 2026); "A nova era da hospitalidade" (9 Jun 2026)
- Portas — "O que está acontecendo com o Airbnb no Brasil em 2026" (15 May 2026)

**Competitors**
- StayCharlie institutional pages and blog (2025–Aug 2026); NeoFeed (2022); Exame (2024); InfoMoney (2024)
- Housi blog and iUrban partnership material
- HostnJoy market reports (Apr–Jul 2026)

**Global benchmarks**
- ShortTermRentalz — "Guesty launches AI agent platform" (4 Jun 2026)
- Travel And Tour World — Guesty Agent Hub launch, 1 Jun 2026
- ShortTermRentalz / Hospitality Technology / AI PropTech News — Hostaway AI CoHost (Jun–Jul 2026)
- Hostaway — AI in Vacation Rentals Report (70.1% adoption figure)
- TechCrunch (13 Feb 2026; 7 Aug 2026), CNBC (7 Aug 2026), Skift (7 May 2026), Yahoo Finance (Aug 2026) — Airbnb AI strategy and Q1/Q2 2026 results

**Market data**
- Airbnb Q1 2026 results via Mercado & Eventos and Diário do Turismo (Jul 2026) — Brazil among top-3 global growth markets
- Inside Airbnb via O Globo (Jul 2026) — 42,354 SP listings, 72.9% multi-listing
- Índice FipeZap (May 2026)
- Embratur / Banco Central — 2025 international tourism figures

---

## Final Recommendation

### TOP 3 OPPORTUNITIES

**🥇 1 — FAROL · Franchise Network Quality & Revenue Copilot**
**Problem:** Quality variance across 110+ independent franchisees, visible as a 6.8/10 complaint reputation under a 4.8/5 review average.
**User:** Franchisee (primary), HQ Operations & CX (secondary).
**Why now:** The network crossed the scale where informal oversight stops working; Guesty and Hostaway just proved the pattern for centralized managers and left the franchise case open.
**Seazone fit:** Attacks the exact bottleneck the business model creates; sits entirely on the contractually digital side.
**Existing solutions:** Hostaway CoHost, Guesty Agent Hub — neither addresses franchise topology.
**Our adaptation:** Add the franchisee dimension, Brazilian operational reality, and predictive intervention rather than retrospective reporting.
**MVP:** Ingest → extract → score → 3-item franchisee feed + HQ console + eval harness.
**Technical difficulty:** Medium. **Business impact:** ~R$1.0M added net revenue + ~R$5.2M retained GMV (base case).
**Demo potential:** Very high. **Cost risk:** Very low (~US$5). **Main risk:** being read as "a dashboard." **Score: 128/140.**

**🥈 2 — ALICERCE · Regulatory & Tax Intelligence Copilot**
**Problem:** Post-STJ and post-Decreto 12.955, neither Seazone nor its owners can answer "is this unit legal, and what will it cost me in 2028?" per property.
**User:** Owner, legal/finance, expansion.
**Why now:** Both events are from Q2 2026 and no vendor covers them.
**Our adaptation:** Convention/minutes reasoning with **cited clauses**, plus per-owner CBS/IBS exposure across 2026–2033.
**MVP:** Upload a convention → verdict + evidence + required next action; simulator for tax exposure.
**Technical difficulty:** Medium. **Impact:** High on retention and supply-acquisition risk. **Demo:** Excellent (upload → verdict). **Main risk:** legal framing. **Score: 122/140.**

**🥉 3 — VITRINE · AI-Era Listing Intelligence**
**Problem:** Airbnb discovery is going conversational; 2,900 listings are optimized for a filter world.
**User:** Growth/marketing, owners.
**Why now:** Airbnb's AI search is in live test *right now*.
**Our adaptation:** Per-property structured knowledge base + retrieval-optimized copy + impression-share risk prediction.
**MVP:** Rewrite engine + before/after retrieval simulation + measurable A/B design.
**Technical difficulty:** Low. **Impact:** Medium-high, growth-side. **Demo:** Good. **Main risk:** hard to prove causally inside a hackathon. **Score: 104/140.**

---

### 🏆 Recommended Hackathon Direction: **FAROL**

**Be decisive about why.**

Every other idea in this dossier could be built by someone who read Seazone's website. FAROL can only be conceived by someone who understood that **Seazone's growth engine and its quality risk are the same mechanism** — a franchise network that scales without headcount precisely because Seazone does not control the people doing the work.

It scores highest on the two criteria that actually decide hackathons — **demonstrability** and **strategic fit** — while being cheap enough to survive a credit limit and simple enough to survive a bad wifi connection. It uses AI in the one place where AI is genuinely irreplaceable (Portuguese free text with no schema) and deliberately refuses to use it where code is better (a scoring formula a franchisee can audit). That refusal is the strongest signal you can send to a company whose entire trainee program is built on the distinction between *operating* AI and *building* with it.

And it ends on the only claim that matters to a company planning a Series A and a move into Argentina, Uruguay, and Chile:

> **This is what makes the 300th franchisee as good as the 10th.**

---

*Prepared as a working document. Update Section 8 the moment the official prompt lands, then re-run Section 15's scoring against it before writing a single line of code.*
