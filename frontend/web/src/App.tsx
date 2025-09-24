import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import { useContext, useEffect, useMemo, useState } from 'react';
import api from './lib/api';
import './index.css';
import Layout from './components/Layout';
import Farms from './pages/Farms';
import Crops from './pages/Crops';
import Payments from './pages/Payments';
import Notifications from './pages/Notifications';
import Subscriptions from './pages/Subscriptions';
import { AuthCtx, AuthState } from './context';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

function useAuth() { return useContext(AuthCtx); }

function Protected({ children }: { children: JSX.Element }) {
	const { state } = useAuth();
	if (state.loading) return <div className="p-8">Loading...</div>;
	return state.user ? children : <Navigate to="/login" replace />;
}

function Login() {
	const nav = useNavigate();
	const { setState } = useAuth();
	const [username, setUsername] = useState('');
	const [password, setPassword] = useState('');
	const [err, setErr] = useState('');
	const submit = async (e: any) => {
		e.preventDefault();
		try {
			const r = await api.post('/api/auth/token/', { username, password });
			localStorage.setItem('access', r.data.access);
			localStorage.setItem('refresh', r.data.refresh);
			const me = await api.get('/api/auth/me/');
			setState({ user: me.data, loading: false });
			nav('/');
		} catch (e: any) {
			setErr(e?.response?.data?.detail || 'Login failed');
		}
	};
	return (
		<div className="min-h-screen flex items-center justify-center bg-gray-50">
			<form onSubmit={submit} className="bg-white p-6 rounded shadow w-full max-w-sm space-y-3">
				<h1 className="text-xl font-semibold">Login</h1>
				{err && <div className="text-red-600 text-sm">{err}</div>}
				<input className="w-full border px-3 py-2 rounded" placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)} />
				<input className="w-full border px-3 py-2 rounded" placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
				<button className="w-full bg-green-600 text-white py-2 rounded">Sign in</button>
			</form>
		</div>
	);
}

function Dashboard() {
	const { state } = useAuth();
    const [revenue, setRevenue] = useState<any>(null);
    const [range, setRange] = useState<'6m'|'1y'|'all'>('6m');
    const [series, setSeries] = useState<{date: string; captured: number; refunded: number}[]>([]);

    const load = async () => {
        const now = new Date();
        let start = '';
        if (range === '6m') { const d = new Date(now); d.setMonth(d.getMonth()-6); start = d.toISOString().slice(0,10); }
        if (range === '1y') { const d = new Date(now); d.setFullYear(d.getFullYear()-1); start = d.toISOString().slice(0,10); }
        const r = await api.get('/api/analytics/revenue', { params: start ? { start } : {} });
        setRevenue(r.data);
        // fake simple series from totals for visualization (backend can be extended later)
        setSeries([
            { date: 'Start', captured: r.data.captured || 0, refunded: r.data.refunded || 0 },
            { date: 'Now', captured: r.data.captured || 0, refunded: r.data.refunded || 0 },
        ]);
    };

    useEffect(() => { load(); }, [range]);
	return (
		<Layout>
			<div className="p-0 space-y-4">
				<h1 className="text-2xl font-bold">Welcome, {state.user?.username}</h1>
				<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
					<div className="p-4 bg-white rounded shadow">
						<div className="text-gray-500">Revenue (captured)</div>
						<div className="text-2xl font-semibold">₹ {revenue?.captured ?? 0}</div>
					</div>
					<div className="p-4 bg-white rounded shadow">
						<div className="text-gray-500">Refunded</div>
						<div className="text-2xl font-semibold">₹ {revenue?.refunded ?? 0}</div>
					</div>
				</div>
                <div className="bg-white rounded shadow p-4">
                    <div className="flex items-center justify-between mb-2">
                        <div className="font-semibold">Revenue Trend</div>
                        <div className="flex gap-2">
                            <button className={`px-3 py-1 border rounded ${range==='6m'?'bg-gray-100':''}`} onClick={()=>setRange('6m')}>6 months</button>
                            <button className={`px-3 py-1 border rounded ${range==='1y'?'bg-gray-100':''}`} onClick={()=>setRange('1y')}>1 year</button>
                            <button className={`px-3 py-1 border rounded ${range==='all'?'bg-gray-100':''}`} onClick={()=>setRange('all')}>All</button>
                        </div>
                    </div>
                    <div style={{ width: '100%', height: 240 }}>
                        <ResponsiveContainer>
                            <LineChart data={series}>
                                <XAxis dataKey="date" />
                                <YAxis />
                                <Tooltip />
                                <Line type="monotone" dataKey="captured" stroke="#16a34a" />
                                <Line type="monotone" dataKey="refunded" stroke="#ef4444" />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>
			</div>
		</Layout>
	);
}

function FarmsPage() { return <Layout><Farms /></Layout>; }
function CropsPage() { return <Layout><Crops /></Layout>; }
function PaymentsPage() { return <Layout><Payments /></Layout>; }
function NotificationsPage() { return <Layout><Notifications /></Layout>; }
function SubscriptionsPage() { return <Layout><Subscriptions /></Layout>; }

function Root() {
	const [state, setState] = useState<AuthState>({ user: null, loading: true });
	useEffect(() => { (async () => {
		try { const me = await api.get('/api/auth/me/'); setState({ user: me.data, loading: false }); }
		catch { setState({ user: null, loading: false }); }
	})(); }, []);
	const ctx = useMemo(() => ({ state, setState }), [state]);
	return (
		<AuthCtx.Provider value={ctx}>
			<Routes>
				<Route path="/login" element={<Login />} />
				<Route path="/" element={<Protected><Dashboard /></Protected>} />
				<Route path="/farms" element={<Protected><FarmsPage /></Protected>} />
				<Route path="/crops" element={<Protected><CropsPage /></Protected>} />
				<Route path="/payments" element={<Protected><PaymentsPage /></Protected>} />
				<Route path="/notifications" element={<Protected><NotificationsPage /></Protected>} />
                <Route path="/subscriptions" element={<Protected><SubscriptionsPage /></Protected>} />
			</Routes>
		</AuthCtx.Provider>
	);
}

export default function App() {
	return (
		<BrowserRouter>
			<Root />
		</BrowserRouter>
	);
}
