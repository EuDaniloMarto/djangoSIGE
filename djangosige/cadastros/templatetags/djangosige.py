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
