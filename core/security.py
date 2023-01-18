from passlib.context import CryptContext

# bcrypt - uma dos schemas mais poderoso para criação de hash e senhas em python
CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verificar_senha(senha: str, hash_senha:str) -> bool:
    """"
    Função para verificar se senha está correta, comparando a
    senha em texto puro, informado pelo usuário, e o hash da senha 
    que estará salvo no banco de dados durante a criação da conta
    """

    return CRIPTO.verify(senha, hash_senha)

def gerar_hash_senha(senha: str) -> str:
    """
    Função que gera e retorna o hash da senha
    """

    return CRIPTO.hash(senha)
