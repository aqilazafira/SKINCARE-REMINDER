import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestPengingatPage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Inisialisasi WebDriver (pastikan chromedriver sudah terinstall dan ada di PATH)
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.base_url = "http://127.0.0.1:5000"  # Sesuaikan URL jika berbeda

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def login(self):
        """Metode untuk melakukan login dengan kredensial valid.
           Pastikan akun 'testuser' dengan password 'password' sudah terdaftar.
        """
        driver = self.driver
        driver.get(f"{self.base_url}/login")
        time.sleep(1)
        # Isi form login; sesuaikan nama field dan kredensial jika berbeda
        driver.find_element(By.NAME, "username").send_keys("testuser")  # Ganti dengan username valid
        driver.find_element(By.NAME, "password").send_keys("password")    # Ganti dengan password valid
        driver.find_element(By.CSS_SELECTOR, "button.login-btn").click()
        time.sleep(2)  # Tunggu hingga proses login selesai

    def setUp(self):
        # Lakukan login sebelum setiap pengujian
        self.login()

    def test_pengingat_page_loads(self):
        """Verifikasi bahwa halaman pengingat dapat dimuat dengan benar setelah login."""
        driver = self.driver
        driver.get(f"{self.base_url}/pengingat")
        time.sleep(2)
        
        # Cek keberadaan container utama
        container = driver.find_element(By.CSS_SELECTOR, ".container")
        self.assertIsNotNone(container, "Container utama tidak ditemukan pada halaman pengingat")
        
        # Cek keberadaan clock section
        clock_section = driver.find_element(By.CSS_SELECTOR, ".clock-section")
        self.assertIsNotNone(clock_section, "Clock section tidak ditemukan pada halaman pengingat")
        
        # Cek keberadaan schedule section
        schedule_section = driver.find_element(By.CSS_SELECTOR, ".schedule-section")
        self.assertIsNotNone(schedule_section, "Schedule section tidak ditemukan pada halaman pengingat")

    def test_edit_routine_overlay(self):
        """Verifikasi bahwa tombol Edit pada schedule card memunculkan overlay input form."""
        driver = self.driver
        driver.get(f"{self.base_url}/pengingat")
        time.sleep(2)
        
        # Temukan setidaknya satu tombol Edit pada schedule card
        edit_buttons = driver.find_elements(By.CSS_SELECTOR, ".schedule-card button.edit-btn")
        self.assertTrue(len(edit_buttons) > 0, "Tidak ditemukan tombol Edit pada schedule card")
        
        # Klik tombol Edit pertama
        edit_buttons[0].click()
        time.sleep(1)
        
        # Verifikasi bahwa overlay input form muncul (overlay memiliki id "inputFormOverlay")
        overlay = driver.find_element(By.ID, "inputFormOverlay")
        self.assertTrue(overlay.is_displayed(), "Overlay input form tidak muncul setelah klik tombol Edit")
        
        # Klik tombol Cancel di dalam overlay untuk menutupnya
        cancel_buttons = overlay.find_elements(By.XPATH, ".//button[contains(text(), 'Cancel')]")
        self.assertTrue(len(cancel_buttons) > 0, "Tombol Cancel tidak ditemukan di dalam overlay")
        cancel_buttons[0].click()
        time.sleep(1)
        
        # Pastikan overlay sudah tidak terlihat
        self.assertFalse(overlay.is_displayed(), "Overlay input form masih tampil setelah klik tombol Cancel")

if __name__ == "__main__":
    unittest.main()
