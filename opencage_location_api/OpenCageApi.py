from opencage.geocoder import OpenCageGeocode

key = '354d26f53bcc48bea6f544be32550d3a'
geocoder = OpenCageGeocode(key)


def get_approx_coordinate(address):
    addr_part = address.split()
    while len(addr_part) > 0:
        query = ' '.join(addr_part)
        results = geocoder.geocode(query)

        if results:
            return results[0]['geometry']['lat'], results[0]['geometry']['lng']
        addr_part.pop(len(addr_part) - 1)
    return "", ""
