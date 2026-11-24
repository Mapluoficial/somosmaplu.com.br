# somosmaplu.com.br

Portal de economia da MAPLU. Site estático (GitHub Pages).

- `_dados/AAAA-MM-DD.json`: matérias de cada dia (fonte de tudo)
- `_tools/build.py`: gera `index.html`, `arquivo.html`, páginas das matérias, `sitemap.xml` e `feed.xml`
- `img/`: imagens 1200x675 (nome-AAAAMMDD.jpg)

Atualização diária: adicionar o JSON do dia + imagens, rodar `python3 _tools/build.py`, commit e push.
