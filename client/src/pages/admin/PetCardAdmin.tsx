export default function PetCardAdmin({
  petDetails,
  setTogglePetConditions,
  setPets,
  pets,
  setEditPetToggle
}: any): JSX.Element {

    async function deletePet() {
      const userSession: any = sessionStorage.getItem("user")
      const user = JSON.parse(userSession);

      try {
        const response = await fetch(
          "http://127.0.0.1:5000/api/v1/admin/deletePet",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ pet_id: petDetails.pet_id, user_id: user.user_id }),
          }
        );
  
        if (response.status === 200) {
          const updatedPets = pets.filter((pet: any) => pet.pet_id !== petDetails.pet_id);
          setPets(updatedPets)
          alert(`${petDetails.name} has been deleted.`);

        } else {
          const data = await response.json();
          alert(data.error || "Failed to delete.");
        }
      } catch (error) {
        console.error("Error deleting pet:", error);
        alert("An error occurred while deleting pet.");
      }
    }

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

        <div className="flex flex-row h-1/6 justify-between items-center space-x-4 p-4 border-t-2">
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-indigo-500 duration-300"
            onClick={() => {
              setTogglePetConditions({ toggle: true, data: petDetails });
            }}
          >
            View Pet Conditions
          </button>
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-indigo-500 duration-300"
            onClick={() => {
              setEditPetToggle({ toggle: true, data: petDetails })
            }}
          >
            Edit Pet Details
          </button>
          <button
            className={`bg-red-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-indigo-500 duration-300`}
            onClick={() => deletePet()}
          >
            Delete Pet
          </button>
        </div>
      </article>
    </>
  );
}
