create view sessoes as
select Instrutor_CPF, Codigo, Nome, Data, Hora from
Aula inner join Sessao on aula.Codigo = sessao.Aula_codigo;