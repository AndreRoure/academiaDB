delimiter $$
create procedure verify (in pasword char(45), in id int, out result bool, out tipo varchar(20))
	begin
		declare c int default 0;
		select count(*), tabela as t into c, tipo from
			(
				select 'funcionario' as tabela, CPF, senha from funcionario
				union all
				select 'instrutor' as tabela, CPF, senha from instrutor
                union all
                select 'aluno' as tabela, CPF, senha from aluno
			) subquery where pasword = senha and id = CPF limit 1;
            
            if (c > 0) then
				set result = true;
            else
				set result = false;
			end if;
    end $$
    delimiter ;