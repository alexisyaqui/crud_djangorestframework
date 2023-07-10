import uuid
from django.db import models

# Create your models here.

class NotaModelo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=255, unique=True)
    contenido = models.TextField()
    categoria = models.CharField(max_length=100, null=True, blank=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaActulizacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notas"
        ordering = ['fechaCreacion']

        def __str__(self) -> str:
            return self.titulo