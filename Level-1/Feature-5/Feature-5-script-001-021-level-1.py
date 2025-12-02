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
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.base_url = "https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=88"
        self.verificationErrors = []

    def test_t_c0050001(self):
        driver = self.driver

        # --- REPORTING VARIABLES ---
        total_count = 0
        pass_count = 0
        fail_count = 0
        failed_cases = []

        with open('Feature-5-data-001-021-level-1.csv', mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            for row in reader:
                total_count += 1
                tc_id = row['TC_ID']
                test_name = row.get('TestName', '')
                print(f"Running Test Case: {tc_id} - {test_name}")
                try:
                    driver.get(self.base_url)
                    driver.find_element(By.LINK_TEXT, "Ask Question").click()

                    driver.find_element(By.NAME, "email").send_keys("dang.nguyen106@hcmut.edu.vn")
                    driver.find_element(By.NAME, "subject").send_keys("A" * int(row["subLen"]))
                    driver.find_element(By.NAME, "message").send_keys("A" * int(row["questionLen"]))
                    driver.find_element(By.NAME, "name").send_keys("A" * int(row["nameLen"]))

                    driver.find_element(By.XPATH, "//button[@type='submit']").click()

                    if row["errorMsg"]:
                        selector = (
                            "//div[contains(@class,'form-group')][.//input[@name='" + row['errorInput'] + "']]"
                            "//div[contains(@class,'error') and contains(@class,'text-danger')] | "
                            "//div[contains(@class,'form-group')][.//textarea[@name='" + row['errorInput'] + "']]"
                            "//div[contains(@class,'error') and contains(@class,'text-danger')]"
                        )
                        actual = driver.find_element(By.XPATH, selector).text
                        self.assertEqual(row["errorMsg"], actual)
                    else:
                        self.assertTrue(
                            self.is_element_present(
                                By.XPATH,
                                "//div[contains(@class,'alert-success') and contains(.,'successfully sent')]"
                            )
                        )

                    print(f"  [PASS] {tc_id}")
                    pass_count += 1
                except AssertionError as e:
                    # --- FAILURE ---
                    full_error = str(e)

                    # Logic: Cut the error string at "not found" to avoid printing the whole page body
                    marker = "not found"
                    if marker in full_error:
                        end_index = full_error.find(marker) + len(marker)
                        short_error = full_error[:end_index]
                    else:
                        short_error = full_error.split('\n')[0]

                    # Print immediate result (Truncated)
                    print(f"  [FAIL] {tc_id} - {short_error}")

                    fail_count += 1
                    failed_cases.append(f"{tc_id}: {short_error}")

                except Exception as e:
                    # --- SCRIPT ERROR ---
                    print(f"  [ERROR] {tc_id} - Script Error: {str(e)}")
                    fail_count += 1
                    failed_cases.append(f"{tc_id}: Script Error - {str(e)}")

                finally:
                    print("-" * 50)

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
        # --- TEST EXECUTION SUMMARY ---

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
