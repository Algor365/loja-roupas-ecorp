from django.contrib import admin
from .models import Cliente, Fornecedor, Produto, Venda

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'telefone', 'email', 'data_cadastro']
    search_fields = ['nome', 'email', 'cpf']
    list_filter = ['data_cadastro']

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'contato', 'telefone', 'data_cadastro']
    search_fields = ['nome', 'contato', 'cnpj']
    list_filter = ['data_cadastro']

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'tamanho', 'quantidade', 'preco_venda', 'data_cadastro']
    list_filter = ['categoria', 'tamanho', 'data_cadastro']
    search_fields = ['nome', 'categoria']

@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['produto', 'quantidade', 'preco_unitario', 'data_venda', 'lucro']
    list_filter = ['data_venda']
    search_fields = ['produto__nome']
    
    def lucro(self, obj):
        return obj.lucro
    lucro.short_description = 'Lucro'