import json

from werkzeug.wrappers import Request, Response

from orderDatabase import OrderDatabase


def calculate_cost(french_fries_count, big_mac_count):
    french_fries_price = 1.95
    big_mac_price = 5.17
    french_fries_cost = french_fries_count * french_fries_price
    big_mac_cost = big_mac_count * big_mac_price
    total_price = french_fries_cost + big_mac_cost
    return [big_mac_cost, french_fries_cost, total_price]


@Request.application
def post_data(request):
    if request.method == "POST":
        print("received")
        request_body = (
            request.get_json()
        )  # Assuming the client sends data in JSON format
        print("Received data from the client:")
        print(request_body)

        # Process the data as needed (e.g., save to database, perform calculations)
        data = request_body["data"]
        args = [data[0], data[1]]
        # Send a response back to the client (e.g., confirming data received)
        args.extend(calculate_cost(data[0], data[1]))

        print("total_price:", args[4])
        # print("username: ", end="")
        username = "root"
        # print("password: ", end="")
        password = "R@ndyli94041424"
        db = OrderDatabase("127.0.0.1", username, password)
        reponse_from_db = db.send_order(args)
        response_data = json.dumps(
            {"total price": args[4], "commit": reponse_from_db[0]}
        )

        return Response(response_data, content_type="application/json", status=200)
    else:
        return Response("Method Not Allowed", status=405)


if __name__ == "__main__":
    from werkzeug.serving import run_simple

    run_simple("192.168.56.1", 80, post_data)
