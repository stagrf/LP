import image_processing as ip
import graphic_interface as gi
import database_statistics as ds


licence_number = ip.get_licence_number(r'images\car1.JPG')
ds.proceseaza_numar(licence_number)


ds.cursor.close()
ds.conn.close()