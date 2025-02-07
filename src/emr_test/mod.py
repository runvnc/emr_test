from lib.providers.commands import command
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
from typing import Dict, Any

def _get_driver(headless: bool = False) -> webdriver.Chrome:
    """Create and configure a Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    if headless:
        options.add_argument('--headless')
    return webdriver.Chrome(options=options)

def _type_with_delay(element, text: str, delay: float = 0.01) -> None:
    """Type text with a realistic delay."""
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

@command()
async def open_emr_record(record_data: Dict[str, Any], headless: bool = False, context=None) -> str:
    """Open EMR with record data.
    
    Args:
        record_data: Dictionary containing record data with keys:
            - name (optional): Patient name
            - dob (optional): Date of birth
            - mrn (optional): Medical record number
            - vitals (optional): Dict with bp, pulse, temp, weight
            - assessment (optional): Clinical assessment text
            - plan (optional): Treatment plan text
        headless: Whether to run browser in headless mode
    
    Example:
    { "open_emr_record": { 
        "record_data": {
            "name": "John Smith",
            "dob": "1980-05-15",
            "mrn": "MRN123456",
            "vitals": {
                "bp": "118/78",
                "pulse": "90",
                "temp": "100.2",
                "weight": "175"
            },
            "assessment": "Patient presents with...",
            "plan": "1. Rest\n2. Hydration..."
        },
        "headless": false
    }}
    """
    driver = _get_driver(headless)
    try:
        # Setup page
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, 'templates', 'index.html')
        driver.get(f'file://{html_path}')
        driver.maximize_window()
        wait = WebDriverWait(driver, 10)

        # Update fields based on provided data
        if record_data.get('name'):
            elem = wait.until(EC.presence_of_element_located((By.ID, "patient-name")))
            elem.clear()
            _type_with_delay(elem, record_data['name'])

        if record_data.get('dob'):
            elem = wait.until(EC.presence_of_element_located((By.ID, "dob")))
            elem.clear()
            elem.send_keys(record_data['dob'])

        if record_data.get('mrn'):
            elem = wait.until(EC.presence_of_element_located((By.ID, "mrn")))
            elem.clear()
            elem.send_keys(record_data['mrn'])

        vitals = record_data.get('vitals', {})
        for field in ['bp', 'pulse', 'temp', 'weight']:
            if vitals.get(field):
                elem = wait.until(EC.presence_of_element_located((By.ID, field)))
                elem.clear()
                elem.send_keys(str(vitals[field]))

        if record_data.get('assessment'):
            print("Entering clinical assessment...")
            elem = wait.until(EC.presence_of_element_located((By.ID, "assessment")))
            elem.clear()
            _type_with_delay(elem, record_data['assessment'])

        if record_data.get('plan'):
            print("Entering treatment plan...")
            elem = wait.until(EC.presence_of_element_located((By.ID, "plan")))
            elem.clear()
            _type_with_delay(elem, record_data['plan'])

        # Save changes
        save_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "save-btn")))
        save_button.click()
        time.sleep(0.5)

        # Don't close automatically - let user control timing
        input("Press Enter to close EMR...")
        return "EMR record opened and updated successfully"

    except Exception as e:
        return f"Error opening EMR record: {str(e)}"
    
    finally:
        driver.quit()
