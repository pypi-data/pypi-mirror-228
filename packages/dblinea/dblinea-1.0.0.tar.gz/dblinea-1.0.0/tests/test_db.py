import os
import unittest

import pandas as pd
import psycopg2
from pandas.testing import assert_frame_equal
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import Table
from sqlalchemy.dialects import postgresql
from sqlalchemy.engine import Engine
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.sql.elements import TextClause
from sqlalchemy.types import INTEGER, VARCHAR

from dblinea import DBBase


class TestAbilityToTest(unittest.TestCase):
    def test_ability_to_test(self):
        # Apenas verifica se é possivel executar os testes.
        self.assertEqual(1, 1)


class TestDaoPostgres(unittest.TestCase):
    def setUp(self):
        print("Setup setUp")
        self.dbhost = os.environ.get("POSTGRES_HOST", "localhost")
        self.dbport = os.environ.get("POSTGRES_PORT", "5432")
        self.dbuser = os.environ.get("POSTGRES_USER", "postgres")
        self.dbpass = os.environ.get("POSTGRES_PASSWORD", "postgres")
        self.dbname = "db_test"
        self.schema = "sch_test"
        self.table = "tb_sample"

        # Create a Test database
        con = psycopg2.connect(host=self.dbhost, user=self.dbuser, password=self.dbpass, port=self.dbport)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with con.cursor() as cursor:
            cursor.execute(f"DROP DATABASE IF EXISTS {self.dbname}")
            cursor.execute(f"create database {self.dbname}")
            cursor.close()

        con = psycopg2.connect(
            host=self.dbhost,
            user=self.dbuser,
            password=self.dbpass,
            port=self.dbport,
            database=self.dbname,
        )
        # Create Schema
        with con.cursor() as cursor:
            cursor.execute(f"DROP SCHEMA IF EXISTS {self.schema} CASCADE")
            cursor.execute(f"CREATE SCHEMA {self.schema};")
            # Create sample Table
            cursor.execute(f"DROP TABLE IF EXISTS {self.schema}.{self.table}")
            cursor.execute(
                f"create table {self.schema}.{self.table} (id serial primary key, name varchar(100), age int)"
            )
            cursor.close()
            con.commit()

        self.dao = DBBase(
            dbhost=self.dbhost,
            dbport=self.dbport,
            dbuser=self.dbuser,
            dbpass=self.dbpass,
            dbname=self.dbname,
        )

        self.select_sql = f"Select * from {self.schema}.{self.table}"

    def add_valid_record(self):
        con = psycopg2.connect(
            host=self.dbhost,
            user=self.dbuser,
            password=self.dbpass,
            port=self.dbport,
            database=self.dbname,
        )
        # Create Schema
        with con.cursor() as cursor:
            # Insert new record
            cursor.execute(f"insert into {self.schema}.{self.table} values (1, 'jose', 30)")
            cursor.close()
            con.commit()

    def test_get_db_uri(self):
        uri = ("postgresql+psycopg2://%(username)s:%(password)s@%(host)s:%(port)s/%(database)s") % {
            "username": self.dbuser,
            "password": self.dbpass,
            "host": self.dbhost,
            "port": self.dbport,
            "database": self.dbname,
        }

        self.assertEqual(self.dao._database.get_db_uri(), uri)

    def test_get_db_uri_without_dbname(self):
        dao = DBBase(
            dbhost=self.dbhost,
            dbport=self.dbport,
            dbuser=self.dbuser,
            dbpass=self.dbpass,
        )

        uri = "postgresql+psycopg2://postgres:postgres@localhost:5432"

        self.assertEqual(dao._database.get_db_uri(), uri)

    def test_set_database(self):
        dao = DBBase(database="gavo")

        engine = dao.get_engine()

        self.assertTrue(isinstance(engine, Engine))

    def test_set_database_not_available(self):
        self.assertRaises(Exception, DBBase.__init__, "test")

        # Same Test using Context
        with self.assertRaises(Exception) as context:
            DBBase(database="test")
        self.assertTrue("Database not available." in str(context.exception))

    def test_available_databases(self):
        rows = [
            {
                "config_name": "gavo",
                "dbname": "prod_gavo",
                "host": "desdb4.linea.gov.br",
                "engine": "postgresql_psycopg2",
            }
        ]
        self.assertEqual(self.dao.available_databases(), rows)

    def test_get_engine_name(self):
        self.assertEqual(self.dao._database.get_engine_name(), "postgresql_psycopg2")

    def test_get_dialect(self):
        self.assertIsInstance(self.dao._database.get_dialect(), postgresql.dialect)

    def test_accept_bulk_insert(self):
        self.assertTrue(self.dao._database.accept_bulk_insert())

    def test_sa_table(self):
        tbl = self.dao.sa_table(self.table, self.schema)

        self.assertTrue(isinstance(tbl, Table))

        self.assertEqual(tbl.name, self.table)

    def test_execute(self):
        sql = "insert into {schema}.{table} values (1, 'jose', 30)".format(schema=self.schema, table=self.table)

        result = self.dao.execute(sql)

        # Verifica se o resultado é uma instancia de CursorResult
        self.assertTrue(isinstance(result, CursorResult))

        # Quantidade de linhas inseridas
        self.assertEqual(result.rowcount, 1)

    def test_fetchall(self):
        row = [(1, "jose", 30)]
        self.add_valid_record()

        result = self.dao.fetchall(self.select_sql)

        self.assertEqual(result, row)

    def test_fetchall_dict(self):
        self.add_valid_record()
        row = [{"id": 1, "name": "jose", "age": 30}]
        sql = "Select * from {}.{}".format(self.schema, self.table)

        self.assertEqual(self.dao.fetchall_dict(sql), row)

    def test_fetchall_df(self):
        self.add_valid_record()
        df = pd.DataFrame([{"id": 1, "name": "jose", "age": 30}])

        assert_frame_equal(self.dao.fetchall_df(self.select_sql), df)

    def test_fetchone(self):
        self.add_valid_record()
        row = (1, "jose", 30)

        self.assertEqual(self.dao.fetchone(self.select_sql), row)

    def test_fetchone_dict(self):
        self.add_valid_record()
        row = {"id": 1, "name": "jose", "age": 30}
        self.assertEqual(self.dao.fetchone_dict(self.select_sql), row)

        # Checks to return None when no results are found.
        sql = f"Select * from {self.schema}.{self.table} where id = 2"
        self.assertEqual(self.dao.fetchone_dict(sql), None)

    def test_fetc_scalar(self):
        self.add_valid_record()
        self.assertEqual(self.dao.fetch_scalar(self.select_sql), 1)

    def test_to_dict(self):
        self.add_valid_record()
        row = {"id": 1, "name": "jose", "age": 30}

        line = self.dao.fetchone(self.select_sql)

        self.assertEqual(self.dao.to_dict(line), row)

    def test_raw_sql_to_stm(self):
        stm = self.dao.raw_sql_to_stm(str(self.select_sql))

        self.assertTrue(isinstance(stm, TextClause))

        # Double Check
        self.assertEqual(self.select_sql, str(stm))

        # Check if a statement is passed.
        self.assertEqual(self.dao.raw_sql_to_stm(stm), stm)

    def test_get_table_columns(self):
        columns = ["id", "name", "age"]

        self.assertEqual(self.dao.get_table_columns(self.table, self.schema), columns)

    def test_describe_table(self):
        columns = [
            {"name": "id", "type": INTEGER()},
            {"name": "name", "type": VARCHAR(length=100)},
            {"name": "age", "type": INTEGER()},
        ]

        # OBS: A comparação só ficou igual quando convertido para String.
        self.assertEqual(str(self.dao.describe_table(self.table, self.schema)), str(columns))

    def test_square_stm(self):
        sql = "q3c_poly_query(ra, dec, '{ {10.0, 40.0}, {30.0, 40.0}, {30.0, 20.0}, {10.0, 20.0}}')"
        stm = self.dao._database.square_stm([10, 20], [30, 40], "ra", "dec")

        self.assertEqual(str(stm), sql)
