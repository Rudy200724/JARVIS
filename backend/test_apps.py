from tools.applications import open_application, refresh_applications


def main() -> None:
    print(refresh_applications())

    while True:
        query = input("Application to open (or 'quit'): ").strip()

        if query.lower() == "quit":
            break

        print(open_application(query))


if __name__ == "__main__":
    main()
