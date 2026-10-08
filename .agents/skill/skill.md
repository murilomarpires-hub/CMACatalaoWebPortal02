---
name: dashboard-builder
description: Skill para criação de dashboards profissionais com React, Supabase e Shadcn/UI.
---

**Nome:** Dashboard Builder  
**Descrição:** Skill para criação de dashboards profissionais com React, Supabase e Shadcn/UI. Guia o usuário passo a passo para coletar todas as informações necessárias, gera um plano completo para aprovação e entrega um prompt pronto para o Claude Code construir o dashboard localmente com link de visualização. Use sempre que o usuário mencionar dashboard, painel, métricas, KPIs, gráficos, visualização de dados ou quiser monitorar informações de um negócio — mesmo que não use a palavra "dashboard" explicitamente.

---

---

## Regra de Execução

**Execute um passo por vez. Envie as perguntas do passo atual, aguarde a resposta do usuário e só então avance. Nunca antecipe etapas.**

---

## PASSO 1 — Identidade e Nicho

Envie estas duas perguntas juntas e aguarde resposta:

1. **Qual é o nome da empresa?**  
   _O nome aparecerá no topo do dashboard._

2. **Qual é o nicho?**  
   _Ex: clínica médica, clínica de estética, escritório de advocacia, imobiliária, academia, restaurante, contabilidade, pet shop, entre outros._

---

## PASSO 2 — Banco de Dados

Pergunte se o usuário já tem banco no Supabase:

**Se SIM — peça o schema:**  
_"Pode mandar um print da estrutura do seu Supabase, o SQL de criação das tabelas, ou listar os nomes e campos principais."_

Após receber, analise internamente:
- Quais tabelas existem e o que representam
- Quais campos permitem cálculos (valores, datas, status, categorias)
- Quais relacionamentos existem entre tabelas
- Quais métricas e gráficos são viáveis com esses dados

**Se NÃO — modo banco do zero:**  
Com base no nicho do Passo 1, sugira uma estrutura de tabelas em linguagem simples (sem SQL). Explique o que cada tabela armazena e confirme com o usuário antes de avançar.

_Exemplo para clínica de estética:_  
_"Vou sugerir: **clientes** (nome, telefone, email), **agendamentos** (data, horário, status, valor, procedimento), **procedimentos** (nome, duração, preço). Faz sentido ou precisa ajustar?"_

Após schema definido, pergunte:

3. **Os dados precisam atualizar em tempo real ou ao recarregar a página já está bom?**

---

## PASSO 3 — Métricas e Gráficos

Com base no nicho (Passo 1) e no schema (Passo 2), sugira ativamente:

4. **KPI Cards (3 a 5):** liste os mais relevantes e peça confirmação.  
   _"Com base nos seus dados, posso mostrar: [sugestão A], [sugestão B], [sugestão C], [sugestão D]. Quais 3 a 5 fazem mais sentido para você?"_

5. **Gráficos (3 a 5):** sugira com tipo e período viáveis para os dados.  
   _"Dá para criar: [gráfico 1 — tipo], [gráfico 2 — tipo], [gráfico 3 — tipo]. Quer todos ou prefere trocar algum?"_

6. **Listas / Tabelas:** sugira registros úteis para o dia a dia.  
   _"Posso incluir uma lista de [sugestão]. Faz sentido?"_

> Só sugira o que for tecnicamente possível com o schema definido no Passo 2.

---

## PASSO 4 — Visual e Aparência

7. **Tem alguma cor de marca ou identidade visual definida?**  
   _Ex: "logo azul e dourado", "usamos verde e branco", "não tenho nada definido"_

8. **Prefere tema claro, escuro ou os dois?**

9. **O dashboard será usado mais no computador ou no celular?**

---

## PASSO 5 — Plano e Aprovação

Com todas as respostas coletadas, **gere o plano completo** e **aguarde aprovação do usuário antes de avançar**.

### 5.1 — Apresente o Plano

Mostre um resumo claro e legível:

```
## Plano do Dashboard — [Nome da Empresa]

### Identidade
- Empresa: ...
- Nicho: ...

### Banco de Dados
- Status: existente / a criar
- Tabelas: [lista com campos principais]
- Atualização: tempo real / ao carregar

### KPI Cards
- Card 1: ...
- Card 2: ...
- Card 3: ...

### Gráficos
- Gráfico 1: [nome — tipo — período]
- Gráfico 2: [nome — tipo — período]
- Gráfico 3: [nome — tipo — período]

### Listas / Tabelas
- ...

### Visual
- Cores de marca: ... (ou "Claude Code escolhe pelo nicho")
- Tema: claro / escuro / ambos
- Dispositivo principal: desktop / mobile

### Requisitos Especiais
- ...
```

Após apresentar, pergunte:  
**"O plano está correto? Posso gerar o prompt para construção?"**

---

---

## Stack Padrão (fixa — nunca alterar)

| Camada | Tecnologia |
|---|---|
| Framework | React + Vite + TypeScript |
| Estilo | Tailwind CSS |
| Componentes UI | Shadcn/UI |
| Gráficos | Recharts (via Shadcn Charts) |
| Banco de dados | Supabase (PostgreSQL) |
| Auth | Supabase Auth |
| Deploy | Vercel |

> Se o usuário solicitar algo fora desta stack, registre como requisito especial no briefing.

---

---

## Layout Padrão (fixo — nunca alterar)

```
┌─────────────────────────────────────────────┐
│  [Nome da Empresa]                [Usuário] │  ← Header
├─────────────────────────────────────────────┤
│  [Hoje] [Ontem] [7 dias] [Este mês]         │
│  [Mês passado] [3 meses] [📅 Personalizado] │  ← Filtros de data
├─────────────────────────────────────────────┤
│   [Card 1]   [Card 2]   [Card 3]  [Card?]   │  ← 3 a 5 KPI cards
├─────────────────────────────────────────────┤
│   [Gráfico principal — largura total]       │  ← 1º gráfico (100%)
├──────────────────────┬──────────────────────┤
│   [Gráfico 2]        │   [Gráfico 3]        │  ← 2ª linha
├──────────────────────┴──────────────────────┤
│   [Gráfico 4]        │   [Gráfico 5]        │  ← 3ª linha (se houver)
└─────────────────────────────────────────────┘
```

**Regras:**
- Header com nome da empresa à esquerda e usuário logado à direita. Sem menu lateral.
- Filtros de data sempre presentes e controlam todos os cards e gráficos simultaneamente.
- De 3 a 5 KPI cards em linha. Se o usuário quiser mais de 5, ajude a priorizar.
- 1º gráfico em largura total. Demais em pares de 2 colunas.
- Entre 3 e 5 gráficos no total. Tipo (barra, linha, pizza, área) decidido pelo Claude Code.
- Página única. Sem navegação entre páginas.

---

---

---

## PASSO 6 — Geração do Prompt e Link Local

Somente após aprovação do Passo 5, gere o prompt completo em inglês técnico para o Claude Code. O prompt deve instruir o Claude Code a construir o dashboard, rodar localmente com `npm run dev` e retornar o link `localhost` para o usuário visualizar antes de qualquer deploy.

```
Build a professional dashboard using the following stack:
- React + Vite + TypeScript
- Tailwind CSS
- Shadcn/UI components
- Recharts (via Shadcn Charts) for all charts
- Supabase for database and authentication

## Business Context
[nome da empresa, nicho, objetivo]

## Supabase Schema
[estrutura completa das tabelas — inclua SQL de criação se banco for do zero]

## KPI Cards
[lista de 3 a 5 cards com descrição e fonte de dados]

## Charts
[lista de gráficos: nome, tipo, eixos, período, tabela/campo de origem]

## Tables / Lists
[listas com colunas e ordenação]

## Data Refresh
[realtime / on-load]

## Layout Structure (mandatory — do not deviate)
1. Header: company name left, logged user right. No sidebar.
2. Date filters: Hoje, Ontem, Últimos 7 dias, Este mês, Mês passado, Últimos 3 meses + custom picker. All filters control all cards and charts simultaneously.
3. KPI Cards: [N] cards in a single row below filters.
4. Charts:
   - 1st chart: full width (100%)
   - 2nd and 3rd: side by side (2 columns)
   - 4th and 5th (if applicable): side by side (2 columns)
5. Single page only. No routing.

## Color Palette
Choose a palette that fits the niche: [nicho]. Apply consistently across header, cards, charts and buttons.
Brand colors (if provided): [cores ou "none — choose freely based on niche"]

## Instructions
- Use Supabase client for all data fetching
- ALL text in Brazilian Portuguese — labels, titles, buttons, placeholders, errors
- Use Shadcn/UI Card for KPI cards
- Use ResponsiveContainer from Recharts for all charts
- Implement loading and error states for all data
- Follow Shadcn/UI design system throughout
- Primary device: [desktop/mobile]

## Local Development
After building, run the project locally with `npm run dev` and return the local URL (localhost) so the user can preview the dashboard before any deployment.
```