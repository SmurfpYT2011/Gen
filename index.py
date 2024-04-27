import aiohttp
import asyncio
import random
import string
import time

async def generate_gift_code(length):
    """Gerar um código de presente."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

async def solicitar(session, link, token):
    """Verificar o código de presente."""
    url = f"https://discord.com/api/v9/entitlements/gift-codes/{link}"
    gift = f"https://discord.com/billing/promotions/{link}"

    querystring = {"country_code":"BR","with_application":"false","with_subscription_plan":"true"}
    webhook = "https://discord.com/api/webhooks/1205895208240418856/4lzRARUOCd0PE3O8XpUj7_mZ4M-m-I1HF8NpcarR2-UV1FwsbNw-Wt3F6TMVSVQgVJjR" 
    headers = {
        "cookie": "__dcfduid=d0d2f460799811ee9b1e410055fc4ae4; __sdcfduid=d0d2f461799811ee9b1e410055fc4ae4a0475f0d7216dcedb4cb08661daf6552af8366a720080dcce20c335dd76276dc; _ga=GA1.2.813504803.1698940872; __stripe_mid=368d4f55-3e75-4dee-820c-c0099c26d553f7ce51; cf_clearance=IgQkpDgVyNwn1DSKvaePE1PRxKqF_siupuehGMV5rvs-1707149714-1-AeVPi5OI0OjFEfMnSSLNiVciprfmroIwYcmfOjEUd6GjZiFLhpK80/amu4/a3bOdR3V6Nj9LOffUGIySQadxlhI=; OptanonConsent=isIABGlobal=false&datestamp=Mon+Feb+05+2024+13%3A15%3A19+GMT-0300+(Hor%C3%A1rio+Padr%C3%A3o+de+Bras%C3%ADlia)&version=6.33.0&hosts=&consentId=72320dff-bc01-400b-9d71-7e81e9d18185&interactionCount=1&landingPath=https%3A%2F%2Fdiscord.com%2F&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0; __cfruid=77a88b6620152a1da6ac4a0f32687e26de0b2c44-1707176083; _cfuvid=ixE1msrGnCmQTOZ_5GbJTJcz5zAuHSffpU9qhlqlbbU-1707176083782-0-604800000; __stripe_sid=af88515e-9328-4dcb-97f2-24c840f3a6b6cc98ac",
        "authority": "discord.com",
        "accept": "*/*",
        "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "authorization": token,
        "referer": "https://discord.com/",
        "sec-ch-ua": '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
        "x-debug-options": "bugReporterEnabled",
        "x-discord-locale": "pt-BR",
        "x-discord-timezone": "America/Sao_Paulo",
    }
    
    async with session.get(url, headers=headers, params=querystring) as response:
        if response.status == 200:
            data = await response.json()
            if data.get('redeemed') == False:
                print(f"O código de presente está disponível para resgate | {gift}")
                webhook_payload = {"content": f"{gift}"}
                async with session.post(webhook, json=webhook_payload) as webhook_response:
                    print()
            else:
                print(f"O código de presente foi resgatado. | {link}")
        elif response.status == 404:
            print(f"O código de presente é inválido. | {link}")
        else:
            print(f"Erro ao verificar o código de presente. Status code: {response.status}")

async def main():
    with open("tokens.txt", "r") as f:
        tokens = f.read().splitlines()
    request_count = 0
    for token in tokens:
        async with aiohttp.ClientSession() as session:
            while True:
                time.sleep(0.11)
                link = await generate_gift_code(24)
                await solicitar(session, link, token)
                request_count += 1
                if request_count % 500 == 0:
                    print("[*] Limite de taxa atingido | Links gerados: 500")
                    await asyncio.sleep(60)

asyncio.run(main())
