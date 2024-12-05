from flask import Flask, request

app = Flask(__name__)


ALLOWED_METHODS = ["OPTIONS", "GET", "HEAD", "POST"]

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

        response = {'status': 'success', 'message': 'Data received successfully'}
        return response, 200

    return {'message': 'Method not allowed'}, 405

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
