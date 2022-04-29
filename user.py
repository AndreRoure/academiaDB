import PySimpleGUI as sg
from PIL import Image
from io import BytesIO
from datetime import date
import sql

def login():

    layout = [
        [sg.Text('CPF:'), sg.Input(key="cpf")],
        [sg.Text('Senha:'), sg.Input(key="senha")],
        [sg.Button('Login')]
    ]

    window = sg.Window("Login", layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Login":
            with sql.conecta() as conexao:
                with conexao.cursor() as cursor:
                    query = f"call academia.verify({values['senha']}, {int(values['cpf'])}, @result, @tabela);"
                    cursor.execute(query)
                    cursor.execute("select @result, @tabela;")
                    result = cursor.fetchone()
            if result["@result"]:
                window.close()
                direct_page(result["@tabela"], values['cpf'])
                break


def direct_page(flag, cpf):
    if flag == "funcionario":
        funcionario(cpf)
    elif flag == "aluno":
        aluno(cpf)
    else:
        instrutor(cpf)

def funcionario(cpf):
    with sql.conecta() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(f"select * from {'funcionario'} where CPF = {cpf}")
            response = cursor.fetchone()
            cursor.execute(f"select 'funcionario' as tabela, nome, email ,CPF, data_nascimento from funcionario union all select 'instrutor' as tabela, nome, email ,CPF, data_nascimento from instrutor union all select 'aluno' as tabela, nome, email ,CPF, data_nascimento from aluno")
            users = cursor.fetchall()
            values_table = [list(d.values()) for d in users ]
            heading = ["Categoria", "Nome", "Email", "CPF", "Data de Nascimento"]

            if response['foto']:
                data = str(response['foto'])[2:-1]
                data = bytes.fromhex(data)
            else:
                data = None

            layout = [
                [sg.Image(size = (300,300), data=data), sg.Text(f"Nome: {response['nome']}  Email: {response['email']}  Data de Nascimento: {response['data_nascimento']}")],
                [sg.Button("Criar Novo Usuario"), sg.Button("Realizar Exame Fisico")],
                [sg.Text("Usuarios:")],
                [sg.Table(key="table", values=values_table, headings=heading, right_click_menu=["Right", ["Delete", "Edit"]])]
            ]
    window = sg.Window("Funcionario Page", layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Criar Novo Usuario":
            createUser()
            with sql.conecta() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(
                        f"select 'funcionario' as tabela, nome, email ,CPF, data_nascimento from funcionario union all select 'instrutor' as tabela, nome, email ,CPF, data_nascimento from instrutor union all select 'aluno' as tabela, nome, email ,CPF, data_nascimento from aluno")
                    users = cursor.fetchall()
                    values_table = [list(d.values()) for d in users]
                    window["table"].update(values = values_table)
        elif event == "Delete":
            cpf = values_table[values["table"][0]][3]
            categoria = values_table[values["table"][0]][0]
            query = f"delete from {categoria} where CPF = {cpf}"
            with sql.conecta() as conexao:
                with conexao.cursor() as cursor:
                    cursor.execute(query)
                    conexao.commit()
                    cursor.execute(
                        f"select 'funcionario' as tabela, nome, email ,CPF, data_nascimento from funcionario union all select 'instrutor' as tabela, nome, email ,CPF, data_nascimento from instrutor union all select 'aluno' as tabela, nome, email ,CPF, data_nascimento from aluno")
                    users = cursor.fetchall()
                    values_table = [list(d.values()) for d in users]
                    window["table"].update(values=values_table)
        elif event == "Edit":
            cpf = values_table[values["table"][0]][3]
            categoria = values_table[values["table"][0]][0]
            email, senha = editUser()
            with sql.conecta() as conexao:
                with conexao.cursor() as cursor:
                    query = f"update {categoria} set email = '{email}', senha = '{senha}' where CPF = {cpf}"
                    cursor.execute(query)
                    conexao.commit()
                    cursor.execute(
                        f"select 'funcionario' as tabela, nome, email ,CPF, data_nascimento from funcionario union all select 'instrutor' as tabela, nome, email ,CPF, data_nascimento from instrutor union all select 'aluno' as tabela, nome, email ,CPF, data_nascimento from aluno")
                    users = cursor.fetchall()
                    values_table = [list(d.values()) for d in users]
                    window["table"].update(values=values_table)
        elif event == "Realizar Exame Fisico":
            exameFisico(response['CPF'])


    login()

def editUser():
    layout = [
        [sg.Text("Novo Email:"), sg.Input(key="email")],
        [sg.Text("Nova Senha"), sg.Input(key="senha")],
        [sg.Button("Salvar")]
    ]

    window = sg.Window("Editar Usuario", layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Salvar":
            window.close()
            return values['email'], values['senha']

def exameFisico(responsavel):
    today = date.today()
    with sql.conecta() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute("select * from aluno")
            alunos = cursor.fetchall()

    cpfs = dict()
    for x in alunos:
        cpfs[x['nome']] = x['CPF']
    alunos = [x['nome'] for x in alunos]

    layout = [
        [sg.Text("Aluno:")],
        [sg.Combo(alunos, key='aluno')],
        [sg.Text("Altura(m):"), sg.Input(key="Altura")],
        [sg.Text("Peso Atual(kg):"), sg.Input(key="Peso_atual")],
        [sg.Text("Peso Usual(kg):"), sg.Input(key="Peso_usual")],
        [sg.Frame("Bioimpedancia",[
            [sg.Text("Condicionamento:"), sg.Combo(["Sedentario", "Ativo", "Atleta"], key="condicionamento")],
            [sg.Text("Gordura Corporal(%):"), sg.Input(key="Gordura_corporal")],
            [sg.Text("Peso Gordura(Kg):"), sg.Input(key="Peso_gordura")],
            [sg.Text("Gordura Alvo(%):"), sg.Input(key="Gordura_alvo")],
            [sg.Text("IMC:"), sg.Input(key="IMC")],
            [sg.Text("TMB:"), sg.Input(key="TMB")],
            [sg.Text("Peso Ideal(Kg):"), sg.Input(key="Peso_ideal")],
            [sg.Text("Massa magra(%):"), sg.Input(key="Massa_magra")],
            [sg.Text("Peso Massa Magra(Kg):"), sg.Input(key="Peso_massa_magra")],
            [sg.Text("Agua(%):"), sg.Input(key="Agua")],
            [sg.Text("Agua(L):"), sg.Input(key="Agua_L")],
            [sg.Text("Agua Ideal(L):"), sg.Input(key="Agua_ideal")]
        ])],
        [sg.Frame("Dobras Cutaneas e Circuferencias", [
            [sg.Frame("Dobras(mm)", [
                [sg.Text("Subescapular:"), sg.Input(key="Dobra_subescapular")],
                [sg.Text("Triceptal:"), sg.Input(key="Dobra_triceptal")],
                [sg.Text("Axilar Media:"), sg.Input(key="Dobra_axilar_media")],
                [sg.Text("Toracica:"), sg.Input(key="Dobra_toracica")],
                [sg.Text("Abdominal:"), sg.Input(key="Dobra_abdominal")],
                [sg.Text("Medial de Coxa:"), sg.Input(key="Dobra_medial_coxa")],
                [sg.Text("Panturrilha:"), sg.Input(key="Dobra_panturrilha")]
            ])],
            [sg.Frame("Circuferencias(cm)", [
                [sg.Text("Braco:"), sg.Input(key="Circu_braco")],
                [sg.Text("Cintura:"), sg.Input(key="Circu_cintura")],
                [sg.Text("Abdomen:"), sg.Input(key="Circu_abdomen")],
                [sg.Text("Quadril:"), sg.Input(key="Circu_quadril")],
                [sg.Text("Panturrilha:"), sg.Input(key="Circu_panturrilha")]
            ])]
        ])],
        [sg.Button("Salvar")]
    ]

    window = sg.Window("Exame Fisico", layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Salvar":
            with sql.conecta() as conexao:
                with conexao.cursor() as cursor:
                    query = f"insert into Exame_fisico (data, Funcionario_CPF, Aluno_CPF, Altura, Peso_atual, Peso_usual) values {today.strftime('%Y-%m-%d'), responsavel, cpfs[values['aluno']], values['Altura'], values['Peso_atual'], values['Peso_usual']}"
                    cursor.execute(query)
                    conexao.commit()
                    if values['condicionamento']:
                        query = f"insert into Bioimpedancia (Condicionamento, Gordura_corporal, Peso_gordura, Gordura_alvo, IMC, TMB, Peso_ideal, Massa_magra, Peso_massa_magra, Agua, Agua_L, Agua_ideal, Exame_fisico_data, Exame_fisico_Aluno_CPF)\
                                    values {values['condicionamento'], values['Gordura_corporal'], values['Peso_gordura'], values['Gordura_alvo'], values['IMC'], values['TMB'], values['Peso_ideal'], values['Massa_magra'], values['Peso_massa_magra'], values['Agua'], values['Agua_L'], values['Agua_ideal'], today.strftime('%Y-%m-%d'), cpfs[values['aluno']]}"
                        cursor.execute(query)
                        conexao.commit()
                    if values['Dobra_subescapular']:
                        query = f"insert into DobrasCutaneas_Circuferencias (Dobra_subescapular, Dobra_triceptal, Dobra_axilar_media, Dobra_toracica, Dobra_abdominal, Dobra_medial_coxa, Dobra_panturrilha, Circu_braco, Circu_cintura, Circu_abdomen, Circu_quadril, Circu_panturrilha, Exame_fisico_data, Exame_fisico_Aluno_CPF)\
                                    values {values['Dobra_subescapular'], values['Dobra_triceptal'], values['Dobra_axilar_media'], values['Dobra_toracica'], values['Dobra_abdominal'], values['Dobra_medial_coxa'], values['Dobra_panturrilha'], values['Circu_braco'], values['Circu_cintura'], values['Circu_abdomen'], values['Circu_quadril'], values['Circu_panturrilha'], today.strftime('%Y-%m-%d'), cpfs[values['aluno']]}"
                        cursor.execute(query)
                        conexao.commit()
            window.close()
            break


def aluno(cpf):
    with sql.conecta() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(f"select * from {'aluno'} where CPF = {cpf}")
            response = cursor.fetchone()
            cursor.execute(f"select Tipo from Treino where Aluno_CPF = {cpf}")
            treinos = cursor.fetchall()
            treinos = [d['Tipo'] for d in treinos]
            cursor.execute(f"select data from Exame_fisico where Aluno_CPF = {cpf}")
            exames = cursor.fetchall()
            exames = [d['data'] for d in exames]

            if response['foto']:
                data = str(response['foto'])[2:-1]
                data = bytes.fromhex(data)
            else:
                data = None

        layout = [
            [sg.Image(size=(300, 300), data=data), sg.Text(
                    f"Nome: {response['nome']}  Email: {response['email']}  Data de Nascimento: {response['data_nascimento']}")],
            [sg.Frame("Treinos", [[sg.Listbox(key='treino', values=treinos, right_click_menu=["rTreino",["View::vTreino", "Delete"]])]]), sg.Frame("Exames Fisicos", [[sg.Listbox(key="exame", values=exames, right_click_menu=["rExame", ['View::vExame']])]])],
        ]
    window = sg.Window("Aluno Page", layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            login()
            break



# def viewExame(data, cpf):
#     print(date.today().strftime('%Y-%m-%d') == data)
#     with sql.conecta() as conexao:
#         with conexao.cursor() as cursor:
#             response = dict()
#             cursor.execute(f"select * from Exame_fisico where Aluno_CPF = {cpf} and date(data) = {data.strftime('%Y-%m-%d')}")
#             exame = cursor.fetchone()
#             print(exame)
#             cursor.execute(f"select * from Bioimpedancia where Exame_fisico_Aluno_CPF = {cpf} and Exame_fisico_data = {data.strftime('%Y-%m-%d')}")
#             response.update(cursor.fetchone())
#             cursor.execute(
#                 f"select * from DobrasCutaneas_Circuferencias where Exame_fisico_Aluno_CPF = {cpf} and Exame_fisico_data = {data.strftime('%Y-%m-%d')}")
#             response.update(cursor.fetchone())
#     print(response)


def instrutor(cpf):
    with sql.conecta() as conexao:
        with conexao.cursor() as cursor:
            cursor.execute(f"select * from {'instrutor'} where CPF = {cpf}")
            response = cursor.fetchone()
            cursor.execute(f"select Codigo, Nome, Duracao from Aula where Instrutor_CPF = {cpf}")



            if response['foto']:
                data = str(response['foto'])[2:-1]
                data = bytes.fromhex(data)
            else:
                data = None

        layout = [
            [sg.Image(size=(300, 300), data=data), sg.Text(
                f"Nome: {response['nome']}  Email: {response['email']}  Data de Nascimento: {response['data_nascimento']}")],
            # [sg.Frame("Treinos", [
            #     [sg.Listbox(key='treino', values=treinos, right_click_menu=["rTreino", ["View::vTreino", "Delete"]])]]),
            #  sg.Frame("Exames Fisicos",
            #           [[sg.Listbox(key="exame", values=exames, right_click_menu=["rExame", ['View::vExame']])]])],
        ]
    window = sg.Window("Instrutor Page", layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            login()
            break


def createUser():
    layout = [
        [sg.Text("Categoria:")],
        [sg.Combo(["funcionario", "instrutor", "aluno"], key="categoria")],
        [sg.Text("CPF:"), sg.Input(key="cpf")],
        [sg.Text("Nome:"), sg.Input(key="nome")],
        [sg.Text("Email:"), sg.Input(key="email")],
        [sg.Text("Senha"), sg.Input(key="senha")],
        [sg.Text("Data de Nascimento"), sg.In(key="data"), sg.CalendarButton(target="data", button_text="Selecionar", format="%Y-%m-%d")],
        [sg.Text("Foto:"), sg.FileBrowse(key="foto")],
        [sg.Button("Salvar")]
    ]

    window = sg.Window("Novo Usuario", layout)
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Salvar":
            bdata = BytesIO()
            img = Image.open(values['foto'])
            img.resize((200, 200))
            img.save(bdata, 'PNG')
            bdata.seek(0)
            img = bdata.read()
            with sql.conecta() as conexao:
                with conexao.cursor() as cursor:
                    query = f"insert into {values['categoria']} (CPF, nome, email, senha, data_nascimento, foto) VALUES {values['cpf'], values['nome'], values['email'], values['senha'], values['data'], img.hex()}"
                    cursor.execute(query)
                    conexao.commit()
            window.close()
            break