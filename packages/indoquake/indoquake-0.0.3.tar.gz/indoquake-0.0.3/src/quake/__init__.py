import requests
from bs4 import BeautifulSoup


def ekstrasi_data():
    """

    Tanggal: 15 Agustus 2023, 16:29:17 WIB
    Magnitudo: 2.6 skala richter
    Kedalaman: 6 km
    Lokasi: ls=6.82 LS - ls=107.13 BT
    Pusat Gempa : Pusat gempa berada di darat 1 km barat laut Kab. Cianjur
    Dirasakan : Dirasakan (Skala MMI): II Cugenang, II Kota Cianjur, II Karangtengah, II Warungkondang
    :return:
    """

    try:
        content = requests.get('https://www.bmkg.go.id/')
    except Exception:
        return None
    if content.status_code == 200:
        soup = BeautifulSoup(content.text, 'html.parser')

        hasilt = soup.find('span', {'class': 'waktu'})
        hasilt = hasilt.text.split(', ')
        tanggal = hasilt[0]
        waktu = hasilt[1]

        hasilt = soup.find('div', {'class': 'col-md-6 col-xs-6 gempabumi-detail no-padding'})
        hasilt = hasilt.findChildren('li')
        i = 0
        magnitudo = None
        kedalaman = None
        ls = None
        bt = None
        lokasi = None
        dirasakan = None

        for res in hasilt:
            print(i, res)
            if i == 1:
                magnitudo = res.text
            elif i == 2:
                kedalaman = res.text
            elif i == 3:
                koordinat = res.text.split(' - ')
                ls = koordinat[0]
                bt = koordinat[1]
            elif i == 4:
                lokasi = res.text
            elif i == 5:
                dirasakan = res.text
            i = i + 1

        hasilt = dict()
        hasilt['tanggal'] = tanggal
        hasilt['waktu'] = waktu
        hasilt['magnitudo'] = magnitudo
        hasilt['kedalaman'] = kedalaman
        hasilt['koordinat'] = {'ls': ls, 'bt': bt}
        hasilt['lokasi'] = lokasi
        hasilt['dirasakan'] = dirasakan

        return hasilt
    else:
        return None


def tampilkan_data(hasil):
    if hasil is None:
        print('Tidak bisa Menemukan data gempa terkini')
        return
    print('Gempa Terakhir Berdasarkan BMKG')
    print(f"Tanggal: {hasil['tanggal']}")
    print(f"Waktu: {hasil['waktu']}")
    print(f"Magnitudo: {hasil['magnitudo']}")
    print(f"kedalaman: {hasil['kedalaman']}")
    print(f"koordinat: LS={hasil['koordinat']['ls']}, BT={hasil['koordinat']['bt']}")
    print(f"lokasi: {hasil['lokasi']}")
    print(f"dirasakan: {hasil['dirasakan']}")
