
# def add_two_numbers(a, b):
#     return a + b

# def test_adds_two_numbers():
#     # Assemble
#     a = 7
#     b = 12
#     expected = 19
#     # Act
#     result = add_two_numbers(a, b)
#     # Assert
#     assert result == expected

# test_adds_two_numbers()

def add_two_numbers(a, b):
    return a + b

def test_add_two_numbers():
    expected = 5
    actual = add_two_numbers(4, 1)
    assert expected == actual