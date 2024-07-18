# Reinicia (Ciclo de desligamento) da impressora HP LaserJet Pro MFP M428fdw

## Instalar virtualenv

```bash
pip install virtualenv
```

## Criar ambiente virtual

Linux

```bash
virtualenv venv
source venv/bin/activate
```

Windows

```cmd
virtualenv venv
venv/Scripts/activate...
```

## Instalar bibliotecas no ambiente virtual

```bash
pip install -r requirements.txt
```

## Preencher o .env conforme .env-exemple

## Executar no docker

```bash
docker build -t hp-reboot .
docker run -d --name hp-reboot --env-file .env hp-reboot
docker run -d --name hp-reboot-test \
    -e "LOGIN=admin" \
    -e "PASSWORD=60210e23" \
    -e "IP_PRINTS=10.15.254.64,10.15.254.65,10.15.254.67,10.15.254.70,10.15.254.71,10.15.254.72" \
    -e "TELEGRAM_BOT_TOKEN=1520356992:AAFj8crCMVsmy1OGE0wpUC0xksrs-LVtQ6g" \
    -e "TELEGRAM_CHAT_ID=128454778" \
    hp-reboot:vt1
```
