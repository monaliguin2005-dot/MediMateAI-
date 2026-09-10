import json
import os
from datetime import date
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from memory import (
    load_profile,
    save_profile,
    load_logs,
    add_checkin,
    calculate_score,
    update_profile_from_checkin
)

from prompts import (
    health_chat_prompt,
    pattern_prompt,
    small_change_prompt
)

from gemini import ask_gemini


HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8000))

FRONTEND_FOLDER = "frontend"


# -----------------------------------
# JSON RESPONSE
# -----------------------------------

def send_json(handler, data, status=200):

    response = json.dumps(data).encode("utf-8")

    handler.send_response(status)

    handler.send_header(
        "Content-Type",
        "application/json; charset=utf-8"
    )

    handler.send_header(
        "Content-Length",
        str(len(response))
    )

    handler.end_headers()

    handler.wfile.write(response)


# -----------------------------------
# READ REQUEST BODY
# -----------------------------------

def read_json(handler):

    length = int(
        handler.headers.get("Content-Length", 0)
    )

    body = handler.rfile.read(length)

    return json.loads(body.decode("utf-8"))


# -----------------------------------
# FRONTEND HANDLER
# -----------------------------------

class Handler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):

        super().__init__(
            *args,
            directory=FRONTEND_FOLDER,
            **kwargs
        )


    # --------------------------------
    # GET
    # --------------------------------

    def do_GET(self):

        path = urlparse(self.path).path


        # Homepage

        if path == "/":

            self.path = "/index.html"

            return super().do_GET()


        # Profile

        if path == "/api/profile":

            profile = load_profile()

            send_json(
                self,
                profile
            )

            return


        # Pattern detector

        if path == "/api/pattern":

            profile = load_profile()

            logs = load_logs()

            prompt = pattern_prompt(
                profile,
                logs
            )

            result = ask_gemini(prompt)

            send_json(
                self,
                result
            )

            return


        # One small change

        if path == "/api/small-change":

            profile = load_profile()

            logs = load_logs()

            prompt = small_change_prompt(
                profile,
                logs
            )

            result = ask_gemini(prompt)

            send_json(
                self,
                result
            )

            return


        # Unknown API route

        if path.startswith("/api/"):

            send_json(
                self,
                {
                    "status": "error",
                    "message": "API route not found"
                },
                404
            )

            return


        return super().do_GET()


    # --------------------------------
    # POST
    # --------------------------------

    def do_POST(self):

        path = urlparse(self.path).path


        # -----------------------------
        # CHAT
        # -----------------------------

        if path == "/api/chat":

            try:

                data = read_json(self)

                message = data.get(
                    "message",
                    ""
                ).strip()


                if not message:

                    send_json(
                        self,
                        {
                            "status": "error",
                            "message": "Please enter a message."
                        },
                        400
                    )

                    return


                profile = load_profile()


                prompt = health_chat_prompt(
                    profile,
                    message
                )


                result = ask_gemini(prompt)


                send_json(
                    self,
                    result
                )


            except Exception as e:

                send_json(
                    self,
                    {
                        "status": "error",
                        "message": str(e)
                    },
                    500
                )

            return


        # -----------------------------
        # DAILY CHECK-IN
        # -----------------------------

        if path == "/api/checkin":

            try:

                data = read_json(self)

                today = str(date.today())


                score = calculate_score(
                    data
                )


                add_checkin(
                    today,
                    data
                )


                profile = update_profile_from_checkin(
                    data
                )


                send_json(
                    self,
                    {
                        "status": "success",
                        "date": today,
                        "score": score,
                        "profile": profile
                    }
                )


            except Exception as e:

                send_json(
                    self,
                    {
                        "status": "error",
                        "message": str(e)
                    },
                    500
                )

            return


        # Unknown POST route

        send_json(
            self,
            {
                "status": "error",
                "message": "API route not found"
            },
            404
        )


# -----------------------------------
# START SERVER
# -----------------------------------

def main():

    print()
    print("==========================================")
    print("          🌿 MEDIMATE AI")
    print("==========================================")
    print()
    print("Frontend: http://127.0.0.1:8000")
    print()
    print("Press CTRL+C to stop the server.")
    print()


    server = ThreadingHTTPServer(
        (HOST, PORT),
        Handler
    )


    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print("\nMediMateAI stopped.")

        server.server_close()


if __name__ == "__main__":
    main()