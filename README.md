# Upload .env to Azure AppConfig

Sincronize seu `.env` local com o Azure App Configuration de forma simples e automatizada — agora com suporte a Key Vault!

---

## 🚀 Features

- 🗝️ **Leitura do `.env`**  
  Extrai pares `CHAVE=VALOR`, ignorando comentários e linhas em branco.  
- 🔖 **Prefixo Personalizado**  
  Adiciona um prefixo (ex.: `prod/DB_HOST`) a cada chave.  
- 🏷️ **Label Opcional**  
  Atribui um label (ex.: `v1.0`) às configurações, se desejado.  
- 🔐 **Autenticação Segura**  
  Usa Service Principal (via `config.json`) para conectar no App Configuration.  
- ⚙️ **Totalmente Parametrizável**  
  Controle tudo pela linha de comando: nome do store, arquivo `.env`, prefixo, label e caminho das credenciais.  
- 🔑 **Integração com Azure Key Vault**  
  • Armazena segredos em um Key Vault (nome opcional) aplicando regras definidas em  
    `secret_transformations` no `config.json` (ex.: substituir `_` por `-`, etc.)  
  • Exibe uma amostra (até 5) dos nomes originais → transformados  
  • Pede confirmação (Y/N) antes de publicar segredos e referências no App Configuration  

---

## 📦 Instalação

```bash
git clone https://github.com/seu-usuario/upload-env-to-appconfig.git
cd upload-env-to-appconfig
pip install -r requirements.txt
```

---

## 🔐 Configuração (`config.json`)

```jsonc
{
  // Tenant, Client e Secret da sua AAD App Registration com função "App Configuration Data Owner" ou similar e permissões para o Key Vault
  "tenant_id": "<SEU_TENANT_ID>",
  "client_id": "<SEU_CLIENT_ID>",
  "client_secret": "<SEU_CLIENT_SECRET>",

  // Regras para transformar nomes de secret antes de enviar ao Key Vault
  "secret_transformations": [
    { "pattern": "_",   "replacement": "-" },
    { "pattern": "\\.", "replacement": "_" }
    // adicione quantas regras precisar
  ]
}
```

---

## 📖 Uso

```bash
python main.py \
  --appconfig-name <STORE_NAME> \
  --env-file      <CAMINHO_PARA_.env> \
  --prefix        <PREFIXO> \
  [--label       <LABEL>] \
  [--keyvault-name <KEYVAULT_NAME>] \
  [--config      <CAMINHO_CONFIG.json>]
```

| Parâmetro                    | Descrição                                                                                                     |
|------------------------------|---------------------------------------------------------------------------------------------------------------|
| `--appconfig-name` 🏷️        | Nome do seu App Configuration Store no Azure (ex: `meu-appconfig`) — **obrigatório**                          |
| `--env-file` 📄              | Caminho para o arquivo `.env` (ex: `./.env`) — **obrigatório**                                                |
| `--prefix` 🔖                | Prefixo para concatenar às chaves (ex: `prod`) — padrão `""`                                                  |
| `--label` 🏷️                | Label para as configurações (ex: `v1.2`) — se omitido, publica sem label                                      |
| `--keyvault-name` 🔑         | Nome do Azure Key Vault — se informado, armazena segredos no Vault (aplicando `secret_transformations`) e cria referências no App Configuration |
| `--config` 🔐               | Caminho para o `config.json` com credenciais AAD e transformações — padrão `./config.json`                     |

---

## 📝 Exemplo

```bash
# Apenas AppConfig
python main.py \
  --appconfig-name meu-appconfig \
  --env-file      .env \
  --prefix        meu-produto \
  --label         dev

# AppConfig + Key Vault
python main.py \
  --appconfig-name  meu-appconfig \
  --env-file       .env \
  --prefix         meu-produto \
  --label          dev \
  --keyvault-name  meu-vault
```

> No segundo exemplo, o script:  
>
> 1. Exibe até 5 transformações de nome de secret (origem → transformado)
> 2. Pede confirmação (Y) para continuar  
> 3. Armazena cada valor como secret no Key Vault (`_`→`-`, etc.)  
> 4. Cria referências no App Configuration apontando para esses secrets  

---

## ❤️ Por que usar?

- Integração rápida com pipelines CI/CD  
- Evita inconsistências entre ambientes local e nuvem  
- Gerencia segredos de forma segura e versionada  

Pronto para simplificar o deploy das suas configurações e segredos? 😉🚀
