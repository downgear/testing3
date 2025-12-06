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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException


class TC0050001(unittest.TestCase):
    # change stuff in here to init
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.base_url = "https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id="
        self.cart_url = "https://ecommerce-playground.lambdatest.io/index.php?route=checkout/cart"
        self.verificationErrors = []
        self.wait = WebDriverWait(self.driver, 10)

    def test_t_c0050001(self):
        driver = self.driver

        # --- REPORTING VARIABLES ---
        total_count = 0
        pass_count = 0
        fail_count = 0
        failed_cases = []
        # --- REPORTING VARIABLES ENDS---

        # read files
        with open('Feature-6-data-0001-0005-level-1.csv', mode='r', encoding='utf-8-sig') as csvfile:
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
                    prod_id = row['pid']
                    driver.get(self.base_url + prod_id)
                    def_price = driver.find_element(By.XPATH, "//h3[@data-update='price']").text
                    # small
                    driver.find_element(By.XPATH, "//div[contains(@class,'form-group') and contains(@class,'required')]//select").click()
                    sel = Select(driver.find_element(By.XPATH, "//div[contains(@class,'form-group') and contains(@class,'required')]//select"))
                    text = [o.text for o in sel.options if "Small" in o.text][0]
                    sel.select_by_visible_text(text)
                    # get original price for small
                    # wait for price to update
                    WebDriverWait(driver, 10).until(
                        lambda d: d.find_element(By.XPATH, "//h3[@data-update='price']").text != def_price
                    )
                    # Now safely get updated price
                    price_el = driver.find_element(By.XPATH, "//h3[@data-update='price']")
                    price_text = price_el.text.strip()
                    original_small_unit_price = float(price_text.replace("$", ""))
                    self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-redirecttocart and contains(@class, 'button-buynow')]/ancestor::div[contains(@class, 'entry-col') or contains(@class, 'entry-component')]//button[contains(@class, 'button-cart') and contains(@class, 'btn-cart')]")))
                    add_to_cart = self.wait.until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            "//button[@data-redirecttocart and contains(@class, 'button-buynow')]/ancestor::div[contains(@class, 'entry-col') or contains(@class, 'entry-component')]//button[contains(@class, 'button-cart') and contains(@class, 'btn-cart')]"
                        ))
                    )
                    add_to_cart.click()
                    # medium
                    driver.find_element(By.XPATH, "//div[contains(@class,'form-group') and contains(@class,'required')]//select").click()
                    sel = Select(driver.find_element(By.XPATH, "//div[contains(@class,'form-group') and contains(@class,'required')]//select"))
                    text = [o.text for o in sel.options if "Medium" in o.text][0]
                    sel.select_by_visible_text(text)
                    self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-redirecttocart and contains(@class, 'button-buynow')]/ancestor::div[contains(@class, 'entry-col') or contains(@class, 'entry-component')]//button[contains(@class, 'button-cart') and contains(@class, 'btn-cart')]")))
                    add_to_cart = self.wait.until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            "//button[@data-redirecttocart and contains(@class, 'button-buynow')]/ancestor::div[contains(@class, 'entry-col') or contains(@class, 'entry-component')]//button[contains(@class, 'button-cart') and contains(@class, 'btn-cart')]"
                        ))
                    )
                    add_to_cart.click()
                    # large
                    driver.find_element(By.XPATH, "//div[contains(@class,'form-group') and contains(@class,'required')]//select").click()
                    sel = Select(driver.find_element(By.XPATH, "//div[contains(@class,'form-group') and contains(@class,'required')]//select"))
                    text = [o.text for o in sel.options if "Large" in o.text][0]
                    sel.select_by_visible_text(text)
                    self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[@data-redirecttocart and contains(@class, 'button-buynow')]/ancestor::div[contains(@class, 'entry-col') or contains(@class, 'entry-component')]//button[contains(@class, 'button-cart') and contains(@class, 'btn-cart')]")))
                    add_to_cart = self.wait.until(
                        EC.element_to_be_clickable((
                            By.XPATH,
                            "//button[@data-redirecttocart and contains(@class, 'button-buynow')]/ancestor::div[contains(@class, 'entry-col') or contains(@class, 'entry-component')]//button[contains(@class, 'button-cart') and contains(@class, 'btn-cart')]"
                        ))
                    )
                    add_to_cart.click()
                    # cart
                    driver.get(self.cart_url)
                    # remove other item
                    rows = driver.find_elements(
                        By.XPATH,
                        f"//tr[td[@class='text-left'] and not(.//a[contains(@href,'product_id={prod_id}')])]"
                    )
                    for i in range(len(rows)-1, -1, -1):
                        tr = rows[i]
                        delete_btn = tr.find_element(
                            By.XPATH,
                            ".//button[contains(@class,'btn-danger') and @type='button']"
                        )
                        self.wait.until(EC.element_to_be_clickable(delete_btn))
                        delete_btn.click()
                    # reset quantity
                    items_to_update = [
                        ("Small", row['xsmall']),
                        ("Medium", row['xmedium']),
                        ("Large", row['xlarge']),
                    ]

                    for size_label, qty in items_to_update:
                        tr = driver.find_element(
                            By.XPATH,
                            f"//tr[td[@class='text-left'] and .//a[contains(@href,'product_id={prod_id}')] and .//small[normalize-space()='Size: {size_label}']]"
                        )
                        qty_input = self.wait.until(lambda d: tr.find_element(By.XPATH, ".//input[contains(@name,'quantity')]"))
                        qty_input.clear()
                        qty_input.send_keys(qty)
                        update_btn = tr.find_element(
                            By.XPATH,
                            ".//button[contains(@class,'btn-primary') and @type='submit']"
                        )
                        self.wait.until(EC.element_to_be_clickable(update_btn))
                        update_btn.click()
                    # end reset quantity

                    tr = driver.find_element(
                        By.XPATH,
                        f"//tr[td[@class='text-left'] and .//a[contains(@href,'product_id={prod_id}')] and .//small[normalize-space()='Size: Small']]"
                    )
                    unit_price_el = tr.find_element(By.XPATH, ".//td[@class='text-right'][1]")
                    new_small_unit_price = float(unit_price_el.text.strip().replace("$", ""))

                    if row['discount']:
                        self.assertLess(
                            new_small_unit_price,
                            original_small_unit_price,
                            f"There was supposed to be a discount."
                        )

                    if (row['error']):
                        self.assertTrue(
                            self.is_element_present(By.XPATH, "//div[contains(@class,'alert-danger')]")
                        )
                    else:
                        self.assertTrue(
                            self.is_element_present(By.XPATH, "//div[contains(@class,'alert-success')]")
                        )
                        self.assertFalse(
                            self.is_element_present(By.XPATH, "//div[contains(@class,'alert-danger')]")
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
