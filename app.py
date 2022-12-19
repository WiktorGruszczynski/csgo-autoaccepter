from autoaccept import *



if __name__ == "__main__":
    settings = get_settings()

    accepter = AutoAccept(settings)
    accepter.run()

