from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from .models import Cliente, Fornecedor, Produto, Venda
from django.views.decorators.csrf import csrf_exempt
import json

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'core/login.html', {'error': 'Usuário ou senha inválidos'})
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def index(request):
    return render(request, 'core/index.html')

@login_required
@csrf_exempt
def api_clientes(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente = Cliente.objects.create(
                nome=data['nome'],
                telefone=data.get('telefone', ''),
                email=data.get('email', ''),
                cpf=data.get('cpf', ''),
                observacoes=data.get('observacoes', '')
            )
            return JsonResponse({'id': cliente.id, 'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'GET':
        try:
            clientes = list(Cliente.objects.values().order_by('-data_cadastro'))
            return JsonResponse(clientes, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@login_required
@csrf_exempt
def api_fornecedores(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            fornecedor = Fornecedor.objects.create(
                nome=data['nome'],
                contato=data.get('contato', ''),
                telefone=data.get('telefone', ''),
                email=data.get('email', ''),
                cnpj=data.get('cnpj', ''),
                observacoes=data.get('observacoes', '')
            )
            return JsonResponse({'id': fornecedor.id, 'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'GET':
        try:
            fornecedores = list(Fornecedor.objects.values().order_by('-data_cadastro'))
            return JsonResponse(fornecedores, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@login_required
@csrf_exempt
def api_produtos(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            produto = Produto.objects.create(
                nome=data['nome'],
                categoria=data.get('categoria', ''),
                tamanho=data.get('tamanho', ''),
                cor=data.get('cor', ''),
                quantidade=data.get('quantidade', 0),
                custo_unitario=data.get('custo_unitario', 0),
                preco_venda=data.get('preco_venda', 0),
                descricao=data.get('descricao', '')
            )
            return JsonResponse({'id': produto.id, 'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'GET':
        try:
            produtos = list(Produto.objects.values().order_by('-data_cadastro'))
            return JsonResponse(produtos, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@login_required
@csrf_exempt
def api_vendas(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            produto = Produto.objects.get(id=data['produto_id'])
            
            # Verificar se há estoque suficiente
            if produto.quantidade < data['quantidade']:
                return JsonResponse({'error': 'Estoque insuficiente'}, status=400)
            
            # Atualiza estoque
            produto.quantidade -= data['quantidade']
            produto.save()
            
            venda = Venda.objects.create(
                produto=produto,
                quantidade=data['quantidade'],
                preco_unitario=data['preco_unitario'],
                custo_unitario=produto.custo_unitario
            )
            return JsonResponse({'id': venda.id, 'success': True})
        except Produto.DoesNotExist:
            return JsonResponse({'error': 'Produto não encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'GET':
        try:
            vendas = list(Venda.objects.values(
                'id', 
                'produto__nome', 
                'quantidade', 
                'preco_unitario', 
                'custo_unitario', 
                'data_venda'
            ).order_by('-data_venda'))
            return JsonResponse(vendas, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@login_required
def api_dashboard(request):
    try:
        total_clientes = Cliente.objects.count()
        total_fornecedores = Fornecedor.objects.count()
        
        # Calcular valor do estoque
        produtos = Produto.objects.all()
        valor_estoque = sum(p.quantidade * p.custo_unitario for p in produtos)
        
        # Calcular vendas totais
        vendas = Venda.objects.all()
        total_vendido = sum(v.quantidade * v.preco_unitario for v in vendas)
        total_custo_vendas = sum(v.quantidade * v.custo_unitario for v in vendas)
        lucro_total = total_vendido - total_custo_vendas
        
        return JsonResponse({
            'total_clientes': total_clientes,
            'total_fornecedores': total_fornecedores,
            'valor_estoque': float(valor_estoque),
            'total_vendido': float(total_vendido),
            'lucro_total': float(lucro_total)
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)