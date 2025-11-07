from django import template

register = template.Library()


@register.inclusion_tag('djangosige/paginacao.html', takes_context=True)
def paginacao(context, page_obj, param_name='page'):
    """
    Gera paginação Bootstrap 5 com elipses tipo:
    | << | < | 1 | 2 | ... | 48 | <49> | 50 | ... | 98 | 99 | > | >> |

    Uso no template:
        {% load pagination_tags %}
        {% bootstrap_pagination page_obj %}

    Ou se quiser preservar filtros:
        {% bootstrap_pagination page_obj 'pagina' %}
    """
    request = context.get('request')
    paginator = page_obj.paginator
    current = page_obj.number
    total = paginator.num_pages

    # Define páginas a mostrar
    if total <= 7:
        pages = list(range(1, total + 1))
    else:
        pages = set([1, 2, total - 1, total])
        pages.update(range(current - 2, current + 3))
        pages = [p for p in sorted(pages) if 1 <= p <= total]

    # Adiciona "..." entre intervalos
    display_pages = []
    last = 0
    for p in pages:
        if last and p - last > 1:
            display_pages.append('...')
        display_pages.append(p)
        last = p

    # Preserva parâmetros GET (ex: busca, filtro)
    params = request.GET.copy() if request else {}
    params.pop(param_name, None)

    # Base da URL (ex: "?busca=abc&page=")
    querystring = '&'.join([f"{k}={v}" for k, v in params.items()])
    base_url = f"?{querystring}&{param_name}=" if querystring else f"?{param_name}="

    return {
        'page_obj': page_obj,
        'pages': display_pages,
        'base_url': base_url,
    }


@register.inclusion_tag("djangosige/contador_registros.html")
def contador_registros(page_obj):
    """
    Exibe contador tipo 'Exibindo 26–50 de 99 registros'
    """
    return {
        "inicio": page_obj.start_index(),
        "fim": page_obj.end_index(),
        "total": page_obj.paginator.count,
    }


@register.simple_tag(takes_context=True)
def order(context, **novos_params):
    request = context["request"]
    params = request.GET.copy()
    for k, v in novos_params.items():
        params[k] = v
    return f"?{params.urlencode()}"
