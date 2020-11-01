

create sequence sq_persona start with 18119 increment by 1 maxvalue 999999999 minvalue 18119 cycle;
insert into dim_instituciones (
                cole_bilingue,
                cole_caracter,
                cole_genero,
                cole_jornada,
                cole_naturaleza,
                cole_nombre_sede,
                cole_calendario)
                select
                "COLE_BILINGUE",
                "COLE_CARACTER",
                "COLE_GENERO",
                "COLE_JORNADA",
                "COLE_NATURALEZA",
                "COLE_NOMBRE_SEDE",
                "COLE_CALENDARIO"
                from table_temp;
                insert into dim_lugares (
                cole_area_ubicacion,
                cole_mcpio_ubicacion,
                estu_mcpio_presentacion,
                estu_reside_mcpio)
                select
                "COLE_AREA_UBICACION",
                "COLE_MCPIO_UBICACION",
                "ESTU_MCPIO_PRESENTACION",
                "ESTU_MCPIO_RESIDE"
                from table_temp;
                insert into dim_pru_c_nat (
                desemp_c_naturales)
                select
                "DESEMP_C_NATURALES"
                from table_temp;
                insert into dim_pru_ingles (
                desemp_ingles)
                select
                "DESEMP_INGLES"
                from table_temp;
                insert into dim_pru_lec_crit (
                desemp_lec_crit)
                select
                "DESEMP_LECTURA_CRITICA"
                from table_temp;
                insert into dim_pru_mat (
                desemp_mat)
                select
                "DESEMP_MATEMATICAS"
                from table_temp;
                insert into dim_pru_soc_ciu (
                desemp_soc_ciu)
                select
                "DESEMP_SOCIALES_CIUDADANAS"
                from table_temp;
                insert into dim_tiempo (
                ano)
                select
                "ANO"
                from table_temp;

alter table fact_saber11 alter column id_estudiante set default nextval('sq_persona');





do $$
declare
conta integer;
orden_sql text;
orden_sql1 text;
orden_sql2 text;
orden_sql3 text;
orden_sql4 text;
orden_sql5 text;
orden_sql6 text;
orden_sql7 text;
orden_sql8 text;
begin
conta := count(*) from fact_saber11;
orden_sql := 'create sequence sequen start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
execute orden_sql;
orden_sql1 := 'create sequence sequen1 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
execute orden_sql1;
orden_sql2 := 'create sequence sequen2 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
execute orden_sql2;
orden_sql3 := 'create sequence sequen3 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
execute orden_sql3;
orden_sql4 := 'create sequence sequen4 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
execute orden_sql4;
orden_sql5 := 'create sequence sequen5 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
execute orden_sql5;
orden_sql6 := 'create sequence sequen6 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
execute orden_sql6;
orden_sql7 := 'create sequence sequen7 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
execute orden_sql7;
orden_sql8 := 'create sequence sequen8 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
execute orden_sql8;
end $$;


do $$
declare
conta1 integer;
uno integer;
conta integer;
orden_sql text;
begin
conta1 := count(*) from fact_saber11;
uno := 1;
conta := conta1+uno;
orden_sql := 'create sequence sequen99 start with '|| conta ||' increment by 1 maxvalue 99999999 minvalue '|| conta ||' cycle';
execute orden_sql;
raise notice 'Value: %', conta;
end$$;


-- script para comparar la existencia de columnas en dos tablas
select column_name from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='your_table_name1'
except
select column_name from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='your_table_name2'

#elimina carpeta desde python
from shutil import rmtree
rmtree("carpeta")