import logging
import os
import re

import pandas as pd
from mpmath import mp
from objectpath import *

PRECISION = 13

mp.dps = PRECISION
mp.pretty = False

logger = logging.getLogger(__name__)


MODEL_DIR_NAMES = {
    "IR": "Nominal_rates",
    "RIR": "Real_rates",
    "EQ": "Equity",
    "RE": "Real_estate",
    "CRED": "Credit",
    "FX": "FX_rate",
}
FILE_MARK = "file::"


# Custom Exception class for sensi validation
class SensiSyntaxError(Exception):
    def __init__(self, msg):
        self.msg = str(msg)

    def __str__(self):
        return self.msg


class Syntax:
    def __init__(self, expression="", col="", condition="", value=""):
        """Initialize a Syntax object

        Args:
            expression (str, optional): The expression to be evaluated.
            col (str, optional): The column name.
            condition (str, optional): The condition to be evaluated.
            value (str, optional): The value to be evaluated.
        """
        self.expression = expression
        self.col = col
        self.condition = condition
        self.value = value

    def __str__(self):
        return f"Syntax(expression={self.expression}, col={self.col}, condition={self.condition}, value={self.value})"


def extract_value_from_equal(param_string):
    """Extracts syntax and value from param_string if param_string contains =

    Args:
        param_string (str): string to be parsed

    Raises:
        SensiSyntaxError: if param_string does not contain =

    Returns:
        tuple: (syntax (str), value (str))
    """
    logger.info(f"Extracting value from {param_string}")

    if not "=" in param_string:
        logger.error(f'Incorrect syntax in param. Unable to find "=" in {param_string}')
        raise SensiSyntaxError('Incorrect syntax in param. Unable to find "="')

    logger.debug(f"Extracting syntax and value from {param_string}")
    equal_char_position = param_string.rindex("=")
    syntax = param_string[:equal_char_position].strip('"').strip()
    value = param_string[equal_char_position + 1 :].strip()

    logger.debug(f"Returned {syntax} and {value}.")
    return syntax, value


def extract_target_column(param_string):
    """Extracts column from param_string if param_string contains
    [ and ends with ]

    Args:
        param_string (str): string to be parsed

    Raises:
        SensiSyntaxError: if param_string does not contain [ and ends with ]

    Returns:
        tuple: (syntax (str), column (str))
    """
    logger.info(f"Extracting target column from {param_string}")
    param_string = param_string.strip('"').strip()

    if not "[" in param_string or not param_string.endswith("]"):
        logger.error(f'Incorrect syntax in param. Unable to find "[" or "]" in {param_string}')
        raise SensiSyntaxError('Incorrect syntax in param. Unable to find "[" or "]"')

    logger.debug(f"Extracting target column from {param_string}")
    right_quote_position = param_string.rindex("]")
    left_quote_position = param_string.rindex("[")
    syntax = param_string[:left_quote_position].strip('"').strip()
    column = param_string[left_quote_position + 1 : right_quote_position].strip()

    if column == "":
        logger.error(f"Incorrect input syntax. Column cannot be empty")
        raise SensiSyntaxError("Incorrect input syntax. Column cannot be empty")

    logger.debug(f"Returned {syntax} and {column}.")
    return syntax, column


def parse_param(input_syntax):
    """Parses input syntax and returns Syntax object

    Args:
        input_syntax (str): input syntax

    Raises:
        SensiSyntaxError: if input_syntax is invalid

    Returns:
        Syntax: Syntax object
    """
    logger.info(f"Parsing param: {input_syntax}")

    if not input_syntax:
        logger.error("Empty input_syntax parameter passed to the parse_param function.")
        raise SensiSyntaxError("Empty input_syntax in parse_param function")

    logger.debug(f"Extracting syntax and value from {input_syntax}")
    param_string, param_value = extract_value_from_equal(input_syntax)

    # Check if param_string contains FILE_MARK
    if not FILE_MARK in param_string:
        logger.debug(f"param_string does not contain {FILE_MARK}.")
        logger.debug(f"Returning Syntax object with expression: {param_string}, value: {param_value}")
        return Syntax(expression=param_string, value=param_value)

    logger.debug(f"Input syntax contains {FILE_MARK}.")

    # Remove FILE_MARK from param_string
    param_string = param_string.replace(FILE_MARK, "").strip()

    logger.debug(f"Checking if param_string contains condition")
    # Checks if '.where' exists in param_string
    if ".where" in param_string:
        logger.debug(f".where exists in param_string.")
        if param_string.count(".where") > 1:
            logger.error(f'Incorrect input_syntax. Multiple ".where" in {param_string}')
            raise SensiSyntaxError('Incorrect input_syntax. Multiple ".where"')
        param_expression, param_condition = param_string.split(".where")
    else:
        logger.debug(f".where does not exist in param_string.")
        param_expression, param_condition = param_string, ""

    # Gets the column in the param_expressions
    logger.debug(f"Extracting target column from {param_expression}")
    param_expression, param_col = extract_target_column(param_expression)

    # Gets the economy from the param_expression
    logger.debug(f"Extracting economy from {param_expression}")
    eco_pattern = ""
    if re.search(r"eco_\d+\.", param_expression):
        eco_pattern = r"eco_\d+\."
        eco = re.search(r"eco_\d+(?=\.)", param_expression).group()  # Gets the 123 from "eco_123."
    elif re.search(r"eco\[\w+?\]\.", param_expression):
        eco_pattern = r"eco\[\w+?\]\."
        eco = re.search(r"(?<=eco\[)\w+(?=\]\.)", param_expression).group()  # Gets the EUR from "eco[EUR]."
    else:
        raise SensiSyntaxError("Unable to a valid eco in expression")

    # Get the driver from the param_expression
    logger.debug(f"Extracting driver from {param_expression}")
    driver_pattern = ""
    if re.search(r"driver_\d+\.", param_expression):
        driver_pattern = r"driver_\d+\."
        driver = re.search(r"driver_\d+(?=\.)", param_expression).group()  # Gets the 123 from "driver_123."
    elif re.search(r"driver\[\w+?\]\.", param_expression):
        driver_pattern = r"driver\[\w+?\]\."
        driver = re.search(r"(?<=driver\[)\w+(?=\]\.)", param_expression).group()  # Gets the IR from "driver[IR]"
    else:
        raise SensiSyntaxError("Unable to a valid driver in expression")

    # Remove eco and driver from param_expression
    param_expression = re.sub(eco_pattern, "", param_expression)
    param_expression = re.sub(driver_pattern, "", param_expression)

    result = (
        "$"
        + (f"..*['{eco}']" if "eco" in eco else f"..*[@.name is '{eco}']")
        + (f"..*['{driver}']" if "driver" in driver else f"..*[@.name is '{driver}']")
        + f".{param_expression}.filename"
    )
    logger.debug(f"Constructed query for input file extraction: {result}")

    logger.debug(
        f"Returning Syntax object with expression: {result}, value: {param_value}, "
        f"column: {param_col}, condition: {param_condition}"
    )
    return Syntax(result, param_col, param_condition, param_value)


def query(data, expression):
    """Queries data using expression

    Args:
        data (json): data to query from
        expression (str): expression to query with

    Raises:
        SensiSyntaxError: if data is empty
        or expression is invalid or the query fails

    Returns:
        list: list of results (or a single result)
    """
    logger.info(f"Querying data with expression: {expression}")

    if data is None or expression is None:
        logger.error(f"Incorrect input. data: {data}, expression: {expression}")
        raise SensiSyntaxError("Incorrect input. data or expression is None")

    expression = expression.strip()
    if not expression.startswith("$"):
        logger.error("Expression does not start with $")
        raise SensiSyntaxError("Expression does not start with $")

    result = []
    logger.debug(f"Executing query: {expression}")
    try:
        tree = Tree(data)
        query_result = tree.execute(expression)
        if query_result:
            if isinstance(query_result, str):
                # Convert string to a list with one element
                result = query_result.split(None, -1)
            else:
                result = list(query_result)

    except Exception as e:
        logger.error(f"Unable to execute query {expression}. Error: {e}")
        raise SensiSyntaxError(f"Failed to query for data")

    logger.debug(f"Returned result: {result}.")
    return result


def get_input_file_path(data, expression, env_dir):
    """Gets the input file path from the data using the expression

    Args:
        data (dict): data to query from
        expression (str): expression to query with
        env_dir (str): environment directory where the input file is located

    Raises:
        SensiSyntaxError: if any of the queries fail

    Returns:
        str: input file path
    """
    logger.info(f"Getting input file path for expression: {expression}")

    # Query for input file
    try:
        filename = query(data, expression)[0]
    except (SensiSyntaxError, IndexError) as e:
        logger.error(f"Unable to get input file path. Error: {e}")
        raise SensiSyntaxError("Unable to get input file path")

    # Query for eco and driver
    matches = re.findall(r"(?<=')\w+(?=')", expression)
    if len(matches) != 2:
        logger.error(f"Unable to get eco and driver from expression: {expression}")
        raise SensiSyntaxError("Unable to get eco and driver from expression")

    eco_name, driver_name = matches[0], matches[1]

    # Get the eco_name using 'eco_123' or 'eco[EUR]'
    # Then use the eco_name to get the eco_folder_id
    try:
        if eco_name.startswith("eco_"):
            eco_name = query(data, f"$..*['{eco_name}'].name")[0]
        else:
            eco_name = query(data, f"$..*[@.name is '{eco_name}'].name")[0]
        logger.debug(f"eco_name: {eco_name}")

        eco_folder_id = query(data, f"$..*[@.name is '{eco_name}'].folder_id")[0]
        logger.debug(f"eco_folder_id: {eco_folder_id}")

    except (SensiSyntaxError, IndexError) as e:
        logger.error(f"Unable to get eco_folder_id. Error: {e}")
        raise SensiSyntaxError("Unable to get eco_folder_id")

    # Get the driver_data using 'driver_123' or 'driver[IR]'
    try:
        if driver_name.startswith("driver_"):
            driver_data = query(data, f"$..*['{driver_name}']")[0]
        else:
            driver_data = query(data, f"$..*[@.name is '{driver_name}']")[0]
        driver_name = driver_data.get("class", driver_data.get("subclass", None))
        logger.debug(f"driver_name: {driver_name}")
    except Exception as e:
        logger.error(f"Unable to find driver_name in data: {e}")
        raise SensiSyntaxError(f"Exception occurred while getting driver_name from data")

    # TODO: Check how to get driver_folder_id correctly
    driver_folder_id = MODEL_DIR_NAMES.get(driver_name, None)
    if driver_folder_id is None:
        logger.error(f"Unable to find driver_folder_id for driver_name: {driver_name}")
        raise SensiSyntaxError(f"Unable to find driver_folder_id for driver_name: {driver_name}")

    # Get the local path of the input file
    local_filepath = "/".join([eco_folder_id, driver_folder_id, filename])

    # Get the framework name, sensi_1 folder id
    try:
        framework_name = query(data, "$.framework.name")[0]
        input_root_name = framework_name + "_inputs"
        folder_name = query(data, "$.framework.sensi_1.name")[0]
        folder_id = query(data, "$.framework.sensi_1.folder_id")[0]
    except (SensiSyntaxError, IndexError) as e:
        logger.error(f"Unable to get all the required data to construct input file path. Error: {e}")
        raise SensiSyntaxError("Unable to get all the required data to construct input file path")

    # Get the full path of the input file
    global_filepath = os.path.join(env_dir, "resources", folder_name, input_root_name, local_filepath).replace(
        "\\", "/"
    )
    if not os.path.exists(global_filepath):
        logger.warning(f"Input file path does not exist: {global_filepath}. Maybe paths are encrypted?")
        global_filepath = os.path.join(env_dir, "resources", folder_id, input_root_name, local_filepath).replace(
            "\\", "/"
        )
        if not os.path.exists(global_filepath):
            logger.error(f"Input file path does not exist: {global_filepath}")
            raise SensiSyntaxError("Input file path does not exist")

    logger.debug(f"Input file path: {global_filepath}")
    return global_filepath


def select_with_column_and_row(dataframe, column=None, row=None):
    """Selects a column and row from a dataframe

    Args:
        dataframe (pd.dataframe): dataframe to select from
        column (str, optional): column to select. Defaults to None.
        row (str, optional): row to select. Defaults to None.

    Raises:
        SensiSyntaxError: if any of the queries fail

    Returns:
        pd.dataframe: selected dataframe
    """
    logger.info(f"Selecting column: {column} and row: {row} from dataframe")

    if dataframe is None or dataframe.empty:
        return dataframe

    logger.debug(f"Selecting column: {column}")
    if column is not None:
        column = column.strip()
        if column == "":
            pass
        elif column.isdigit():
            column = int(column)
            if column < 1 or column > len(dataframe.columns):
                logger.error(f"Column index out of range: {column}")
                raise SensiSyntaxError(f"Column index out of range: {column}")
            dataframe = dataframe[[dataframe.columns[column - 1]]]
        elif column.startswith("'") and column.endswith("'"):
            column = column.strip("'")
            if column not in dataframe.columns:
                logger.error(f"Column not found: {column}")
                raise SensiSyntaxError(f"Column not found: {column}")
            dataframe = dataframe[[column]]
        elif column == "*":
            pass
        else:
            logger.error(f"Invalid column: {column}")
            raise SensiSyntaxError(f"Invalid column: {column}")

    if row is not None:
        row = row.strip()
        if row == "":
            pass
        elif row.isdigit():
            row = int(row)
            if row < 1 or row > len(dataframe):
                logger.error(f"Row index out of range: {row}")
                raise SensiSyntaxError(f"Row index out of range: {row}")
            dataframe = dataframe.iloc[[row - 1], :]
        elif row.startswith("'") and row.endswith("'"):
            row = row.strip("'")
            if row not in dataframe.index:
                logger.error(f"Row not found: {row}")
                raise SensiSyntaxError(f"Row not found: {row}")
            dataframe = dataframe.loc[[row]]
        elif row == "*":
            pass
        else:
            logger.error(f"Invalid row: {row}")
            raise SensiSyntaxError(f"Invalid row: {row}")

    return dataframe


def get_selection_from_dataframe(selection, dataframe):
    """Gets the selection from the dataframe

    Args:
        selection (str): selection to get
        dataframe (pd.dataframe): dataframe to get selection from

    Raises:
        SensiSyntaxError: if selection is invalid

    Returns:
        pd.dataframe: selected dataframe
    """
    logger.info(f"Getting selection from dataframe: {selection}")

    # Check if the dataframe is not empty
    if dataframe is None or dataframe.empty:
        return dataframe

    # Strip spaces and remove brackets from selection if present
    selection = selection.strip()
    if selection.startswith("[") and selection.endswith("]"):
        selection = selection[1:-1]

    logger.debug(f"Getting column and row from selection: {selection}")
    if selection.count(",") == 1:
        column, row = selection.split(",")
        column = column.strip()
        row = row.strip()
    else:
        column = selection.strip()
        row = None

    logger.debug(f"Getting column and row from dataframe: {column}, {row}")
    try:
        return select_with_column_and_row(dataframe, column, row)
    except SensiSyntaxError as e:
        logger.error(f"Unable to get selection from dataframe: {e}")
        raise SensiSyntaxError("Unable to get selection from dataframe")


def convert_value_to_true_type(value):
    """Parses the value for selection

    Args:
        value (str): value to parse

    Returns:
        int, float, str, bool, None: parsed value
    """
    logger.info(f"Parsing value for selection: {value}")

    real_value = None
    if value is None:
        logger.debug(f"Value is None")
        pass
    elif value.lower() in ["true", "false"]:
        logger.debug(f"Value is boolean")
        real_value = value.lower() == "true"
    else:
        try:
            logger.debug(f"Value is integer")
            real_value = int(value)
        except ValueError:
            try:
                logger.debug(f"Value is float")
                real_value = float(value)
            except ValueError:
                logger.debug(f"Value is string")
                real_value = value.strip("'")
    return real_value


def select_from_dataframe(condition, operation, dataframe):
    """Selects from the dataframe based on the condition and operation

    Args:
        condition (str): condition to select
        operation (str): operation to select
        dataframe (pd.dataframe): dataframe to select from

    Raises:
        SensiSyntaxError: if condition or operation is invalid

    Returns:
        pd.dataframe: selected dataframe
    """
    logger.info(f"Selecting from dataframe: {condition}, {operation}")

    try:
        lvalue, rvalue = condition.split(operation)
    except ValueError:
        logger.error(f"Invalid condition: {condition}")
        raise SensiSyntaxError("Condition must be in the form of 'lvalue operation rvalue'")
    logger.debug(f"Parsed condition: {lvalue}, {rvalue}")

    if lvalue is None or lvalue.strip() == "":
        logger.error(f"lvalue from condition is empty: {condition}")
        raise SensiSyntaxError("lvalue from condition is empty")
    lvalue = lvalue.strip()

    logger.debug(f"Getting selection from dataframe: {lvalue}")
    selected = get_selection_from_dataframe(lvalue, dataframe)

    if selected is not None and not selected.empty:
        logger.debug("Converting non empty selection to numeric")
        selected = selected.apply(pd.to_numeric, errors="ignore")

        if rvalue is None or rvalue.strip() == "":
            logger.error(f"rvalue from condition is empty: {condition}")
            raise SensiSyntaxError("rvalue from condition is empty")
        values = rvalue.strip().split(",")

        # Parse all elements in the list 'values' to their respective types
        values = [convert_value_to_true_type(value) for value in values]

        logger.debug("Using condition and values to select from dataframe")
        try:
            if operation == "==":
                dataframe = dataframe[selected.T.iloc[0].isin(values)]
            elif operation == "!=":
                dataframe = dataframe[~selected.T.iloc[0].isin(values)]
            elif operation == ">=":
                dataframe = dataframe[selected.T.iloc[0] >= values[0]]
            elif operation == ">":
                dataframe = dataframe[selected.T.iloc[0] > values[0]]
            elif operation == "<=":
                dataframe = dataframe[selected.T.iloc[0] <= values[0]]
            elif operation == "<":
                dataframe = dataframe[selected.T.iloc[0] < values[0]]
            else:
                logger.error(f"{operation} is unsupported by this tool.")
                raise SensiSyntaxError("{} is an unsupported Operation!".format(operation))
        except Exception as e:
            logger.error(f"Selection failed using {operation}: {e}")
            raise SensiSyntaxError(f"Failed to execute selection with {operation}")
    else:
        logger.warning(f"Selection from dataframe using condition {condition} is empty")
        dataframe = pd.DataFrame()

    return dataframe


def interpret_condition(condition, dataframe):
    """Interprets the condition and returns the selected dataframe

    Args:
        condition (str): condition to interpret
        dataframe (pandas.dataframe): dataframe to select from

    Raises:
        SensiSyntaxError: if condition is invalid

    Returns:
        pd.dataframe: selected dataframe
    """
    logger.info(f"Interpreting condition: {condition}")

    if condition.strip() and not dataframe.empty:
        condition = condition.strip()
        logger.debug(f"Choosing selection method using correct operator in condition")
        if condition.count("==") == 1:
            dataframe = select_from_dataframe(condition, "==", dataframe)
        elif condition.count("!=") == 1:
            dataframe = select_from_dataframe(condition, "!=", dataframe)
        elif condition.count(">=") == 1:
            dataframe = select_from_dataframe(condition, ">=", dataframe)
        elif condition.count(">") == 1:
            dataframe = select_from_dataframe(condition, ">", dataframe)
        elif condition.count("<=") == 1:
            dataframe = select_from_dataframe(condition, "<=", dataframe)
        elif condition.count("<") == 1:
            dataframe = select_from_dataframe(condition, "<", dataframe)
        else:
            logger.error(f"Incorrect condition '{condition}'.")
            raise SensiSyntaxError(f"'{condition}' is not a correct condition")

    return dataframe


def apply_value_to_selection(value, selected_dict):
    """Applies the value to the selected dataframe

    Args:
        value (str): value to apply
        selected_dict (dict): dictionary of selected data

    Raises:
        SensiSyntaxError: if value is invalid or unable to apply value to selection

    Returns:
        dict: dictionary of selected data with value applied
    """
    logger.info(f"Applying value to selection: {value}")

    applying_operation = False

    value = value.strip('"').replace(" ", "")
    if value.startswith("(") and value.endswith(")"):
        logger.debug(f"Operation {value} is inclosed in parentheses.")
        value = value.strip("()")
        applying_operation = True

    if value:
        if not applying_operation:
            if str(value).lower() in ["true", "false"]:
                value = value.lower() == "true"

            logger.debug(f"Replacing selection with value: {value}")
            for column in selected_dict.keys():
                selected_dict[column] = {k: value for k in selected_dict[column].keys()}
        else:
            logger.debug(f"Applying operation to selection")

            operation = ""
            if value[0] in ("+", "-", "*", "/"):
                operation, value = value[0], value[1:]
            try:
                value = mp.mpf(value.replace(",", "."))
                logger.debug(f"Converted value to {type(value)} .")
            except ValueError:
                logger.error(f"Invalid value: {value}")
                raise SensiSyntaxError(f"'{value}' is not a correct value")
            try:
                logger.debug(f"Applying operation: {operation}")
                # We use the mpmath module to execute operations with maximum of precision (currently 13)
                if operation == "+":
                    for column in selected_dict.keys():
                        selected_dict[column] = {
                            k: mp.nstr(mp.mpf(v) + value, PRECISION) for k, v in selected_dict[column].items()
                        }
                elif operation == "-":
                    for column in selected_dict.keys():
                        selected_dict[column] = {
                            k: mp.nstr(mp.mpf(v) - value, PRECISION) for k, v in selected_dict[column].items()
                        }
                elif operation == "*":
                    for column in selected_dict.keys():
                        selected_dict[column] = {
                            k: mp.nstr(mp.mpf(v) * value, PRECISION) for k, v in selected_dict[column].items()
                        }
                elif operation == "/":
                    for column in selected_dict.keys():
                        selected_dict[column] = {
                            k: mp.nstr(mp.mpf(v) / value, PRECISION) for k, v in selected_dict[column].items()
                        }
                else:
                    logger.debug("Applying a + as the default operation")
                    for column in selected_dict.keys():
                        selected_dict[column] = {
                            k: mp.nstr(mp.mpf(v) + value, PRECISION) for k, v in selected_dict[column].items()
                        }

            except Exception as exc:
                logger.error(
                    f"Failed to execute operation: {operation} between {selected_dict} and {value}: {str(exc)}"
                )
                raise SensiSyntaxError(
                    "Unable to execute operation '{}' between '{}' and '{}'".format(operation, selected_dict, value)
                )

    logger.debug(f"Returned dict:\n {selected_dict}")
    return selected_dict


def apply_syntax_to_file(input_path, syntax, settings_json):
    """Applies the syntax to the input file

    Args:
        input_path (str): path to the input file
        syntax (str): syntax to apply
        settings_json (dict): settings to use

    Raises:
        SensiSyntaxError: if failed to apply syntax to file

    Returns:
        boolean: True if syntax was applied successfully, False otherwise
    """
    logger.info(f"Applying syntax to file: {input_path}")

    try:
        if input_path is None:
            logger.error("No input file specified.")

        if syntax is None:
            logger.error("No syntax specified.")
            raise SensiSyntaxError("No syntax specified.")
        if settings_json is None:
            logger.error("No settings specified.")
            raise SensiSyntaxError("No settings specified.")

        logger.debug(f"Getting separators from settings.json:\n {settings_json}")
        seps = settings_json.get("gen_param").get("input_format")
        if seps is None:
            logger.error("No separators specified in settings.json.")
            raise SensiSyntaxError("No separators specified in settings.json.")
        try:
            dec_sep = seps["dec_sep"]
            col_sep = seps["col_sep"]
            logger.debug(f"Found dec_sep: {dec_sep} and col_sep: {col_sep}")
        except KeyError as e:
            logger.error(f"Missing separator in settings.json: {e}")
            raise SensiSyntaxError(f"Missing separator in settings.json: {e}")

        if not os.path.isfile(input_path):
            logger.error(f"Input file not found: {input_path}")
            raise SensiSyntaxError(f"Input file not found: {input_path}")

        logger.debug(f"Reading input file: {input_path}")
        input_df = pd.read_csv(input_path, sep=col_sep, converters={i: str for i in range(100)})

        if syntax.condition:
            logger.debug(f"Selecting from dataframe: {syntax.condition}")
            condition = syntax.condition.strip("()")
            or_conditions = condition.split("||")
            logger.debug(f"Applying conditions separated by ||: {or_conditions}")
            df_indexes_list_or = []
            for or_cond in or_conditions:
                logger.debug(f"Applying {or_cond}")
                if or_cond.strip():
                    and_conditions = or_cond.split("&&")
                    logger.debug(f"Applying conditions separated by &&: {and_conditions}")
                    df_indexes_list_and = []
                    for and_cond in and_conditions:
                        logger.debug(f"\tApplying {and_cond}")
                        selected_df = interpret_condition(and_cond, input_df)
                        df_indexes_list_and.append(set(selected_df.index))

                        logger.debug(f"Appended result of and_condition to the list.")

                    df_common_indexes = set.intersection(*df_indexes_list_and)
                    df_indexes_list_or.append(df_common_indexes)
                    logger.debug(f"Appended result of or_condition to the list.")

            df_total_indexes = set().union(*df_indexes_list_or)
            df_concat = input_df.iloc[list(df_total_indexes)]

        if syntax.col:
            logger.debug(f"Selecting data using {syntax.col} .")
            try:
                if syntax.condition:
                    logger.debug(f"Using condition {condition}")
                    selected_df = get_selection_from_dataframe(syntax.col, df_concat)
                else:
                    selected_df = get_selection_from_dataframe(syntax.col, input_df)
            except SensiSyntaxError as err:
                logger.error(f"{err.msg} in file {input_path}")
                raise err

            selected_dict = selected_df.to_dict()  # {"Nom_column": {"Num de ligne": "valeur associé"}}
            logger.debug(f"Converted selected_df to dict:\n {selected_dict}")

            if syntax.value:
                applied_dict = apply_value_to_selection(syntax.value, selected_dict)

            for column, indexes in applied_dict.items():
                for index in indexes:
                    logger.debug(f"Replacing value at [{index},{column}] with {indexes[index]}")
                    input_df.loc[index, column] = indexes[index]

            logger.debug(f"Dataframe types are:\n {input_df.dtypes}")
            os.remove(input_path)
            input_df.to_csv(input_path, sep=col_sep, index=False, float_format="%.18g")
            logger.debug(f"Saved to {input_path}:\n" + "\t" + input_df.to_string().replace("\n", "\n\t"))
            return True
        else:
            logger.error("No col found for selection")
            raise SensiSyntaxError("No col found for selection")
    except Exception as exc:
        logger.error(f"Failed to apply syntax to file: {input_path}: {exc}")
        return False
