from flask import Flask, request
import requests
import logging

app = Flask(__name__)

ALLOWED_METHODS = ["OPTIONS", "GET", "HEAD", "POST"]

WEBHOOK_URL = "https://hook.eu1.make.com/lc74y3fjlqcoaoocdfhr7x5r3os81zd6"  # Target URL

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/lufthansacargo/trackingCallback', methods=['OPTIONS', 'GET', 'HEAD', 'POST'])
def webhook():
    print(f"Received {request.method} request at /lufthansacargo/trackingCallback")

    # Handle the OPTIONS method to provide the ALLOW header
    if request.method == 'OPTIONS':
        response = app.response_class(
            status=200,
            headers={
                'Allow': ', '.join(ALLOWED_METHODS),  # Specifies allowed HTTP methods
            }
        )
        print(f"OPTIONS response headers: {response.headers}")
        return response

    if request.method == 'POST':
        # Handle POST request (get JSON body)
        data = request.get_json()
        print(f"Received data (POST): {data}")

    elif request.method == 'GET':
        # Handle GET request (get query parameters)
        data = request.args.to_dict()
        print(f"Received data (GET): {data}")

    else:
        print(f"Method {request.method} not allowed")
        return {'message': 'Method not allowed'}, 405

    # Send the data to the target webhook URL
    try:
        print(f"Forwarding data to {WEBHOOK_URL}")
        forward_response = requests.post(WEBHOOK_URL, json=data)
        forward_response.raise_for_status()  # Will raise an exception for 4xx/5xx responses
        print(f"Forward response status: {forward_response.status_code}")
        print(f"Forward response data: {forward_response.text}")
        print("Data forwarded successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Error forwarding data: {e}")
        return {'status': 'error', 'message': 'Failed to forward data'}, 500

    # Respond back to the sender
    response = {'status': 'success', 'message': 'Data received and forwarded successfully'}
    print(f"Response to sender: {response}")
    return response, 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
