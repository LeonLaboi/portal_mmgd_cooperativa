import json
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

from django.shortcuts import render, get_object_or_404, redirect #get_list_or_404
from django.http import JsonResponse #HttpResponse
from django.templatetags.static import static
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

from galeria.models import Cliente as Perfil, BaseMicro


def index(request):
  
    image_path = "https://static.wixstatic.com/media/f98783_421f8b496bf44a31a146dd289460e2ae~mv2_d_4000_2000_s_2.jpg/v1/fill/w_1903,h_811,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/f98783_421f8b496bf44a31a146dd289460e2ae~mv2_d_4000_2000_s_2.jpg"
    context = {
        'image_path': image_path,
        'welcome_message': "CONVIDAMOS COOPERATIVAS \
                           A REPENSAREM SEUS MODOS DE GERAÇÃO E CONSUMO DE ENERGIA!"
    }
    return render(request, 'galeria/index.html', context)#return render(request, 'index.html') #

def alura(request):
    perfis = Perfil.objects.all()
    return render(request, 'galeria/alura.html', {'cards': perfis})


def imagem(request, perfil_id):
    perfil = get_object_or_404(Perfil, pk=perfil_id)

    if perfil.nome == 'Gestor de Energia':
        clientes = BaseMicro.objects.values('id_client').distinct()
        selected_filter = 'id_client'
    else:
        clientes = BaseMicro.objects.values('id_uc').distinct()
        selected_filter = 'id_uc'

    selected_id = request.GET.get(selected_filter, clientes[0][selected_filter])
    leituras = BaseMicro.objects.filter(**{selected_filter: selected_id})

    mes_refs = [leitura.mes_ref.strftime("%m/%Y") for leitura in leituras]
    consumo = [leitura.consumo_kwh for leitura in leituras]

    plt.figure(figsize=(14, 7.5))
    plt.bar(mes_refs, consumo, color='skyblue')
    # plt.title(f'Consumo de Energia - {selected_filter}={selected_id}')
    plt.xlabel('Mês Referência')
    plt.ylabel('Energia (kWh)')
    plt.xticks(rotation=45)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graphic = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return render(request, 'galeria/graph.html', {
        'page_title': 'Projeto MMGD',
        'show_home_button': True,
        'perfil': perfil,
        'graphic': graphic,
        'clientes': clientes,
        'selected_filter': selected_filter,
        'selected_id': selected_id,
    })


def get_graph(request, client_id):
    # Obtém os dados do gráfico para o cliente específico
    # leituras = BaseMicro.objects.filter(id_client=client_id).values('mes_ref', 'qtd_enrg_te')

    # # Criação do gráfico
    # meses = [leitura['mes_ref'] for leitura in leituras]
    # consumos = [leitura['qtd_enrg_te'] for leitura in leituras]

    # plt.figure(figsize=(10, 5))
    # plt.bar(meses, consumos)
    # plt.xlabel('Meses')
    # plt.ylabel('Quantidade de Energia (kWh)')
    # plt.title(f'Consumo de Energia para Cliente ID {client_id}')

    # Salvar o gráfico em um buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    
    # Codificar o gráfico em base64
    graphic = base64.b64encode(buf.read()).decode('utf-8')
    return JsonResponse({'graphic': graphic})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redireciona para a página 'alura' em caso de sucesso
        else:
            messages.error(request, 'Credenciais inválidas')
    return render(request, 'galeria/login.html')

def home(request):
    perfis = Perfil.objects.all()
    # caminho relativo dentro de static/
    default_images = {
        'micro': 'assets/imagens/galeria/micro.png',
        'macro': 'assets/imagens/galeria/macro.png',
        'default': 'assets/imagens/galeria/micro.png',
    }
    return render(request, 'galeria/home.html', {
        'page_title': 'Projeto MMGD',
        'cards': perfis,
        'show_home_button': False,
        'default_images': default_images
    })
