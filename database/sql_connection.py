"""
This module I've created handles the direct connection to SQL. It actually utilises a MySQL library but works fine
with Windows SQL in the rudimentary way we use it here.
"""

import pyodbc
from mysql.connector import Error


def update_sql_db(data_list_for_sql, data_set_string):
    """This function is the final step in SENDING to SQL.
     The data is passed from update_databases.py in a list form along with a reference to the data_set from
     which it came."""
    
    # create a connection (conn) using the below credentials
    conn = pyodbc.connect("Driver={SQL Server};"
                          "Server=ITVD-GFXMSTRSQL\MAESTRO;"
                          "Database=GMB_TICKER;"
                          "uid=sa;pwd=Ma3str0")

    # Useful queries for troubleshooting:
    #
    # """ DELETE FROM dbo.Generic """
    # """ UPDATE dbo.Generic
    #         SET TYPE = NULL """
    # """ INSERT INTO dbo.Generic (ID, TYPE, ITEM)
    #         VALUES(?, ?, ?)"""
    #
    # ## data = (id, type, item)
    # data = (type, item, id)
    #
    # query_insert = """ INSERT INTO dbo.Generic (ID, TYPE, ITEM)
    #                    VALUES(?, ?, ?)"""

    #
    # THE QUERY FOR SQL:
    # UPDATE (which table)
    # SET TYPE, ITEM (each row category and text)
    # At the position of it's ID/index number
    query_generic = """ UPDATE dbo.Generic
                        SET TYPE = ?, ITEM = ?
                        WHERE ID = ?"""

    query_breaking = """ UPDATE dbo.Breaking_News
                            SET TYPE = ?, ITEM = ?
                            WHERE ID = ?"""

    query_obit = """ UPDATE dbo.Obit
                            SET TYPE = ?, ITEM = ?
                            WHERE ID = ?"""

    try:
        with conn:
            cursor = conn.cursor()
            # In computer science a database cursor is a control structure that enables traversal over
            # the records in a database. Cursors facilitate subsequent processing in conjunction with the traversal,
            # such as retrieval, addition and removal of database records.

            # Loop through each item in the list of data passed through to the function and execute a query against it
            if 'generic' in data_set_string:
                for individual_row_data in data_list_for_sql:
                    cursor.execute(query_generic, individual_row_data)
            elif 'breaking' in data_set_string:
                for individual_row_data in data_list_for_sql:
                    cursor.execute(query_breaking, individual_row_data)
            else:
                for individual_row_data in data_list_for_sql:
                    cursor.execute(query_obit, individual_row_data)

        # Finalise
        conn.commit()
        cursor.close()
        conn.close()

    except Error as error:
        print(error)


def retrieve_sql_data(data_set_title):
    """This is more or less the same as above but just working in reverse in order to popualte the rows when the
    program is started."""

    conn = pyodbc.connect("Driver={SQL Server};"
                          "Server=ITVD-GFXMSTRSQL\MAESTRO;"
                          "Database=GMB_TICKER;"
                          "uid=sa;pwd=Ma3str0")

    try:
        with conn:

            cursor = conn.cursor()

            if 'generic' in data_set_title:
                cursor.execute("SELECT TYPE, ITEM FROM dbo.Generic")
            elif 'breaking' in data_set_title:
                cursor.execute("SELECT TYPE, ITEM FROM dbo.Breaking_News")
            else:
                cursor.execute("SELECT TYPE, ITEM FROM dbo.Obit")

            data_list = []

            # Some formatting whilst bringing the data in:
            for cat, text in cursor:
                cat = cat.replace(".", "")
                cat = cat.replace(" CONT", "")
                cat = cat.replace("BREAKING NEWS", "BREAKING")
                cat = cat.replace("ENTERTAINMENT", "ENTS")

                if "BLANK" not in cat and "WEATHER" not in cat and "ACT" not in cat:
                    data_list.append({'category': cat, 'text': text})

            cursor.close()

            return [x for x in data_list]

    except Error as error:
        print(error)
