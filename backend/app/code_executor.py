import subprocess
import sys
import os
import tempfile
import time
import json
import re
from typing import Dict, List, Tuple, Optional

class CodeExecutor:
    """Secure Python code executor with sandboxing"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
    
    def execute_code(self, code: str, test_inputs: List[str], expected_outputs: List[str]) -> Dict:
        """
        Execute Python code with test cases
        
        Returns:
            {
                "status": "correct" | "incorrect" | "error" | "timeout",
                "results": List of test case results,
                "error_message": str or None,
                "execution_time": float
            }
        """
        start_time = time.time()
        
        # Create temporary file for code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            results = []
            all_correct = True
            
            for i, (test_input, expected_output) in enumerate(zip(test_inputs, expected_outputs)):
                try:
                    # Prepare input
                    input_data = test_input.strip()
                    
                    # Execute code with timeout
                    process = subprocess.Popen(
                        [sys.executable, temp_file],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    # Use communicate with timeout
                    try:
                        stdout, stderr = process.communicate(input=input_data, timeout=self.timeout)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                        raise subprocess.TimeoutExpired(process.args, self.timeout)
                    
                    if process.returncode != 0:
                        all_correct = False
                        results.append({
                            "test_case": i + 1,
                            "status": "error",
                            "output": stdout.strip(),
                            "error": stderr.strip(),
                            "expected": expected_output.strip()
                        })
                        continue
                    
                    # Compare output with flexible matching
                    actual_output = stdout.strip()
                    expected = expected_output.strip()
                    
                    # Try exact match first
                    if actual_output == expected:
                        results.append({
                            "test_case": i + 1,
                            "status": "correct",
                            "output": actual_output,
                            "expected": expected
                        })
                    else:
                        # Try flexible matching - extract the actual answer
                        is_correct = _flexible_match(actual_output, expected)
                        
                        if is_correct:
                            results.append({
                                "test_case": i + 1,
                                "status": "correct",
                                "output": actual_output,
                                "expected": expected
                            })
                        else:
                            all_correct = False
                            results.append({
                                "test_case": i + 1,
                                "status": "incorrect",
                                "output": actual_output,
                                "expected": expected
                            })
                
                except subprocess.TimeoutExpired:
                    try:
                        process.kill()
                        process.wait()
                    except:
                        pass
                    all_correct = False
                    results.append({
                        "test_case": i + 1,
                        "status": "timeout",
                        "output": None,
                        "error": f"Execution exceeded {self.timeout} seconds",
                        "expected": expected_output.strip()
                    })
                
                except Exception as e:
                    all_correct = False
                    results.append({
                        "test_case": i + 1,
                        "status": "error",
                        "output": None,
                        "error": str(e),
                        "expected": expected_output.strip()
                    })
            
            execution_time = time.time() - start_time
            
            # Determine overall status
            if all_correct:
                status = "correct"
                error_message = None
            else:
                # Check if any test case timed out
                if any(r.get("status") == "timeout" for r in results):
                    status = "timeout"
                elif any(r.get("status") == "error" for r in results):
                    status = "error"
                else:
                    status = "incorrect"
                
                error_message = "\n".join([
                    f"Test {r['test_case']}: {r.get('error', 'Incorrect output')}"
                    for r in results if r.get("status") != "correct"
                ])
            
            return {
                "status": status,
                "results": results,
                "error_message": error_message,
                "execution_time": execution_time
            }
        
        except Exception as e:
            return {
                "status": "error",
                "results": [],
                "error_message": str(e),
                "execution_time": time.time() - start_time
            }
        
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file)
            except:
                pass
    
    def validate_syntax(self, code: str) -> Tuple[bool, Optional[str]]:
        """Check if Python code has valid syntax"""
        try:
            compile(code, '<string>', 'exec')
            return True, None
        except SyntaxError as e:
            return False, str(e)

def _flexible_match(actual: str, expected: str) -> bool:
    """
    Flexible output matching - accepts answers in any format as long as they're correct.
    Tries to extract the actual answer value from the output.
    """
    # First, try exact match (case-insensitive, whitespace normalized)
    if actual.lower().strip() == expected.lower().strip():
        return True
    
    # Try to extract numbers from both
    # Extract all numbers (integers and floats) from actual output
    actual_numbers = re.findall(r'-?\d+\.?\d*', actual)
    expected_numbers = re.findall(r'-?\d+\.?\d*', expected)
    
    if actual_numbers and expected_numbers:
        # Compare the last number in actual with expected (most common case)
        try:
            actual_val = float(actual_numbers[-1])
            expected_val = float(expected_numbers[0])
            if abs(actual_val - expected_val) < 0.0001:  # Handle floating point precision
                return True
        except ValueError:
            pass
    
    # Try to extract the expected value from actual output
    # For cases like "Sum = 8" vs "8", or "The answer is 8" vs "8"
    if expected_numbers:
        try:
            expected_val = expected_numbers[0]
            # Check if the expected value appears in the actual output
            if expected_val in actual or expected in actual:
                return True
        except:
            pass
    
    # For string outputs, try case-insensitive substring matching
    # Remove common prefixes/suffixes and compare
    actual_clean = re.sub(r'^(sum|result|answer|output|the|is|:|=|\s)+', '', actual.lower(), flags=re.IGNORECASE)
    actual_clean = re.sub(r'[^\w\s]', '', actual_clean).strip()
    expected_clean = re.sub(r'[^\w\s]', '', expected.lower()).strip()
    
    if actual_clean == expected_clean:
        return True
    
    # For dictionary/string outputs, try to normalize and compare
    # Remove extra whitespace and compare
    actual_normalized = ' '.join(actual.split())
    expected_normalized = ' '.join(expected.split())
    if actual_normalized == expected_normalized:
        return True
    
    return False
