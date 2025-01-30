import pytest
from PySide2.QtCore import Qt
from views.main_view import MainView
from utils.ui_components import ComponentFactory, LoadingOverlay
from utils.toastr import Toast

@pytest.fixture
def view(qtbot):
    view = MainView()
    qtbot.addWidget(view)
    view.show()  
    qtbot.waitForWindowShown(view)  
    return view

def test_initial_state(view):
    assert view.windowTitle() == "MasterMicro Internship assessment (Two Functions Solver)"
    assert view.geometry().width() == 1000
    assert view.geometry().height() == 600
    
    assert view.input1.placeholderText() == "Enter f(x)"
    assert view.input2.placeholderText() == "Enter g(x)"
    assert view.input1.text() == ""
    assert view.input2.text() == ""
    
    
    assert view.solutions_label.text() == ""

def test_input_fields(view, qtbot):
    qtbot.keyClicks(view.input1, "x^2")
    assert view.input1.text() == "x^2"
    
    qtbot.keyClicks(view.input2, "2*x")
    assert view.input2.text() == "2*x"

def test_update_solutions(view):
    solutions = [1.0, 2.0]
    view.update_solutions(solutions)
    assert "x = 1.0" in view.solutions_label.text()
    assert "x = 2.0" in view.solutions_label.text()
    
    view.update_solutions([])
    assert view.solutions_label.text() == "No intersections found"

def test_loading_overlay(view, qtbot):
    overlay = view.loading_overlay
    overlay.show_loading()
    qtbot.wait(200)  
    assert overlay.isVisible()
    
    overlay.hide_loading()
    qtbot.wait(200)  
    assert not overlay.isVisible()

def test_button_styles(view):
    assert "background-color: #4CAF50" in view.solve_button.styleSheet()
    assert "background-color: #ff4444" in view.clear_button.styleSheet()