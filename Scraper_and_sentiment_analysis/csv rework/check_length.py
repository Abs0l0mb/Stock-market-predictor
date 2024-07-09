import csv

# Remplacez 'votre_fichier.csv' par le chemin de votre fichier CSV
fichier_csv = 'apple_scraping.csv'

# Initialisation des variables pour suivre la cellule avec le plus de caractères
max_length = 0
max_cell = None
row_index = -1
col_index = -1

# Ouverture du fichier CSV
with open(fichier_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row_num, row in enumerate(reader):
        for col_num, cell in enumerate(row):
            cell_length = len(cell)
            if cell_length > max_length:
                max_length = cell_length
                max_cell = cell
                row_index = row_num
                col_index = col_num

print(f"La cellule contenant le plus de caractères est : '{max_cell}'")
print(f"Nombre de caractères : {max_length}")
print(f"Position : ligne {row_index + 1}, colonne {col_index + 1}")
