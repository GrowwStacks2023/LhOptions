from flask import Flask, request
import requests

app = Flask(__name__)

ALLOWED_METHODS = ["OPTIONS", "GET", "HEAD", "POST"]

WEBHOOK_URL = "https://hook.eu1.make.com/lc74y3fjlqcoaoocdfhr7x5r3os81zd6"  # Target URL

@app.route('/lufthansacargo/trackingCallback', methods=['OPTIONS', 'GET', 'HEAD', 'POST'])
def webhook():
    # Handle the OPTIONS method to provide the ALLOW header
    if request.method == 'OPTIONS':
        response = app.response_class(
            status=200,
            headers={
                'Allow': ', '.join(ALLOWED_METHODS),  # Specifies allowed HTTP methods
            }
        )
        return response

    if request.method == 'POST':
        data = request.get_json()
        print(f"Received data: {data}")

        # Send the data to the target webhook URL
        try:
            forward_response = requests.post(WEBHOOK_URL, json=data)
            forward_response.raise_for_status()  # Will raise an exception for 4xx/5xx responses
            print("Data forwarded successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error forwarding data: {e}")
            return {'status': 'error', 'message': 'Failed to forward data'}, 500

        # Respond back to the sender
        response = {'status': 'success', 'message': 'Data received and forwarded successfully'}
        return response, 200

    return {'message': 'Method not allowed'}, 405

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
