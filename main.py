#!/usr/bin/env python3
"""
upload_env_to_appconfig.py

Recebe:
  --appconfig-name NOME_DO_STORE         (ex: "meu-appconfig")
  --env-file CAMINHO_PARA_.env           (ex: "./.env")
  --prefix PREFIXO                       (ex: "prod" gera "prod/CHAVE")
  [--label LABEL]                        (ex: "v1.0"; se omitido, publica sem label)
  [--config CAMINHO_PARA_config.json]    (padrão: "./config.json")

Lê o .env, formata as chaves, e faz set_configuration_setting em cada par.
"""

import argparse, json, os
from azure.identity import ClientSecretCredential
from azure.appconfiguration import AzureAppConfigurationClient, ConfigurationSetting

def load_config(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_env(env_path):
    settings = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, val = line.split('=', 1)
            settings[key.strip()] = val.strip().strip('"').strip("'")
    return settings

def main():
    p = argparse.ArgumentParser(description="Publica variáveis do .env no Azure App Configuration")
    p.add_argument('--appconfig-name', required=True, help="Nome do seu AppConfiguration Store")
    p.add_argument('--env-file',       required=True, help="Arquivo .env a ler")
    p.add_argument('--prefix',         default='',   help="Prefixo a adicionar antes da chave")
    p.add_argument('--label',          default=None, help="Label a atribuir (opcional)")
    p.add_argument('--config',         default='config.json', help="Configurações AAD (tenant/client/secret)")
    args = p.parse_args()

    cfg = load_config(args.config)
    credential = ClientSecretCredential(
        tenant_id=cfg['tenant_id'],
        client_id=cfg['client_id'],
        client_secret=cfg['client_secret'],
    )

    endpoint = f"https://{args.appconfig_name}.azconfig.io"

    client = AzureAppConfigurationClient(endpoint, credential)

    envs = parse_env(args.env_file)

    prefix = args.prefix.strip('/')
    for key, val in envs.items():
        key_name = f"{prefix}/{key}" if prefix else key

        setting = ConfigurationSetting(
            key=key_name,
            label=args.label,
            value=val
        )

        client.set_configuration_setting(setting)

        print(f"✔ Publicado: {key_name}  label={args.label or '<none>'}")

if __name__ == '__main__':
    main()
