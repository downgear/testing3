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
        self.base_url = "https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=88"
        self.verificationErrors = []

    def test_t_c0050001(self):
        driver = self.driver

        # --- REPORTING VARIABLES ---
        total_count = 0
        pass_count = 0
        fail_count = 0
        failed_cases = []
        # --- REPORTING VARIABLES ENDS---

        # read files
        with open('Feature-5-data-0042-level-1.csv', mode='r', encoding='utf-8-sig') as csvfile:
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
                    driver.get(self.base_url)
                    driver.find_element(By.LINK_TEXT, "Ask Question").click()

                    driver.find_element(By.NAME, "email").send_keys("dang.nguyen106@hcmut.edu.vn")
                    driver.find_element(By.NAME, "subject").send_keys(row["subject"])
                    driver.find_element(By.NAME, "message").send_keys(row["question"])
                    driver.find_element(By.NAME, "name").send_keys(row["name"])

                    driver.find_element(By.XPATH, "//button[@type='submit']").click()
                    inp = row["input"]
                    inps = inp.split(",") if inp else []
                    errMsg = row["errorMsg"]
                    errMsgs = errMsg.split(",") if errMsg else []

                    for (input, errMessage) in zip(inps, errMsgs):
                        selector = (
                            "//div[contains(@class,'form-group')][.//input[@name='" + input + "']]"
                            "//div[contains(@class,'error') and contains(@class,'text-danger')] | "
                            "//div[contains(@class,'form-group')][.//textarea[@name='" + input + "']]"
                            "//div[contains(@class,'error') and contains(@class,'text-danger')]"
                        )
                        self.assertTrue(
                            self.is_element_present(
                                By.XPATH,
                                selector,
                            ),
                            f"Did not handle {input} correctly"
                        )
                        actual = driver.find_element(By.XPATH, selector).text
                        self.assertEqual(errMessage, actual)

                    driver.find_element(By.NAME, "subject").clear()
                    driver.find_element(By.NAME, "message").clear()
                    driver.find_element(By.NAME, "name").clear()
                    driver.find_element(By.NAME, "subject").send_keys(row["csubject"])
                    driver.find_element(By.NAME, "message").send_keys(row["cquestion"])
                    driver.find_element(By.NAME, "name").send_keys(row["cname"])

                    driver.find_element(By.XPATH, "//button[@type='submit']").click()
                    self.assertTrue(
                        self.is_element_present(
                            By.XPATH,
                            "//div[contains(@class,'alert-success') and contains(.,'successfully sent')]"
                        ),
                        f"Did not handle correctly"
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
