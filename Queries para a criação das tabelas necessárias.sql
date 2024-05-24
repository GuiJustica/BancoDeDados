  --TABELA ALUNO1
  CREATE TABLE IF NOT EXISTS aluno1 (
      id_aluno serial NOT NULL,
      PRIMARY KEY(id_aluno),
      nome VARCHAR(100),
      id_curso int
  );




  --TABELA PROFESSOR1
  CREATE TABLE IF NOT EXISTS professor1
  (
      id_professor serial NOT NULL,
      nome VARCHAR(255),
      PRIMARY KEY (id_professor)
  );




  --TABELA CURSO1
  CREATE TABLE IF NOT EXISTS curso1
  (
    id_curso serial NOT NULL,
    nome VARCHAR(255),
    id_depto int,
    PRIMARY KEY (id_curso)
  );




  --TABELA DEPARTAMENTO1
  CREATE TABLE IF NOT EXISTS departamento1
  (
    id_depto serial NOT NULL,
    nome VARCHAR(255),
    id_chefe int,
    PRIMARY KEY (id_depto)
  );




  --TABELA DISCIPLINA1
  CREATE TABLE IF NOT EXISTS disciplina1
  (
    id_disciplina serial NOT NULL,
    nome VARCHAR(255),
    id_curso int,
    PRIMARY KEY (id_disciplina),
    FOREIGN KEY (id_curso) REFERENCES curso1(id_curso)
  );




  --TABELA MATRIZ CURRICULAR1
  CREATE TABLE IF NOT EXISTS matriz_curricular1
  (
    id_matriz serial NOT NULL,
    id_curso int,
    PRIMARY KEY (id_matriz),
    FOREIGN KEY (id_curso) REFERENCES curso1(id_curso)
  );




  --TABELA MATRIZ CURRICULAR DISCIPLINA1
  CREATE TABLE IF NOT EXISTS matrizcurricular_disciplina1
  (
    id_matriz int,
    id_disciplina int,
    semestre int,
    ano int,
    FOREIGN KEY (id_matriz) REFERENCES matriz_curricular1(id_matriz),
    FOREIGN KEY (id_disciplina) REFERENCES disciplina1(id_disciplina)
  );




  --TABELA HIST_ALUNO1
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




  --TABELA HIST_PROFESSOR1
  CREATE TABLE IF NOT EXISTS hist_professor1
  (
    id_professor int ,
    id_disciplina int ,
    semestre int,
    ano int,
    FOREIGN KEY (id_professor) REFERENCES professor1(id_professor),
    FOREIGN KEY (id_disciplina) REFERENCES disciplina1(id_disciplina)
  );




  --TABELA TCC1
  CREATE TABLE IF NOT EXISTS tcc1
  (
    id_tcc serial NOT NULL PRIMARY KEY,
    titulo VARCHAR(255),
    id_professor int,
    FOREIGN KEY (id_professor) REFERENCES professor1(id_professor)
  );




  --TABELA ALUNO_TCC1
  CREATE TABLE IF NOT EXISTS aluno_tcc1
  (
    id_tcc int,
    id_aluno int,
    FOREIGN KEY (id_aluno) REFERENCES aluno1(id_aluno),
    FOREIGN KEY (id_tcc) REFERENCES tcc1(id_tcc)
  );



