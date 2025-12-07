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
import traceback


class TC0050001(unittest.TestCase):
    # change stuff in here to init
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        self.config = self._load_config('Feature-6-config-level-2.csv')
        self.verificationErrors = []
        self.wait = WebDriverWait(self.driver, 10)

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
        with open('Feature-6-data-0001-0005-level-2.csv', mode='r', encoding='utf-8-sig') as csvfile:
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
                    driver.get(self.config['BaseUrl']['value'] + prod_id)
                    def_price = driver.find_element(self.config['PriceText']['type'], self.config['PriceText']['value']).text
                    # small
                    driver.find_element(self.config['SizeForm']['type'], self.config['SizeForm']['value']).click()
                    sel = Select(driver.find_element(self.config['SizeForm']['type'], self.config['SizeForm']['value']))
                    text = [o.text for o in sel.options if "Small" in o.text][0]
                    sel.select_by_visible_text(text)
                    # get original price for small
                    # wait for price to update
                    WebDriverWait(driver, 10).until(
                        lambda d: d.find_element(self.config['PriceText']['type'], self.config['PriceText']['value']).text != def_price
                    )
                    # Now safely get updated price
                    price_el = driver.find_element(self.config['PriceText']['type'], self.config['PriceText']['value'])
                    price_text = price_el.text.strip()
                    original_small_unit_price = float(price_text.replace("$", ""))
                    self.wait.until(EC.presence_of_element_located((self.config['AddCartBtn']['type'], self.config['AddCartBtn']['value'])))
                    add_to_cart = self.wait.until(
                        EC.element_to_be_clickable((
                            self.config['AddCartBtn']['type'], self.config['AddCartBtn']['value']
                        ))
                    )
                    add_to_cart.click()
                    # medium
                    driver.find_element(self.config['SizeForm']['type'], self.config['SizeForm']['value']).click()
                    sel = Select(driver.find_element(self.config['SizeForm']['type'], self.config['SizeForm']['value']))
                    text = [o.text for o in sel.options if "Medium" in o.text][0]
                    sel.select_by_visible_text(text)
                    self.wait.until(EC.presence_of_element_located((self.config['AddCartBtn']['type'], self.config['AddCartBtn']['value'])))
                    add_to_cart = self.wait.until(
                        EC.element_to_be_clickable((
                            self.config['AddCartBtn']['type'], self.config['AddCartBtn']['value']
                        ))
                    )
                    add_to_cart.click()
                    # large
                    driver.find_element(self.config['SizeForm']['type'], self.config['SizeForm']['value']).click()
                    sel = Select(driver.find_element(self.config['SizeForm']['type'], self.config['SizeForm']['value']))
                    text = [o.text for o in sel.options if "Large" in o.text][0]
                    sel.select_by_visible_text(text)
                    self.wait.until(EC.presence_of_element_located((self.config['AddCartBtn']['type'], self.config['AddCartBtn']['value'])))
                    add_to_cart = self.wait.until(
                        EC.element_to_be_clickable((
                            self.config['AddCartBtn']['type'], self.config['AddCartBtn']['value']
                        ))
                    )
                    add_to_cart.click()
                    # cart
                    driver.get(self.config['CartUrl']['value'])
                    # remove other item
                    rows = driver.find_elements(
                        self.config['TrNot']['type'], self.config['TrNot']['value'].format(prod_id=prod_id)
                    )
                    for i in range(len(rows)-1, -1, -1):
                        tr = rows[i]
                        delete_btn = tr.find_element(
                            self.config['ErrTxt']['type'], self.config['ErrTxt']['value']
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
                        retry = 0
                        while (retry < 3):
                            try:
                                qty_input = self.wait.until(lambda d: d.find_element(
                                    self.config['SizeBtn']['type'],
                                    self.config['SizeBtn']['value'].format(prod_id=prod_id, size_label=size_label)
                                ).find_element(self.config['QuantInp']['type'], self.config['QuantInp']['value']))
                                qty_input.clear()
                                qty_input.send_keys(qty)
                                break
                            except StaleElementReferenceException:
                                retry += 1

                        retry = 0
                        while (retry < 3):
                            try:
                                update_btn = self.wait.until(lambda d: d.find_element(
                                    self.config['SizeBtn']['type'],
                                    self.config['SizeBtn']['value'].format(prod_id=prod_id, size_label=size_label)
                                ).find_element(self.config['UpdCartBtn']['type'], self.config['UpdCartBtn']['value']))
                                self.wait.until(EC.element_to_be_clickable(update_btn))
                                update_btn.click()
                                break
                            except StaleElementReferenceException:
                                retry += 1
                    # end reset quantity

                    unit_price_el = self.wait.until(lambda d:
                                                    d.find_element(
                                                        self.config['SizeBtn']['type'],
                                                        self.config['SizeBtn']['value'].format(prod_id=prod_id, size_label="Small")
                                                    ).find_element(
                                                        self.config['UnitPrcTxt']['type'],
                                                        self.config['UnitPrcTxt']['value']
                                                    )
                                                    )
                    new_small_unit_price = float(unit_price_el.text.strip().replace("$", ""))

                    if row['discount']:
                        self.assertLess(
                            new_small_unit_price,
                            original_small_unit_price,
                            f"There was supposed to be a discount."
                        )

                    if (row['fail']):
                        self.assertTrue(
                            self.is_element_present(self.config['ErrTxt']['type'], self.config['ErrTxt']['value'])
                        )
                        text = self.driver.find_element(self.config['ErrTxt']['type'], self.config['ErrTxt']['value']).text
                        self.assertIn(row['Expected Result'], text)
                    else:
                        self.assertTrue(
                            self.is_element_present(self.config['SuccessTxt']['type'], self.config['SuccessTxt']['value'])
                        )
                        text = self.driver.find_element(self.config['SuccessTxt']['type'], self.config['SuccessTxt']['value']).text
                        self.assertIn(row['Expected Result'], text)
                        self.assertFalse(
                            self.is_element_present(self.config['ErrTxt']['type'], self.config['ErrTxt']['value'])
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
                    # Get full traceback as a string
                    tb_str = ''.join(traceback.format_exception(type(e), e, e.__traceback__))

                    print(f"  [ERROR] {tc_id} - Script Error:\n{tb_str}")
                    fail_count += 1
                    failed_cases.append(f"{tc_id}: Script Error:\n{tb_str}")

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
