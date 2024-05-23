import random
import numpy as np
from faker import Faker
import psycopg2
from psycopg2 import sql
import os

fake = Faker("pt_BR")

config = {
    'dbname':'',
    'user':'',
    'password':'',
    'host':'',
    'port': ''
}


def connect():
    # Estabelecer a conexão
    conn = psycopg2.connect(**config)
    print("Conexão bem-sucedida!")

    # Criar um cursor
    with conn.cursor() as cur:
        # Executar uma consulta SQL
        cur.execute("SELECT NOW();")
        criar_queries(cur,conn)



def criar_queries(cur,conn):
    #Excluir Tabelas para gerar novos dados
    cur.execute("DROP TABLE IF EXISTS aluno1,aluno_tcc1,curso1,departamento1,disciplina1,hist_aluno1,hist_professor1,matriz_curricular1,matrizcurricular_disciplina1,professor1,tcc1;")
    print("Tabelas Excluídas!(ou não)")

    #TABELA ALUNO1
    create_table_query = """
    CREATE TABLE IF NOT EXISTS aluno1 (
        id_aluno serial NOT NULL,
        PRIMARY KEY(id_aluno),
        nome VARCHAR(100),
        id_curso int
    );
    """

    cur.execute(create_table_query)


    #TABELA PROFESSOR1
    create_table_query = """
    CREATE TABLE IF NOT EXISTS professor1
    (
        id_professor serial NOT NULL,
        nome VARCHAR(255),
        PRIMARY KEY (id_professor)

    );
    """

    cur.execute(create_table_query)


    #TABELA CURSO1
    create_table_query = """
    CREATE TABLE IF NOT EXISTS curso1
(
    id_curso serial NOT NULL,
    nome VARCHAR(255),
    id_depto int,
    PRIMARY KEY (id_curso)


);"""

    cur.execute(create_table_query)


    #TABELA DEPARTAMENTO1
    create_table_query = """
    CREATE TABLE IF NOT EXISTS departamento1
    (
        id_depto serial NOT NULL,
        nome VARCHAR(255),
        id_chefe int,
        PRIMARY KEY (id_depto)


    );"""

    cur.execute(create_table_query)


    #TABELA DISCIPLINA1
    create_table_query = """
    CREATE TABLE IF NOT EXISTS disciplina1
    (
        id_disciplina serial NOT NULL,
        nome VARCHAR(255),
        id_curso int,
        PRIMARY KEY (id_disciplina),
        FOREIGN KEY (id_curso) REFERENCES curso1(id_curso)
    );
    """
    cur.execute(create_table_query)


    #TABELA MATRIZ CURRICULAR1
    create_table_query = """
    CREATE TABLE IF NOT EXISTS matriz_curricular1
    (
        id_matriz serial NOT NULL,
        id_curso int,
        PRIMARY KEY (id_matriz),
        FOREIGN KEY (id_curso) REFERENCES curso1(id_curso)
    );"""

    cur.execute(create_table_query)


    #TABELA MATRIZ CURRICULAR DISCIPLINA1
    create_table_query = """
    CREATE TABLE IF NOT EXISTS matrizcurricular_disciplina1
    (
        id_matriz int,
        id_disciplina int,
        semestre int,
        ano int,
        FOREIGN KEY (id_matriz) REFERENCES matriz_curricular1(id_matriz),
        FOREIGN KEY (id_disciplina) REFERENCES disciplina1(id_disciplina)
    );"""

    cur.execute(create_table_query)


    #TABELA HIST_ALUNO1
    create_table_query = """
    CREATE TABLE IF NOT EXISTS hist_aluno1
(
    id_aluno int ,
    id_disciplina int ,
    nota_final int,
    semestre int,
    ano int,
    FOREIGN KEY (id_aluno) REFERENCES aluno1(id_aluno),
    FOREIGN KEY (id_disciplina) REFERENCES disciplina1(id_disciplina)
);
"""
    cur.execute(create_table_query)


    #TABELA HIST_PROFESSOR1
    create_table_query = """
    CREATE TABLE IF NOT EXISTS hist_professor1
    (
        id_professor int ,
        id_disciplina int ,
        semestre int,
        ano int,
        FOREIGN KEY (id_professor) REFERENCES professor1(id_professor),
        FOREIGN KEY (id_disciplina) REFERENCES disciplina1(id_disciplina)
    );"""

    cur.execute(create_table_query)


    #TABELA TCC1
    create_table_query = """
    CREATE TABLE IF NOT EXISTS tcc1
(
    id_tcc serial NOT NULL PRIMARY KEY,
    titulo VARCHAR(255),
    id_professor int,
    FOREIGN KEY (id_professor) REFERENCES professor1(id_professor)
);"""

    cur.execute(create_table_query)


    #TABELA ALUNO_TCC1
    create_table_query = """
    CREATE TABLE IF NOT EXISTS aluno_tcc1
(
    id_tcc int,
    id_aluno int,
    FOREIGN KEY (id_aluno) REFERENCES aluno1(id_aluno),
    FOREIGN KEY (id_tcc) REFERENCES tcc1(id_tcc)
);"""

    cur.execute(create_table_query)

    conn.commit()
    print("Tabelas Criadas!")
    alter_queries(cur,conn)

def alter_queries(cur,conn):

    alter_query = """
    ALTER TABLE aluno1
    ADD CONSTRAINT id_curso FOREIGN KEY (id_curso) REFERENCES curso1(id_curso)
    ON DELETE CASCADE;

    ALTER TABLE curso1
    ADD CONSTRAINT id_depto FOREIGN KEY (id_depto) REFERENCES departamento1(id_depto)
    ON DELETE CASCADE;

    ALTER TABLE departamento1
    ADD CONSTRAINT id_chefe FOREIGN KEY (id_chefe) REFERENCES professor1(id_professor)
    ON DELETE CASCADE;
    """
    cur.execute(alter_query)

    conn.commit()
    print("Tabelas Alteradas!")
    insert_queries(cur,conn)


def insert_queries(cur,conn):
    #Professor
    insert_query = """
    INSERT INTO professor1 (id_professor,nome)
    VALUES (%s,%s);
    """
    for i in range(1,19):
        gender = np.random.choice(["M", "F"], p=[0.5, 0.5])
        first_name = fake.first_name_male() if gender =="M" else fake.first_name_female()
        data = (i,first_name)
        cur.execute(insert_query, data)
        conn.commit()
    #Departamento
    insert_query = """
    INSERT INTO departamento1 (id_depto, nome,id_chefe)
    VALUES (%s,%s,%s);
    """
    id_chefe_ran = random.sample(range(1, 9), 3)
    nome_dpto=["Ciência da Computação","Engenharia Elétrica","Engenharia Química"]
    for i in range(len(id_chefe_ran)):
        data = (i+1,nome_dpto[i],id_chefe_ran[i])
        cur.execute(insert_query,data)
        conn.commit()
    #CURSO
    insert_query = """
    INSERT INTO curso1 (id_curso,nome, id_depto)
    VALUES (1,'Ciência da Computação',1);

    INSERT INTO curso1 (id_curso,nome, id_depto)
    VALUES (2,'Engenharia Elétrica',2);

    INSERT INTO curso1 (id_curso,nome, id_depto)
    VALUES (3,'Engenharia Química',3);
    """

    cur.execute(insert_query, data)
    conn.commit()


    #ALUNO
    insert_query = """
    INSERT INTO aluno1 (id_aluno,nome, id_curso)
    VALUES (%s,%s, %s);
    """
    for i in range(1,51):
        gender = np.random.choice(["M", "F"], p=[0.5, 0.5])
        first_name = fake.first_name_male() if gender =="M" else fake.first_name_female()
        data = (i,first_name,random.randint(1, 3))
        cur.execute(insert_query, data)
        conn.commit()



    #Disciplina
    insert_query = """
    INSERT INTO disciplina1 VALUES (1, 'Banco de Dados', 1);
    INSERT INTO disciplina1 VALUES (2, 'Automatos', 1);
    INSERT INTO disciplina1 VALUES (3, 'Algoritmos', 1);
    INSERT INTO disciplina1 VALUES (4, 'Python', 1);
    INSERT INTO disciplina1 VALUES (5, 'Mobile', 1);
    INSERT INTO disciplina1 VALUES (6, 'Java', 1);


    INSERT INTO disciplina1 VALUES (7, 'Fios', 2);
    INSERT INTO disciplina1 VALUES (8, 'Pilhas', 2);
    INSERT INTO disciplina1 VALUES (9, 'Cabos', 2);
    INSERT INTO disciplina1 VALUES (10,'Eletricidade', 2);
    INSERT INTO disciplina1 VALUES (11,'Corrente', 2);
    INSERT INTO disciplina1 VALUES (12,'Lâmpada', 2);

    INSERT INTO disciplina1 VALUES (13, 'Reações Químicas', 3);
    INSERT INTO disciplina1 VALUES (14, 'Fusão', 3);
    INSERT INTO disciplina1 VALUES (15, 'Elementos', 3);
    INSERT INTO disciplina1 VALUES (16, 'Laboratório',3);
    INSERT INTO disciplina1 VALUES (17, 'Resíduos Tóxicos',3);
    INSERT INTO disciplina1 VALUES (18, 'Química Orgânica',3);
    """
    cur.execute(insert_query)
    conn.commit()



    #TCC
    insert_query = """
    INSERT INTO tcc1 (id_tcc,titulo,id_professor)
    VALUES (%s,%s,%s);
    """

    id_prof_tcc = random.sample(range(1, 19), 10)
    for i in range(len(id_prof_tcc)):
        data = (i+1,fake.word(),id_prof_tcc[i])
        cur.execute(insert_query,data)
        conn.commit()



    #AlunoTCC
    insert_query = """
    INSERT INTO aluno_tcc1 (id_tcc,id_aluno)
    VALUES (%s,%s);
    """

    id_aluno_tcc = random.sample(range(1, 51), 21)
    id_tcc_tcc1 = random.sample(range(1, 11), 10)
    id_tcc_tcc2 = random.sample(range(1, 11), 10)
    for i in range(1,len(id_aluno_tcc)):
        if i <= 8:
            data = (id_tcc_tcc1[i],id_aluno_tcc[i])
        else:
            data = (id_tcc_tcc2[i-11],id_aluno_tcc[i])
        cur.execute(insert_query,data)
        conn.commit()


    #Matriz curricular
    insert_query = """
    INSERT INTO matriz_curricular1 (id_matriz,id_curso)
    VALUES (%s,%s);
    """

    for i in range(1,4):
        data = (i,i)
        cur.execute(insert_query,data)
        conn.commit()

    #Matriz curricular disciplina
    insert_query = """
    INSERT INTO matrizcurricular_disciplina1 VALUES (1, 1, 1, 2024);
    INSERT INTO matrizcurricular_disciplina1 VALUES (1, 2, 1, 2024);
    INSERT INTO matrizcurricular_disciplina1 VALUES (1, 3, 2, 2024);
    INSERT INTO matrizcurricular_disciplina1 VALUES (1, 4, 2, 2024);
    INSERT INTO matrizcurricular_disciplina1 VALUES (1, 5, 1, 2025);
    INSERT INTO matrizcurricular_disciplina1 VALUES (1, 6, 1, 2025);

    INSERT INTO matrizcurricular_disciplina1 VALUES (2, 7, 1, 2024);
    INSERT INTO matrizcurricular_disciplina1 VALUES (2, 8, 1, 2024);
    INSERT INTO matrizcurricular_disciplina1 VALUES (2, 9, 2, 2024);
    INSERT INTO matrizcurricular_disciplina1 VALUES (2, 10, 2, 2024);
    INSERT INTO matrizcurricular_disciplina1 VALUES (2, 11, 1, 2025);
    INSERT INTO matrizcurricular_disciplina1 VALUES (2, 12, 1, 2025);


    INSERT INTO matrizcurricular_disciplina1 VALUES (3, 13, 1, 2024);
    INSERT INTO matrizcurricular_disciplina1 VALUES (3, 14, 1, 2024);
    INSERT INTO matrizcurricular_disciplina1 VALUES (3, 15, 2, 2024);
    INSERT INTO matrizcurricular_disciplina1 VALUES (3, 16, 2, 2024);
    INSERT INTO matrizcurricular_disciplina1 VALUES (3, 17, 1, 2025);
    INSERT INTO matrizcurricular_disciplina1 VALUES (3, 18, 1, 2025);
    """
    cur.execute(insert_query,data)
    conn.commit()


    #Histórico do Aluno
    cur.execute("SELECT id_curso FROM aluno1")
    aluno_cursos_guardado=cur.fetchall()


    for i in range(len(aluno_cursos_guardado)-1):
        cur.execute("""SELECT disciplina1.id_disciplina,semestre,ano FROM disciplina1
                    JOIN matrizcurricular_disciplina1 ON disciplina1.id_disciplina = matrizcurricular_disciplina1.id_disciplina
                    WHERE id_curso=%s""" % aluno_cursos_guardado[i])
        id_disciplina_guardada=cur.fetchall()
        for x in range(len(id_disciplina_guardada)-1):

            insert_query = """
            INSERT INTO hist_aluno1 (id_aluno,id_disciplina,nota_final,semestre,ano)
            VALUES (%s,%s,%s,%s,%s);
            """
            data = (i+1,id_disciplina_guardada[x][0],random.randint(0,10),id_disciplina_guardada[x][1],id_disciplina_guardada[x][2])
            cur.execute(insert_query,data)
            conn.commit()


    #ARRUMAR
    cur.execute("SELECT id_curso FROM aluno1 WHERE id_aluno=%s" % 50)
    aluno_50=cur.fetchall()

    cur.execute("""SELECT disciplina1.id_disciplina,semestre,ano FROM disciplina1
                JOIN matrizcurricular_disciplina1 ON disciplina1.id_disciplina = matrizcurricular_disciplina1.id_disciplina
                WHERE id_curso=%s""" % aluno_50[0])
    id_disciplina_guardada2=cur.fetchall()
    for x in range(len(id_disciplina_guardada2)):

        insert_query = """
        INSERT INTO hist_aluno1 (id_aluno,id_disciplina,nota_final,semestre,ano)
        VALUES (%s,%s,%s,%s,%s);
        """
        data = (50,id_disciplina_guardada2[x][0],random.randint(5,10),id_disciplina_guardada2[x][1],id_disciplina_guardada2[x][2])
        cur.execute(insert_query,data)
        conn.commit()





    #Histórico do Professor
    cur.execute("SELECT id_professor FROM professor1")
    id_professor_guardado=cur.fetchall()

    cur.execute("SELECT id_disciplina,semestre,ano FROM matrizcurricular_disciplina1")
    id_d_semeste_ano_gaurdados=cur.fetchall()

    for i in range(len(id_professor_guardado)-1):
        insert_query = """
        INSERT INTO hist_professor1 (id_professor,id_disciplina,semestre,ano)
        VALUES (%s,%s,%s,%s);
        """
        aleatorio = random.randint(0,8)
        data = (i+1,i+1,id_d_semeste_ano_gaurdados[aleatorio][1],id_d_semeste_ano_gaurdados[aleatorio][2])
        cur.execute(insert_query,data)
        conn.commit()

    print("Dados inseridos com sucesso!")


if __name__ == "__main__":
    connect()
