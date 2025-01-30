import pytest
from controllers.main_controller import MainController
from views.main_view import MainView
from PySide2.QtCore import Qt

@pytest.fixture
def controller(qtbot):
    view = MainView()
    qtbot.addWidget(view)
    return MainController(view)

@pytest.mark.parametrize("expression,is_valid", [
    #! Valid expressions
    ("2*x + 1", True),
    ("x*2", True),
    ("log(x)", True),
    ("sqrt(x)", True),
    ("log(x^2) + 2*x", True),
    ("sqrt(x + 2*x + 3)", True),
    ("log(sqrt(x))", True),
    ("log(x^2 + 2*x + 1)", True),
    ("sqrt(x + log(x))", True),
    ("log(sqrt(x^2 + 1))", True),
    
    #! Invalid expressions - implicit multiplication
    ("2x + 1", False),
    ("x2", False),
    
    #! Invalid expressions - wrong variables
    ("y + x", False),
    ("2*x + y + z", False),
    
    #! Invalid expressions - wrong functions
    ("sin(x)", False),
    ("cos(x) + tan(x)", False),
    
    #! Invalid expressions - unbalanced parentheses
    ("log(x", False),
    ("(2*x + 1", False),
])
def test_expression_validation(controller, expression, is_valid):
    result, _ = controller.validate_expression(expression)
    assert result == is_valid