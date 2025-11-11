from django.urls import path
from .views import index, alura, imagem_micro, estatistica_descritiva, login_view, home, get_graph # Importando as views necessárias

urlpatterns = [
    path('', index, name='index'), #Página inicial
    path('login/', login_view, name='login'),  # URL para a página de login
    path('alura/', alura, name='alura'), #Página alura
    path('home/', home, name='home'), #Homepage
    path('imagem/<int:perfil_id>/', imagem_micro, name='imagem_micro'),
    path('estatistica/<int:perfil_id>/', estatistica_descritiva, name='estatistica_descritiva'),
    path('get_graph/<int:client_id>/', get_graph, name='get_graph'),
]
