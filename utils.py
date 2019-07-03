def dict_triples(grafo):
    dict = {}
    for subj, predi, obje in grafo.triples((None, None, None)):
        type =str(predi).rsplit('/', 1)[-1]
        dict[type] = str(obje).rsplit('/', 1)[-1]
        # print(str(predi).rsplit('/', 1)[-1])
        # print(predi, obje + "\n")
    return dict
def formato_html(dict):
    lista = ["<div><table><tbody>","<tr>","<th> Property </th>  <th> Value </th>","</tr>"]
    for key, value in dict.items():
        lista.append("<tr><td><small>cod:</small>"+key+"</td><td><ul><li><span>"+value+"</span></li></ul></td></tr>")
    lista.append("</tbody></table></div>")
    string_html = ''.join(str(i) for i in lista)
    #print(string_html)
    return string_html
