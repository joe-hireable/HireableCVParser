def test_simple_addition():
    """Test that basic Python arithmetic works."""
    assert 1 + 1 == 2

def test_string_operations():
    """Test that basic string operations work."""
    assert "hello" + " world" == "hello world"
    assert "hello".upper() == "HELLO"

def test_list_operations():
    """Test that basic list operations work."""
    my_list = [1, 2, 3]
    my_list.append(4)
    assert len(my_list) == 4
    assert my_list == [1, 2, 3, 4] 