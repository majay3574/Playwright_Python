"""
Data Helper utility module for managing test data
"""
import json
import os
import random
import string
import csv
from pathlib import Path

class DataHelper:
    """Data Helper class for test data management"""


    @staticmethod
    def read_leads_from_csv(file_path):
        """
        Read lead data from a CSV file and return a list of dictionaries.

        Args:
            file_path (str): Path to the CSV file relative to project root.

        Returns:
            list[dict]: List of dictionaries representing each row of lead data.
        """
        abs_path = Path(file_path).resolve()
        with open(abs_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]
        return data
    
    @staticmethod
    def load_test_data(file_path):
        """
        Load test data from JSON file
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            dict: Test data from JSON file
        """
        with open(file_path, 'r') as file:
            return json.load(file)
    
    @staticmethod
    def generate_random_string(length=8):
        """
        Generate a random string of specified length
        
        Args:
            length: Length of the random string (default: 8)
            
        Returns:
            str: Random string
        """
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    @staticmethod
    def generate_random_email():
        """
        Generate a random email address
        
        Returns:
            str: Random email address
        """
        username = DataHelper.generate_random_string(8)
        domain = DataHelper.generate_random_string(6).lower()
        return f"{username}@{domain}.com"
    
    @staticmethod
    def generate_random_phone():
        """
        Generate a random US phone number
        
        Returns:
            str: Random phone number
        """
        area_code = random.randint(100, 999)
        prefix = random.randint(100, 999)
        line_number = random.randint(1000, 9999)
        return f"{area_code}-{prefix}-{line_number}"
    
    @staticmethod
    def generate_test_lead_data():
        """
        Generate random test data for a lead
        
        Returns:
            dict: Random lead data
        """
        company_name = f"Company {DataHelper.generate_random_string(5)}"
        first_name = f"Test{DataHelper.generate_random_string(4)}"
        last_name = f"User{DataHelper.generate_random_string(4)}"
        
        return {
            "companyName": company_name,
            "firstName": first_name,
            "lastName": last_name,
            "source": "LEAD_EMPLOYEE",  # Example value
            "industry": "IND_SOFTWARE",  # Example value
            "phone": DataHelper.generate_random_phone(),
            "email": DataHelper.generate_random_email()
        }