from sqlalchemy import select
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy import func

# Cria uma base declarativa para definir modelos de tabelas
Base = declarative_base()

# Define a classe User como uma tabela no banco de dados
class User(Base):
    __tablename__ = "user_account"
    # atributos
    id = Column(Integer, primary_key = True)
    name = Column(String)
    fullname = Column(String)

    # Define o relacionamento com a tabela Address
    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User (id={self.id}, name={self.name}, fullname={self.fullname})"

# Define a classe Address como uma tabela no banco de dados
class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    # Define o relacionamento com a tabela User
    user = relationship(
        "User", back_populates="address"
    )

    def __repr__(self):
        return f"Address (id={self.id}, email_address={self.email_address})"

'''
imprime os nomes das tabelas

print(User.__tablename__)
print(Address.__tablename__)
'''

# Cria o mecanismo de conexão com o banco de dados usando o SQLite
engine = create_engine("sqlite://")

# Cria as tabelas no banco de dados
Base.metadata.create_all(engine)

# Inspeção do mecanismo do banco de dados
inspetor_engine = inspect(engine)


# Verifica se a tabela user_account existe no banco de dados
def confere_tabela(inspetor_engine):
    tabela = inspetor_engine.has_table("user_account")
    if tabela:
        print(tabela)
    else:
        print("Tabela não existe no banco de dados")

# Lista todas as tabelas no banco de dados
def lista_tabelas(inspetor_engine):
    print(inspetor_engine.get_table_names())


# Inicia uma sessão para interagir com o banco de dados
with Session(engine) as session:
    # Cria objetos User e Address
    camila = User(
        name='camila',
        fullname = 'Camila louise gomes',
        address=[Address(email_address='camila@gmail.com')]
    )

    julia = User(
        name='julia',
        fullname ='Julia goncalves',
        address =[Address(email_address='julia@hotmail.com'),
                Address(email_address='juliazinha@gmail.com')]
    )

    yuri = User(name='yuri',fullname =' Yuri varela')

# Adiciona os objetos à sessão para persistência no banco de dados
session.add_all([camila,julia,yuri])

# Confirma as mudanças na sessão para efetivar a persistência
session.commit()


# Recupera usuários com base em uma condição de filtragem
def recuperar_usuarios_por_nome(session, *nomes):
    print('Recuperando usuários a partir de condição de filtragem...')
    stmt = select(User).where(User.name.in_(nomes))
    for user in session.scalars(stmt):
        print(user)

# Recupera emails de um usuário com base em seu id
def recuperar_emails_por_id(session, user_id):
    print('Recuperando emails de um usuário a partir de seu id...')
    stmt_address = select(Address).where(Address.user_id.in_(user_id))
    for email_address in session.scalars(stmt_address):
        print(email_address)

# Recupera informações ordenadas
def recuperar_infos_ordenadas(session):
    print('Recuperando infos de maneira ordenada...')
    stmt_order = select(User).order_by(User.fullname.desc())
    for result in session.scalars(stmt_order):
        print(result)

# Conta o total de instâncias em User
def contar_instancias_user(session):
    print('Contando o número total de instâncias em User...')
    stmt_count = select(func.count('*')).select_from(User)
    for result in session.scalars(stmt_count):
        print(result)

# Executa uma consulta SQL para exibir o nome e o email
def exibir_nome_email(session):
    print('Executando statement a partir da connection, exibindo o nome e o email...')
    stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
    # Executa a consulta e exibe os resultados
    connection = engine.connect()
    results = connection.execute(stmt_join).fetchall()
    for result in results:
        print (result)


#confere_tabela(inspetor_engine)
#lista_tabelas(inspetor_engine)
#recuperar_usuarios_por_nome(session, 'camila')
#recuperar_emails_por_id(session, [1])
#recuperar_infos_ordenadas(session)
#contar_instancias_user(session)
#exibir_nome_email(session)