# Portal de Acompanhamento de Dados de Mini e Micro Geração Distribuída
<!-- Portal de Acompanhamento de Dados de Mini e Micro Geração Distribuída(link_para_imagem) -->

## Descrição do Projeto

A **Portal de Acompanhamento de Dados de Mini e Micro Geração Distribuída** visa Sistema para acompanhanmento de dados de MMGD ANEEL. Inclui dashboards comparativos e análise preditiva.

## Funcionalidades

O portal de acompanhamento de dados de MMGD incluirá as seguintes funcionalidades principais:

1. **Cadastro de Clientes**: Os usuários poderão cadastrar e gerenciar informações sobre seus clientes, incluindo dados pessoais, histórico de crédito, informações de contato e outras informações relevantes.

2. **Análise preditiva e ML**: previsão de geração/consumo, estimativa de créditos futuros, clustering por perfil.

3. **Monitoramento e Controle**: O portal fornecerá recursos para monitorar os créditos e realizar comparativos com demais sistemas fotovoltaicos.

4. **Geração de Relatórios**: Os usuários poderão gerar relatórios personalizados com informações relevantes sobre os créditos, como histórico, entre outros.

<!-- 5. **Integração com Sistemas Externos**: A plataforma terá capacidade de integração com outros sistemas e ferramentas existentes na organização, como sistemas de contabilidade, CRM (Customer Relationship Management) e sistemas de gestão empresarial. -->

## Tecnologias Utilizadas

O projeto será desenvolvido utilizando as seguintes tecnologias:

- Linguagem de programação: **Python**
- Framework web: **DJANGO**
- Banco de dados: **PostGree** <!-- - Front-end: **HTML**, **CSS**, **JavaScript** -->
- Controle de versão: **Git**

## Instalação e Uso

Para executar a Portal de Acompanhamento de Dados de Mini e Micro Geração Distribuída em ambiente local, siga as instruções abaixo:

1. Clone este repositório: `git clone https://github.com/LeonLaboi/portal_mmgd_cooperativa.git`
2. Acesse o diretório do projeto: `cd portal_mmgd_cooperativa`
3. Crie e ative um ambiente virtual (opcional, mas recomendado): `python3 -m venv env` e `source env/bin/activate`
4. Instale as dependências do projeto: `pip install -r requirements.txt`
5. Configure as variáveis de ambiente no arquivo `.env` conforme necessário.
6. Execute as migrações do banco de dados: `python manage.py migrate`
7. Inicie o servidor de desenvolvimento: `python manage.py runserver`
