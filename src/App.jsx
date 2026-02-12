import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, Navigate } from 'react-router-dom';
import axios from 'axios';
import { 
  FaShoppingCart, FaHome, FaChartLine, FaBoxes, 
  FaUsers, FaDollarSign, FaCog, FaSignInAlt, FaSignOutAlt 
} from 'react-icons/fa';
import './index.css';

// Configuração do Axios
const api = axios.create({
  baseURL: 'http://localhost:5000/api'
});

// Interceptor para adicionar token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Context de Autenticação
const AuthContext = React.createContext();

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      api.get('/auth/me')
        .then(res => setUser(res.data))
        .catch(() => localStorage.removeItem('token'))
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (email, senha) => {
    const res = await api.post('/auth/login', { email, senha });
    localStorage.setItem('token', res.data.access_token);
    setUser(res.data.usuario);
    return res.data;
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

// Hook personalizado
const useAuth = () => React.useContext(AuthContext);

// Componente de Login
function Login() {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [erro, setErro] = useState('');
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErro('');
    setLoading(true);
    
    try {
      await login(email, senha);
    } catch (err) {
      setErro(err.response?.data?.erro || 'Erro ao fazer login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-pink-100 to-blue-100">
      <div className="card max-w-md w-full">
        <h2 className="text-3xl font-bold text-center mb-6 text-primary-600">
          Loja de Roupas Infantis
        </h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          {erro && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {erro}
            </div>
          )}
          
          <div>
            <label className="block text-sm font-medium mb-2">Email</label>
            <input
              type="email"
              className="input-field"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-2">Senha</label>
            <input
              type="password"
              className="input-field"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              required
            />
          </div>
          
          <button 
            type="submit" 
            className="btn-primary w-full"
            disabled={loading}
          >
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>
        
        <p className="mt-4 text-center text-sm text-gray-600">
          Usuário demo: admin@loja.com / senha: admin123
        </p>
      </div>
    </div>
  );
}

// Header do E-commerce
function EcommerceHeader({ cartCount }) {
  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold text-primary-600">
            👶 Baby Fashion
          </Link>
          
          <nav className="flex items-center space-x-6">
            <Link to="/" className="hover:text-primary-600">Início</Link>
            <Link to="/produtos" className="hover:text-primary-600">Produtos</Link>
            <Link to="/admin" className="hover:text-primary-600">Administração</Link>
            <Link to="/carrinho" className="relative">
              <FaShoppingCart className="text-2xl" />
              {cartCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs">
                  {cartCount}
                </span>
              )}
            </Link>
          </nav>
        </div>
      </div>
    </header>
  );
}

// Página Inicial E-commerce
function Home() {
  return (
    <div>
      <section className="bg-gradient-to-r from-pink-300 to-blue-300 py-20">
        <div className="container mx-auto px-4 text-center text-white">
          <h1 className="text-5xl font-bold mb-4">Roupas Infantis com Amor</h1>
          <p className="text-xl mb-8">Qualidade e conforto para seu bebê</p>
          <Link to="/produtos" className="btn-primary text-lg">
            Ver Produtos
          </Link>
        </div>
      </section>
      
      <section className="container mx-auto px-4 py-12">
        <h2 className="text-3xl font-bold mb-8 text-center">Categorias</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <CategoryCard icon="👕" title="Roupinhas" />
          <CategoryCard icon="👟" title="Calçados" />
          <CategoryCard icon="🧸" title="Acessórios" />
        </div>
      </section>
    </div>
  );
}

function CategoryCard({ icon, title }) {
  return (
    <div className="card text-center hover:shadow-lg transition-shadow cursor-pointer">
      <div className="text-6xl mb-4">{icon}</div>
      <h3 className="text-xl font-semibold">{title}</h3>
    </div>
  );
}

// Página de Produtos
function Produtos() {
  const [produtos, setProdutos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/produtos')
      .then(res => setProdutos(res.data.produtos))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="text-center py-12">Carregando...</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Nossos Produtos</h1>
      
      <div className="grid md:grid-cols-3 lg:grid-cols-4 gap-6">
        {produtos.map(produto => (
          <ProdutoCard key={produto.id} produto={produto} />
        ))}
      </div>
      
      {produtos.length === 0 && (
        <p className="text-center text-gray-500 py-12">
          Nenhum produto cadastrado ainda.
        </p>
      )}
    </div>
  );
}

function ProdutoCard({ produto }) {
  return (
    <div className="card hover:shadow-xl transition-shadow">
      <div className="bg-gray-200 h-48 rounded-lg mb-4 flex items-center justify-center">
        {produto.imagem ? (
          <img src={produto.imagem} alt={produto.nome} className="h-full object-cover rounded-lg" />
        ) : (
          <span className="text-6xl">👶</span>
        )}
      </div>
      
      <h3 className="font-semibold text-lg mb-2">{produto.nome}</h3>
      <p className="text-gray-600 text-sm mb-3 line-clamp-2">{produto.descricao}</p>
      
      <div className="flex justify-between items-center">
        <span className="text-2xl font-bold text-primary-600">
          R$ {produto.preco_venda.toFixed(2)}
        </span>
        <button className="btn-primary text-sm">
          <FaShoppingCart className="inline mr-1" /> Comprar
        </button>
      </div>
    </div>
  );
}

// Sidebar do Admin
function AdminSidebar() {
  const { logout } = useAuth();
  
  const menuItems = [
    { icon: <FaChartLine />, label: 'Dashboard', path: '/admin' },
    { icon: <FaBoxes />, label: 'Produtos', path: '/admin/produtos' },
    { icon: <FaShoppingCart />, label: 'Vendas', path: '/admin/vendas' },
    { icon: <FaUsers />, label: 'Clientes', path: '/admin/clientes' },
    { icon: <FaDollarSign />, label: 'Financeiro', path: '/admin/financeiro' },
  ];

  return (
    <div className="w-64 bg-gray-800 text-white min-h-screen p-4">
      <h2 className="text-2xl font-bold mb-8">ERP Admin</h2>
      
      <nav className="space-y-2">
        {menuItems.map((item, idx) => (
          <Link
            key={idx}
            to={item.path}
            className="flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-gray-700 transition-colors"
          >
            {item.icon}
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>
      
      <button
        onClick={logout}
        className="flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-gray-700 transition-colors w-full mt-8"
      >
        <FaSignOutAlt />
        <span>Sair</span>
      </button>
    </div>
  );
}

// Dashboard Admin com BI
function Dashboard() {
  const [dados, setDados] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get('/dashboard/resumo')
      .then(res => setDados(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div>Carregando...</div>;

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <MetricCard
          title="Vendas do Mês"
          value={`R$ ${dados?.vendas_mes?.toFixed(2) || '0.00'}`}
          change={`${dados?.crescimento_percentual || 0}%`}
          positive={dados?.crescimento_percentual > 0}
        />
        <MetricCard
          title="Nº de Vendas"
          value={dados?.numero_vendas || 0}
        />
        <MetricCard
          title="Ticket Médio"
          value={`R$ ${dados?.ticket_medio?.toFixed(2) || '0.00'}`}
        />
        <MetricCard
          title="Alertas Estoque"
          value={dados?.alertas_estoque || 0}
          isAlert={dados?.alertas_estoque > 0}
        />
      </div>
      
      <div className="grid md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-xl font-semibold mb-4">Produtos Ativos</h3>
          <p className="text-4xl font-bold text-primary-600">{dados?.produtos_ativos || 0}</p>
        </div>
        
        <div className="card">
          <h3 className="text-xl font-semibold mb-4">Total de Clientes</h3>
          <p className="text-4xl font-bold text-primary-600">{dados?.total_clientes || 0}</p>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ title, value, change, positive, isAlert }) {
  return (
    <div className={`card ${isAlert ? 'border-2 border-red-500' : ''}`}>
      <h3 className="text-gray-600 text-sm mb-2">{title}</h3>
      <p className="text-3xl font-bold mb-1">{value}</p>
      {change && (
        <span className={`text-sm ${positive ? 'text-green-600' : 'text-red-600'}`}>
          {positive ? '↑' : '↓'} {change}
        </span>
      )}
    </div>
  );
}

// Layout Admin
function AdminLayout() {
  return (
    <div className="flex">
      <AdminSidebar />
      <div className="flex-1 bg-gray-50">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/produtos" element={<AdminProdutos />} />
          <Route path="/vendas" element={<AdminVendas />} />
          <Route path="/clientes" element={<AdminClientes />} />
          <Route path="/financeiro" element={<AdminFinanceiro />} />
        </Routes>
      </div>
    </div>
  );
}

// Páginas Admin simplificadas
function AdminProdutos() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Gestão de Produtos</h1>
      <div className="card">
        <p>Módulo de gestão de produtos em desenvolvimento...</p>
      </div>
    </div>
  );
}

function AdminVendas() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Gestão de Vendas</h1>
      <div className="card">
        <p>Módulo de vendas em desenvolvimento...</p>
      </div>
    </div>
  );
}

function AdminClientes() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Gestão de Clientes</h1>
      <div className="card">
        <p>Módulo de clientes em desenvolvimento...</p>
      </div>
    </div>
  );
}

function AdminFinanceiro() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Gestão Financeira</h1>
      <div className="card">
        <p>Módulo financeiro em desenvolvimento...</p>
      </div>
    </div>
  );
}

// Rota Protegida
function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  
  if (loading) return <div>Carregando...</div>;
  
  return user ? children : <Navigate to="/login" />;
}

// App Principal
function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          
          <Route
            path="/*"
            element={
              <div>
                <EcommerceHeader cartCount={0} />
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/produtos" element={<Produtos />} />
                </Routes>
              </div>
            }
          />
          
          <Route
            path="/admin/*"
            element={
              <ProtectedRoute>
                <AdminLayout />
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
