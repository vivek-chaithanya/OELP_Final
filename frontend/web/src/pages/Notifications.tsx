import { useEffect, useState } from 'react';
import api from '../lib/api';

export default function Notifications() {
	const [receiver, setReceiver] = useState('');
	const [subject, setSubject] = useState('');
	const [body, setBody] = useState('');
	const [channels, setChannels] = useState<string[]>(['email']);
	const [items, setItems] = useState<any[]>([]);

	const load = async () => {
		const r = await api.get('/api/notifications/');
		setItems(r.data);
	};
	useEffect(() => { load(); }, []);

	const toggle = (ch: string) => {
		setChannels(prev => prev.includes(ch) ? prev.filter(c=>c!==ch) : [...prev, ch]);
	};

	const send = async (e:any) => {
		e.preventDefault();
		await api.post('/api/notifications/', { receiver, subject, body, channels });
		setSubject(''); setBody('');
		load();
	};

	return (
		<div className="space-y-4">
			<h2 className="text-xl font-semibold">Notifications</h2>
			<form onSubmit={send} className="space-y-2 bg-white p-4 rounded shadow">
				<input className="border px-3 py-2 rounded w-full" placeholder="Receiver User ID" value={receiver} onChange={e=>setReceiver(e.target.value)} />
				<input className="border px-3 py-2 rounded w-full" placeholder="Subject" value={subject} onChange={e=>setSubject(e.target.value)} />
				<textarea className="border px-3 py-2 rounded w-full" placeholder="Body" value={body} onChange={e=>setBody(e.target.value)} />
				<div className="flex gap-3">
					<label className="flex items-center gap-2"><input type="checkbox" checked={channels.includes('email')} onChange={()=>toggle('email')} /> Email</label>
					<label className="flex items-center gap-2"><input type="checkbox" checked={channels.includes('sms')} onChange={()=>toggle('sms')} /> SMS</label>
					<label className="flex items-center gap-2"><input type="checkbox" checked={channels.includes('push')} onChange={()=>toggle('push')} /> Push</label>
				</div>
				<button className="bg-green-600 text-white px-3 py-2 rounded">Send</button>
			</form>
			<table className="min-w-full bg-white rounded shadow">
				<thead>
					<tr className="text-left border-b">
						<th className="p-3">ID</th>
						<th className="p-3">Subject</th>
						<th className="p-3">Channels</th>
						<th className="p-3">Sent</th>
					</tr>
				</thead>
				<tbody>
					{items.map(n => (
						<tr key={n.id} className="border-b">
							<td className="p-3">{n.id}</td>
							<td className="p-3">{n.subject}</td>
							<td className="p-3">{(n.channels||[]).join(', ')}</td>
							<td className="p-3">{n.sent_at || '-'}</td>
						</tr>
					))}
				</tbody>
			</table>
		</div>
	);
}
