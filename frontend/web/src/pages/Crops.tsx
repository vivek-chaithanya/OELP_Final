import { useEffect, useState } from 'react';
import api from '../lib/api';

export default function Crops() {
	const [crops, setCrops] = useState<any[]>([]);
	const [name, setName] = useState('');

	const load = async () => {
		const r = await api.get('/api/crops/');
		setCrops(r.data);
	};

	useEffect(() => { load(); }, []);

	const add = async (e:any) => {
		e.preventDefault();
		await api.post('/api/crops/', { name });
		setName('');
		load();
	};

	return (
		<div className="space-y-4">
			<h2 className="text-xl font-semibold">Crops</h2>
			<form onSubmit={add} className="flex gap-2">
				<input className="border px-3 py-2 rounded" placeholder="Crop Name" value={name} onChange={e=>setName(e.target.value)} />
				<button className="bg-green-600 text-white px-3 py-2 rounded">Add</button>
			</form>
			<table className="min-w-full bg-white rounded shadow">
				<thead>
					<tr className="text-left border-b">
						<th className="p-3">ID</th>
						<th className="p-3">Name</th>
					</tr>
				</thead>
				<tbody>
					{crops.map(f => (
						<tr key={f.id} className="border-b">
							<td className="p-3">{f.id}</td>
							<td className="p-3">{f.name}</td>
						</tr>
					))}
				</tbody>
			</table>
		</div>
	);
}

