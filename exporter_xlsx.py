import xlsxwriter
from helpers import sanitize

from io import BytesIO
from urllib.request import urlopen

def write_excel_row(sheet, row, row_vals, col_iter=0):
    for val in row_vals:
        sheet.write(row, col_iter, val)
        col_iter += 1

def export_albums_xlsx(sp):
    workbook = xlsxwriter.Workbook('saved_albums.xlsx')
    worksheet = workbook.add_worksheet()
    row_iter = 0
    
    # TODO: add release date
    fields = ["", "Title", "Artist(s)", "Spotify Link"]
    write_excel_row(worksheet, row_iter, fields)
    row_iter += 1

    # get all saved albums and write to CSV
    albums = sp.current_user_saved_albums()

    # TODO: for testing
    limit = 10

    while albums and row_iter < limit:
        for i, item in enumerate(albums['items']):
            row = []
            row.append(sanitize(item['album']['name']))
            # append artists as comma-separated list
            artists = sanitize(item['album']['artists'][0]['name'])
            for ar in item['album']['artists'][1:]:
                artists += ", " + sanitize(ar['name'])
            row.append(artists)
            row.append(item["album"]["external_urls"]["spotify"])

            # write the album cover image in first row
            # TODO: scaling doesn't work properly due to differing DPIs of Images pulled from Spotify
            img_idx = 0
            img_height = float(item['album']['images'][img_idx]['height'])
            scale = 64.0 / img_height

            img_url = item['album']['images'][img_idx]['url']
            worksheet.insert_image(row_iter, 0, img_url, {'image_data': BytesIO(urlopen(img_url).read()), 'x_scale': scale, 'y_scale': scale})
            write_excel_row(worksheet, row_iter, row, 1)
            
            row_iter += 1

        if albums['next']:
            albums = sp.next(albums)
        else:
            albums = None

    workbook.close()
