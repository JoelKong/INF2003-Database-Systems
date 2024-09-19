import { useState, useEffect } from "react";
import axios from "axios";

export default function PetCard({
  petDetails,
  setTogglePetConditions,
}: any): JSX.Element {
  const [isFavourite, setIsFavourite] = useState<boolean>(false);

  // Check if the pet is already in the favourites (server-side check)
  useEffect(() => {
    const user = sessionStorage.getItem("user");
    if (user) {
      // Make a request to the backend to check if the pet is in the user's favourites
      const fetchFavourites = async () => {
        try {
          const response = await axios.get(
            `http://127.0.0.1:5000/api/v1/checkFavourite?pet_id=${petDetails.pet_id}`,
            { withCredentials: true } // Ensure cookies/session is included
          );

          // If the pet is already in favourites, mark it as favourite
          if (response.data.isFavourite) {
            setIsFavourite(true);
          }
        } catch (error) {
          console.error("Error checking favourites:", error);
        }
      };

      fetchFavourites();
    }
  }, [petDetails]);

  // Function to handle adding the pet to favourites
  const handleAddToFavourites = async () => {
    const user = sessionStorage.getItem("user");
    if (!user) {
      alert("You need to log in to add pets to favourites.");
      return;
    }

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/api/v1/addFavourite",
        { pet_id: petDetails.pet_id }, // Send pet_id to the backend
        { withCredentials: true } // Ensure session cookies are sent
      );

      if (response.status === 201) {
        setIsFavourite(true);
        alert(`${petDetails.name} has been added to your favourites.`);
      } else {
        alert(response.data.error || "Failed to add to favourites.");
      }
    } catch (error) {
      console.error("Error adding pet to favourites:", error);
      alert("An error occurred while adding to favourites.");
    }
  };
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
          <button className="bg-blue-500 text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-indigo-500 duration-300">
            Reserve Pet
          </button>
          <button
            className={`${
              isFavourite ? "bg-gray-500" : "bg-red-500"
            } text-white px-4 py-2 rounded-lg transition ease-in-out hover:scale-110 hover:bg-indigo-500 duration-300`}
            onClick={handleAddToFavourites}
            disabled={isFavourite}
          >
            {isFavourite ? "Added to Favourite" : "Add to Favourite"}
          </button>
        </div>
      </article>
    </>
  );
}
