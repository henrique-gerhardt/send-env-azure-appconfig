#!/usr/bin/env python3
"""
upload_env_to_appconfig.py

Publica variáveis de um .env no Azure App Configuration.
Opcionalmente armazena em Key Vault e publica referência no AppConfig.

Usage:
  python upload_env_to_appconfig.py \
    --appconfig-name meu-appconfig \
    --env-file .env \
    --prefix prod \
    [--label v1.2] \
    [--keyvault-name meu-vault] \
    [--config config.json]
"""

import argparse
import json
import re
import sys
from azure.identity import ClientSecretCredential
from azure.appconfiguration import AzureAppConfigurationClient, ConfigurationSetting
from azure.keyvault.secrets import SecretClient

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

def apply_transformations(s: str, rules: list[dict]) -> str:
    for rule in rules:
        s = re.sub(rule["pattern"], rule["replacement"], s)
    return s

def confirm_sample(samples: dict):
    print("\nAmostra de transformação de nomes de secret:")
    for orig, transformed in samples.items():
        print(f"  {orig!r}  →  {transformed!r}")
    ans = input("\nEstá de acordo? (Y/N): ").strip().lower()
    if ans != 'y':
        print("Abortando conforme solicitado.")
        sys.exit(0)

def main():
    p = argparse.ArgumentParser(description="Publica .env no AppConfig e Key Vault")
    p.add_argument('--appconfig-name', required=True, help="Nome do AppConfig Store")
    p.add_argument('--env-file',       required=True, help="Arquivo .env a ler")
    p.add_argument('--prefix',         default='',   help="Prefixo a adicionar antes da chave")
    p.add_argument('--label',          default=None, help="Label a atribuir (opcional)")
    p.add_argument('--keyvault-name',  default=None, help="Nome do Key Vault (opcional)")
    p.add_argument('--config',         default='config.json', help="Config AAD e transformações")
    args = p.parse_args()

    cfg = load_config(args.config)
    envs = parse_env(args.env_file)
    prefix = args.prefix.strip('/')

    secret_rules = cfg.get("secret_transformations", [])

    credential = ClientSecretCredential(
        tenant_id=cfg['tenant_id'],
        client_id=cfg['client_id'],
        client_secret=cfg['client_secret'],
    )

    appconf = AzureAppConfigurationClient(f"https://{args.appconfig_name}.azconfig.io", credential)
    secret_client = None
    if args.keyvault_name:
        vault_url = f"https://{args.keyvault_name}.vault.azure.net"
        secret_client = SecretClient(vault_url=vault_url, credential=credential)

    if secret_client and secret_rules:
        sample_keys = list(envs.keys())[:5]
        samples = { k: apply_transformations(k, secret_rules) for k in sample_keys }
        confirm_sample(samples)

    for key, val in envs.items():
        full_key = f"{prefix}/{key}" if prefix else key

        if secret_client:
            secret_name = apply_transformations(key, secret_rules)
            sec = secret_client.set_secret(secret_name, val)
            ref_value = json.dumps({"uri": sec.id})
            setting = ConfigurationSetting(
                key=full_key,
                label=args.label,
                value=ref_value,
                content_type="application/vnd.microsoft.appconfig.keyvaultref+json;charset=utf-8"
            )
            dest = f"KeyVault secret '{secret_name}'"
        else:
            setting = ConfigurationSetting(key=full_key, label=args.label, value=val)
            dest = f"value '{val}'"

        appconf.set_configuration_setting(setting)
        print(f"✔ {dest}  →  AppConfig key='{full_key}' label='{args.label or '<none>'}'")

if __name__ == '__main__':
    main()
