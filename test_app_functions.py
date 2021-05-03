
from unittest.mock import Mock, patch
from miniprojectfinal import add_product_name
from miniprojectfinal import add_product_price
from miniprojectfinal import id_update_product_func
from miniprojectfinal import showing_current_product_name
from miniprojectfinal import add_customer_address

def test_add_product_name():

    def mock_input_1():
        return "carrot"

    expected_1 = "carrot"
    actual_1 = add_product_name(mock_input_1)
    assert actual_1 == expected_1

test_add_product_name()

def test_add_product_price():
    
    def mock_input_2():
            return "1.3"

    expected_2 = "1.3"
    actual_2 = add_product_name(mock_input_2)
    assert actual_2 == expected_2

test_add_product_price()

@patch("builtins.input")
@patch("builtins.print")
def test_add_customer_address(mock_print, mock_input):
    mock_input.return_value = "34 poplar road"
    
    add_customer_address()

