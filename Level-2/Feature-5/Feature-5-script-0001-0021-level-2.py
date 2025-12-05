# -*- coding: utf-8 -*-
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class TC0050001(unittest.TestCase):
    # change stuff in here to init
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.config = self._load_config('Feature-5-config-level-2.csv')
        self.verificationErrors = []

    def _load_config(self, config_file):
        """
        Load element configuration from CSV file.

        Returns a dictionary mapping element names to their locator information.
        Format: {element_name: {'type': locator_type, 'value': locator_value}}
        """
        LOCATOR_MAP = {
            'id': By.ID,
            'name': By.NAME,
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'link_text': By.LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT,
            'tag_name': By.TAG_NAME,
            'class_name': By.CLASS_NAME,
            'url': 'url'  # Special case
        }
        config = {}
        try:
            with open(config_file, mode='r', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile, delimiter='\t')
                for row in reader:
                    element_name = row['ElementName']
                    locator_type = row['LocatorType']
                    locator_value = row['LocatorValue']
                    if locator_type not in LOCATOR_MAP:
                        raise ValueError(f"Unknown locator type: {locator_type}")
                    config[element_name] = {
                        'type': LOCATOR_MAP[locator_type],
                        'value': locator_value
                    }
            return config
        except FileNotFoundError:
            raise Exception(f"Configuration file '{config_file}' not found!")

    def test_t_c0050001(self):
        driver = self.driver

        # --- REPORTING VARIABLES ---
        total_count = 0
        pass_count = 0
        fail_count = 0
        failed_cases = []
        # --- REPORTING VARIABLES ENDS---

        # read files
        with open('Feature-5-data-0001-0021-level-2.csv', mode='r', encoding='utf-8-sig') as csvfile:
            # set correct delimiter for csv file (\t for tab)
            reader = csv.DictReader(csvfile, delimiter='\t')
            # read in row
            for row in reader:
                # begin testing
                total_count += 1
                tc_id = row['TC_ID']
                test_name = row.get('TestName', '')
                print(f"Running Test Case: {tc_id} - {test_name}")
                try:
                    driver.get(self.config['BaseUrl']['value'])
                    driver.find_element(self.config['AskQuestionBtn']['type'], self.config['AskQuestionBtn']['value']).click()

                    driver.find_element(self.config['Email']['type'], self.config['Email']['value']).send_keys("dang.nguyen106@hcmut.edu.vn")
                    driver.find_element(self.config['Subject']['type'], self.config['Subject']['value']).send_keys("A" * int(row["subLen"]))
                    driver.find_element(self.config['Message']['type'], self.config['Message']['value']).send_keys("A" * int(row["questionLen"]))
                    driver.find_element(self.config['Name']['type'], self.config['Name']['value']).send_keys("A" * int(row["nameLen"]))

                    driver.find_element(self.config['SubmitBtn']['type'], self.config['SubmitBtn']['value']).click()

                    if row["errorMsg"]:
                        selector = (
                            "//div[contains(@class,'form-group')][.//input[@name='" + row['input'] + "']]" +
                            self.config['ErrToast']['value'] +
                            " | " +
                            "//div[contains(@class,'form-group')][.//textarea[@name='" + row['input'] + "']]" +
                            self.config['ErrToast']['value']
                        )
                        self.assertTrue(
                            self.is_element_present(
                                self.config['ErrToast']['type'],
                                selector,
                            ),
                            f"Did not handle {row['input']} correctly"
                        )
                        actual = driver.find_element(By.XPATH, selector).text
                        self.assertEqual(row["errorMsg"], actual)
                    else:
                        self.assertTrue(
                            self.is_element_present(
                                self.config['SuccessToast']['type'], self.config['SuccessToast']['value']
                            ),
                            f"Did not handle {row['input']} correctly"
                        )

                    print(f"  [PASS] {tc_id}")
                    pass_count += 1

                # --- ERR LOG ---
                except AssertionError as e:
                    full_error = str(e)
                    marker = "not found"
                    if marker in full_error:
                        end_index = full_error.find(marker) + len(marker)
                        short_error = full_error[:end_index]
                    else:
                        short_error = full_error.split('\n')[0]
                    print(f"  [FAIL] {tc_id} - {short_error}")

                    fail_count += 1
                    failed_cases.append(f"{tc_id}: {short_error}")

                except Exception as e:
                    print(f"  [ERROR] {tc_id} - Script Error: {str(e)}")
                    fail_count += 1
                    failed_cases.append(f"{tc_id}: Script Error - {str(e)}")

                finally:
                    print("-" * 50)
                # --- ERR LOG ENDS ---

        # --- TEST EXECUTION SUMMARY ---
        print("\n" + "="*50)
        print("            TEST EXECUTION SUMMARY")
        print("="*50)
        print(f"Total Test Cases Run : {total_count}")
        print(f"Passed               : {pass_count}")
        print(f"Failed               : {fail_count}")
        print("-" * 50)

        if fail_count > 0:
            print("FAILED CASES DETAILS:")
            for failure in failed_cases:
                print(f" -> {failure}")
        else:
            print("All test cases passed successfully.")
        print("="*50 + "\n")
        # --- TEST EXECUTION SUMMARY ENDS---

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
