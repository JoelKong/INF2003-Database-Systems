import NavBar from "../general/NavBar";
import {useEffect, useState} from "react";
import PetCard from "../listofpets/components/PetCard";
import Loader from "../general/Loader.tsx"

export default function FavouritesPage(): JSX.Element {
  const [favouritedPets, setFavouritedPets] = useState<any[]>([]);
  const [loading, setLoading] = useState<any>(true);

  useEffect(() => {
    getFavourites();
  }, []);

  async function getFavourites() {
    setLoading(true);
    try {
      const user = JSON.parse(sessionStorage.getItem("user"));
      console.log(user);
      const response = await fetch(`http://127.0.0.1:5000/api/v1/getFavourites?adopter_id=${user.adopter_id}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        }
      });
      const data = await response.json();
      setFavouritedPets(data);
    } catch (error) {
      console.error("Error fetching pets:", error);
    } finally {
      setLoading(false);
    }
  }

  console.log(favouritedPets);

  return (
    <div className="h-screen w-screen">
      <NavBar/>

      {loading && <Loader message="Fetching your favourite pets..."/>}

      <div className="pt-16">
        <h1 className="text-2xl font-bold mb-4">Your Favourite Pets</h1>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {favouritedPets.length > 0 ? (
            favouritedPets.map((pet) => (
              <PetCard
                key={pet.pet_id}
                petDetails={pet}
                setTogglePetConditions={() => {
                }} // If you need to handle conditions
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
