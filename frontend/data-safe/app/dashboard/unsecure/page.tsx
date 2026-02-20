
export default function UnsecurePage() {
    return (
        <>
            <h1 className="text-2xl font-bold text-red-600 mb-8">
                Unsecure Endpoints
            </h1>

            <div className="bg-zinc-50 dark:bg-zinc-900 p-6 rounded-xl border">
                <div className="grid grid-cols-3 font-semibold mb-4 dark:text-white">
                    <span>Endpoint</span>
                    <span>Issue</span>
                    <span>Date Detected</span>
                </div>

                {[1, 2, 3].map((item) => (
                    <div key={item} className="grid grid-cols-3 py-3 border-t">
                        <span>public-api-{item}</span>
                        <span className="text-red-500">Open Port 22</span>
                        <span>04/17/2026</span>
                    </div>
                ))}
            </div>
        </>
    );
}