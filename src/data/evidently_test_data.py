from src.classes.data.DataManager import DataManager
from definitions import ROOT_DIR

from evidently.metric_preset import DataDriftPreset
from evidently.test_suite import TestSuite
from evidently.report import Report
from evidently.tests import *

import pandas as pd
import sys
import os


def main():
    df_reference_file = os.path.join(ROOT_DIR, "data", "reference_data.csv")
    df_reference = pd.read_csv(df_reference_file)

    df_current_file = os.path.join(ROOT_DIR, "data", "current_data.csv")
    df_current = pd.read_csv(df_current_file)

    report = Report(metrics=[
        DataDriftPreset()
    ])

    report.run(
        reference_data=df_reference,
        current_data=df_current
    )

    # Create directory for reports if it doesn't exist
    reports_dir = os.path.join(ROOT_DIR, "reports", "data_tests")
    DataManager.make_directory_if_missing(reports_dir)

    report.save(os.path.join(reports_dir, "data_drift.json"))

    tests = TestSuite(tests=[
        TestNumberOfConstantColumns(),
        TestNumberOfDuplicatedRows(),
        TestNumberOfDuplicatedColumns(),
        TestColumnsType(),
        TestNumberOfDriftedColumns(),
    ])

    tests.run(
        reference_data=df_reference,
        current_data=df_current
    )
    test_results = tests.as_dict()

    # Check if any test failed
    if test_results['summary']['failed_tests'] > 0:
        print("Some tests failed:")
        print(test_results['summary'])

        sys.exit(1)
    else:
        print("All tests passed!")

    # Create directory for reports if it doesn't exist
    reports_dir = os.path.join(ROOT_DIR, "reports", "sites")
    DataManager.make_directory_if_missing(reports_dir)

    tests.save_html(os.path.join(reports_dir, "stability_tests.html"))


if __name__ == "__main__":
    main()
