import { BrowserRouter, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import OperationPage from './pages/OperationPage'
import MainPage from './pages/MainPage';

const backend_base = 'http://localhost:8000/';
function App() {

  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MainPage backend_base={backend_base} />} />
          <Route path="/:wallet_id/operation" element={<OperationPage backend_base={backend_base} />} />
          <Route path="/login" element={<LoginPage backend_base={backend_base} />} />
          <Route path="/register" element={<RegisterPage backend_base={backend_base} />} />
        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App
