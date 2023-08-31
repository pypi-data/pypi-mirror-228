import requests
from bs4 import BeautifulSoup


def ekstrasi_data():
    try:
        content = requests.get('https://www.bmkg.go.id/')
    except Exception:
        return None

    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')

        # Ekstrak tanggal dan waktu
        result = soup.find('span', {'class': 'waktu'})
        tanggal, waktu = result.text.split(', ')

        # Ekstrak data tambahan
        result = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        result = result.findChildren('li')

        magnitudo = kedalaman = ls = bt = lokasi = dirasakan = None

        for i, res in enumerate(result):
            if i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                ls, bt = res.text.split(' - ')
            elif i == 4:
                lokasi = res.text
            elif i == 5:
                dirasakan = res.text

        return {
            'tanggal': tanggal,
            'waktu': waktu,
            'magnitudo': magnitudo,
            'kedalaman': kedalaman,
            'koordinat': {'ls': ls, 'bt': bt},
            'lokasi': lokasi,
            'dirasakan': dirasakan,
        }
    else:
        return None


def tampilkan_data(result):
    if result is None:
        print('Tidak bisa menemukan data gempa terkini')
        return

    print('Gempa Terakhir Berdasarkan BMKG')
    print(f"Tanggal: {result['tanggal']}")
    print(f"Waktu: {result['waktu']}")
    print(f"Magnitudo: {result['magnitudo']}")
    print(f"Kedalaman: {result['kedalaman']}")
    print(f"Koordinat: LS={result['koordinat']['ls']}, BT={result['koordinat']['bt']}")
    print(f"Lokasi: {result['lokasi']}")
    print(f"Dirasakan: {result['dirasakan']}")


