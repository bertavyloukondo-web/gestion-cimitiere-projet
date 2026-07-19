import os

fichiers = [
    'frontend/pages/dashboard.py',
    'frontend/pages/login.py',
    'frontend/pages/carte.py',
    'frontend/pages/reservations.py',
    'frontend/pages/nouvelle_reservation.py',
    'frontend/pages/concessions.py',
    'frontend/pages/finance.py',
    'frontend/pages/utilisateurs.py',
]

for f in fichiers:
    try:
        content = open(f, encoding='latin-1').read()
        open(f, 'w', encoding='utf-8').write(content)
        print('OK:', f)
    except Exception as e:
        print('ERREUR:', f, e)