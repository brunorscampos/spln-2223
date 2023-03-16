import json

with open("medicina_teste.json", "r") as f:
    med = json.load(f)["completas"]

pagina_html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Medicina</title>
        <meta charset="utf-8"/>
        <style>
        body {
    background-color: powderblue;
    margin: 0;
}

h1 {
    color: blue;
}

p {
    color: red;
}

img {
    height: 250px;
}

.wrapingimage {  
    float: right;
    border: 2px solid blue;
}

.index {
    width: 22%;
    height: 100%;
    padding-left: 1%;
    padding-right: 1%;
    vertical-align: top;
}

.index2 {
    position: fixed;
}

.data {
    padding-right: 1%;
}
        </style>
    </head>
    <body>
        <table>
            <tr>
                <td class="index">
                    <div class="index2">
                        <h1>Medicina</h1>
                        <h2>Index</h3>
                        <h4>Indice</h4>
                        <!-- Lista com indice -->
                        <ul>
"""

for entry in med:
    pagina_html += f"""
                            <li>
                                <a href="#{med[entry]['index']}">{med[entry]['termo']}</a>
                            </li>
"""
    
pagina_html += """
                        </ul>
                    </div>
                </td>
                <td class="data">
                    <h2>Medicina</h2>
"""

for entry in med:
    pagina_html += f"""
                    <a name="{med[entry]['index']}"/>
                    <h3><b>Termo: </b> {med[entry]['termo']} </h3>
                    <p><b>Genero: </b> {med[entry]['genero']} </p>
                    <p><b>Areas: </b> {str(med[entry]['areas'])} </p>
                    <p><b>Sinonimos: </b> {str(med[entry]['sinonimos'])} </p>
                    <p><b>Variacoes: </b> {str(med[entry]['variacoes'])} </p>
                    <p><b>Traducoes: </b></p>
                    <ul>
"""
    for trad in med[entry]['traducoes']:
        pagina_html += f"""
                        <li><p><b>{trad}: </b> {med[entry]['traducoes'][trad]} </p></li>
"""
            
    pagina_html += f"""
                    </ul>
                    <p><b>Nota: </b> {med[entry]['nota']} </p>
                    <br>
"""

pagina_html += """
                </td>
            </tr>
        </table>
    </body>
</html>
"""

with open("medicina.html", "w") as f:
    f.write(pagina_html)


