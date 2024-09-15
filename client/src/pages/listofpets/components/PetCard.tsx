export default function PetCard({
  petDetails,
  setTogglePetConditions,
}: any): JSX.Element {
  return (
    <>
      <article className="w-96 h-full border-2 rounded-lg shadow-xl mb-4">
        <div className="w-full h-2/6 border-b-2">
          <img
            className="w-full h-full object-cover"
            src={petDetails.image}
            alt={petDetails.name}
          />
        </div>
        <div className="flex flex-col h-3/6 justify-evenly p-4 tracking-wide overflow-y-auto overflow-x-hidden break-words">
          <div className="flex flex-row mb-2">
            <p className="font-bold mr-1">Pet ID:</p> {petDetails.pet_id}
          </div>
          <div className="flex flex-row mb-2">
            <p className="text-2xl italic underline font-bold mr-1">
              {petDetails.name}
            </p>
          </div>
          <div className="flex flex-row mb-2">
            <p className="font-bold mr-1">Type: </p> {petDetails.type}
          </div>
          <div className="flex flex-row mb-2">
            <p className="font-bold mr-1">Breed: </p> {petDetails.breed}
          </div>
          <div className="flex flex-row mb-2">
            <p className="font-bold mr-1">Gender: </p> {petDetails.gender}
          </div>
          <div className="flex flex-row mb-2">
            <p className="font-bold mr-1">Age: </p> {petDetails.age_month} month
          </div>
          <p>{petDetails.description}</p>
        </div>
        <div className="flex flex-row h-1/6 justify-evenly items-center">
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-indigo-500 duration-300"
            onClick={() => {
              setTogglePetConditions({ toggle: true, data: petDetails });
            }}
          >
            View Pet Conditions
          </button>
          <button className="bg-blue-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-indigo-500 duration-300">
            Reserve Pet
          </button>
        </div>
      </article>
    </>
  );
}
