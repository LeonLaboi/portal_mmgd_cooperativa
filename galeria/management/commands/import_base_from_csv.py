import os, pandas as pd
from django.core.management.base import BaseCommand
from galeria.models import LeituraCSV
from datetime import datetime
from django.conf import settings  # Importar configurações do Django

class Command(BaseCommand):
    help = 'Importa dados do CSV para o banco de dados'

    def handle(self, *args, **kwargs):
        # Ler o CSV
        data = pd.read_csv(os.path.join(settings.BASE_DIR, 'base.csv'), sep=';', decimal=',')

        # Converter 'mes_ref' para o formato de data (assumindo que está como 'mm/yyyy')
        data['mes_ref'] = pd.to_datetime(data['mes_ref'], format='%m/%Y')

        # Iterar sobre as linhas e salvar no banco de dados
        for _, row in data.iterrows():
            LeituraCSV.objects.create(
                mes_ref=row['mes_ref'],
                dt_vcto=datetime.strptime(row['dt_vcto'], '%Y-%m-%d'),
                id_client=row['id_client'],
                id_uc=row['id_uc'],
                grandezas=row['grandezas'],
                leitura_anterior=row['leitura_anterior'],
                leitura_atual=row['leitura_atual'],
                const_medidor=row['const_medidor'],
                consumo_kwh=row['consumo_kwh'],
                qtd_enrg_tusd=row['qtd_enrg_tusd'],
                prc_unit_tributos_tusd=row['prc_unit_tributos_tusd'],
                tusd=row['tusd'],
                pis_cofins_tusd=row['pis_cofins_tusd'],
                aliq_icms_tusd=row['aliq_icms_tusd'],
                icms_tusd=row['icms_tusd'],
                tarifa_unit_tusd=row['tarifa_unit_tusd'],
                qtd_enrg_te=row['qtd_enrg_te'],
                prc_unit_tributos_te=row['prc_unit_tributos_te'],
                te=row['te'],
                pis_cofins_te=row['pis_cofins_te'],
                aliq_icms_te=row['aliq_icms_te'],
                icms_te=row['icms_te'],
                tarifa_unit_te=row['tarifa_unit_te'],
                qtd_enrg_compensada_tusd=row['qtd_enrg_compensada_tusd'],
                prc_unit_tributos_compensada_tusd=row['prc_unit_tributos_compensada_tusd'],
                compensada_tusd=row['compensada_tusd'],
                pis_cofins_compensada_tusd=row['pis_cofins_compensada_tusd'],
                aliq_icms_compensada_tusd=row['aliq_icms_compensada_tusd'],
                icms_compensada_tusd=row['icms_compensada_tusd'],
                tarifa_unit_compensada_tusd=row['tarifa_unit_compensada_tusd'],
                qtd_enrg_compensada_te=row['qtd_enrg_compensada_te'],
                prc_unit_tributos_compensada_te=row['prc_unit_tributos_compensada_te'],
                compensada_te=row['compensada_te'],
                pis_cofins_compensada_te=row['pis_cofins_compensada_te'],
                aliq_icms_compensada_te=row['aliq_icms_compensada_te'],
                icms_compensada_te=row['icms_compensada_te'],
                tarifa_unit_compensada_te=row['tarifa_unit_compensada_te'],
                multa=row['multa'],
                juros_mora=row['juros_mora'],
                tx_2_emss_fat=row['tx_2_emss_fat'],
                dmic=row['dmic'],
                pc_art113_ren414=row['pc_art113_ren414'],
                cosip_cip=row['cosip_cip'],
                atualz_monetaria=row['atualz_monetaria'],
                rev_fat_atualiz=row['rev_fat_atualiz'],
                ren_1000=row['ren_1000'],
                art_323=row['art_323'],
                devol_pgto_fat_cancel=row['devol_pgto_fat_cancel'],
                sem_corresp_saldo=row['sem_corresp_saldo'],
                cred_solu_rclm=row['cred_solu_rclm'],
                cred_prox_fat=row['cred_prox_fat'],
                total=row['total'],
                pis_cofins_total=row['pis_cofins_total'],
                icms_total=row['icms_total'],
                tipo=row['tipo']
            )

        self.stdout.write(self.style.SUCCESS('Dados importados com sucesso!'))
