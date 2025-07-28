import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';


export default function LoginPage({ backend_base }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async () => {
        try {
            const response = await axios.post(`${backend_base}/auth/token/`, {
                username, password
            });
            localStorage.setItem('access', response.data.access);
            localStorage.setItem('refresh', response.data.refresh);
            navigate('/');
        } catch (error) {
            alert('Неправильные данные')
        }
    };
    
    return (
        <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md ml-auto mr-auto mt-60">
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold text-gray-800">Авторизация</h1>
        <p className="text-gray-600">Пожалуйста, введите данные для авторизации</p>
      </div>

        <div className="space-y-6">
          <label
            htmlFor="email"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Имя пользователя
          </label>
          <input
            value={username} 
            onChange={e => setUsername(e.target.value)}
            placeholder="Имя пользователя"
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div className='mt-2'>
          <label
            htmlFor="password"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Пароль
          </label>
          <input
            type="password"
            placeholder="••••••••"
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            required=""
            value={password} 
            onChange={e => setPassword(e.target.value)}
          />
        </div>
        <div>
          <button
            onClick={handleLogin}
            className="w-full bg-blue-600 text-white mt-5 py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition duration-150"
          >
            Войти
          </button>
        </div>
      <div className="mt-6">
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-gray-500">Или если нет аккаунта</span>
          </div>
        </div>
        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            <a href="/register" className="font-medium text-blue-600 hover:text-blue-500">
              Зарегестрируйтесь
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}
