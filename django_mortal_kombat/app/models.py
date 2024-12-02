from django.db import models
from django.contrib.auth.models import User

class Pontuacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Relaciona a pontuação ao usuário
    ganhador = models.CharField(max_length=20,  null=True)  # Pode ser 'vermelho' ou 'azul'
    data = models.DateTimeField(auto_now_add=True)  # Data em que a pontuação foi registrada

    def __str__(self):
        return f"{self.usuario.username} - {self.ganhador}"

