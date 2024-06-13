# Desafio de Negócio

A Cury Company é uma empresa de tecnologia que desenvolveu um aplicativo conectando restaurantes, entregadores e clientes. A plataforma permite aos usuários solicitar refeições de diversos restaurantes e recebê-las em suas casas através de entregadores cadastrados. Apesar do crescimento contínuo das operações de entrega, o CEO enfrenta desafios na obtenção de visibilidade completa dos principais indicadores de desempenho (KPIs) da empresa.

Como Cientista de Dados contratado, sua missão inicial é organizar os principais KPIs estratégicos em uma ferramenta centralizada. Isso permitirá ao CEO tomar decisões fundamentadas para impulsionar o crescimento da empresa. A Cury Company opera como um Marketplace, facilitando transações entre restaurantes, entregadores e clientes finais. Para acompanhar o crescimento dessas operações, o CEO deseja monitorar de perto as seguintes métricas:

## Métricas Estratégicas

### Visão Corporativa:

1. Número diário e semanal de pedidos.
2. Distribuição dos pedidos por tipo de tráfego.
3. Comparação do volume de pedidos por cidade e tipo de tráfego.
4. Quantidade de pedidos por entregador por semana.
5. Localização centralizada dos pontos de entrega por tipo de tráfego.

### Visão do Entregador:

1. Faixa etária dos entregadores.
2. Condição dos veículos utilizados (melhor e pior).
3. Avaliação média por entregador.
4. Avaliação média por tipo de tráfego e condições climáticas.
5. Lista dos 10 entregadores mais rápidos e mais lentos por cidade.

### Visão dos Restaurantes:

1. Número de entregadores únicos utilizados.
2. Distância média entre restaurantes e locais de entrega.
3. Tempo médio de entrega durante festivais e dias regulares.
4. Desvio padrão do tempo de entrega durante festivais e dias regulares.
5. Tempo médio de entrega por cidade e tipo de pedido.

# Premissas da Análise

Para esta análise, foram considerados dados coletados entre 11/02/2022 e 06/04/2022. O modelo de negócio adotado é o Marketplace, com foco nas transações entre restaurantes, entregadores e clientes finais.

# Estratégia de Implementação

O painel estratégico foi desenvolvido para apresentar as métricas essenciais que refletem as três principais visões do modelo de negócio da Cury Company:

1. Crescimento corporativo
2. Crescimento dos restaurantes parceiros
3. Desempenho dos entregadores

# Insights Principais

1. Os pedidos apresentam variações sazonais diárias, com uma flutuação média de 10% entre dias consecutivos.
2. Cidades do tipo Semi-Urbano não registram baixas condições de tráfego.
3. As maiores variações no tempo de entrega ocorrem em condições ensolaradas.

# Produto Final

Um painel online hospedado em nuvem, acessível de qualquer dispositivo conectado à internet. Para acessar o painel, clique neste [link](https://project-currycompany.streamlit.app/).

# Conclusão

O objetivo deste projeto foi fornecer ao CEO um conjunto claro de gráficos e tabelas que destacam as métricas essenciais para tomada de decisão estratégica. Observou-se um crescimento significativo no número de pedidos entre as semanas 06 e 13 de 2022.

# Próximos Passos

1. Simplificar as métricas apresentadas.
2. Implementar novos filtros interativos.
3. Expandir as visões de negócio disponíveis para análise.
