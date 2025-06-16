from flask import Flask, render_template
import re
from playwright.sync_api import sync_playwright
from time import sleep
from faker import Faker
import random 
fake = Faker('pt-br')
nomes_gerados = set()
telefones_gerados = set()

def gerar_nome_telefone_unicos():
    while True:
        nome = fake.name()
        telefone = fake.phone_number()
        if nome not in nomes_gerados and telefone not in telefones_gerados:
            nomes_gerados.add(nome)
            telefones_gerados.add(telefone)
            return nome, telefone
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Index.html')


@app.route(r"/automatizar",methods=["POST"])
def automatizar():
        with sync_playwright() as p:
           browser = p.chromium.launch(headless=True)
            #abrir navegador
           page = browser.new_page()
           page_app = browser.new_page()
           page.goto('https://www.emailnator.com/')
           #agora desativar funções
           page.get_by_role('checkbox', name='domain').click()
           page.locator('//*[@id="custom-switch-plusGmail"]').wait_for(state='visible')
           page.locator('//*[@id="custom-switch-plusGmail"]').click()
           page.locator('//*[@id="custom-switch-googleMail"]').wait_for(state='visible')
           page.locator('//*[@id="custom-switch-googleMail"]').click()
           page.locator('//*[@id="root"]/div/main/div[1]/div/div/div/div[2]/div/div[5]/div/button').click()
           sleep(1)
           page.locator('//*[@id="root"]/div/main/div[1]/div/div/div/div[2]/div/div[3]/button').click()
           email = [parte for parte in page.get_by_text('@gmail.com').inner_text().split() if '@' in parte][0]
           #print(email)
           sleep(1)
           page_app.goto('https://www.meuguru.com/guru-ia')
           page_app.locator('body > div.flex.flex-1.flex-col.overflow-clip > header > div > div > div > button.flex.items-center.justify-center.whitespace-nowrap.disabled\:bg-gray-100.disabled\:text-gray-300.disabled\:border-none.disabled\:cursor-not-allowed.disabled\:hover\:opacity-100.text-base.h-10.rounded-full.bg-primary-700.text-white.hover\:opacity-100.hover\:bg-primary-900.gap-2.px-6.font-semibold').wait_for(state='visible')
           page_app.locator('body > div.flex.flex-1.flex-col.overflow-clip > header > div > div > div > button.flex.items-center.justify-center.whitespace-nowrap.disabled\:bg-gray-100.disabled\:text-gray-300.disabled\:border-none.disabled\:cursor-not-allowed.disabled\:hover\:opacity-100.text-base.h-10.rounded-full.bg-primary-700.text-white.hover\:opacity-100.hover\:bg-primary-900.gap-2.px-6.font-semibold').click()
           page_app.get_by_role('button', name='Crie sua conta com e-mail').click()
            #parte do login
           nome, telefone = gerar_nome_telefone_unicos()
           page_app.get_by_role('textbox', name='Nome').fill(nome)
           page_app.get_by_role('textbox',name='Celular').fill(telefone+'111')
           page_app.get_by_role('textbox',name='E-mail').fill(email)
           senha = email+'222'
           page_app.get_by_role('textbox',name='Senha').fill(senha)
            #agora enviar
           page_app.get_by_role('button',name='Criar conta').click()
           sleep(1)
           page.reload()
           while True:
                try:
                    page.get_by_text('Seu código de acesso é').wait_for(timeout=3500)
                    break
                except:
                    page.get_by_text('Reload').click()
           elemento = page.get_by_text('Seu código de acesso é',exact=False)
           texto_completo = elemento.inner_text()
           match = re.search(r"\d{4,6}", texto_completo)
           if match:
                codigo = match.group(0)
                #print("Código encontrado:", codigo)
           else:
                raise Exception("Código não encontrado.")
            #concluido, agora colocoremos a codigo no site forneceresmo a conta ao usuario senha+login
           page_app.locator('#token').first.click()
           page_app.locator("#token").first.fill("1")
           page_app.locator("#token").nth(1).fill("2")
           page_app.locator("#token").nth(2).fill("3")
           page_app.locator("#token").nth(3).fill("4")
           return render_template('resultado.html', email=email, code=codigo, senha=senha)

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=5000, debug=True)

