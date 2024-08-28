def handle_response(message) -> str:
    p_message = message.lower()
    if p_message == "hello":
        return "Hey there!"
    else:
        return "It is good to see you again, "
    