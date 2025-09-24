import { useState } from 'react';
import api from '../lib/api';

export default function Payments() {
	const [amount, setAmount] = useState('100');
	const [order, setOrder] = useState<any>(null);
    const [paymentId, setPaymentId] = useState('');

	const createOrder = async () => {
		const r = await api.post('/api/payments/order', { amount });
		setOrder(r.data.order);
	};

    const capture = async () => {
        if (!order) return;
        await api.post('/api/payments/capture', { order_id: order.id, payment_id: paymentId, amount });
        alert('Captured');
    };

    const refund = async () => {
        await api.post('/api/payments/refund', { payment_id: paymentId });
        alert('Refund requested');
    };

	return (
		<div className="space-y-4">
			<h2 className="text-xl font-semibold">Payments</h2>
			<div className="flex gap-2 items-center">
				<input className="border px-3 py-2 rounded" value={amount} onChange={e=>setAmount(e.target.value)} />
				<button className="bg-green-600 text-white px-3 py-2 rounded" onClick={createOrder}>Create Order</button>
			</div>
			{order && <pre className="bg-white p-3 rounded shadow overflow-auto">{JSON.stringify(order, null, 2)}</pre>}
        <div className="flex gap-2 items-center">
            <input className="border px-3 py-2 rounded" placeholder="Payment ID" value={paymentId} onChange={e=>setPaymentId(e.target.value)} />
            <button className="px-3 py-2 rounded border" onClick={capture}>Capture</button>
            <button className="px-3 py-2 rounded border" onClick={refund}>Refund</button>
        </div>
		</div>
	);
}

