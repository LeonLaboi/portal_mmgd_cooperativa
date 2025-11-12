from django.urls import path
from .views import index, alura, imagem_micro, estatistica_descritiva, login_view, home, boxplot_consumo, regressao_consumo # Importando as views necessárias

urlpatterns = [
    path('', index, name='index'), #Página inicial
    path('login/', login_view, name='login'),  # URL para a página de login
    path('alura/', alura, name='alura'), #Página alura
    path('home/', home, name='home'), #Homepage
    path('imagem/<int:perfil_id>/', imagem_micro, name='imagem_micro'),
    path('estatistica/<int:perfil_id>/', estatistica_descritiva, name='estatistica_descritiva'),
    path('boxplot_consumo/', boxplot_consumo, name='boxplot_consumo'),
    path('regressao_consumo/', regressao_consumo, name='regressao_consumo'),
    # path('get_graph/<int:client_id>/', get_graph, name='get_graph'),
]
