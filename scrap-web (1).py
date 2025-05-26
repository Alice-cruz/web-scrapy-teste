#!/usr/bin/env python
# coding: utf-8

# In[35]:


import requests
from bs4 import BeautifulSoup
import base64
import json


## configuraçaõ de headers e key e link ##
link_geral = 'x'
token = "y"
headers = {
    "Authorization": f"Bearer {token}" #assim como na documentacao da openai
}
link_api = 'z'
modelo_api = 'microsoft-florence-2-large'
prompt = "<DETAILED_CAPTION>"

## fim das configuracoes ##

## Parte 1: executar via script - baixar imagem 
def baixar_imagem():
    #aqui há um pequeno problema, a imgagem não está como uma url, mas em Base64
    resposta = requests.get(link_geral, headers=headers)
    soup = BeautifulSoup(resposta.text, "html.parser")
    #print(soup.prettify())
    
    img_tag = soup.find("img")
    img_base64 = img_tag['src']
    
    #separa o delimitador e pega o item da imagem 0 eh o data:image.. 
    base64_data = img_base64.split(",")[1]
    #deocdifica 
    imagem = base64.b64decode(base64_data)
    nome_arquivo = "imagem.jpeg"
    
    with open(nome_arquivo, "wb") as f:
        f.write(imagem)
        
    print(nome_arquivo)
    return nome_arquivo


## Envie a imagem coletada para inferência no modelo disponibilizado:
#isso deu bastante trabalho e tive que usar a IA para me ajudar na formatacao da imagem e o modelo da openia 
def enviar_imagem(imagem_coletada):
    with open(imagem_coletada, "rb") as image_file:
        imagem_bytes = image_file.read()

    img_base64_str = base64.b64encode(imagem_bytes).decode('utf-8')
    imagem_data_url = f"data:image/jpeg;base64,{img_base64_str}"

    payload = {
        "model": modelo_api,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": imagem_data_url}}
                ]
            }
        ]
    }

    response = requests.post(
        link_api,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json=payload
    )

    print("[OK]")
    return response.json()




def enviar_resposta_submissao(json_resposta):
    response = requests.post(
        "x",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json=json_resposta
    )
    print(response.status_code)
    response.raise_for_status()
    print(response.text)


def main():
        caminho_imagem = baixar_imagem()
        resultado = enviar_imagem(caminho_imagem)


        print(resultado)

        with open("resposta_modelo.json", "w") as f:
            json.dump(resultado, f, indent=4)
            print("Resposta salva")


        enviar_resposta_submissao(resultado)



#execução
if __name__ == "__main__":
    main()


# In[ ]:




