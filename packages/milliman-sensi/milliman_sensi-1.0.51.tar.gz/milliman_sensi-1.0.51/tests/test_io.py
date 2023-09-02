import inspect
import os
import shutil
import sys
import tempfile

import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

import milliman_sensi.io as sio

TEST_DIR = os.path.dirname(inspect.getfile(inspect.currentframe())).replace("\\", "/")


def test_read_json_successful():
    data = sio.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/settings.json")
    assert data is not None


def test_read_json_inexistent_file():
    with pytest.raises(FileNotFoundError):
        sio.read_json_file("not_exists.json")


def test_read_json_invalid_file():
    with pytest.raises(ValueError):
        sio.read_json_file(f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/resources/invalid_settings.json")


############################################################################################################


def test_find_file_in_directory_successful():
    res = sio.find_file_in_directory(
        "Sensi_config.csv",
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities",
    )
    assert res == f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config.csv"


def test_find_file_in_directory_with_file_inexistent():
    assert sio.find_file_in_directory("inexistent_file.csv", ".") is None


def test_find_file_in_directory_with_target_dir_inexistent():
    assert sio.find_file_in_directory("searched_file.csv", "inexistent_directory") is None


############################################################################################################


def test_read_csv_from_filepath_successful():
    sensi_config_input_csv = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config.csv"
    assert isinstance(sio.read_csv_from_filepath(sensi_config_input_csv), type(pd.DataFrame()))


def test_read_csv_from_filepath_with_inexistent_file():
    with pytest.raises(FileNotFoundError):
        sio.read_csv_from_filepath("inexistent_file.csv")


def test_read_csv_from_filepath_with_non_allowed_extension():
    csv_file_input = (
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_with_non_allowed_extension.txt"
    )
    with pytest.raises(ValueError):
        sio.read_csv_from_filepath(csv_file_input)


def test_read_csv_from_filepath_with_file_containing_unallowed_characters():
    csv_file_input = (
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_with_unallowed_characters.csv"
    )
    with pytest.raises(ValueError):
        sio.read_csv_from_filepath(csv_file_input)


def test_read_csv_from_filepath_with_file_using_comma_as_delimiter():
    csv_file_input = (
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_with_comma_as_delimiter.csv"
    )
    assert isinstance(sio.read_csv_from_filepath(csv_file_input), type(pd.DataFrame()))


def test_read_csv_from_filepath_with_file_containing_semicolons_in_values():
    csv_file_input = (
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_with_semicolons_in_values.csv"
    )
    res = sio.read_csv_from_filepath(csv_file_input)
    assert res.iloc[1, 0] == "Sensi_1_SEMI_COL"


############################################################################################################


def test_validate_sensi_config_successful():
    sensi_config_input_csv = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config.csv"
    res = sio.validate_sensi_config(sensi_config_input_csv)
    assert isinstance(res, type(pd.DataFrame()))
    assert (res.columns == ["Scenario", "Stress name", "Apply stress"]).all()


def test_validate_sensi_config_with_incorrect_csv():
    sensi_config_input_csv = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_bad_csv.csv"
    res = sio.validate_sensi_config(sensi_config_input_csv)
    assert (
        res
        == "Sensitivity configuration file header is incorrect. Expected ['Scenario', 'Stress name', 'Apply stress'], got ['Scenario_123', 'Stress name', 'Apply stress']"
    )


def test_validate_sensi_config_with_incorrect_header():
    sensi_config_input_csv = (
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_incorrect_header.csv"
    )
    res = sio.validate_sensi_config(sensi_config_input_csv)
    assert (
        res
        == "Sensitivity configuration file header is incorrect. Expected ['Scenario', 'Stress name', 'Apply stress'], got ['Scenario_123', 'Stress name123', 'Apply stress']"
    )


def test_validate_sensi_config_with_missing_header():
    sensi_config_input_csv = (
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_missing_header.csv"
    )
    res = sio.validate_sensi_config(sensi_config_input_csv)
    assert (
        res
        == "Sensitivity configuration file header is incorrect. Expected ['Scenario', 'Stress name', 'Apply stress'], got ['Scenario', 'Apply stress123']"
    )


def test_validate_sensi_config_with_extra_header():
    sensi_config_input_csv = (
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_extra_header.csv"
    )
    res = sio.validate_sensi_config(sensi_config_input_csv)
    assert (
        res
        == "Sensitivity configuration file header is incorrect. Expected ['Scenario', 'Stress name', 'Apply stress'], got ['Scenario', 'Stress name', 'Stress value', 'Apply stress', 'Remove stress']"
    )


def test_validate_sensi_config_with_incorrect_values_in_Apply_stress():
    sensi_config_input_csv = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_incorrect_values_in_Apply_stress.csv"
    res = sio.validate_sensi_config(sensi_config_input_csv)
    assert (
        res == "Sensitivity configuration file has the wrong values in 'Apply stress'. Rows with wrong values: [1, 3]"
    )


def test_validate_sensi_config_with_empty_input_file():
    sensi_config_input_csv = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_empty.csv"
    res = sio.validate_sensi_config(sensi_config_input_csv)
    assert res == "File is empty"


def test_validate_sensi_config_with_invalid_character():
    sensi_config_input_csv = (
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_with_invalid_char.csv"
    )
    res = sio.validate_sensi_config(sensi_config_input_csv)
    assert res == "File is not a valid csv file"


def test_validate_sensi_config_with_invalid_separator():
    sensi_config_input_csv = (
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_with_invalid_sep.csv"
    )
    res = sio.validate_sensi_config(sensi_config_input_csv)
    assert res == 'File contains the delimiter "~" which is not allowed in sensi csv files'


def test_validate_sensi_config_with_file_containing_semicolons_in_values():
    sensi_config_input_csv = (
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_config_with_semicolons_in_values.csv"
    )
    res = sio.validate_sensi_config(sensi_config_input_csv)
    assert isinstance(res, type(pd.DataFrame()))
    assert res.iloc[0, 0] == "Sensi_1_SEMI_COL"


############################################################################################################


def test_validate_sensi_param_successful():
    sensi_param_input_csv = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_param.csv"
    res = sio.validate_sensi_param(sensi_param_input_csv)
    assert isinstance(res, type(pd.DataFrame()))
    assert res.columns[0] == "Name"


def test_validate_sensi_param_with_incorrect_csv():
    sensi_param_bad_path = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_param_bad_csv.csv"
    res = sio.validate_sensi_param(sensi_param_bad_path)
    assert (
        res
        == "Sensitivities parameters file has the wrong number of columns. Rows with wrong number of columns: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
    )


def test_validate_sensi_param_without_Name():
    sensi_param_bad_path = (
        f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_param_missing_Name.csv"
    )
    res = sio.validate_sensi_param(sensi_param_bad_path)
    assert res == 'Sensitivity parameters file first column is not the "Name" column'


############################################################################################################


def test_read_sensitivities_successful():
    env_dir = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857"
    sensi_list, _, param_map = sio.read_sensitivities(env_dir)
    assert sensi_list == {"Sensi_1": ["Stress_vol_1"]}
    assert param_map == {"Stress_vol_1": ["param.n_s=500"]}


def test_copy_dir_nested_files_and_subdirs():
    temp_dir = tempfile.mkdtemp()
    base_rsrc_dir = os.path.join(temp_dir, "base_rsrc_dir")
    sensi_rsrc_dir = os.path.join(temp_dir, "sensi_rsrc_dir")
    try:
        os.makedirs(base_rsrc_dir)
        temp_subdir1 = os.path.join(base_rsrc_dir, "subdir1")
        temp_subdir2 = os.path.join(base_rsrc_dir, "subdir2")
        os.makedirs(temp_subdir1)
        os.makedirs(temp_subdir2)
        temp_file1 = os.path.join(base_rsrc_dir, "file1.txt")
        temp_file2 = os.path.join(temp_subdir1, "file2.txt")
        with open(temp_file1, "w") as f1, open(temp_file2, "w") as f2:
            f1.write("File 1 contents")
            f2.write("File 2 contents")

        sio.copy_dir(base_rsrc_dir, sensi_rsrc_dir)

        assert os.path.exists(os.path.join(sensi_rsrc_dir, "file1.txt"))
        assert os.path.exists(os.path.join(sensi_rsrc_dir, "subdir1", "file2.txt"))
        assert os.path.isfile(os.path.join(sensi_rsrc_dir, "file1.txt"))
        assert os.path.isfile(os.path.join(sensi_rsrc_dir, "subdir1", "file2.txt"))
        assert os.path.isdir(os.path.join(sensi_rsrc_dir, "subdir2"))
    finally:
        shutil.rmtree(temp_dir)


@pytest.mark.skipif(sys.platform != "linux", reason="Symlinks only supported on Linux")
def test_copy_dir_symlink_point_to_dir():
    temp_dir = tempfile.mkdtemp()
    base_rsrc_dir = os.path.join(temp_dir, "base_rsrc_dir")
    sensi_rsrc_dir = os.path.join(temp_dir, "sensi_rsrc_dir")
    try:
        os.makedirs(base_rsrc_dir)
        temp_subdir = os.path.join(temp_dir, "subdir")
        os.makedirs(temp_subdir)
        temp_file = os.path.join(temp_subdir, "file1.txt")
        with open(temp_file, "w") as f:
            f.write("File 1 contents")

        temp_link = os.path.join(base_rsrc_dir, "symlink")
        os.symlink(temp_subdir, temp_link)

        sio.copy_dir(base_rsrc_dir, sensi_rsrc_dir)

        assert os.path.exists(os.path.join(sensi_rsrc_dir, "symlink", "file1.txt"))

    finally:
        shutil.rmtree(temp_dir)


@pytest.mark.skipif(sys.platform != "linux", reason="Symlinks only supported on Linux")
def test_copy_dir_skip_dangling_symlink():
    temp_dir = tempfile.mkdtemp()
    base_rsrc_dir = os.path.join(temp_dir, "base_rsrc_dir")
    sensi_rsrc_dir = os.path.join(temp_dir, "sensi_rsrc_dir")
    try:
        os.makedirs(base_rsrc_dir)
        temp_link = os.path.join(base_rsrc_dir, "symlink")
        os.symlink("/path/to/nonexistent/target", temp_link)

        sio.copy_dir(base_rsrc_dir, sensi_rsrc_dir)

        assert not os.path.exists(os.path.join(sensi_rsrc_dir, "symlink"))
    finally:
        shutil.rmtree(temp_dir)


def test_copy_dir_existing_destination():
    temp_dir = tempfile.mkdtemp()
    base_rsrc_dir = os.path.join(temp_dir, "base_rsrc_dir")
    sensi_rsrc_dir = os.path.join(temp_dir, "sensi_rsrc_dir")
    try:
        os.makedirs(base_rsrc_dir)
        temp_file = os.path.join(base_rsrc_dir, "file.txt")
        with open(temp_file, "w") as f:
            f.write("File contents")

        # Create an existing directory in the destination path
        os.makedirs(os.path.join(sensi_rsrc_dir, "existing_dir"))

        sio.copy_dir(base_rsrc_dir, sensi_rsrc_dir)

        assert os.path.isdir(os.path.join(sensi_rsrc_dir, "existing_dir"))
        assert not os.path.isfile(os.path.join(sensi_rsrc_dir, "existing_dir", "file.txt"))
    finally:
        shutil.rmtree(temp_dir)


############################################################################################################


def test_create_dir_for_one_sensi_from_base_successful(tmpdir):
    base_dir = f"{TEST_DIR}/LMMP_Up_31122020_RN_Simulation"

    tmpath = str(tmpdir.mkdir("test_sensi_path")).replace("\\", "/")
    sensi_path = f"{tmpath}/Sensi_1"
    sensi_name = "Sensi_1"
    os.mkdir(sensi_path)

    path_to_sensi = sio.create_dir_for_one_sensi_from_base(sensi_name, sensi_path, base_dir)
    assert path_to_sensi == sensi_path and os.path.exists(path_to_sensi) is True

    path_to_sensi_list = os.listdir(path_to_sensi)
    assert len(path_to_sensi_list) == 2


def test_create_dir_for_one_sensi_from_base_dir_inexistent():
    sensi_name = "Sensi_1"
    sensi_path = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857/sensitivities/Sensi_1"
    base_dir = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857_inexistent"
    res = sio.create_dir_for_one_sensi_from_base(sensi_name, sensi_path, base_dir)
    assert isinstance(res, sio.SensiIOError)


############################################################################################################


def test_get_stress_desc_successful():
    env_dir = f"{TEST_DIR}/LMMP_Up_31122020_RN_Simulation"
    test_SensiConfig = sio.SensiConfig(env_dir)
    assert (
        test_SensiConfig.get_stress_desc("Sensi_2")
        == """file::eco[EUR].driver[RIR].data.init_curve.mkt['BEIR rate',1]=(-0.023933085882)>>file::eco[EUR].driver[RIR].data.init_curve.mkt['BEIR rate',2]=(-0.023933085882)>>file::eco[EUR].driver[RIR].data.init_curve.mkt['BEIR rate',3]=(-0.023933085882)>>file::eco[EUR].driver[RIR].data.init_curve.mkt['BEIR rate',4]=(-0.023863016373)>>file::eco[EUR].driver[RIR].data.init_curve.mkt['BEIR rate',5]=(-0.023574089337)"""
    )


############################################################################################################


def test_create_tables_successful(tmpdir):
    env_dir = f"{TEST_DIR}/LMMP_Up_31122020_RN_Simulation"
    test_SensiConfig = sio.SensiConfig(env_dir)

    tmpath = str(tmpdir.mkdir("test_create_tables")).replace("\\", "/")
    sensi_1_dir = f"{tmpath}/Sensi_1"
    os.mkdir(sensi_1_dir)
    sensi_dirs = {"Sensi_1": sensi_1_dir}

    assert test_SensiConfig.create_tables(sensi_dirs) == sensi_dirs


############################################################################################################


def test_apply_successful(tmpdir):
    env_dir = f"{TEST_DIR}/LMMP_Up_31122020_RN_Simulation"
    test_SensiConfig = sio.SensiConfig(env_dir)

    test_sensi_path = str(tmpdir.mkdir("test_sensi_path")).replace("\\", "/")
    if os.path.exists(test_sensi_path):
        shutil.rmtree(test_sensi_path)

    shutil.copytree(f"{TEST_DIR}/test_apply_bnp_backup", test_sensi_path)

    sensi_dirs = {
        "Sensi_1": f"{test_sensi_path}/Sensi_1",
        "Sensi_2": f"{test_sensi_path}/Sensi_2",
    }

    expected_apply = {
        "Sensi_1": "Applied 11 modification(s) on Sensi_1",
        "Sensi_2": "Applied 5 modification(s) on Sensi_2",
    }
    res_apply = test_SensiConfig.apply(sensi_dirs)
    assert res_apply == expected_apply


def test_apply_only_settings_modif(tmpdir):
    env_dir = f"{TEST_DIR}/Central_RN_Simulation_20201218_152857"
    test_SensiConfig = sio.SensiConfig(env_dir)

    test_sensi_path = str(tmpdir.mkdir("test_sensi_path")).replace("\\", "/")
    if os.path.exists(test_sensi_path):
        shutil.rmtree(test_sensi_path)

    shutil.copytree(f"{TEST_DIR}/test_apply_backup", test_sensi_path)

    sensi_dirs = {"Sensi_1": f"{test_sensi_path}/Sensi_1"}

    expected_apply = {"Sensi_1": "Applied 1 modification(s) on Sensi_1"}

    res_apply = test_SensiConfig.apply(sensi_dirs)
    assert res_apply == expected_apply
