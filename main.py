from fetch_sqs_data import fetch_sqs_data
from write_to_postgres import write_to_postgres

def main():
    while True:
        for data in fetch_sqs_data():
            write_to_postgres(data)

if __name__ == "__main__":
    main()