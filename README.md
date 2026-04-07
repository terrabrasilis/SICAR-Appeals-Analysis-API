# SICAR Appeals Analysis API

Esta API consulta os dados do **SICAR** a partir de um **banco de dados próprio**, previamente gerado pela equipe.  
Esse banco é alimentado com informações obtidas do serviço de consulta pública do CAR (**GeoServer**), disponível em:  
https://consultapublica.car.gov.br/publico/imoveis/index

Após a ingestão, os dados do SICAR são **cruzados com as bases PRODES** disponíveis no projeto.

Com esse cruzamento, a API consolida informações territoriais e ambientais para apoiar análises e decisões relacionadas aos recursos processados.

## Sumário

- [Pré-requisitos](#pré-requisitos)
- [Execução local](#execução-local)
- [Docker Swarm](#docker-swarm)
- [Configuração](#configuração)

## Pré-requisitos

- Python 3.10+ (ou versão compatível com o projeto)
- Docker
- Docker Swarm inicializado (`docker swarm init`)
- (Opcional) Portainer para gerenciamento de stack e secrets

## Execução local

1. Clone o repositório:
   ```bash
   git clone <repository-url>
   cd SICAR-Appeals-Analysis-API
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute a aplicação:
   ```bash
   python run.py
   ```

A API ficará disponível em: `http://localhost:8001`

## Docker Swarm

### 1) Inicializar o Swarm (uma única vez no host)
```bash
docker swarm init
```

### 2) Build da imagem
```bash
docker build -t sicar-appeals-analysis-api:latest .
```

### 3) Deploy da stack
> Se o projeto já possui `docker-compose.yml` compatível com Swarm:
```bash
docker stack deploy -c docker-compose.yml sicar-api
```

### 4) Verificar serviços
```bash
docker stack services sicar-api
docker service ls
```

### 5) Remover stack
```bash
docker stack rm sicar-api
```

A API ficará disponível na porta publicada pelo serviço (ex.: `http://localhost:8001/docs`).

## Configuração

A aplicação utiliza secrets para informações sensíveis. Garanta que os secrets abaixo existam no ambiente (Swarm/Portainer):

- `prodes.pantanal.database.url`
- `prodes.amazonia.database.url`
- `prodes.cerrado.database.url`
- `prodes.pampa.database.url`
- `prodes.mata_atlantica.database.url`
- `prodes.caatinga.database.url`
- `sicar.database.url`

No Docker Swarm, os secrets podem ser criados via CLI:
```bash
printf "valor-do-secret" | docker secret create nome.do.secret -
```