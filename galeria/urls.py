from django.urls import path
from .views import index, alura, imagem, get_graph, login_view, home # Importando as views necessárias

urlpatterns = [
    path('', index, name='index'), #Página inicial
    path('login/', login_view, name='login'),  # URL para a página de login
    path('alura/', alura, name='alura'), #Página alura
    path('home/', home, name='home'), #Homepage
    path('imagem/<int:perfil_id>', imagem, name='imagem'),
    path('get_graph/<int:client_id>/', get_graph, name='get_graph'),
]
