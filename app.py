from flask import Flask, render_template, request, jsonify, session
import techniques as techniques_pkg
from techniques.technique import Technique
import pkgutil
import importlib
import inspect
import secrets

app = Flask(__name__)
# Generate a secure secret key for session management
app.secret_key = secrets.token_hex(32)

def load_classes_from_package(package, base_class=None):
    """
    Load all technique classes from the package dynamically.
    
    Args:
        package: The package module to search.
        base_class: The class to filter by (optional).
        
    Returns:
        dict: A dictionary of class names to class objects.
    """
    classes = {}
    for finder, module_name, ispkg in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ != module.__name__:
                continue
            if base_class and not issubclass(obj, base_class):
                continue
            classes[name] = obj
    return classes


@app.route('/')
def index():
    """Render the main page of the web application."""
    return render_template('index.html')

@app.route('/api/techniques', methods=['GET'])
def get_techniques():
    """
    API Endpoint: Get list of available encryption techniques.
    
    Returns:
        JSON response containing a sorted list of technique names.
    """
    techniques = load_classes_from_package(techniques_pkg, Technique)
    technique_list = [name for name in techniques.keys() if name != 'Technique']
    return jsonify({'techniques': sorted(technique_list)})

@app.route('/api/technique_info/<technique_name>', methods=['GET'])
def get_technique_info(technique_name):
    """
    API Endpoint: Get information about a specific technique.
    
    Args:
        technique_name: Name of the technique class
        
    Returns:
        JSON response with technique description and parameters.
    """
    try:
        techniques = load_classes_from_package(techniques_pkg, Technique)
        if technique_name not in techniques:
            return jsonify({'error': f'Technique {technique_name} not found'}), 404
        
        technique_class = techniques[technique_name]
        # Create temporary instance to get metadata
        try:
            temp_instance = technique_class()
        except:
            # If instantiation fails, create with basic defaults
            temp_instance = technique_class(**{})
        
        return jsonify({
            'name': technique_name,
            'description': temp_instance.get_description(),
            'params': temp_instance.get_params()
        })
    except Exception as e:
        return jsonify({'error': f'Failed to get technique info: {str(e)}'}), 500


@app.route('/api/execute', methods=['POST'])
def execute_technique():
    """
    API Endpoint: Execute encryption/decryption/brute force operation.
    
    Expects JSON payload with:
    - technique: Name of the technique class
    - operation: 'E' (Encrypt), 'D' (Decrypt), or 'B' (Brute Force)
    - input_text: The text to process
    - params: Optional dictionary of technique-specific parameters
    
    Returns:
        JSON response with result or error message.
    """
    try:
        data = request.json
        technique_name = data.get('technique')
        operation = data.get('operation')  # 'E', 'D', or 'B'
        input_text = data.get('input_text')
        
        # Get technique-specific parameters
        params = data.get('params', {})
        
        if not all([technique_name, operation, input_text]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Load the technique class dynamically
        techniques = load_classes_from_package(techniques_pkg, Technique)
        if technique_name not in techniques:
            return jsonify({'error': f'Technique {technique_name} not found'}), 404
        
        technique_class = techniques[technique_name]
        
        # Instantiate technique with parameters (like main.py does with technique_class())
        # Pass params as keyword arguments for flexibility
        try:
            technique_instance = technique_class(**params) if params else technique_class()
        except TypeError:
            # If params are invalid, try without params
            technique_instance = technique_class()
        
        # Execute the operation (matching main.py's execute pattern)
        result = technique_instance.execute(option=operation, input_text=input_text)
        
        # Get extra information from the technique (empty dict by default)
        extra_info = technique_instance.get_extra_info()
        
        return jsonify({
            'success': True,
            'result': result,
            'extra_info': extra_info
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
