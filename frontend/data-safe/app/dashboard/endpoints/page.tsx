
export default function EndpointsPage() {
    return (
        <>
            <h1 className="text-2xl font-bold mb-8 dark:text-white">
                Endpoint Management
            </h1>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {["AWS Endpoints", "Azure Endpoints", "Google Cloud Endpoints"].map(
                    (provider) => (
                        <div
                            key={provider}
                            className="bg-zinc-50 dark:bg-zinc-900 p-6 rounded-xl border"
                        >
                            <div className="flex justify-between items-center mb-4">
                                <h2 className="font-semibold dark:text-white">
                                    {provider}
                                </h2>
                                <button className="text-green-600 text-xl font-bold">
                                    +
                                </button>
                            </div>

                            <div className="space-y-3">
                                {[1, 2, 3].map((item) => (
                                    <div
                                        key={item}
                                        className="h-10 bg-white dark:bg-black rounded border"
                                    ></div>
                                ))}
                            </div>
                        </div>
                    )
                )}
            </div>
        </>
    );
}