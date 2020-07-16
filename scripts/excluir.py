from dashboard.models import *

data_atualizacao = DataAtualizacao.objects.all()
dados_estado = DadosEstado.objects.all()
casos_cidade = CasosCidade.objects.all()
leitos = Leitos.objects.all()
casos_sexo = CasosSexo.objects.all().last()
casos_faixa_etaria = CasosFaixaEtaria.objects.all()
comorbidades = Comorbidades.objects.all()
dados_estado_pred = DadosEstadoPredicao.objects.all()
dados_leitos_pred = LeitosPredicao.objects.all()

data_atualizacao.delete()
dados_estado.delete()
casos_cidade.delete()
leitos.delete()
casos_sexo.delete()
casos_faixa_etaria.delete()
comorbidades.delete()
dados_estado_pred.delete()
dados_leitos_pred.delete()