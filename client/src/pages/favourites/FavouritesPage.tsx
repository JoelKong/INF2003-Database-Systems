import NavBar from "../general/NavBar";
import { useEffect, useState } from "react";
import PetCard from "../listofpets/components/PetCard";
import Loader from "../general/Loader.tsx";

export default function FavouritesPage(): JSX.Element {
  const [favouritedPets, setFavouritedPets] = useState<any[]>([]);
  const [reservedPets, setReservedPets] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    getFavourites();
    getReservedPets();
  }, []);

  async function getFavourites() {
    setLoading(true);
    try {
      const user = JSON.parse(sessionStorage.getItem("user") || "{}");
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/getFavourites?user_id=${user.user_id}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const data = await response.json();
      setFavouritedPets(data);
    } catch (error) {
      console.error("Error fetching favourite pets:", error);
    } finally {
      setLoading(false);
    }
  }

  async function getReservedPets() {
    try {
      const user = JSON.parse(sessionStorage.getItem("user") || "{}");
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/getReservedPets?user_id=${user.user_id}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      const data = await response.json();
      setReservedPets(data);
    } catch (error) {
      console.error("Error fetching reserved pets:", error);
    }
  }

  function setTogglePetConditions(conditions: any) {
    // Implement the logic for toggling pet conditions if needed
    console.log("Toggle pet conditions:", conditions);
  }

  return (
    <div className="h-screen w-screen">
      <NavBar />

      {loading && <Loader message="Fetching your favourite pets..." />}

      <div className="bg-white border border-gray-300 rounded-lg shadow-lg p-8 m-4">
        <h1 className="text-2xl font-bold mb-4">Your Favourite Pets</h1>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {favouritedPets.length > 0 ? (
            favouritedPets.map((pet) => (
              <PetCard
                key={pet.pet_id}
                petDetails={pet}
                setTogglePetConditions={setTogglePetConditions}
                reservedPets={reservedPets}
                favouritedPets={favouritedPets}
              />
            ))
          ) : (
            <p>You have no favourite pets yet.</p>
          )}
        </div>
      </div>
    </div>
  );
}