import { Link, NavLink } from 'react-router-dom';
import { useContext } from 'react';
import { AuthCtx } from '../context';

export default function Layout({ children }: { children: any }) {
	const { state, setState } = useContext(AuthCtx);
	const logout = () => {
		localStorage.removeItem('access');
		localStorage.removeItem('refresh');
		setState({ user: null, loading: false });
	};
	return (
		<div className="min-h-screen bg-gray-100 flex">
			<aside className="w-64 bg-white shadow">
				<div className="p-4 font-bold text-lg">Agri Platform</div>
				<nav className="space-y-1 px-2">
					<NavLink to="/" end className={({isActive})=>`block px-3 py-2 rounded ${isActive? 'bg-green-600 text-white':'hover:bg-gray-100'}`}>Dashboard</NavLink>
					<NavLink to="/farms" className={({isActive})=>`block px-3 py-2 rounded ${isActive? 'bg-green-600 text-white':'hover:bg-gray-100'}`}>Farms</NavLink>
					<NavLink to="/crops" className={({isActive})=>`block px-3 py-2 rounded ${isActive? 'bg-green-600 text-white':'hover:bg-gray-100'}`}>Crops</NavLink>
					<NavLink to="/payments" className={({isActive})=>`block px-3 py-2 rounded ${isActive? 'bg-green-600 text-white':'hover:bg-gray-100'}`}>Payments</NavLink>
					<NavLink to="/subscriptions" className={({isActive})=>`block px-3 py-2 rounded ${isActive? 'bg-green-600 text-white':'hover:bg-gray-100'}`}>Subscriptions</NavLink>
					<NavLink to="/notifications" className={({isActive})=>`block px-3 py-2 rounded ${isActive? 'bg-green-600 text-white':'hover:bg-gray-100'}`}>Notifications</NavLink>
					<a className="block px-3 py-2 rounded hover:bg-gray-100" href={`${import.meta.env.VITE_API_BASE || 'http://localhost:8000'}/api/reports/export/soil`} target="_blank">Download Soil CSV</a>
					<a className="block px-3 py-2 rounded hover:bg-gray-100" href={`${import.meta.env.VITE_API_BASE || 'http://localhost:8000'}/api/reports/export/crops`} target="_blank">Download Crops CSV</a>
				</nav>
			</aside>
			<main className="flex-1">
				<header className="bg-white shadow px-6 py-3 flex items-center justify-between">
					<div/>
					<div className="flex items-center gap-3">
						<span className="text-gray-600">{state.user?.username}</span>
						<button onClick={logout} className="px-3 py-1 border rounded">Logout</button>
					</div>
				</header>
				<div className="p-6">{children}</div>
			</main>
		</div>
	);
}

