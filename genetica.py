import random

'''

GENES DEL JUGADOR

    redColor: 0 - 255
    greenColor: 0 - 255
    blueColor: 0 - 255
    speed: 1 - 10
    attack: 10 - 50
    evasion: 0.0 - 1.0
    accuracy: 0.0 - 1.0
    health_regeneration: 1 - 10
    velocity_recolection: 1 - 10
    heal_by_damage: 1 - 5
    points_increase: 1 - 5

'''

def personajeInicial():
    
    redColor = random.randint(0, 255)
    greenColor = random.randint(0, 255)
    blueColor = random.randint(0, 255)
    
    color = (redColor, greenColor, blueColor)

    player = {
        'redColor': redColor,
        'greenColor': greenColor,
        'blueColor': blueColor,
        'color': color,
        'speed': 1,
        'attack': 10,
        'evasion': 0.1,
        'accuracy': 0.8,
        'health_regeneration': 2,
        'velocity_recolection': 1,
        'heal_by_damage': 2,
        'points_increase': 2
    }
    
    return player
    

personajeInicial()
