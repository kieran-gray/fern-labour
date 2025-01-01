import {LabourDTO, ContractionDTO, BirthingPersonDTO} from '../client/types.gen'



const ContractionCard = ( {contraction}: { contraction : ContractionDTO }) => (
    <div className="bg-white p-4 rounded-lg shadow border border-gray-200">
        <div className="grid grid-cols-2 gap-2">
            <div>
                <p className="text-sm text-gray-600">Start Time</p>
                <p className="font-medium">{contraction.start_time}</p>
            </div>
            <div>
                <p className="text-sm text-gray-600">End Time</p>
                <p className="font-medium">{contraction.end_time}</p>
            </div>
            <div>
                <p className="text-sm text-gray-600">Duration</p>
                <p className="font-medium">{contraction.duration}</p>
            </div>
            <div>
                <p className="text-sm text-gray-600">Intensity</p>
                <p className="font-medium">{contraction.intensity ?? 'Not recorded'}</p>
            </div>
        </div>
        {contraction.notes && (
            <div className="mt-2">
                <p className="text-sm text-gray-600">Notes</p>
                <p className="text-sm mt-1">{contraction.notes}</p>
            </div>
        )}
        <div className="mt-2">
            <span className={`px-2 py-1 text-xs rounded ${contraction.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                }`}>
                {contraction.is_active ? 'Active' : 'Completed'}
            </span>
        </div>
    </div>
);

const LabourCard = ( {labour}: { labour : LabourDTO } ) => (
    <div className="bg-white p-6 rounded-lg shadow-lg mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
                <p className="text-gray-600">Start Time</p>
                <p className="text-lg font-medium">{labour.start_time}</p>
            </div>
            <div>
                <p className="text-gray-600">End Time</p>
                <p className="text-lg font-medium">
                    {labour.end_time ? labour.end_time : 'Ongoing'}
                </p>
            </div>
            <div>
                <p className="text-gray-600">Current Phase</p>
                <p className="text-lg font-medium">{labour.current_phase}</p>
            </div>
            <div>
                <p className="text-gray-600">Pattern</p>
                <p className="text-lg font-medium">
                    {labour.pattern ? JSON.stringify(labour.pattern) : 'No pattern detected'}
                </p>
            </div>
        </div>

        {labour.notes && (
            <div className="mb-4">
                <p className="text-gray-600">Notes</p>
                <p className="mt-1">{labour.notes}</p>
            </div>
        )}

        <div>
            <h4 className="text-lg font-semibold mb-3">Contractions</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {labour.contractions.map(contraction => (
                    <ContractionCard key={contraction.id} contraction={contraction} />
                ))}
            </div>
        </div>
    </div>
);

const BirthingPersonDetails = ( {birthingPerson}: { birthingPerson: BirthingPersonDTO } ) => {
    return (
        <div className="min-h-screen bg-gray-100 py-8 px-4">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="bg-white p-6 rounded-lg shadow-lg mb-6">
                    <div className="flex justify-between items-start">
                        <div>
                            <h1 className="text-3xl font-bold">
                                {birthingPerson.first_name} {birthingPerson.last_name}
                            </h1>
                            <p className="text-gray-600 mt-2">ID: {birthingPerson.id}</p>
                        </div>
                        <div>
                            <p className="text-gray-600">
                                Subscribers: {birthingPerson.subscribers.length}
                            </p>
                        </div>
                    </div>
                </div>

                {/* Labour History */}
                <div>
                    <h2 className="text-2xl font-semibold mb-4">Labour History</h2>
                    {birthingPerson.labours.length === 0 ? (
                        <p className="text-gray-600">No labour records found.</p>
                    ) : (
                        birthingPerson.labours.map(labour => (
                            <LabourCard key={labour.id} labour={labour} />
                        ))
                    )}
                </div>
            </div>
        </div>
    );
};

export default BirthingPersonDetails;