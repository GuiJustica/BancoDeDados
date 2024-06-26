--1 Histórico escolar de qualquer aluno, retornando o código e nome da disciplina, semestre e ano que a disciplina foi cursada e nota final
SELECT id_aluno, hist_aluno1.id_disciplina, disciplina1.nome, hist_aluno1.nota_final, semestre, ano
FROM hist_aluno1 JOIN disciplina1 ON disciplina1.id_disciplina = hist_aluno1.id_disciplina
WHERE id_aluno = 1; --> Mude o valor para saber o histórico específico de cada aluno


--2 Histórico de disciplinas ministradas por qualquer professor, com semestre e ano
SELECT id_depto, departamento1.nome, departamento1.id_chefe, professor1.nome
FROM departamento1 JOIN professor1 ON departamento1.id_chefe = professor1.id_professor


--3 Listar alunos que já se formaram (foram aprovados em todos os cursos de uma matriz curricular)
SELECT aluno1.id_aluno, aluno1.nome
FROM aluno1
JOIN hist_aluno1 ON aluno1.id_aluno = hist_aluno1.id_aluno
GROUP BY aluno1.id_aluno, aluno1.nome
HAVING MIN(hist_aluno1.nota_final) >= 5;


--3.1 Listar alunos que já se formaram (foram aprovados em todos os cursos de uma matriz curricular) em um determinado semestre de um ano
SELECT aluno1.id_aluno, aluno1.nome
FROM aluno1
JOIN hist_aluno1 ON aluno1.id_aluno = hist_aluno1.id_aluno
WHERE hist_aluno1.semestre = 1 AND hist_aluno1.ano = 2025 --> Mude o valor para um semestre(1 ou 2) e ano(2024 ou 2025)
GROUP BY aluno1.id_aluno, aluno1.nome
HAVING MIN(hist_aluno1.nota_final) >= 5;


--4 Listar todos os professores que são chefes de departamento, junto com o nome do departamento
SELECT professor1.nome, departamento1.id_chefe, departamento1.nome
FROM professor1 JOIN departamento1 ON id_chefe = id_professor


--5 Saber quais alunos formaram um grupo de TCC e qual professor foi o orientador
SELECT aluno1.nome, tcc1.titulo,aluno_tcc1.id_aluno, tcc1.id_professor, professor1.nome
FROM aluno_tcc1 JOIN tcc1 ON aluno_tcc1.id_tcc = tcc1.id_tcc
JOIN aluno1 ON aluno1.id_aluno = aluno_tcc1.id_aluno
JOIN professor1 ON tcc1.id_professor = professor1.id_professor
WHERE tcc1.id_tcc = 1; --> Mude o valor para saber os alunos de um grupo de tcc
