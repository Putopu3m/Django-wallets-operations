import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function OperationPage({ backend_base }) {
	const [forecast, setForecast] = useState(null);
	const [recents, setRecents] = useState([]);
	const [query, setQuery] = useState('');
	const navigate = useNavigate();

	const handleLogout = () => {
		localStorage.removeItem('access');
		localStorage.removeItem('refresh');
		navigate('/');
	}

	const handleLogin = () => {
		navigate('/login');
	}

	const handleRefresh = async () => {
		const response = await axios.post(`${backend_base}auth/token/refresh/`, {
			'refresh': localStorage.getItem('refresh')
		});
		localStorage.setItem('access', response.data.access);
		window.location.reload(); 
	}

	useEffect(() => {
		if (!localStorage.getItem('access')){
			handleRefresh();
		}
	}, [])

	return <>
		<div className="w-[500px] ml-120 mt-30 px-4 py-5 bg-white flex flex-col gap-3 rounded-md shadow-[0px_0px_15px_rgba(0,0,0,0.09)]">
      <legend className="text-xl font-semibold mb-3 select-none">Выберите операцию</legend>
      <label htmlFor="html" name="status" className="font-medium h-14 relative hover:bg-zinc-100 flex items-center px-3 gap-3 rounded-lg has-[:checked]:text-blue-500 has-[:checked]:bg-blue-50 has-[:checked]:ring-blue-300 has-[:checked]:ring-1 select-none">
        <div className="w-5 fill-blue-500">
         	<svg xmlns="http://www.w3.org/2000/svg" id="Layer_1" data-name="Layer 1" viewBox="0 0 24 24">
  				<path d="M18.5,14.5c.828,0,1.5,.672,1.5,1.5s-.672,1.5-1.5,1.5-1.5-.672-1.5-1.5,.672-1.5,1.5-1.5Zm4.5-4.5c-.553,0-1,.448-1,1v10c0,.552-.448,1-1,1H5c-1.654,0-3-1.346-3-3V9s0-.004,0-.005c.854,.64,1.903,1.005,2.999,1.005H13c.553,0,1-.448,1-1s-.447-1-1-1H5c-.856,0-1.653-.381-2.217-1.004,.549-.607,1.335-.996,2.217-.996h7c.553,0,1-.448,1-1s-.447-1-1-1H5C2.224,3.994,.02,6.304,0,9v10c0,2.757,2.243,5,5,5H21c1.654,0,3-1.346,3-3V11c0-.552-.447-1-1-1Zm-5.503-.615c.815,.815,2.148,.822,2.964,.009l2.236-2.177c.396-.385,.404-1.018,.02-1.414-.387-.396-1.02-.405-1.414-.019l-1.303,1.268V1c0-.552-.447-1-1-1s-1,.448-1,1V7.07l-1.297-1.281c-.394-.388-1.025-.385-1.415,.009-.388,.393-.384,1.026,.009,1.414l2.2,2.173Z"/>
			</svg>
        </div>
        Внести
        <input defaultChecked type="radio" name="status" className="peer/html w-4 h-4 absolute accent-current right-3" id="html" />
      </label>
      <label htmlFor="css" className="font-medium h-14 relative hover:bg-zinc-100 flex items-center px-3 gap-3 rounded-lg has-[:checked]:text-blue-500 has-[:checked]:bg-blue-50 has-[:checked]:ring-blue-300 has-[:checked]:ring-1 select-none">
        <div className="w-5">
          	<svg xmlns="http://www.w3.org/2000/svg" id="Layer_1" data-name="Layer 1" viewBox="0 0 24 24">
  				<path d="m20,16c0,.828-.672,1.5-1.5,1.5s-1.5-.672-1.5-1.5.672-1.5,1.5-1.5,1.5.672,1.5,1.5Zm3-8c-.553,0-1,.448-1,1v12c0,.551-.448,1-1,1H5c-1.654,0-3-1.346-3-3v-10s0-.004,0-.005c.854.64,1.903,1.005,2.999,1.005h10c.553,0,1-.448,1-1s-.447-1-1-1H5c-.856,0-1.653-.381-2.217-1.004.549-.607,1.335-.996,2.217-.996h7c.553,0,1-.448,1-1s-.447-1-1-1h-7c-3,0-5,2.5-5,5v10c0,2.757,2.243,5,5,5h16c1.654,0,3-1.346,3-3v-12c0-.552-.447-1-1-1Zm-6.297-3.789l1.297-1.281v6.07c0,.552.447,1,1,1s1-.448,1-1V2.948l1.303,1.268c.194.189.445.284.697.284.261,0,.521-.101.717-.302.385-.396.377-1.029-.02-1.414l-2.227-2.168c-.821-.819-2.152-.818-2.97-.004l-2.204,2.177c-.393.388-.396,1.021-.009,1.414.39.394,1.021.396,1.415.009Z"/>
			</svg>
        </div>
        Снять
        <input type="radio" name="status" className="w-4 h-4 absolute accent-current right-3" id="css" />
      </label>
    </div>
	

	<div className="bg-white w-[500px] ml-120 mt-5 border border-slate-200 grid grid-cols-6 gap-2 rounded-xl p-2 text-sm">
      <h1 className="  text-xl font-bold col-span-6">Введите сумму</h1>
      <textarea placeholder="Введите сумму" className="bg-slate-100 text-slate-600 h-10 placeholder:text-slate-600 placeholder:opacity-50 border border-slate-200 col-span-6 resize-none outline-none rounded-lg p-2 duration-300 focus:border-slate-600" defaultValue={""} />
      <button className="col-span-3 w-45 my-2 cursor-pointer group relative flex gap-1.5 px-8 py-4 bg-blue-50 bg-opacity-80 text-black rounded-xl hover:bg-opacity-70 transition font-semibold shadow-md">
      <svg className='w-5' xmlns="http://www.w3.org/2000/svg" id="Layer_1" data-name="Layer 1" viewBox="0 0 24 24">
  <path d="m24,12c0,6.617-5.383,12-12,12S0,18.617,0,12,5.383,0,12,0c.553,0,1,.447,1,1s-.447,1-1,1C6.486,2,2,6.486,2,12s4.486,10,10,10,10-4.486,10-10c0-.553.447-1,1-1s1,.447,1,1ZM22,0h-4c-.553,0-1,.447-1,1s.447,1,1,1h2.586l-3.293,3.293c-.391.391-.391,1.023,0,1.414.195.195.451.293.707.293s.512-.098.707-.293l3.293-3.293v2.586c0,.553.447,1,1,1s1-.447,1-1V2c0-1.103-.897-2-2-2Zm-9,6c0-.553-.447-1-1-1s-1,.447-1,1v1c-1.654,0-3,1.346-3,3,0,1.359.974,2.51,2.315,2.733l3.04.506c.374.062.645.382.645.761,0,.552-.448,1-1,1h-2.268c-.356,0-.688-.191-.867-.501-.276-.479-.887-.643-1.366-.364-.478.276-.642.888-.364,1.366.534.925,1.53,1.499,2.598,1.499h.268v1c0,.553.447,1,1,1s1-.447,1-1v-1c1.654,0,3-1.346,3-3,0-1.359-.974-2.51-2.315-2.733l-3.04-.506c-.374-.062-.645-.382-.645-.761,0-.552.448-1,1-1h2.268c.356,0,.688.191.867.501.275.478.886.642,1.366.364.478-.276.642-.888.364-1.366-.534-.925-1.53-1.499-2.598-1.499h-.268v-1Z"/>
</svg>
      Выполнить
    </button>
    </div>
	</>
}