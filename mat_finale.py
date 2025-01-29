mat_finale = []
nb_de_choix = len(choix)
nbmax = len(liste_de_postes) - 3

# Create a dictionary of coefficients
dic = {liste_de_postes[m]: coefficients[m] for m in range(nbmax)}

for i in range(1, len(mat5)):  # Skip the header row
    x = mat5[i][11]
    y = 0
    nbdeparam = sum(mat5[i][j] for j in range(nbmax))
    nbdechoixpresent = sum(mat5[i][j] for j in range(nbmax) if mat5[0][j] in choix)
    
    if nbdechoixpresent == 0:  # Case 1
        y = mat5[i][9] + sum(dic[choice] for choice in choix)
        y -= sum(mat5[i][nn] * dic[mat5[0][nn]] for nn in range(nbmax))
    
    elif nbdechoixpresent == nb_de_choix:
        if nbdechoixpresent == nbdeparam:  # Case 2
            y = mat5[i][9]
        elif nbdechoixpresent < nbdeparam:  # Case 3
            y = mat5[i][9]
            y -= sum(mat5[i][n] * dic[mat5[0][n]] for n in range(nbmax) if mat5[0][n] not in choix)
    
    elif nbdechoixpresent < nb_de_choix:
        if nbdechoixpresent == nbdeparam:  # Case 4
            y = mat5[i][9]
            missing_choices = choix.copy()
            for n in range(nbmax):
                if mat5[i][n] == 1:
                    if mat5[0][n] in choix:
                        missing_choices.remove(mat5[0][n])
            y += sum(dic[choice] for choice in missing_choices)
        elif nbdechoixpresent < nbdeparam:  # Case 5
            y = mat5[i][9]
            missing_choices = choix.copy()
            for n in range(nbmax):
                if mat5[i][n] == 1:
                    if mat5[0][n] in choix:
                        missing_choices.remove(mat5[0][n])
                    else:
                        y -= mat5[i][n] * dic[mat5[0][n]]
            y += sum(dic[choice] for choice in missing_choices)
    
    y *= mat5[i][10]
    y /= mat5[i][11]
    z = y**2
    y = z**0.5
    mat_finale.append([x, y])