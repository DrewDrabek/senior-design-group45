
export default function EventsPage() {
    return (
        <>
            <h1 className="text-2xl font-bold mb-8 dark:text-white">
                Information Events
            </h1>

            <div className="bg-zinc-50 dark:bg-zinc-900 p-6 rounded-xl border">
                <div className="grid grid-cols-3 font-semibold mb-4 dark:text-white">
                    <span>Endpoint</span>
                    <span>Event</span>
                    <span>Date</span>
                </div>

                {[1, 2, 3, 4].map((item) => (
                    <div key={item} className="grid grid-cols-3 py-3 border-t">
                        <span>api-server-{item}</span>
                        <span>Configuration Change</span>
                        <span>04/18/2026</span>
                    </div>
                ))}
            </div>
        </>
    );
}