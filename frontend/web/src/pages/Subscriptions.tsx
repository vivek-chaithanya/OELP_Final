import { useEffect, useState } from 'react';
import api from '../lib/api';

export default function Subscriptions() {
	const [mainPlans, setMainPlans] = useState<any[]>([]);
	const [topupPlans, setTopupPlans] = useState<any[]>([]);
	const [userPlans, setUserPlans] = useState<any[]>([]);

	const load = async () => {
		const [m, t, u] = await Promise.all([
			api.get('/api/plans/main/'),
			api.get('/api/plans/topup/'),
			api.get('/api/user/plans/'),
		]);
		setMainPlans(m.data); setTopupPlans(t.data); setUserPlans(u.data);
	};

	useEffect(() => { load(); }, []);

	const upgrade = async (plan_type: string, plan_id: number) => {
		await api.post('/api/user/plans/upgrade/', { plan_type, plan_id });
		load();
	};

	const downgrade = async () => {
		await api.post('/api/user/plans/downgrade/');
		load();
	};

	return (
		<div className="space-y-6">
			<h2 className="text-xl font-semibold">Subscriptions</h2>
			<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
				{mainPlans.map(p => (
					<div key={p.id} className="bg-white rounded shadow p-4">
						<div className="font-semibold">{p.name}</div>
						<div className="text-gray-600">₹ {p.price}</div>
						<button className="mt-3 px-3 py-2 rounded bg-green-600 text-white" onClick={()=>upgrade('main', p.id)}>Choose</button>
					</div>
				))}
			</div>
			<div className="space-y-2">
				<h3 className="font-semibold">Top-ups</h3>
				<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
					{topupPlans.map(p => (
						<div key={p.id} className="bg-white rounded shadow p-4">
							<div className="font-semibold">{p.name}</div>
							<div className="text-gray-600">₹ {p.price} • Quota {p.quota}</div>
							<button className="mt-3 px-3 py-2 rounded border" onClick={()=>upgrade('topup', p.id)}>Add</button>
						</div>
					))}
				</div>
			</div>
			<div className="bg-white rounded shadow p-4">
				<div className="flex items-center justify-between">
					<div className="font-semibold">Your Plans</div>
					<button className="px-3 py-2 rounded border" onClick={downgrade}>Cancel latest</button>
				</div>
				<table className="min-w-full mt-3">
					<thead><tr className="text-left border-b"><th className="p-2">ID</th><th className="p-2">Type</th><th className="p-2">Plan</th><th className="p-2">Status</th></tr></thead>
					<tbody>
						{userPlans.map(up => (
							<tr key={up.id} className="border-b">
								<td className="p-2">{up.id}</td>
								<td className="p-2">{up.plan_type}</td>
								<td className="p-2">{up.plan_id}</td>
								<td className="p-2">{up.status}</td>
							</tr>
						))}
					</tbody>
				</table>
			</div>
		</div>
	);
}

