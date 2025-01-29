import pytest
from model.function_model import FunctionModel

@pytest.mark.parametrize("fx_expr,gx_expr,expected_solutions", [
    ("x^2", "x", [0, 1]),              
    ("x^2 - 4", "0", [-2, 2]),         
    ("x^2", "4", [-2, 2]),             
    ("x^2 - 2*x + 1", "0", [1]),       
    ("x^3", "x^2", [0, 1]),            
    ("x^2 - x - 2", "0", [-1, 2]),     
    ("x^2 - 4*x + 4", "0", [2]),       
])
def test_polynomial_intersection(fx_expr,gx_expr,expected_solutions):
    fx = FunctionModel(fx_expr)
    gx = FunctionModel(gx_expr)
    
    real_solutions = fx.solve_with(gx)
    assert real_solutions == expected_solutions


@pytest.mark.parametrize("fx_expr,gx_expr,expected_solutions", [
    ("log(x)", "log(x) + 1", []),
    ("x^2", "2*x - 1", [1]),     
    ("sqrt(x)", "0", [0]),  
    ("log(x)", "-x + 1", [1]),
])
def test_log_intersection(fx_expr,gx_expr,expected_solutions):
    fx = FunctionModel(fx_expr)
    gx = FunctionModel(gx_expr)
    real_solutions = fx.solve_with(gx)
    assert real_solutions == expected_solutions 

@pytest.mark.parametrize("fx_expr,gx_expr",[
    ("x^2 + 1","0"),
    ("x^2", "x^2 + 1"),            
    ("log(x)","sqrt(x)")
])
def test_no_intersection(fx_expr,gx_expr):
    fx = FunctionModel(fx_expr)
    gx = FunctionModel(gx_expr)
    
    solutions = fx.solve_with(gx)
    assert solutions == []