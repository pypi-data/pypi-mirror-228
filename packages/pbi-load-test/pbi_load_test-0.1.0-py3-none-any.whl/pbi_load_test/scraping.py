from pathlib import Path

from selenium import webdriver

filename = "RealisticLoadTest.html"
filepath = Path(__file__).parent / "static" / filename
fileurl = f"file://{filepath}"

driver = webdriver.Chrome()
