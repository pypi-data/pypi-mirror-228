import logging
import psycopg2
import cx_Oracle
import MySQLdb
from scrippy_db import ScrippyDbError


class Db:
  """Generic class for database client."""
  def __init__(self,
               username=None,
               host=None,
               database=None,
               port=None,
               password=None,
               service=None,
               db_type="postgres"):
    self.db_types = {"postgres": {"connect": self.connect_pgsql,
                                  "execute": self.execute_pgsql},
                     "oracle": {"connect": self.connect_oracle,
                                "execute": self.execute_oracle},
                     "mysql": {"connect": self.connect_mysql,
                               "execute": self.execute_mysql}}
    self.username = username
    self.host = host
    self.database = database
    self.port = port
    self.password = password
    self.service = service
    self.db_type = db_type
    self.connection = None
    self.cursor = None

  def __enter__(self):
    """Entry point."""
    self.connect()
    return self

  def __exit__(self, type_err, value, traceback):
    """Exit point."""
    del type_err, value, traceback
    self.close()

  def connect(self):
    """Connect to database (generic).
    """
    try:
      logging.debug("[+] Connecting to database service:")
      self.connection = self.db_types[self.db_type]["connect"]()
    except (psycopg2.Error,
            cx_Oracle.DatabaseError,
            MySQLdb.Error) as err:
      err_msg = f"Error while connecting: [{err.__class__.__name__}] {err}"
      raise ScrippyDbError(err_msg) from err

  def connect_oracle(self):
    """Coonect to Oracle database."""
    dsn = cx_Oracle.makedsn(self.host, self.port, service_name=self.database)
    logging.debug(f" '-> {dsn}")
    return cx_Oracle.connect(self.username, self.password, dsn)

  def connect_pgsql(self):
    """Connect to Postgres database."""
    if self.service:
      logging.debug(f" '-> {self.service}")
      return psycopg2.connect(service=self.service)
    logging.debug(f" '-> {self.username}@{self.host}:{self.port}/{self.database}")
    return psycopg2.connect(user=self.username,
                            host=self.host,
                            port=self.port,
                            dbname=self.database,
                            password=self.password)

  def connect_mysql(self):
    """Connect to MySQL/MariaDB database."""
    logging.debug(f" '-> {self.username}@{self.host}:{self.port}/{self.database}")
    return MySQLdb.connect(user=self.username,
                           host=self.host,
                           port=self.port,
                           database=self.database,
                           password=self.password)

  def close(self):
    """Close database connection."""
    try:
      if self.cursor:
        self.cursor.close()
    except (psycopg2.Error,
            cx_Oracle.InterfaceError,
            MySQLdb.Error) as err:
      logging.warning(f" '-> Error while closing connection: [{err.__class__.__name__}] {err}")
    finally:
      if self.connection:
        logging.debug("[+] Closing connection")
        self.connection.close()
        self.connection = None

  def execute(self, request, params=None, verbose=False, commit=False):
    """Execute SQL query (generic).
    """
    try:
      logging.debug("[+] Executing query:")
      result = self.db_types[self.db_type]["execute"](request,
                                                      params,
                                                      verbose)
      if commit:
        self.connection.commit()
      return result
    except Exception as err:
      logging.error(f" '-> Error while executing query [{err.__class__.__name__}] {err}")
      self.connection.rollback()
      self.close()

  def execute_oracle(self, request, params, verbose):
    """Execute SQL query (Oracle)."""
    with self.connection.cursor() as self.cursor:
      if verbose:
        logging.debug(f" '-> {request}")
        logging.debug(f" '-> {params}")
      if params is not None:
        self.cursor.execute(request, params)
      else:
        self.cursor.execute(request)
      logging.debug(f" '-> {self.cursor.rowcount} modified line(s)")
      try:
        result = self.cursor.fetchall()
      except cx_Oracle.InterfaceError:
        logging.debug(" '-> No result")
        return None
      if verbose:
        for row in result:
          logging.debug(f"  '-> {' | '.join([str(i) for i in row])}")
      return result

  def execute_pgsql(self, request, params, verbose):
    """Execute SQL query (Postgres)."""
    with self.connection.cursor() as self.cursor:
      if verbose:
        logging.debug(f" '-> {self.cursor.mogrify(request, params)}")
      self.cursor.execute(request, params)
      logging.debug(f" '-> {self.cursor.rowcount} modified line(s)")
      try:
        result = self.cursor.fetchall()
      except psycopg2.ProgrammingError:
        logging.debug(" '-> No result")
        return None
      if verbose:
        for row in result:
          logging.debug(f"  '-> {' | '.join([str(i) for i in row])}".format())
      return result

  def execute_mysql(self, request, params, verbose):
    """Execute SQL query (MySQL)."""
    with self.connection.cursor() as self.cursor:
      if verbose:
        logging.debug(f" '-> {request}")
        logging.debug(f" '-> {params}")
      modified = self.cursor.execute(request, params)
      logging.debug(f" '-> {modified} modified line(s)")
      try:
        result = self.cursor.fetchall()
      except MySQLdb.Error:
        logging.debug(" '-> No result")
        return None
      if verbose:
        for row in result:
          logging.debug(f"  '-> {' | '.join([str(i) for i in row])}".format())
      return result


class ConnectionChain:
  """The ConnectionChain object allows you to retrieve connection information to a database from a character string following the format <DB_TYPE>:<ROLE>/<PASSWORD>@<HOST>:<PORT>//<DB_NAME>.
  """
  def __init__(self, connection_chain):
    self.db_type = connection_chain.split(':')[0]
    self.username = connection_chain.split(':')[1].split('/')[0]
    self.password = connection_chain.split('@')[0].split('/')[1]
    self.host = connection_chain.split('@')[1].split(':')[0]
    self.port = int(connection_chain.split(':')[2].split('/')[0])
    self.database = connection_chain.split('/')[-1]


class DbFromCc(Db):
  """The DbFromCc class allows a Db obkject instanciation directly from a ConnectionChain object.
  """

  def __init__(self, connection_chain):
    c_chain = ConnectionChain(connection_chain)
    super().__init__(username=c_chain.username,
                     host=c_chain.host,
                     database=c_chain.database,
                     port=c_chain.port,
                     password=c_chain.password,
                     service=None,
                     db_type=c_chain.db_type)
