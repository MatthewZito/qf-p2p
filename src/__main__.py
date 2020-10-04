from server.server import Server

if __name__ == "__main__":
    from gevent import monkey; monkey.patch_all()
    try:
        print("[+] Launching server...")
        Server().run()

    except KeyboardInterrupt:
        print("\n[+] User terminated server")