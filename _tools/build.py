#!/usr/bin/env python3
"""Gera o site estático da MAPLU a partir de _dados/AAAA-MM-DD.json.
Uso: python3 _tools/build.py   (rodar na raiz do site)
Saída: index.html, arquivo.html, AAAA/MM/DD/<slug>.html, sitemap.xml, feed.xml"""
import json, os, glob, html, datetime

SITE = 'https://somosmaplu.com.br'
INSTA = 'https://www.instagram.com/somosmaplu/'
SISTEMA = 'https://sistema.somosmaplu.com.br'
MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
DIAS = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
e = html.escape

LOGO = '<svg viewBox="0 0 34 20" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" aria-hidden="true"><path d="M2 18 12 2M9 18 19 2M19 18V8a6 6 0 0 1 12 0v0a6 6 0 0 1-6 6h-6"/></svg>'


def data_ext(d):
    dt = datetime.date.fromisoformat(d)
    return f'{DIAS[dt.weekday()].capitalize()}, {dt.day} de {MESES[dt.month - 1]} de {dt.year}'


def data_curta(d):
    dt = datetime.date.fromisoformat(d)
    return f'{dt.day:02d}/{dt.month:02d}/{dt.year}'


def url_materia(d, slug):
    return f'/{d[:4]}/{d[5:7]}/{d[8:10]}/{slug}.html'


def head(titulo, desc, url, img=None):
    og = f'<meta property="og:image" content="{SITE}/img/{img}">' if img else ''
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(titulo)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{url}">
<meta property="og:title" content="{e(titulo)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="article"><meta property="og:url" content="{SITE}{url}">{og}
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="MAPLU" href="/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/estilo.css"></head><body>'''


def topo(d):
    return f'''<div class="barra"><div class="w barra-in"><span>{e(data_ext(d))}</span>
<div class="ticker" id="ticker" aria-live="polite"><span class="tk" data-k="USDBRL">Dólar <b>—</b></span><span class="tk" data-k="EURBRL">Euro <b>—</b></span><span class="tk" data-k="BTCBRL">Bitcoin <b>—</b></span></div></div></div>
<header class="cab"><div class="w cab-in"><a class="marca" href="/"><i>{LOGO}</i><span>MAPLU<small>Notícias e economia, sem enrolação</small></span></a>
<div class="acoes"><a class="btn-ghost" href="{INSTA}" target="_blank" rel="noopener">Instagram</a><a class="btn-insta" href="{SISTEMA}">Entrar no sistema</a></div></div>
<nav class="w nav"><a href="/">Hoje</a><a href="/#seu-bolso">Seu bolso</a><a href="/#mercado">Mercado</a><a href="/#impostos">Impostos</a><a href="/arquivo.html">Arquivo</a><a class="nav-sis" href="/sistema.html">Sistema de Gestão</a></nav></header>'''


def rodape():
    ano = datetime.date.today().year
    return f'''<footer class="rod"><div class="w"><div class="rod-in"><a class="marca" href="/"><i>{LOGO}</i><span>MAPLU</span></a>
<p>Economia e o seu bolso, com fonte em cada número e sem medo de dizer o óbvio: quem paga a conta é você.</p></div>
<p class="peq">Atualizado toda manhã. Textos próprios da MAPLU, com links para as fontes originais em cada matéria. Imagens ilustrativas de bancos de uso livre (Unsplash e Pexels). Cotações ao vivo: AwesomeAPI, com atraso, apenas informativas. Nada aqui é recomendação de investimento.</p>
<p class="peq">© {ano} MAPLU · <a href="{INSTA}" target="_blank" rel="noopener">@somosmaplu</a> · <a href="/sistema.html">Sistema de Gestão MAPLU</a> · <a href="{SISTEMA}">Entrar no sistema</a> · <a href="/feed.xml">RSS</a></p></div></footer>
<script src="/cotacoes.js" defer></script></body></html>'''


def card(d, m, cls='card'):
    u = url_materia(d, m['slug'])
    return f'''<article class="{cls}"><a href="{u}"><div class="ph"><img src="/img/{m['img']}" alt="" loading="lazy"></div>
<span class="ed">{e(m['editoria'])}</span><h3>{e(m['titulo'])}</h3><p>{e(m['linha_fina'])}</p></a></article>'''


def ancora(ed):
    return {'Seu bolso': 'seu-bolso', 'Mercado': 'mercado', 'Impostos': 'impostos'}.get(ed, '')


def pagina_inicial(dia, anteriores):
    d = dia['data']; ms = dia['materias']
    man = next((m for m in ms if m.get('destaque')), ms[0])
    resto = [m for m in ms if m is not man]
    n = 4 if len(resto) % 3 == 1 else 3
    lado, grade = resto[:n], resto[n:]
    u = url_materia(d, man['slug'])
    h = head('MAPLU | Economia e o seu bolso, todo dia', 'As notícias de economia que mexem no seu bolso, explicadas sem enrolação. Atualizado toda manhã.', '/', man['img'])
    h += topo(d) + '<main class="w">'
    h += f'''<section class="abre"><article class="manchete"><a href="{u}"><div class="ph"><img src="/img/{man['img']}" alt=""></div>
<span class="ed">{e(man['editoria'])}</span><h1>{e(man['titulo'])}</h1><p>{e(man['linha_fina'])}</p></a></article>
<aside class="lado">{''.join(card(d, m, 'mini') for m in lado)}</aside></section>'''
    h += '<section class="resumo"><h2>O dia em 1 minuto</h2><ol>' + ''.join(f'<li>{e(x)}</li>' for x in dia.get('resumo', [])) + '</ol></section>'
    if dia.get('indicadores'):
        h += '<section class="ind">' + ''.join(f'<div><span>{e(i["nome"])}</span><b>{e(i["valor"])}</b><small>{e(i["obs"])}</small></div>' for i in dia['indicadores']) + '</section>'
    h += '<section class="grade">'
    for m in grade:
        a = ancora(m['editoria'])
        h += card(d, m).replace('<article class="card">', f'<article class="card"{f" id={chr(34)}{a}{chr(34)}" if a else ""}>', 1)
    h += '</section>'
    h += f'''<section class="cta"><div><b>Prefere em vídeo?</b><p>Todo dia um Reels com a notícia que mais pesa no seu bolso.</p></div><a class="btn-insta grande" href="{INSTA}" target="_blank" rel="noopener">@somosmaplu</a></section>'''
    h += f'''<section class="sis-box"><div><span class="ed">Para a sua empresa</span><h2>Sistema de Gestão MAPLU</h2><p>Estoque, financeiro, vendas, RH e mais de 30 módulos num lugar só. Teste grátis por 30 dias.</p></div><div class="sis-btns"><a class="btn-insta grande2" href="/sistema.html">Conhecer o sistema</a><a class="btn-ghost" href="{SISTEMA}">Já sou cliente</a></div></section>'''
    if anteriores:
        h += '<section class="ant"><h2>Edições anteriores</h2><ul>'
        for dd in anteriores[:6]:
            m0 = next((m for m in dd['materias'] if m.get('destaque')), dd['materias'][0])
            h += f'<li><a href="{url_materia(dd["data"], m0["slug"])}"><time>{data_curta(dd["data"])}</time>{e(m0["titulo"])}</a></li>'
        h += '</ul><a class="mais" href="/arquivo.html">Ver arquivo completo</a></section>'
    h += '</main>' + rodape()
    return h


def pagina_materia(dia, m):
    d = dia['data']; u = url_materia(d, m['slug'])
    h = head(f'{m["titulo"]} | MAPLU', m['linha_fina'], u, m['img']) + topo(d)
    h += f'''<main class="w"><article class="mat"><span class="ed">{e(m['editoria'])}</span><h1>{e(m['titulo'])}</h1><p class="lf">{e(m['linha_fina'])}</p>
<p class="por">Por Redação MAPLU · <time datetime="{d}">{data_curta(d)}</time></p>
<figure><img src="/img/{m['img']}" alt=""><figcaption>{e(m['credito'])}</figcaption></figure><div class="corpo">'''
    h += ''.join(f'<p>{e(p)}</p>' for p in m['texto'])
    h += f'<div class="bolso"><b>E no seu bolso?</b><p>{e(m["bolso"])}</p></div>'
    h += '<div class="fontes"><b>Fontes</b><ul>' + ''.join(f'<li><a href="{e(f["url"])}" target="_blank" rel="noopener nofollow">{e(f["nome"])}</a></li>' for f in m['fontes']) + '</ul></div>'
    h += '</div></article>'
    outras = [x for x in dia['materias'] if x is not m][:3]
    h += '<section class="rel"><h2>Também hoje</h2><div class="grade">' + ''.join(card(d, x) for x in outras) + '</div></section></main>' + rodape()
    return h


def pagina_arquivo(dias):
    h = head('Arquivo | MAPLU', 'Todas as edições da MAPLU.', '/arquivo.html') + topo(dias[0]['data']) + '<main class="w"><section class="ant arq"><h1>Arquivo</h1>'
    for dd in dias:
        h += f'<h2>{e(data_ext(dd["data"]))}</h2><ul>' + ''.join(f'<li><a href="{url_materia(dd["data"], m["slug"])}"><span class="ed">{e(m["editoria"])}</span>{e(m["titulo"])}</a></li>' for m in dd['materias']) + '</ul>'
    return h + '</section></main>' + rodape()


MODULOS = [
 ("Financeiro", "Contas a pagar e receber, centro de custos, orçamento por departamento e recorrências."),
 ("Estoque e Almoxarifado", "Saldo em tempo real, estoque mínimo com alerta, validade e requisições com aprovação."),
 ("Comercial e CRM", "Funil de vendas em Kanban, propostas com validade, comissão por vendedor e onboarding."),
 ("PDV / Frente de loja", "Abre e fecha caixa, venda que já baixa o estoque e o resumo do dia."),
 ("Compras e Fornecedores", "Cadastro, pedidos e cotação que destaca o menor preço."),
 ("RH e Departamento Pessoal", "Funcionários, cargos e salários, benefícios, ASO, ponto, treinamentos e avaliação."),
 ("Marketing e Trade", "Campanhas, solicitações de supervisores, aprovação e integração com o almoxarifado."),
 ("Segurança do Trabalho", "Acidentes, EPIs, controle de PGR e PCMSO, inspeções e APR."),
 ("Logística e Frota", "Entregas, veículos, manutenção e abastecimento."),
 ("TI e Helpdesk", "Chamados internos, equipamentos, cofre de senhas criptografado e chamado do cliente."),
 ("Jurídico e Compliance", "Contratos com alerta de vencimento e controles de LGPD."),
 ("BI e Metas", "Painéis que cruzam os módulos e metas por departamento com barra de progresso."),
]


def pagina_sistema(d):
    h = head('Sistema de Gestão MAPLU | ERP simples para a sua empresa', 'Sistema de gestão MAPLU: financeiro, estoque, vendas, RH e mais de 30 módulos. Teste grátis por 30 dias.', '/sistema.html') + topo(d)
    h += f'''<main><section class="sis-hero"><div class="w"><span class="ed">Sistema de Gestão MAPLU</span><h1>Gestão simples.<br>Resultados reais.</h1>
<p>Um sistema na nuvem para organizar a empresa inteira: financeiro, estoque, vendas, RH e muito mais, com cada empresa vendo só os próprios dados.</p>
<div class="sis-btns"><a class="btn-insta grande2" href="{SISTEMA}">Começar teste grátis de 30 dias</a><a class="btn-ghost claro" href="{SISTEMA}">Já sou cliente: entrar</a></div></div></section>
<div class="w"><section class="sis-num"><div><b>30+</b><span>módulos e seções</span></div><div><b>30 dias</b><span>de teste grátis</span></div><div><b>4</b><span>módulos à sua escolha no teste</span></div><div><b>CSV</b><span>relatório em todo módulo</span></div></section>
<h2 class="sis-t">O que dá para fazer</h2><section class="sis-mods">'''
    h += ''.join(f'<div><b>{e(n)}</b><p>{e(t)}</p></div>' for n, t in MODULOS)
    h += f'''</section><section class="sis-seg"><h2>Segurança levada a sério</h2><p>Conexão criptografada, senhas protegidas por hash, isolamento total entre empresas e proteção contra ataques de força bruta e CSRF. Como todo sistema em evolução, seguimos aprimorando continuamente.</p></section>
<section class="cta"><div><b>Pronto para testar?</b><p>Escolha 4 módulos e use grátis por 30 dias.</p></div><a class="btn-insta grande" href="{SISTEMA}">Criar conta grátis</a></section></div></main>''' + rodape()
    return h


def main():
    dias = [json.load(open(f)) for f in sorted(glob.glob('_dados/*.json'), reverse=True)]
    hoje = dias[0]
    open('index.html', 'w').write(pagina_inicial(hoje, dias[1:]))
    urls = ['/', '/arquivo.html']
    for dd in dias:
        for m in dd['materias']:
            u = url_materia(dd['data'], m['slug']); os.makedirs('.' + os.path.dirname(u), exist_ok=True)
            open('.' + u, 'w').write(pagina_materia(dd, m)); urls.append(u)
    open('arquivo.html', 'w').write(pagina_arquivo(dias))
    open('sistema.html', 'w').write(pagina_sistema(hoje['data'])); urls.append('/sistema.html')
    open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{SITE}{u}</loc></url>' for u in urls) + '</urlset>')
    itens = ''
    for dd in dias[:5]:
        for m in dd['materias']:
            u = SITE + url_materia(dd['data'], m['slug'])
            pd = datetime.datetime.fromisoformat(dd['data'] + 'T07:00:00-03:00').strftime('%a, %d %b %Y %H:%M:%S %z')
            itens += f'<item><title>{e(m["titulo"])}</title><link>{u}</link><guid>{u}</guid><pubDate>{pd}</pubDate><description>{e(m["linha_fina"])}</description></item>'
    open('feed.xml', 'w').write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>MAPLU</title><link>{SITE}</link><description>Economia e o seu bolso</description><language>pt-BR</language>{itens}</channel></rss>')
    print('ok', len(urls), 'páginas')


if __name__ == '__main__':
    main()
