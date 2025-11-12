import json
import matplotlib.pyplot as plt, seaborn as sns
import numpy as np, pandas as pd
import io, base64
from datetime import datetime, timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
# from django.templatetags.static import static
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
# from django.db.models import Avg, Sum, Count

from galeria.models import Cliente as Perfil, BaseMicro, Cliente
from galeria.estatisticas import obter_metricas_validacao

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

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
    consumidores = Cliente.objects.filter(tipo__in=['consumidor', 'prosumidor'])
    return render(request, 'galeria/alura.html', {'cards': consumidores}) #perfis})

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
    cards = [
        {
            'id': 1,
            'nome': 'Visão Micro',
            'legenda': 'Monitoramento histórico de Geração, Consumo e Compensação de Créditos.',
            'imagem': 'assets/imagens/galeria/micro.jpg',
            'url': 'imagem_micro',  # nome da rota Django
        },
        {
            'id': 2,
            'nome': 'Visão Macro',
            'legenda': 'Análises Estastíticas e Performance de Projeção.',
            'imagem': 'assets/imagens/galeria/macro.jpg',
            'url': 'estatistica_descritiva',
        },
    ]

    return render(request, 'galeria/home.html', {
        'page_title': 'Projeto MMGD',
        'cards': cards,
        'show_home_button': False
    })


def imagem_micro(request, perfil_id):
    perfil = get_object_or_404(Perfil, pk=perfil_id)
    clientes = BaseMicro.objects.values('id_uc').distinct()
    selected_filter = 'id_uc'

    selected_id = request.GET.get(selected_filter, clientes[0][selected_filter])
    leituras = BaseMicro.objects.filter(**{selected_filter: selected_id})

    mes_refs = [leitura.mes_ref.strftime("%m/%Y") for leitura in leituras]
    consumo = [leitura.consumo_kwh for leitura in leituras]

    plt.figure(figsize=(14, 7.5))
    plt.bar(mes_refs, consumo, color='skyblue')
    plt.xlabel('Mês Referência')
    plt.ylabel('Energia (kWh)')
    plt.xticks(rotation=45)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graphic = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return render(request, 'galeria/graph.html', {
        'page_title': 'Visão Micro',
        'perfil': perfil,
        'graphic': graphic,
        'clientes': clientes,
        'selected_filter': selected_filter,
        'selected_id': selected_id,
        'show_home_button': True,
    })



def estatistica_descritiva(request, perfil_id):
    
    relatorio = obter_metricas_validacao()
    perfil = {
        'id': perfil_id,
        'nome': 'Visão Macro',
        'legenda': 'Análises estatísticas e desempenho da projeção.',
    }

    return render(request, 'galeria/estatistica.html', {
        'page_title': 'Visão Macro',
        'perfil': perfil,
        'relatorio': relatorio,
        'show_home_button': True,
    })



def boxplot_consumo(request):
    # obtém todos os dados da tabela BaseMicro
    dados = BaseMicro.objects.all().values('mes_ref', 'consumo_kwh')
    df = pd.DataFrame(dados)

    if df.empty:
        return JsonResponse({'error': 'Sem dados disponíveis'}, status=400)

    df['mes_ref'] = pd.to_datetime(df['mes_ref'], errors='coerce')
    df = df.dropna(subset=['mes_ref', 'consumo_kwh'])

    df['semestre'] = df['mes_ref'].dt.month.apply(lambda m: '1º Semestre' if m <= 6 else '2º Semestre')

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, y='semestre', x='consumo_kwh', orient='h', width=0.5, palette='winter')
    plt.title('Distribuição do Consumo de Energia por Semestre')
    plt.xlabel('')
    plt.ylabel('Consumo (kWh)')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    graphic = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return JsonResponse({'graphic': graphic})


def regressao_consumo(request):
    dados = BaseMicro.objects.all().values('mes_ref', 'consumo_kwh')
    df = pd.DataFrame(dados)
    if df.empty or len(df) < 12:
        return JsonResponse({'error': 'Dados insuficientes'}, status=400)

    df['mes_ref'] = pd.to_datetime(df['mes_ref'], errors='coerce')
    df = df.dropna(subset=['mes_ref', 'consumo_kwh'])
    df = df.sort_values('mes_ref')

    df_recent = df.iloc[-12:]
    X = np.arange(len(df_recent)).reshape(-1, 1)
    y = df_recent['consumo_kwh'].values

    model = LinearRegression().fit(X, y)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)

    plt.figure(figsize=(8, 4))
    ax = sns.scatterplot(x=y_pred, y=y, color='steelblue')
    sns.lineplot(x=y_pred, y=y_pred, color='crimson', lw=2, ax=ax)

    plt.title('Previsão x Real', fontsize=16)
    plt.xlabel('Consumo de Energia (kWh) - Previsão', fontsize=13)
    plt.ylabel('Consumo de Energia (kWh) - Real', fontsize=13)

    plt.text(min(y_pred)*1.01, max(y)*0.95, f'$R^2$ = {r2:.3f}',
             fontsize=12, color='black',
             bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3'))

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    graphic = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    return JsonResponse({'graphic': graphic})

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