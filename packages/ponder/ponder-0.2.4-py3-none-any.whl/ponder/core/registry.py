from enum import Enum

from packaging import version

from ponder.core.error_codes import PonderError, make_exception

##########################################
#
#  Registry of supported connection types
#

try:
    import duckdb

    check_duckdb = True
    if version.parse(duckdb.__version__) < version.parse("0.8.0"):
        raise make_exception(
            AssertionError,
            PonderError.PONDER_DUCKDB_VERSION_ERROR,
            "Ponder requires duckdb>=0.8, "
            + "please `pip install ponder[duckdb]` to upgrade.",
        )
except ImportError:
    check_duckdb = False

try:
    import snowflake.connector

    check_snowflake = True
    if version.parse(snowflake.connector.__version__) < version.parse("3.0.2"):
        raise make_exception(
            AssertionError,
            PonderError.PONDER_SNOWFLAKE_VERSION_ERROR,
            "Ponder requires snowflake-connector-python[pandas]>3.0.2, "
            + "please `pip install ponder[snowflake]` to upgrade.",
        )
except ImportError:
    check_snowflake = False

try:
    from google.cloud import bigquery
    from google.cloud.bigquery import dbapi

    check_bigquery = True
    if version.parse(bigquery.__version__) < version.parse("3.8.0"):
        raise make_exception(
            AssertionError,
            PonderError.PONDER_BIGQUERY_VERSION_ERROR,
            "Ponder requires google-cloud-bigquery>=3.8.0, "
            + "please `pip install ponder[bigquery]` to upgrade.",
        )
except ImportError:
    check_bigquery = False


try:
    import psycopg

    check_postgres = True
except ImportError:
    check_postgres = False

try:
    import redshift_connector

    check_redshift = True
except ImportError:
    check_redshift = False
try:
    import polars  # noqa: F401

    check_polars = True
except ImportError:
    check_polars = False

try:
    import pymssql

    check_mssql = True
except ImportError:
    check_mssql = False


class EngineEnum(Enum):
    UNSUPPORTED = "unsupported"
    SNOWFLAKE = "snowflake"
    BIGQUERY = "bigquery"
    DUCKDB = "duckdb"
    POSTGRESQL = "postgres"
    REDSHIFT = "redshift"
    POLARS = "polars"
    MSSQL = "mssql"


def get_connection_type(con):
    if check_snowflake and isinstance(
        con, snowflake.connector.connection.SnowflakeConnection
    ):
        return EngineEnum.SNOWFLAKE
    elif check_bigquery and isinstance(con, dbapi.Connection):
        return EngineEnum.BIGQUERY
    elif check_duckdb and isinstance(con, duckdb.DuckDBPyConnection):
        return EngineEnum.DUCKDB
    elif check_postgres and isinstance(con, psycopg.Connection):
        return EngineEnum.POSTGRESQL
    elif check_redshift and isinstance(con, redshift_connector.Connection):
        return EngineEnum.REDSHIFT
    elif check_polars and isinstance(con, str) and con == "polars":
        return EngineEnum.POLARS
    elif check_mssql and isinstance(con, pymssql.Connection):
        return EngineEnum.MSSQL
    else:
        return EngineEnum.UNSUPPORTED


def get_connection_attributes(connection_type):
    # TODO: This function can be merged with _get_connection_type into
    # a proper connection registry class, where dialects can be assigned
    # and so-forth
    name = "Unknown"
    dbtype = None
    read_sql_fn = None
    read_csv_fn = None
    read_parquet_fn = None
    from_pandas_fn = None
    db_license_key = None

    if connection_type is EngineEnum.SNOWFLAKE:
        from ponder.engines.snowflake.io import SnowflakeIO

        name = "Snowflake"
        dbtype = "snowflake"
        db_license_key = dbtype
        read_sql_fn = SnowflakeIO.read_sql
        read_csv_fn = SnowflakeIO.read_csv
        read_parquet_fn = SnowflakeIO.read_parquet
        from_pandas_fn = SnowflakeIO.from_pandas

    elif connection_type is EngineEnum.BIGQUERY:
        from ponder.engines.bigquery.io import BigQueryIO

        name = "Google BigQuery"
        dbtype = "bigquery"
        # The license key for GBQ is different from the
        # connection class name
        db_license_key = "gbq"
        read_sql_fn = BigQueryIO.read_sql
        read_csv_fn = BigQueryIO.read_csv
        read_parquet_fn = None
        from_pandas_fn = BigQueryIO.from_pandas

    elif connection_type is EngineEnum.DUCKDB:
        from ponder.engines.duckdb.io import DuckDBIO

        name = "DuckDB"
        dbtype = "duckdb"
        db_license_key = dbtype
        read_sql_fn = DuckDBIO.read_sql
        read_csv_fn = DuckDBIO.read_csv
        read_parquet_fn = DuckDBIO.read_parquet
        from_pandas_fn = DuckDBIO.from_pandas

    elif connection_type is EngineEnum.POSTGRESQL:
        from ponder.engines.postgres.io import PostgresIO

        name = "PostgreSQL"
        dbtype = "postgres"
        db_license_key = dbtype
        read_sql_fn = PostgresIO.read_sql
        read_csv_fn = PostgresIO.read_csv
        read_parquet_fn = PostgresIO.read_parquet
        from_pandas_fn = PostgresIO.from_pandas

    elif connection_type is EngineEnum.POLARS:
        from ponder.engines.polars.io import PolarsIO

        name = "Polars"
        dbtype = "polars"
        db_license_key = dbtype
        read_sql_fn = PolarsIO.read_sql
        read_csv_fn = PolarsIO.read_csv
        read_parquet_fn = PolarsIO.read_parquet
        from_pandas_fn = PolarsIO.from_pandas

    elif connection_type is EngineEnum.REDSHIFT:
        from ponder.engines.redshift.io import RedshiftIO

        name = "Amazon Redshift"
        dbtype = "redshift"
        db_license_key = dbtype
        read_sql_fn = RedshiftIO.read_sql
        read_csv_fn = RedshiftIO.read_csv
        read_parquet_fn = RedshiftIO.read_parquet
        from_pandas_fn = RedshiftIO.from_pandas

    elif connection_type is EngineEnum.MSSQL:
        from ponder.engines.mssql.io import MSSQLIO

        name = "Microsoft SQL Server"
        dbtype = "mssql"
        db_license_key = dbtype
        read_sql_fn = MSSQLIO.read_sql
        read_csv_fn = MSSQLIO.read_csv
        read_parquet_fn = MSSQLIO.read_parquet
        from_pandas_fn = MSSQLIO.from_pandas

    return {
        "name": name,
        "dbtype": dbtype,
        "db_license_key": db_license_key,
        "read_sql_fn": read_sql_fn,
        "read_csv_fn": read_csv_fn,
        "read_parquet_fn": read_parquet_fn,
        "from_pandas_fn": from_pandas_fn,
    }
