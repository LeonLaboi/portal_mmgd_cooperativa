# galeria/estatisticas.py
import numpy as np
import pandas as pd
from scipy import stats
from django.db.models import Avg, StdDev, Count
from .models import BaseMicro

class ValidadorDadosMaisRecentess:
    """
    Validar estatisticamente se os dados dos últimos 12 meses
    tem as mesmas características dos demais dados dados históricos
    """
    
    def __init__(self):
        self.df_historico = None
        self.df_recente = None
        self.carregar_dados()
    
    def carregar_dados(self):
        """Carrega dados históricos"""
        todos_dados = pd.DataFrame(list(BaseMicro.objects.all().values()))
        
        if len(todos_dados) == 0:
            return
        
        # Ordena por data e separa históricos
        todos_dados['mes_ref'] = pd.to_datetime(todos_dados['mes_ref'])
        todos_dados = todos_dados.sort_values('mes_ref')
        
        # Considera os últimos 12 meses
        if len(todos_dados) > 12:
            self.df_historico = todos_dados.iloc[:-12]
            self.df_recente = todos_dados.iloc[-12:]
        else:
            self.df_historico = todos_dados
            self.df_recente = pd.DataFrame()
    
    def teste_ks_duas_amostras(self, coluna):
        """
        Teste de Kolmogorov-Smirnov para duas amostras
        Verifica se as distribuições são semelhantes
        """
        if self.df_recente.empty or coluna not in self.df_historico.columns:
            return None
        
        dados_hist = self.df_historico[coluna].dropna()
        dados_sint = self.df_recente[coluna].dropna()
        
        if len(dados_hist) < 2 or len(dados_sint) < 2:
            return None
        
        stat, p_value = stats.ks_2samp(dados_hist, dados_sint)
        
        return {
            'estatistica': stat,
            'p_valor': p_value,
            'significativo': p_value > 0.05,  # Não rejeita H0 (distribuições iguais)
            'interpretacao': 'Distribuições similares' if p_value > 0.05 else 'Distribuições diferentes'
        }
    
    def teste_t_medias(self, coluna):
        """
        Teste t para comparar médias de duas amostras
        """
        if self.df_recente.empty or coluna not in self.df_historico.columns:
            return None
        
        dados_hist = self.df_historico[coluna].dropna()
        dados_sint = self.df_recente[coluna].dropna()
        
        if len(dados_hist) < 2 or len(dados_sint) < 2:
            return None
        
        # Teste t assumindo variâncias diferentes
        stat, p_value = stats.ttest_ind(dados_hist, dados_sint, equal_var=False)
        
        return {
            'estatistica': stat,
            'p_valor': p_value,
            'significativo': p_value > 0.05,  # Não rejeita H0 (médias iguais)
            'media_historico': dados_hist.mean(),
            'media_sintetico': dados_sint.mean(),
            'interpretacao': 'Médias similares' if p_value > 0.05 else 'Médias diferentes'
        }
    
    def analise_descritiva_comparativa(self, coluna):
        """Análise descritiva comparativa entre históricos"""
        if self.df_recente.empty or coluna not in self.df_historico.columns:
            return None
        
        dados_hist = self.df_historico[coluna].dropna()
        dados_sint = self.df_recente[coluna].dropna()
        
        return {
            'historico': {
                'n': len(dados_hist),
                'media': dados_hist.mean(),
                'mediana': dados_hist.median(),
                'desvio_padrao': dados_hist.std(),
                'min': dados_hist.min(),
                'max': dados_hist.max()
            },
            'sintetico': {
                'n': len(dados_sint),
                'media': dados_sint.mean(),
                'mediana': dados_sint.median(),
                'desvio_padrao': dados_sint.std(),
                'min': dados_sint.min(),
                'max': dados_sint.max()
            },
            'diferenca_percentual_media': abs((dados_sint.mean() - dados_hist.mean()) / dados_hist.mean() * 100) if dados_hist.mean() != 0 else 0
        }
    
    def validar_todas_colunas_numericas(self):
        """Executa validação para todas as colunas numéricas"""
        if self.df_historico is None or self.df_recente.empty:
            return {'erro': 'Dados insuficientes para validação'}
        
        colunas_numericas = self.df_historico.select_dtypes(include=[np.number]).columns

        ignorar_prefixos = ('leitura', 'prc', 'tarifa', 'cred', 'pis', 'const', 'icms', 'qtd')
        colunas_filtradas = [
        c for c in colunas_numericas
        if not c.lower().startswith(ignorar_prefixos) and c not in ['id', 'id_client', 'id_uc']]

        resultados = {}
        
        for coluna in colunas_filtradas:
                
            resultados[coluna] = {
                'descricao': self.analise_descritiva_comparativa(coluna),
                'teste_ks': self.teste_ks_duas_amostras(coluna),
                'teste_t': self.teste_t_medias(coluna)
            }
        
        return resultados
    
    def gerar_relatorio_validacao(self):
        """Gera um relatório completo de validação"""
        validacao = self.validar_todas_colunas_numericas()
        
        if 'erro' in validacao:
            return validacao
        
        # Calcula métricas de qualidade geral
        colunas_validas = 0
        colunas_totais = 0
        
        for coluna, resultados in validacao.items():
            colunas_totais += 1
            if (resultados['teste_ks'] and resultados['teste_ks']['significativo'] and
                resultados['teste_t'] and resultados['teste_t']['significativo']):
                colunas_validas += 1
        
        qualidade_geral = (colunas_validas / colunas_totais) * 100 if colunas_totais > 0 else 0
        
        relatorio = {
            'qualidade_geral': qualidade_geral,
            'colunas_validas': colunas_validas,
            'colunas_totais': colunas_totais,
            'status': '✅ Dados recentes válidados' if qualidade_geral > 80 else '⚠️ Dados mais com divergências',
            'detalhes': validacao
        }
        
        return relatorio

# Função para usar nas views
def obter_metricas_validacao():
    """Retorna métricas de validação para usar na view da home"""
    validador = ValidadorDadosMaisRecentess()
    relatorio = validador.gerar_relatorio_validacao()
    
    return relatorio