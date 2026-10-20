"""Páginas internas de Parisotto (servicios.html, el-estudio.html) con head/header/footer del index.
Uso: python _scripts/generar_paginas.py   (correr DESPUÉS de generar_extras.py: así heredan el link a privacidad)
Todo el contenido sale de su web actual (_contenido-web-actual.txt)."""
import re
from pathlib import Path

D = Path(__file__).resolve().parent.parent
idx = (D / "index.html").read_text(encoding="utf8")
head_tpl = idx[:idx.index("<title>")]
links_head = idx[idx.index('<link rel="preconnect"'):idx.index("</head>")]
links_head = re.sub(r'<script type="application/ld\+json">.*?</script>\s*', "", links_head, flags=re.S)
links_head = re.sub(r'<meta property="og:[^>]*>\n|<meta name="twitter:[^>]*>\n', "", links_head)
top = idx[idx.index("<!-- ============ HEADER ============ -->"):idx.index("<main>")]
f0 = idx.index("<!-- ============ FOOTER ============ -->")
foot = idx[f0:idx.index('<a class="wa-float', f0)]
tail = idx[idx.index('<a class="wa-float', f0):]
tail = re.sub(r'<div class="modal".*?</div>\n</div>\n\n', "", tail, flags=re.S)   # el modal solo hace falta en el index

def interna(s):
    s = re.sub(r'href="#(?!")', 'href="./index.html#', s)
    return s.replace('href="./index.html#inicio"', 'href="./index.html"')
top, foot = interna(top), interna(foot)

def page(name, title, desc, body):
    og = re.search(r'<meta property="og:image" content="([^"]+)"', idx)
    og = og.group(1) if og else "./og.png"
    meta = (f'<meta property="og:type" content="website">\n<meta property="og:locale" content="es_AR">\n'
            f'<meta property="og:title" content="{title}">\n<meta property="og:description" content="{desc}">\n'
            f'<meta property="og:image" content="{og}">\n<meta name="twitter:card" content="summary">\n')
    html = (head_tpl + f'<title>{title}</title>\n<meta name="description" content="{desc}">\n'
            '<meta name="theme-color" content="#0A0E26">\n<link rel="icon" type="image/png" href="./favicon.png">\n'
            '<link rel="apple-touch-icon" href="./favicon.png">\n' + meta + links_head + "</head>\n<body>\n\n"
            + top + "<main>\n" + body + "\n</main>\n\n" + foot + tail)
    (D / name).write_text(html, encoding="utf8", newline="\n")
    print("ok", name)

def cabecera(t1, t2, ruta, bajada, foto, extra=""):
    return f'''<!-- ============ CABECERA ============ -->
<section class="page-hero">
  <div class="page-hero-bg" style="background-image:linear-gradient(100deg,rgba(10,14,38,.96),rgba(10,14,38,.8) 55%,rgba(10,14,38,.6)),url(img/{foto})" aria-hidden="true"></div>
  <span class="dots dots-tl dots-on-dark" aria-hidden="true"></span>
  <span class="hairline hl-b" aria-hidden="true" data-overflow-ok></span>
  <span class="shard shard-bl-ink" aria-hidden="true"></span>
  <span class="shard shard-br" aria-hidden="true"></span>
  <div class="wrap page-hero-in">
    <nav class="ruta rise" aria-label="Ruta"><a href="./index.html">Inicio</a><i class="ti ti-chevron-right" aria-hidden="true"></i><span>{ruta}</span></nav>
    <h1 class="page-h1 rise d1">{t1} <span>{t2}</span></h1>
    <p class="page-sub rise d2">{bajada}</p>
{extra}  </div>
</section>
'''

CTA = '''<!-- ============ CTA ============ -->
<section class="sec t1 cta-int">
  <span class="dots dots-l dots-on-dark" aria-hidden="true"></span>
  <div class="wrap cta-in reveal">
    <h2 class="h2">¿Necesitás asesoramiento <span>sobre tu situación?</span></h2>
    <p class="lead">Lunes a viernes de 8 a 20 h, en Córdoba y La Falda.</p>
    <div class="cta-btns">
      <a class="btn btn-bronce js-wa" href="#" data-msg="Hola, quisiera hacer una consulta.">Consultar por WhatsApp</a>
      <a class="btn btn-line" href="./index.html#contacto">Ver contacto</a>
    </div>
  </div>
</section>'''

# ---------------- SERVICIOS ----------------
SERV = [
    ("defensas", "ti-shield-half", "Defensas penales",
     "Para aquellas personas que puedan estar atravesando una privación de libertad (detención o prisión preventiva) o se encuentren investigadas en causas penales. En todas las etapas del proceso: investigación penal y juicio oral.", []),
    ("victimas", "ti-user-shield", "Representación de víctimas",
     "Nos constituimos como querellantes particulares para impulsar el proceso penal y representar a las víctimas hasta el juicio, para obtener una sentencia justa.", []),
    ("denuncias", "ti-file-alert", "Denuncias de delitos",
     "Para asistir, guiar, ayudar o llevar a cabo denuncias, colaborando con aquellas personas que resultaron víctimas de un hecho delictivo.", []),
    ("urgentes", "ti-clock-exclamation", "Presentaciones urgentes, beneficios y recursos", "",
     ["Excarcelaciones", "Cese de prisión preventiva", "Control jurisdiccional", "Prisiones domiciliarias", "Recurso de apelación", "Recurso de casación", "Recurso extraordinario", "Recurso de queja"]),
    ("ejecucion", "ti-gavel", "Ejecución penal",
     "Desarrollo de la defensa penal para obtener los distintos beneficios que admite la ley: libertad condicional, asistida o régimen de semilibertad.", []),
    ("vehiculos", "ti-car", "Restitución de vehículos secuestrados",
     "Gestión para el recupero de vehículos secuestrados en causas penales, en etapa de investigación o de juicio.", []),
    ("otros", "ti-scale", "Otros servicios", "",
     ["Contravención: representación en procesos contravencionales", "Mediación penal: nuevas herramientas para buscar la solución de los conflictos penales"]),
]
# orden de grilla sin huérfanos: [defensas, víctimas] [urgentes ancha] [denuncias, ejecución] [vehículos, otros]
ORDEN = ["defensas", "victimas", "urgentes", "denuncias", "ejecucion", "vehiculos", "otros"]
SERV.sort(key=lambda x: ORDEN.index(x[0]))
cards = []
for sid, ic, tit, txt, items in SERV:
    lst = ('<ul class="det-list">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>") if items else ""
    p = f"<p>{txt}</p>" if txt else ""
    cls = " det-wide" if sid == "urgentes" else ""
    cards.append(f'      <article class="det{cls} reveal" id="{sid}"><i class="ti {ic}" aria-hidden="true"></i><div><h3>{tit}</h3>{p}{lst}</div></article>')

RAMAS = [
    ("civil", "Derecho civil y comercial", ["Accidentes de tránsito", "Juicios ejecutivos", "Desalojo", "Declaratoria de herederos", "Sucesiones", "Usucapión"]),
    ("familia", "Derecho de familia", ["Divorcio", "Régimen de comunicación y cuota alimentaria", "División de bienes", "Violencia familiar y de género", "Menores"]),
    ("laboral", "Derecho laboral", ["Despidos injustificados", "Indemnizaciones", "Accidentes laborales", "Reclamos a la ART"]),
]
ramas = "\n".join(f'      <article class="rama reveal" id="{rid}"><h3>{t}</h3><ul>' + "".join(f"<li>{x}</li>" for x in it) + "</ul></article>" for rid, t, it in RAMAS)

indice = ('    <nav class="area-index rise d3" aria-label="Secciones de la página">'
          '<a href="#penal">Derecho penal</a><a href="#delitos">Delitos</a><a href="#civil">Civil y comercial</a>'
          '<a href="#familia">Familia</a><a href="#laboral">Laboral</a></nav>\n')
cuerpo = cabecera("Nuestros", "servicios.", "Servicios", "Defensa penal en todas las etapas del proceso y representación en otras ramas del derecho.", "columnas.jpg", indice)
cuerpo += f'''
<!-- ============ PENAL ============ -->
<section class="sec t2" id="penal">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Derecho penal</p>
      <h2 class="h2">Defensa y representación <span>con soluciones concretas.</span></h2>
    </div>
    <div class="det-grid">
{chr(10).join(cards)}
    </div>
  </div>
</section>

<!-- ============ DELITOS ============ -->
<section class="sec t3 delitos" id="delitos">
  <span class="shard shard-bl" aria-hidden="true"></span>
  <div class="delitos-bg" aria-hidden="true"></div>
  <div class="wrap delitos-grid">
    <div class="delitos-head reveal">
      <p class="eyebrow">Todas las áreas</p>
      <h2 class="h2">Delitos en los que <span>intervenimos.</span></h2>
      <p class="lead">Actuación presencial en toda la Provincia de Córdoba, en la competencia provincial y federal.</p>
    </div>
    <ul class="delitos-list reveal">
      <li><b>Delitos contra las personas</b><span>Homicidio, lesiones, amenazas.</span></li>
      <li><b>Delitos contra la propiedad</b><span>Daños, robos, usurpación, estafas.</span></li>
      <li><b>Estupefacientes</b><span>Comercialización o tenencia.</span></li>
      <li><b>Violencia familiar y de género</b><span>Defensa y representación.</span></li>
      <li><b>Delitos contra la integridad sexual</b><span>Defensa y querella.</span></li>
      <li><b>Delitos informáticos</b><span>Grooming, ciberestafas.</span></li>
      <li><b>Delitos especiales</b><span>Asociación ilícita, societarios, penal tributario.</span></li>
    </ul>
  </div>
</section>

<!-- ============ OTRAS RAMAS ============ -->
<section class="sec t2" id="ramas">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Otras ramas del derecho</p>
      <h2 class="h2">Profesionales asociados <span>con amplia trayectoria.</span></h2>
      <p class="lead">La integración de otros profesionales a nuestro equipo nos permite ofrecer una solución concreta y responsable.</p>
    </div>
    <div class="ramas-grid">
{ramas}
    </div>
  </div>
</section>

{CTA}'''
page("servicios.html", "Servicios | Parisotto & Asociados · Abogados en Córdoba",
     "Defensas penales, representación de víctimas, recursos, ejecución penal y vehículos secuestrados. También civil y comercial, familia y laboral. Córdoba y La Falda.", cuerpo)

# ---------------- EL ESTUDIO ----------------
cuerpo = cabecera("El", "estudio.", "El estudio", "Compromiso, responsabilidad, transparencia y eficacia.", "libros.jpg")
cuerpo += '''
<!-- ============ QUIÉNES SOMOS ============ -->
<section class="sec t2">
  <div class="wrap qs-grid">
    <div class="qs-head reveal">
      <p class="eyebrow">Quiénes somos</p>
      <h2 class="h2">Más de 20 años <span>de trayectoria.</span></h2>
    </div>
    <div class="qs-txt reveal">
      <p class="lead">Nuestro estudio jurídico está compuesto por profesionales del derecho con más de 20 años de experiencia y trayectoria, ofreciendo representación y asistencia jurídica en las diferentes etapas del proceso penal, para brindar soluciones concretas.</p>
      <p class="lead">Desarrollamos la actividad de forma presencial en toda la Provincia de Córdoba (competencia provincial y federal) y coordinamos la asistencia y representación en otras jurisdicciones del país con el apoyo de otros profesionales.</p>
      <ul class="valores-list">
        <li><i class="ti ti-target-arrow" aria-hidden="true"></i>Compromiso</li>
        <li><i class="ti ti-shield-check" aria-hidden="true"></i>Responsabilidad</li>
        <li><i class="ti ti-eye" aria-hidden="true"></i>Transparencia</li>
        <li><i class="ti ti-bolt" aria-hidden="true"></i>Eficacia</li>
      </ul>
    </div>
  </div>
</section>

<!-- ============ EQUIPO ============ -->
<section class="sec t3">
  <span class="shard shard-bl" aria-hidden="true"></span>
  <span class="dots dots-r dots-on-dark" aria-hidden="true"></span>
  <div class="wrap estudio-grid">
    <figure class="retrato reveal">
      <img src="./img/parisotto.jpg" alt="Dr. Darío Luciano Parisotto" width="768" height="1024" loading="lazy">
      <figcaption><b>Dr. Darío Luciano Parisotto</b><span>Mat. Prov. 1-34.106 · Mat. Fed. T502 F121</span></figcaption>
    </figure>
    <div class="estudio-txt reveal">
      <p class="eyebrow">Equipo</p>
      <h2 class="h2">Profesionales <span>del estudio.</span></h2>
      <p class="lead">Un equipo de profesionales del derecho, que integra a colegas asociados con trayectoria en otras ramas.</p>
      <div class="socios">
        <article><span class="socio-ini" aria-hidden="true">MN</span><div><b>Dr. Mariano Alejandro Neme</b><span>MP 1-40041</span></div></article>
        <article><span class="socio-ini" aria-hidden="true">GN</span><div><b>Dr. Gustavo Guillermo Neme</b><span>MP 1-26424</span></div></article>
      </div>
      <p class="asoc-txt">Con importante trayectoria y experiencia en derecho civil y comercial, laboral, ART, familia, declaratoria de herederos, sucesiones, usucapión, accidentes de tránsito y desalojo.</p>
    </div>
  </div>
</section>

<!-- ============ SEDES Y ALCANCE ============ -->
<section class="sec t2">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Dónde estamos</p>
      <h2 class="h2">Dos sedes <span>en la provincia.</span></h2>
    </div>
    <div class="sedes-grid">
      <article class="sede reveal"><small>Sede central</small><h3>Córdoba</h3><p>Belgrano 54, 5º piso, oficina «G»<br>Torre Nubis (CP 5000)</p><a class="link-arrow" href="https://www.google.com/maps/search/?api=1&amp;query=Belgrano+54+Torre+Nubis+C%C3%B3rdoba" target="_blank" rel="noopener">Cómo llegar <i class="ti ti-arrow-right" aria-hidden="true"></i></a></article>
      <article class="sede reveal"><small>Sucursal</small><h3>La Falda</h3><p>Av. Edén 444, local 18<br>Valle de Punilla</p><a class="link-arrow" href="https://www.google.com/maps/search/?api=1&amp;query=Av.+Ed%C3%A9n+444+La+Falda+C%C3%B3rdoba" target="_blank" rel="noopener">Cómo llegar <i class="ti ti-arrow-right" aria-hidden="true"></i></a></article>
    </div>
    <div class="otras-jur reveal">
      <p>Coordinamos la asistencia en:</p>
      <ul class="provincias"><li>Buenos Aires</li><li>Santa Fe</li><li>La Pampa</li><li>Entre Ríos</li><li>Mendoza</li><li>San Luis</li><li>Santiago del Estero</li><li>Salta</li><li>Jujuy</li><li>Tierra del Fuego</li></ul>
    </div>
  </div>
</section>

''' + CTA
page("el-estudio.html", "El estudio | Parisotto & Asociados · Abogados en Córdoba",
     "Estudio Jurídico Parisotto Darío Luciano & Asoc.: más de 20 años de trayectoria en derecho penal. Sedes en Córdoba y La Falda. Dres. Parisotto y Neme.", cuerpo)
