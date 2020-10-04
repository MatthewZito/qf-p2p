from server.server import Server

if __name__ == "__main__":
    from gevent import monkey; monkey.patch_all()
    try:
        print("[+] Launching server")
        print("[+] Listening on port 31337")
        Server().run()

    except KeyboardInterrupt:
        print("\n[+] User terminated server")