# comanda_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Cliente, Produto, Pedido
from .forms import ClienteForm, ProdutoForm
from django.contrib import messages
from django.db.models import Sum



def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

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

    for cliente in clientes:
        pedidos_cliente = cliente.pedido_set.values('produto__nome').annotate(total=Sum('quantidade'))
        cliente.itens_quantidades = pedidos_cliente
        cliente.total_pedido = sum(pedido_quantity['total'] * Pedido.objects.filter(cliente=cliente, produto__nome=pedido_quantity['produto__nome']).first().produto.preco for pedido_quantity in pedidos_cliente)


    return render(request, 'listar_clientes.html', {'clientes': clientes})

def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, ('Produto adicionado'))
            return redirect('listar_produtos')
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


def listar_produtos(request):
    produtos = Produto.objects.all()
    clientes = Cliente.objects.all()

    if request.method == 'POST':
        produto_id = request.POST.get('produto_id')
        cliente_id = request.POST.get('cliente')

        produto = Produto.objects.get(id=produto_id)
        cliente = Cliente.objects.get(id=cliente_id)

        # Crie um novo pedido associando o produto ao cliente
        Pedido.objects.create(produto=produto, cliente=cliente, quantidade=1)
        messages.success(request, ('Item adicionado a comanda de: '+ str(cliente.nome)))

        # Redirecione para a mesma página após associar o produto ao cliente
        return redirect('listar_produtos')

    return render(request, 'listar_produtos.html', {'produtos': produtos, 'clientes': clientes})


def delete(request, cliente_id):
    cliente = Cliente.objects.get(pk=cliente_id)
    cliente.delete()
    messages.success(request, ('Item removido da sua lista!'))
    return redirect('home')

def comanda_individual(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    # Agrupe os pedidos pelo produto e calcule a quantidade total para cada produto
    pedidos_agrupados = cliente.pedido_set.values('produto__nome').annotate(quantidade_total=Sum('quantidade'))

    return render(request, 'comanda_individual.html', {'cliente': cliente, 'pedidos_agrupados': pedidos_agrupados})