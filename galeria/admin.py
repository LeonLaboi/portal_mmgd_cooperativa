from django.contrib import admin
from galeria.models import Cliente

class ListandoClientes(admin.ModelAdmin):
    list_display = ('cnpj', 'nome', 'legenda')
    list_display_links = ('nome',)
    search_fields = ('nome',)

admin.site.register(Cliente, ListandoClientes)
