from src.quake import ekstrasi_data, tampilkan_data

if __name__ == '__main__':
    print('Data Gempa')
    result = ekstrasi_data()
    tampilkan_data(result)
