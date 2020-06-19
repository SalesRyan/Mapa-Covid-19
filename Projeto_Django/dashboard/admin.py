from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(DadosEstado)
admin.site.register(CasosCidade)
admin.site.register(Leitos)
admin.site.register(CasosSexo)
admin.site.register(CasosFaixaEtaria)
admin.site.register(Comorbidades)
admin.site.register(DataAtualizacao)