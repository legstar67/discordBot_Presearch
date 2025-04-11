import sqlite3
from enum import Enum
#from bot import NAME_FILE_DATABASE

class _typeDataSQL(Enum):
    TEXT = "TEXT"
    INT = "INTEGER"
    FLOAT = "REAL"

class selectData(Enum):
    NAME = "NAME"
    TYPE = "TYPE"

#TODO maybe to be cleaner i can put all enum element in a ordered list for both enum (so two lists)
class Alerts(Enum):
    NAME_BASE = "alerts"
    PRIMARY_KEY_SMART_CONTRACT = {selectData.NAME: "SMART_CONTRACT", selectData.TYPE: _typeDataSQL.TEXT}
    PRICE = {selectData.NAME: "PRICE", selectData.TYPE: _typeDataSQL.TEXT}
    #LAST_ERC20_TRANSACTION = {selectData.NAME: "lastERC20Transaction", selectData.TYPE: _typeDataSQL.TEXT}
    #KIND = {selectData.NAME : "kind", selectData.TYPE: _typeDataSQL.TEXT} 

class TOKEN(Enum):
    NAME_BASE = "prices"
    KEY_CONTRACT = {selectData.NAME: "contractAddress", selectData.TYPE: _typeDataSQL.TEXT}
    NAME_TOKEN = {selectData.NAME: "nameToken", selectData.TYPE: _typeDataSQL.TEXT}
    SYMBOL_TOKEN = {selectData.NAME: "symbolToken", selectData.TYPE: _typeDataSQL.TEXT}
    PRICE = {selectData.NAME: "price", selectData.TYPE: _typeDataSQL.FLOAT}
    P_24H = {selectData.NAME: "pricePercentage24h", selectData.TYPE: _typeDataSQL.FLOAT}
    P_7D = {selectData.NAME: "pricePercentage7D", selectData.TYPE: _typeDataSQL.FLOAT}
    P_30D = {selectData.NAME: "pricePercentage30D", selectData.TYPE: _typeDataSQL.FLOAT}
    UNIX_DATE_LAST_UPDATE = {selectData.NAME: "unixDateLastUpdate", selectData.TYPE: _typeDataSQL.INT}




def createTable(
        base : sqlite3.Connection,
        #fileDataBase : str, 
        nameTable : str, 
        primaryKeyColunm : str , 
        typeKey :_typeDataSQL, 
        valuesAndTypes : dict[str,_typeDataSQL] ):
    """
    Creates a new table in the specified SQLite database.
    
    Args:
        base (sqlite3.Connection): The SQLite database connection object.
        nameTable (str): The name of the table to be created.
        primaryKeyColunm (str): The name of the primary key column.
        typeKey (_typeDataSQL): The data type of the primary key column.
        valuesAndTypes (dict[str, _typeDataSQL]): A dictionary where keys are column names 
            and values are their respective data types.
    Returns:
        None
    Side Effects:
        Executes a SQL command to create a table in the database and commits the changes.
    Notes:
        - The function assumes that the database connection is already established.
        - The `getCursor` and `_commandToCreateTable` helper functions are used internally.
        - The database connection is not closed within this function.
    """
    
    cursor = getCursor(base)
    cursor.execute(_commandToCreateTable(
            nameTable=nameTable,
            primaryKeyColunm=primaryKeyColunm,
            typeKey=typeKey,
            valuesAndTypes=valuesAndTypes
        ))
    base.commit()
    cursor.close()
    #base.close()
    

def newRow(base : sqlite3.Connection, tableName : str, primaryKeyColunm : str, keyValue, values : dict[str,]):

    """
    Inserts a new row into the specified table in the SQLite database.

    This function adds a new row to the given table in the SQLite database. The row is identified by a primary key and contains additional column values provided in the `values` dictionary.

        base (sqlite3.Connection): The SQLite database connection object.
        tableName (str): The name of the table where the new row will be inserted.
        primaryKeyColunm (str): The name of the column that serves as the primary key for the table.
        keyValue (Any): The value of the primary key for the new row.
        values (dict[str, Any]): A dictionary containing column names as keys and their corresponding values to insert into the new row.

    Raises:
        sqlite3.Error: If an error occurs during the execution of the SQL command.

    """
    cursor = getCursor(base)
    cursor.execute(_commandToInsertElement(tableName=tableName,primaryKeyColunm=primaryKeyColunm,keyValue=keyValue,values=values))
    base.commit()
    cursor.close()

def updateRow(base : sqlite3.Connection, tableName : str, primaryKeyColunm : str, keyValue, values : dict[str,]):
    cursor = getCursor(base)
    cursor.execute(_commandToUpdateRow(tableName=tableName,primaryKeyColunm=primaryKeyColunm,keyValue=keyValue,values=values))
    base.commit()
    cursor.close()

def getRow(base : sqlite3.Connection, tableName : str, primaryKeyColunm : str, keyValue):

    """
    Retrieve a row from a specified table in the database based on the primary key value.
    
    Args:
        base (sqlite3.Connection): The SQLite database connection object.
        tableName (str): The name of the table to query.
        primaryKeyColunm (str): The name of the primary key column in the table.
        keyValue: The value of the primary key to search for.
    
    Returns:
        list or None: The row as a list if a matching row is found, or None if no row matches the given key.

    """
    cursor = getCursor(base)
    cursor.execute(_commandToGetRow(tableName=tableName,primaryKeyColunm=primaryKeyColunm,keyValue=keyValue,))
    row = cursor.fetchone()
    cursor.close()
    return row

def deleteRow(base : sqlite3.Connection, tableName : str, primaryKeyColunm : str, keyValue):
    """    
    Deletes a row from the specified table in the database based on the primary key column and its value.
    
    Args:
        base (sqlite3.Connection): The SQLite database connection object.
        tableName (str): The name of the table from which the row will be deleted.
        primaryKeyColunm (str): The name of the primary key column used to identify the row to delete.
        keyValue (Any): The value of the primary key column for the row to be deleted.
    Raises:
        sqlite3.Error: If an error occurs during the execution of the SQL command.
    """
    cursor = getCursor(base)
    cursor.execute(_commandToDeleteRow(tableName=tableName,primaryKeyColunm=primaryKeyColunm,keyValue=keyValue))
    base.commit()
    cursor.close()   


#return the SQLite Base
def getBase(fileDataBase : str) -> sqlite3.Connection:
    """Open the base with the given file name

    Args:
        fileDataBase (str): file name

    Returns:
        sqlite3.Connection: sqliteBase opened 
    """
    return sqlite3.connect(fileDataBase)
#return the cursor of the base
def getCursor(base : sqlite3.Connection) -> sqlite3.Cursor:
    """Get the cursor of the base

    Args:
        base (sqlite3.Connection): your sqlite base opened

    Returns:
        sqlite3.Cursor: A cursor of the base
    """
    return base.cursor()




def _commandToCreateTable(nameTable : str, primaryKeyColunm : str , typeKey :_typeDataSQL, valuesAndTypes : dict[str,_typeDataSQL]):
    """
    Generates an SQL command to create a table if it does not already exist.

    Args:
        nameTable (str): The name of the table to be created.
        primaryKeyColunm (str): The name of the primary key column.
        typeKey (_typeDataSQL): The data type of the primary key column.
        valuesAndTypes (dict[str, _typeDataSQL]): A dictionary where keys are column names 
                and values are their corresponding data types.

    Returns:
        str: The SQL command string to create the table.
    """
    command = ('CREATE TABLE IF NOT EXISTS '+ nameTable +' ( ' +
                primaryKeyColunm + " " + typeKey.value + " PRIMARY KEY, "
)   
    nbOfParameters = len(valuesAndTypes)
    for index, (primaryKeyColunm, typeKey) in enumerate(valuesAndTypes.items()):
        command += primaryKeyColunm + " " + typeKey.value + (" )" if index == nbOfParameters-1 else ", ")
    return command


def _commandToInsertElement(tableName : str, primaryKeyColunm : str, keyValue, values : dict[str,]):
    """
    Generates an SQL INSERT command string for inserting an element into a database table.
    Args:
        tableName (str): The name of the database table where the element will be inserted.
        primaryKeyColunm (str): The name of the primary key column in the table.
        keyValue: The value for the primary key column.
        values (dict[str,]): A dictionary containing column names as keys and their corresponding values to be inserted.
    Returns:
        str: A formatted SQL INSERT command string.
    Example:
        "INSERT INTO Wallets (wallet) VALUES ('0x98372HB212B1E2F1298372HB212B1E2F12')"
    """

    cmd = f'INSERT INTO {tableName} ({primaryKeyColunm}' + (", " if len(values) > 0 else "" )
    cmdValue = f"({_placeValueInCmd(keyValue)}" + (", " if len(values) > 0 else "" )

    if(len(values) == 0):
        cmd += ") VALUES "
        cmdValue += ")"
    else:
        for index, (name, value) in enumerate(values.items()):
            isItNotLast = index < len(values) - 1
            isItStrValue = type(value)== str

            cmd += name + (", " if isItNotLast else ") VALUES ")
            cmdValue += _placeValueInCmd(value) + (", " if isItNotLast else ")")
    
    #print(cmd + cmdValue)
    return cmd + cmdValue


def _commandToUpdateRow(tableName : str, primaryKeyColunm : str, keyValue, values : dict[str,]):
    """
    Generates an SQL command string to update a row in a database table.

    Args:
        tableName (str): The name of the table where the update will occur.
        primaryKeyColunm (str): The name of the primary key column used to identify the row to update.
        keyValue: The value of the primary key for the row to update.
        values (dict[str,]): A dictionary containing column-value pairs to update in the row.

    Returns:
        str: An SQL command string to update the specified row in the table.

    Note:
        This function assumes that `_placeValueInCmd` is a helper function that safely formats
        values for inclusion in the SQL command to prevent SQL injection.
    Example:
        "UPDATE users SET age = 31 WHERE name = 'Alice'"
    """
    cmd = f"UPDATE {tableName} SET "
    for index , (name, value) in enumerate(values.items()):
        cmd += f"{name} = {_placeValueInCmd(value)}" + (", " if index < len(values)-1 else "")
    cmd += f" WHERE {primaryKeyColunm} = {_placeValueInCmd(keyValue)}"
    return cmd

def _commandToDeleteRow(tableName : str, primaryKeyColunm  : str, keyValue):
    """
    Generates a SQL DELETE command to remove a row from a specified table 
    based on the value of the primary key column.
    Args:
        tableName (str): The name of the table from which the row will be deleted.
        primaryKeyColunm (str): The name of the primary key column used to identify the row.
        keyValue: The value of the primary key column for the row to be deleted.
    Returns:
        str: A SQL DELETE command as a string.

    Example: 
        "UPDATE users SET age = 31 WHERE name = 'Alice'"
    """
    return f'DELETE FROM {tableName} WHERE {primaryKeyColunm } = {_placeValueInCmd(keyValue)}'


def _commandToGetRow(tableName : str, primaryKeyColunm : str, keyValue):
    """
    Generates an SQL SELECT command to retrieve a row from a specified table 
    where the primary key column matches the given key value.
    
    Args:
        tableName (str): The name of the table to query.
        primaryKeyColunm (str): The name of the primary key column in the table.
        keyValue: The value of the primary key to match.
    Returns:
        str: An SQL SELECT command as a string.
    """

    return f'SELECT * FROM {tableName} WHERE {primaryKeyColunm} = {_placeValueInCmd(keyValue)}'


# Return the string value, and if it's a string, add quote
def _placeValueInCmd(value):
    """
    Converts a given value into a string representation suitable for use in a SQL command.

    Args:
        value: The value to be converted. It can be of any type, including None.

    Returns:
        str: A string representation of the value. If the value is None, it returns 'NULL'.
             If the value is a string, it wraps the value in single quotes. For other types,
             it converts the value to a string without additional formatting.
    """
    if value is None:
        return 'NULL'
    return (("'" if type(value) == str else "") + str(value) + ("'" if type(value) == str else "") )



def table_to_dict(base, table_name, primary_key_column):
    """
    Converts a SQLite table into a dictionary of sub-dictionaries.

    Args:
        db_path: Path to the SQLite database.
        table_name: Name of the table to convert.
        primary_key_column: Name of the column that serves as the primary key.
    Return: 
        Dictionary where keys are primary key values and values are sub-dictionaries of column names and associated values.
    """
    cursor = base.cursor()

    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()
    column_names = [col[1] for col in columns_info]

    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    result_dict = {}

    for row in rows:
        row_dict = {column_names[i]: row[i] for i in range(len(column_names))}
        primary_key_value = row_dict[primary_key_column]
        result_dict[primary_key_value] = row_dict

    return result_dict

#TODO NOT TESTED :
def update_dict(listOfKeys, ExistantDict, sub_dict_keys):
    """
    Updates the wallet dictionary to ensure each wallet in the list is present.
    If a wallet is not present, it is added with a sub-dictionary initialized with None values.

    Args:
        wallet_list: List of wallet addresses (strings).
        wallet_dict: Dictionary where keys are wallet addresses and values are sub-dictionaries.
        sub_dict_keys: List of keys to initialize in the sub-dictionary if a wallet is not present.
    Return:
        Updated wallet dictionary.
    """
    for wallet in listOfKeys:
        if wallet not in ExistantDict:
            # Initialize the sub-dictionary with None values for each key
            ExistantDict[wallet] = {key: None for key in sub_dict_keys}

    return ExistantDict


def row_exists(base, table, primary_key_column, primary_key_value):
    """
    Checks if a row exists in a SQLite table using the value of the primary key.

    Args:
        base: SQLite database connection object.
        table: Name of the table to query.
        primary_key_column: Name of the primary key column.
        primary_key_value: Value of the primary key to check for existence.
    Return :
        True if the row exists, False otherwise.
    """
    try:
        cursor = base.cursor()

        query = f"SELECT 1 FROM {table} WHERE {primary_key_column} = ?"
        cursor.execute(query, (primary_key_value,))

        exists = cursor.fetchone() is not None

        return exists
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        return False