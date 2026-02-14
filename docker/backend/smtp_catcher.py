import asyncore
from smtpd import DebuggingServer

def run():
    print("SMTP Catcher started on port 2526...")
    foo = DebuggingServer(('0.0.0.0', 2526), ('localhost', 25))
    try:
        asyncore.loop()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run()
