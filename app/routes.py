from flask import Blueprint, render_template, request, jsonify
from .quantum.teleport import quantum_teleportation
import numpy as np

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/teleport', methods=['POST'])
def teleport():
    data = request.json
    try:
        theta = float(data['theta'].replace(",", "."))
        phi = float(data['phi'].replace(",", "."))

        results = quantum_teleportation(theta, phi)

        formatted = []
        for m0, m1, alpha, beta in results:
            formatted.append({
                'm0': m0,
                'm1': m1,
                'alpha': str(np.round(alpha, 4)),
                'beta': str(np.round(beta, 4))
            })

        return jsonify({'results': formatted})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
