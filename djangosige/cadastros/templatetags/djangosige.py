# cadastros/templatetags/filtros_tags.py
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def querystring(context, **kwargs):
    """
    Constrói a query string, mantendo os parâmetros GET existentes,
    mas sobrescrevendo-os com os kwargs fornecidos.

    Se um valor for None, o parâmetro é removido da query string.

    Exemplo de uso:
    <a href="?{% querystring relacionamento='cliente' %}">Clientes</a>
    <a href="?{% querystring relacionamento=None %}">Todos (remove o parametro)</a>
    """
    request = context["request"]

    # Faz uma cópia mutável dos parâmetros GET atuais
    updated_params = request.GET.copy()

    for key, value in kwargs.items():
        if value is not None:
            # Sobrescreve/adiciona o novo parâmetro
            updated_params[key] = str(value)
        else:
            # Remove o parâmetro se o valor for None (usado para o link 'todos')
            if key in updated_params:
                del updated_params[key]

    # Converte os parâmetros de volta para uma string de consulta e retorna
    return updated_params.urlencode()


@register.inclusion_tag("djangosige/_paginacao.html", takes_context=True)
def paginacao(context, page_obj, base_url="?page="):
    """
    Renderiza paginação estilo Bootstrap 5 com elipses (...).

    Args:
        context: Contexto atual do template (mantém variáveis globais).
        page_obj: Objeto de página do Django (Paginator.page).
        base_url: Prefixo da URL (pode incluir parâmetros de busca).

    Retorna:
        Contexto com:
            - page_obj: página atual
            - pages: lista de páginas e elipses
            - base_url: prefixo da URL (para montar links)
    """
    paginator = page_obj.paginator
    total_pages = paginator.num_pages
    current = page_obj.number

    # Lógica de exibição de páginas
    if total_pages <= 7:
        pages = range(1, total_pages + 1)
    else:
        if current <= 4:
            pages = [1, 2, 3, 4, 5, "...", total_pages - 1, total_pages]
        elif current >= total_pages - 3:
            pages = [1, 2, "...", total_pages - 4, total_pages - 3, total_pages - 2, total_pages - 1, total_pages]
        else:
            pages = [1, 2, "...", current - 1, current, current + 1, "...", total_pages - 1, total_pages]

    return {
        "page_obj": page_obj,
        "pages": pages,
        "base_url": base_url,
    }


@register.inclusion_tag("djangosige/_contar_registros.html")
def contar_registros(page_obj):
    """
    Exibe contador tipo 'Exibindo 26–50 de 99 registros'
    """
    return {
        "inicio": page_obj.start_index(),
        "fim": page_obj.end_index(),
        "total": page_obj.paginator.count,
    }
