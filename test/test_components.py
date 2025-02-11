import unittest
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class TestComponents(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Inisialisasi Chrome WebDriver (pastikan chromedriver sudah terinstall dan ada di PATH)
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)  # waktu tunggu implisit 10 detik
        cls.base_url = "http://127.0.0.1:5000"  # sesuaikan dengan URL aplikasi kamu

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def register_and_login(self):
        """
        Helper function untuk mendaftarkan dan melakukan login dengan user baru.
        Digunakan untuk mengakses halaman-halaman yang membutuhkan autentikasi.
        """
        driver = self.driver
        rand = random.randint(1000, 9999)
        email = f"componentuser{rand}@example.com"
        username = f"componentuser{rand}"
        password = "Password123!"

        # Daftar user baru
        driver.get(f"{self.base_url}/register")
        time.sleep(1)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "confirm_password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button.register-btn").click()
        time.sleep(2)  # tunggu hingga redirect ke halaman login

        # Login dengan user yang baru didaftarkan
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button.login-btn").click()
        time.sleep(2)  # tunggu hingga login berhasil

    def test_profile_page(self):
        """Pengujian halaman profile (harus login terlebih dahulu)."""
        driver = self.driver
        # Lakukan registrasi dan login terlebih dahulu
        self.register_and_login()
        # Akses halaman profile
        driver.get(f"{self.base_url}/profile")
        time.sleep(2)
        # Verifikasi bahwa container profile muncul (misal, dengan class .profile-container)
        profile_container = driver.find_elements(By.CSS_SELECTOR, ".profile-container")
        self.assertTrue(len(profile_container) > 0, "Profile container tidak ditemukan pada halaman profile")
        # Opsional: periksa keberadaan tombol Edit
        edit_button = driver.find_elements(By.CSS_SELECTOR, "button.edit-btn")
        self.assertTrue(len(edit_button) > 0, "Tombol Edit tidak ditemukan pada halaman profile")

    def test_reset_password_page(self):
        """Pengujian halaman reset password dengan token dummy."""
        driver = self.driver
        # Gunakan token dummy, misalnya "dummytoken"
        token = "dummytoken"
        driver.get(f"{self.base_url}/reset_password/{token}")
        time.sleep(1)
        # Verifikasi bahwa form reset password memuat field untuk password dan konfirmasi password
        password_field = driver.find_elements(By.NAME, "password")
        confirm_field = driver.find_elements(By.NAME, "confirm_password")
        self.assertTrue(len(password_field) > 0, "Field password tidak ditemukan di halaman reset password")
        self.assertTrue(len(confirm_field) > 0, "Field confirm_password tidak ditemukan di halaman reset password")
        # Verifikasi bahwa tombol reset (dengan class .login-btn) ada
        reset_button = driver.find_elements(By.CSS_SELECTOR, "button.login-btn")
        self.assertTrue(len(reset_button) > 0, "Tombol reset password tidak ditemukan")

    def test_forgot_password_page(self):
        """Pengujian halaman forgot password dengan email yang tidak terdaftar."""
        driver = self.driver
        driver.get(f"{self.base_url}/forgot_password")
        time.sleep(1)
        # Isi field email dengan alamat email yang tidak terdaftar
        email = "nonexistent@example.com"
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.CSS_SELECTOR, "button.login-btn").click()
        time.sleep(2)
        # Verifikasi bahwa muncul flash message error "Email address not found."
        flash_messages = driver.find_elements(By.CSS_SELECTOR, ".flash-message.error")
        self.assertTrue(any("Email address not found." in msg.text for msg in flash_messages),
                        "Flash message 'Email address not found.' tidak muncul pada halaman forgot password")

if __name__ == "__main__":
    unittest.main()
