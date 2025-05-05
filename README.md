# Upload .env to Azure AppConfig
Sincronize seu `.env` local com o Azure App Configuration de forma simples e automatizada!

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

---

## 📦 Instalação

```bash
git clone https://github.com/seu-usuario/upload-env-to-appconfig.git
cd upload-env-to-appconfig
pip install -r requirements.txt
```

---

## 🔐 Autenticação

```json
{
  // Tenant, Client e Secret da sua AAD App Registration com função "App Configuration Data Owner" ou similar
  "tenant_id": "<SEU_TENANT_ID>",
  "client_id": "<SEU_CLIENT_ID>",
  "client_secret": "<SEU_CLIENT_SECRET>"
}
```

---

## 📖 Uso

```bash
python upload_env_to_appconfig.py \
  --appconfig-name <STORE_NAME> \
  --env-file      <CAMINHO_PARA_.env> \
  --prefix        <PREFIXO> \
  [--label       <LABEL>] \
  [--config      <CAMINHO_CONFIG.json>]
```

| Parâmetro                 | Descrição                                                                                 |
|---------------------------|-------------------------------------------------------------------------------------------|
| `--appconfig-name` 🏷️     | Nome do seu App Configuration Store no Azure (ex: `meu-appconfig`) — **obrigatório**      |
| `--env-file` 📄           | Caminho para o arquivo `.env` (ex: `./.env`) — **obrigatório**                            |
| `--prefix` 🔖             | Prefixo para concatenar às chaves (ex: `prod`) — padrão `""`                              |
| `--label` 🏷️             | Label para as configurações (ex: `v1.2`) — se omitido, publica sem label                  |
| `--config` 🔐             | Caminho para o `config.json` com credenciais AAD — padrão `./config.json`                 |

---

## 📝 Exemplo

```bash
python upload_env_to_appconfig.py \
  --appconfig-name meu-appconfig \
  --env-file      .env \
  --prefix        prod \
  --label         v1.2 \
  --config        config.json
```

> Neste exemplo, todas as variáveis do `.env` serão publicadas como `prod/CHAVE` com o label `v1.2`.  

---

## ❤️ Por que usar?

- Integração rápida com pipelines CI/CD  
- Evita inconsistências entre ambientes local e nuvem  
- Facilita o versionamento de configurações  

Pronto para simplificar o deploy das suas configurações? 😉🚀
