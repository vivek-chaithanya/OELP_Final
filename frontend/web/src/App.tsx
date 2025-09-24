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
    const roleName = state.user?.role?.name || 'User';
    const [revenue, setRevenue] = useState<any>(null);
    const [activeUsers, setActiveUsers] = useState<number | null>(null);
    const [counts, setCounts] = useState<{ farms: number; fields: number; crops: number; soil: number; notifications: number; plans: number; payments: number }>({ farms: 0, fields: 0, crops: 0, soil: 0, notifications: 0, plans: 0, payments: 0 });
    const [range, setRange] = useState<'6m'|'1y'|'all'>('6m');
    const [series, setSeries] = useState<{date: string; captured: number; refunded: number}[]>([]);

    const load = async () => {
        const now = new Date();
        let start = '';
        if (range === '6m') { const d = new Date(now); d.setMonth(d.getMonth()-6); start = d.toISOString().slice(0,10); }
        if (range === '1y') { const d = new Date(now); d.setFullYear(d.getFullYear()-1); start = d.toISOString().slice(0,10); }

        const reqs: Promise<any>[] = [
            api.get('/api/analytics/revenue', { params: start ? { start } : {} }),
            api.get('/api/farms/'),
            api.get('/api/fields/'),
            api.get('/api/crops/'),
            api.get('/api/soil-reports/'),
            api.get('/api/notifications/'),
            api.get('/api/user/plans/'),
        ];
        if (roleName === 'SuperAdmin' || roleName === 'Admin') {
            reqs.push(api.get('/api/analytics/active-users'));
        }
        // For payments count, reuse revenue range; as a fallback count all payments via payments history if available later.
        // We will approximate by treating any revenue response as at least one payment

        const results = await Promise.allSettled(reqs);
        const revRes = results[0].status === 'fulfilled' ? (results[0] as any).value.data : { captured: 0, refunded: 0 };
        setRevenue(revRes);
        setSeries([
            { date: 'Start', captured: revRes.captured || 0, refunded: revRes.refunded || 0 },
            { date: 'Now', captured: revRes.captured || 0, refunded: revRes.refunded || 0 },
        ]);

        const safeLen = (idx: number) => results[idx] && results[idx].status === 'fulfilled' ? ((results[idx] as any).value.data.length || 0) : 0;
        const farms = safeLen(1);
        const fields = safeLen(2);
        const crops = safeLen(3);
        const soil = safeLen(4);
        const notifications = safeLen(5);
        const plans = safeLen(6);
        const payments = (revRes.captured || 0) > 0 || (revRes.refunded || 0) > 0 ? 1 : 0;
        setCounts({ farms, fields, crops, soil, notifications, plans, payments });

        if (roleName === 'SuperAdmin' || roleName === 'Admin') {
            const auIdx = 7; // last in array if pushed
            if (results[auIdx] && results[auIdx].status === 'fulfilled') {
                setActiveUsers((results[auIdx] as any).value.data.active_users || 0);
            } else {
                setActiveUsers(0);
            }
        } else {
            setActiveUsers(null);
        }
    };

    useEffect(() => { load(); }, [range]);

    const Card = ({ title, value, accent }: { title: string; value: any; accent?: string }) => (
        <div className={`p-4 bg-white rounded shadow border-t-4 ${accent || 'border-green-600'}`}>
            <div className="text-gray-500">{title}</div>
            <div className="text-2xl font-semibold">{value}</div>
        </div>
    );

    return (
        <Layout>
            <div className="p-0 space-y-4">
                <h1 className="text-2xl font-bold">Welcome, {state.user?.username}</h1>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {(roleName === 'SuperAdmin' || roleName === 'Admin' || roleName === 'Business' || roleName === 'Analyst') && (
                        <Card title="Revenue (captured)" value={`₹ ${revenue?.captured ?? 0}`} accent="border-green-600" />
                    )}
                    {(roleName === 'SuperAdmin' || roleName === 'Admin' || roleName === 'Business') && (
                        <Card title="Refunded" value={`₹ ${revenue?.refunded ?? 0}`} accent="border-red-500" />
                    )}
                    {(roleName === 'SuperAdmin' || roleName === 'Admin') && (
                        <Card title="Active Users" value={activeUsers ?? 0} accent="border-blue-600" />
                    )}
                    {(roleName === 'User' || roleName === 'Admin' || roleName === 'SuperAdmin') && (
                        <Card title="Farms" value={counts.farms} accent="border-amber-500" />
                    )}
                    {(roleName === 'Agronomist' || roleName === 'User' || roleName === 'Admin' || roleName === 'SuperAdmin') && (
                        <Card title="Soil Reports" value={counts.soil} accent="border-emerald-600" />
                    )}
                    {(roleName === 'User' || roleName === 'Agronomist' || roleName === 'Admin' || roleName === 'SuperAdmin') && (
                        <Card title="Crops" value={counts.crops} accent="border-indigo-600" />
                    )}
                    {(roleName === 'Business') && (
                        <Card title="Active Plans" value={counts.plans} accent="border-fuchsia-600" />
                    )}
                    {(roleName === 'Support') && (
                        <Card title="Notifications (assigned/sent)" value={counts.notifications} accent="border-cyan-600" />
                    )}
                    {(roleName === 'Development') && (
                        <Card title="Entities (total)" value={counts.farms + counts.fields + counts.crops} accent="border-slate-600" />
                    )}
                </div>

                {(roleName === 'SuperAdmin' || roleName === 'Admin' || roleName === 'Business' || roleName === 'Analyst') && (
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
                )}
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
