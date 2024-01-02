# comanda_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Cliente, Produto, Pedido
from .forms import ClienteForm, ProdutoForm
from django.contrib import messages



def home(request):
    return render(request, 'home.html')

def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/clientes/')
    else:
        form = ClienteForm()

    return render(request, 'cadastrar_cliente.html', {'form': form})

def listar_clientes(request):
    clientes = Cliente.objects.all()

    if request.method == 'POST':
        for cliente in clientes:
            pagamento_checkbox = request.POST.get(f'cliente_{cliente.id}')
            cliente.pagamento = pagamento_checkbox == 'on'
            cliente.save()

    for cliente in clientes:
        pedidos_cliente = Pedido.objects.filter(cliente=cliente)
        cliente.total_pedido = sum(pedido.total_item() for pedido in pedidos_cliente)

    return render(request, 'listar_clientes.html', {'clientes': clientes})

def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/produtos/')
    else:
        form = ProdutoForm()

    return render(request, 'cadastrar_produto.html', {'form': form})

def associar_produto(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)

    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        produto = get_object_or_404(Produto, pk=produto_id)
        quantidade = int(request.POST.get('quantidade', 1))

        pedido, created = Pedido.objects.get_or_create(cliente=cliente, produto=produto)
        if not created:
            pedido.quantidade += quantidade
            pedido.save()

    pedidos_cliente = Pedido.objects.filter(cliente=cliente)
    total_pedido_cliente = sum(pedido.total_item() for pedido in pedidos_cliente)

    produtos = Produto.objects.all()
    return render(request, 'associar_produto.html', {'cliente': cliente, 'produtos': produtos, 'pedidos_cliente': pedidos_cliente, 'total_pedido_cliente': total_pedido_cliente})

def marcar_pagamento(request):
    # Redirecione para a página de listar_clientes após marcar os pagamentos
    return redirect('listar_clientes')

def listar_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'listar_produtos.html', {'produtos': produtos})