
# def get_path(special_cells, player):
#     x_player, y_player = player.x, player.y
#     path = []
    
#     for punto in special_cells:
#         x_punto, y_punto = punto['position']
#         dx = x_punto - x_player
#         dy = y_punto - y_player
        
#         # Determinar la dirección más cercana
#         if abs(dx) > abs(dy):
#             # Mover en el eje x
#             if dx > 0:
#                 path.append(3)  # Derecha
#             else:
#                 path.append(2)  # Izquierda
#         else:
#             # Mover en el eje y
#             if dy > 0:
#                 path.append(1)  # Abajo
#             else:
#                 path.append(0)  # Arriba
    
#     return path

def get_path(special_cells, player):
    x_player, y_player = player.x, player.y
    nearest_cell = None
    min_distance = float('inf')
    
    # Buscar el punto más cercano dentro de la lista de celdas especiales
    for cell in special_cells:
        x_cell, y_cell = cell['position']
        distance = abs(x_cell - x_player) + abs(y_cell - y_player)
        if distance < min_distance:
            min_distance = distance
            nearest_cell = cell
    
    if nearest_cell is None:
        return []  # No hay celdas especiales disponibles
    
    # Generar el camino hacia el punto más cercano
    x_nearest, y_nearest = nearest_cell['position']
    path = []
    # dx = x_nearest - x_player
    # dy = y_nearest - y_player
    
    while (x_nearest != x_player) and (y_nearest != y_player):  # Usamos 'or' en lugar de 'and'
        # Recalcular las diferencias de coordenadas
        dx = x_nearest - player.x
        dy = y_nearest - player.y
        
        # Añadir la dirección tomada al camino
        if abs(dx) > abs(dy):
            # Mover en el eje x
            if dx > 0:
                path.append(3)  # Derecha
            else:
                path.append(2)  # Izquierda
        else:
            # Mover en el eje y
            if dy > 0:
                path.append(1)  # Abajo
            else:
                path.append(0)  # Arriba

    
    return path
