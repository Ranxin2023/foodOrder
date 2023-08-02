import json
from typing import Any

from werkzeug.wrappers import Request, Response

from orderDatabase import OrderDatabase


class App:
    def __init__(self) -> None:
        self.db_username = "root"
        self.db_password = "R@ndyli94041424"
        self.db = OrderDatabase("127.0.0.1", self.db_username, self.db_password)

    def calculate_cost(self, french_fries_count, big_mac_count):
        french_fries_price = 1.95
        big_mac_price = 5.17
        french_fries_cost = french_fries_count * french_fries_price
        big_mac_cost = big_mac_count * big_mac_price
        total_price = french_fries_cost + big_mac_cost
        return [big_mac_cost, french_fries_cost, total_price]

    def handle_request(self, request):
        if request.method == "POST":
            # print("received")
            request_body = request.get_json()
            print("Received data from the client:")
            print(request_body)
            # handle each request
            if request_body["method"] == "ordering":
                # Process the data as needed (e.g., save to database, perform calculations)
                data = request_body["args"]
                args = [data[0], data[1]]
                # Send a response back to the client (e.g., confirming data received)
                args.extend(self.calculate_cost(data[0], data[1]))

                # print("total_price:", args[4])

                reponse_from_db = self.db.send_order(args)
                response_data = json.dumps(
                    {"total price": args[4], "commit": reponse_from_db[0]}
                )
                return Response(
                    response_data, content_type="application/json", status=200
                )
            if request_body["method"] == "view order":
                data = request_body["args"]
                args = [request_body["args"][0]]
                response_from_db = self.db.get_order(args)
                response_data = json.dumps(
                    {
                        "commit": response_from_db[0],
                        "response data": response_from_db[1],
                    }
                )
                print("response data")
                print(response_from_db[1])
                return Response(
                    response_data, content_type="application/json", status=200
                )
        else:
            return Response("Method Not Allowed", status=405)

    def wsgi_app(self, environ, start_response):
        """WSGI application that processes requests and returns responses."""
        request = Request(environ)
        response = self.handle_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        """The WSGI server calls this method as the WSGI application."""
        return self.wsgi_app(environ, start_response)


if __name__ == "__main__":
    from werkzeug.serving import run_simple

    run_simple("192.168.56.1", 80, App())
