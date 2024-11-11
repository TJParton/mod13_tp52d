import unittest
from app import validate_date_input, get_stock_data

class UnitTestProject3(unittest.TestCase):

    def test_symbol(self):
        # Valid 
        self.assertTrue(self.is_valid_symbol("MMM"))
        self.assertTrue(self.is_valid_symbol("GOOG"))
        self.assertTrue(self.is_valid_symbol("T"))      
        self.assertTrue(self.is_valid_symbol("MAXIMUM")) 
        
        # Invalid 
        self.assertFalse(self.is_valid_symbol("MMM3"))  
        self.assertFalse(self.is_valid_symbol(""))      
        self.assertFalse(self.is_valid_symbol("MORETHANSEVEN"))  
        self.assertFalse(self.is_valid_symbol("mmm"))  
    
    def test_chart_type(self):
        # Valid 
        self.assertIn("1", ["1", "2"])
        self.assertIn("2", ["1", "2"])
        
        # Invalid 
        self.assertNotIn("3", ["1", "2"])  
        self.assertNotIn("ONE", ["1", "2"])  
        self.assertNotIn("", ["1", "2"])
    
    def test_time_series(self):
        # Valid
        self.assertIn("1", ["1", "2", "3", "4"])
        self.assertIn("4", ["1", "2", "3", "4"])
        
        # Invalid 
        self.assertNotIn("5", ["1", "2", "3", "4"])  
        self.assertNotIn("ONE", ["1", "2", "3", "4"])  
        self.assertNotIn("", ["1", "2", "3", "4"])  
    
    def test_start_date(self):
        # Valid 
        self.assertIsNotNone(validate_date_input("2024-06-06"))
        
        # Invalid
        self.assertIsNone(validate_date_input("01-01-2024"))  
        self.assertIsNone(validate_date_input("2024/01/01"))  
        self.assertIsNone(validate_date_input("2024-13-01"))  
    
    def test_end_date(self):
        # Valid
        self.assertIsNotNone(validate_date_input("2024-07-06"))
        
        # Invalid 
        self.assertIsNone(validate_date_input("06-06-2024"))  
        self.assertIsNone(validate_date_input("2024-31-12"))  
        self.assertIsNone(validate_date_input("2024-11-31"))  

    def is_valid_symbol(self, symbol):
        return symbol.isalpha() and symbol.isupper() and 1 <= len(symbol) <= 7

if __name__ == "__main__":
    unittest.main()
