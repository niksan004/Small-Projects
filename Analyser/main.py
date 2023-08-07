import csv
from datetime import datetime


def fetch_data(file_name, start_date, end_date):
    data = []
    customers = {}

    with open(file_name, newline='', mode='r') as csv_file:
        reader = csv.reader(csv_file)
        for record in reader:
            if record[0] == 'DATE':
                continue

            record_date = datetime.strptime(record[0], '%Y-%m-%d %H:%M:%S')
            if start_date <= record_date <= end_date:
                service = record[3]

                if service[2] == 'M':
                    record.append('Mobile')
                    record.append(service[3:5])
                else:
                    record.append('Desktop')
                    record.append(service[2:4])

                if service[-3:] == 'USD':
                    record.append('USD')
                else:
                    record.append('EUR')

                data.append(record)

                if record[1] not in customers:
                    customers[record[1]] = []

                customers[record[1]].append(record[6])

    return data, customers


def analyse(data, customers):
    # 1)
    num_of_24h_mobile = 0
    num_of_24h_desktop = 0

    for row in data:
        if row[6] == '05':
            if row[5] == 'Mobile':
                num_of_24h_mobile += 1
            else:
                num_of_24h_desktop += 1

    print(f'24-hour subscriptions: {num_of_24h_mobile + num_of_24h_desktop}')
    print(f'    mobile: {num_of_24h_mobile}')
    print(f'    desktop: {num_of_24h_desktop}')
    print()

    # 2)
    print('One-time customers of 24-hour subscriptions:')
    list_cust = []
    for customer, services in customers.items():
        cnt = 0
        for el in services:
            if el == '05':
                cnt += 1

        if cnt == 1:
            list_cust.append(customer)

    print(f'Count: {len(list_cust)}')
    print(' '.join(list_cust))
    print()

    # 3)
    print('Multiple 24-hour subscriptions but no higher subscription:')
    list_cust = []
    for customer, services in customers.items():
        cnt = 0
        for el in services:
            if el == '05':
                cnt += 1

        services_to_check = ['01', '02', '03', '04']
        if cnt > 1 and not any(element in services[services.index('05') + 1:] for element in services_to_check):
            list_cust.append(customer)

    print(f'Count: {len(list_cust)}')
    print(' '.join(list_cust))
    print()

    # 4)
    print('24-hour subscription/s -> PREMIUM:')
    list_cust = []
    for customer, services in customers.items():
        cnt = 0
        for el in services:
            if el == '05':
                cnt += 1

        if cnt >= 1 and '01' in services[services.index('05') + 1:]:
            list_cust.append(customer)

    print(f'Count: {len(list_cust)}')
    print(' '.join(list_cust))
    print()

    # 5)
    print('24-hour subscription/s -> monthly SAT:')
    list_cust = []
    for customer, services in customers.items():
        cnt = 0
        for el in services:
            if el == '05':
                cnt += 1

        if cnt >= 1 and '04' in services[services.index('05') + 1:]:
            list_cust.append(customer)

    print(f'Count: {len(list_cust)}')
    print(' '.join(list_cust))
    print()

    # 6)
    print('24-hour subscription/s -> yearly SAT:')
    list_cust = []
    for customer, services in customers.items():
        cnt = 0
        for el in services:
            if el == '05':
                cnt += 1

        if cnt >= 1 and '03' in services[services.index('05') + 1:]:
            list_cust.append(customer)

    print(f'Count: {len(list_cust)}')
    print(' '.join(list_cust))
    print()

    # 7)
    print('2 or more yearly subscriptions:')
    list_cust = []
    for customer, services in customers.items():
        cnt = 0
        for el in services:
            if el == '03':
                cnt += 1

        if cnt >= 2:
            list_cust.append(customer)

    print(f'Count: {len(list_cust)}')
    # print(' '.join(list_cust))
    print()


if __name__ == '__main__':
    file_name = 'avangate_ipn.csv'
    start_date = datetime.strptime('2018-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime('2023-08-07 07:17:31', '%Y-%m-%d %H:%M:%S')
    data, customers = fetch_data(file_name, start_date, end_date)

    analyse(data, customers)
