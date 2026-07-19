import os

fichiers = [
    'frontend/pages/dashboard.py',
    'frontend/pages/reservations.py',
    'frontend/pages/concessions.py',
    'frontend/pages/finance.py',
    'frontend/pages/utilisateurs.py',
]

for f in fichiers:
    try:
        content = open(f, encoding='utf-8').read()
        content = content.replace('ft.border.all(', 'ft.Border.all(')
        content = content.replace('ft.border.left(', 'ft.Border.left(')
        open(f, 'w', encoding='utf-8').write(content)
        print('OK:', f)
    except Exception as e:
        print('ERREUR:', f, e)