import os
import re

CATEGORIES = {
    'AEA': 'Análises Espaciais e Ambientais',
    'MAN': 'Manejo de Florestas Plantadas',
    'NAT': 'Manejo de Florestas Nativas',
    'OPT': 'Otimização Florestal'
}

def get_title(html_path):
    """Extrai o conteúdo da tag <title> de um arquivo HTML ou usa o nome do arquivo."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
            if match:
                return match.group(1).strip()
    except Exception:
        pass
    
    # Fallback: nome do arquivo sem extensão, com capitalização correta
    filename = os.path.basename(html_path)
    title = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').title()
    return title

def generate():
    # Estrutura de dados para armazenar materiais por categoria
    materials = {cat: [] for cat in CATEGORIES}
    
    # Percorre cada diretório de categoria
    for cat_code in CATEGORIES:
        if not os.path.exists(cat_code):
            continue
            
        for file in os.listdir(cat_code):
            if file.endswith('.html'):
                full_path = os.path.join(cat_code, file)
                title = get_title(full_path)
                # O link deve ser relativo à raiz do repositório
                materials[cat_code].append({
                    'title': title,
                    'path': f"{cat_code}/{file}"
                })
    
    # Geração do HTML
    html_content = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recursos Educacionais - Curadoria</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <header>
        <h1>Curadoria de Recursos Educacionais</h1>
        <p>Acesse os materiais organizados por categoria abaixo.</p>
    </header>

    <main class="container">
        <section class="categories">
"""
    
    # Adiciona botões de categoria
    for code, name in CATEGORIES.items():
        html_content += f"""
            <a href="#{code}" class="category-btn">
                {code}
                <span>{name}</span>
            </a>
"""
            
    html_content += """
        </section>

        <section class="materials-section">
"""

    # Adiciona lista de materiais para cada categoria
    for code, name in CATEGORIES.items():
        if materials[code]:
            html_content += f"""
            <div id="{code}" class="category-header">
                <h2>{name} ({code})</h2>
            </div>
            <div class="materials-grid">
"""
            for mat in materials[code]:
                html_content += f"""
                <a href="{mat['path']}" class="material-card">
                    <h3>{mat['title']}</h3>
                    <p>Localizado em: {code}</p>
                </a>
"""
            html_content += "</div><br>"
        else:
            # Caso não haja materiais na categoria (opcional: ocultar ou mostrar aviso)
            pass

    html_content += """
        </section>
    </main>

    <footer>
        <p>&copy; 2026 - Repositório de Recursos Educacionais</p>
    </footer>
</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    print("index.html gerado com sucesso!")

if __name__ == "__main__":
    generate()
