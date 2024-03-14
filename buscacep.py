import requests

class CEPNaoExisteException(Exception):
    pass

def endereco(rua):
    url = f'https://viacep.com.br/ws/{rua}/json/'
    r = requests.get(url)
    if r.status_code != 200:
        return CEPNaoExisteException
    
    info = r.json()
    return info['logradouro']


