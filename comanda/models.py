from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    produtos = models.ManyToManyField('Produto', related_name='clientes', blank=True)


    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='produtos/', null=True, blank=True)
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    pagamento = models.BooleanField(default=False)


    def total_item(self):
        return self.produto.preco * self.quantidade