import NavBar from "../general/NavBar";
import { useEffect, useState } from "react";
import PetCard from "../listofpets/components/PetCard";

export default function FavouritesPage(): JSX.Element {
  const [favouritedPets, setFavouritedPets] = useState<any[]>([]);

  // useEffect(() => {
  //   const user = sessionStorage.getItem("user");
  //   if (user) {
  //     const storedFavourites = JSON.parse(
  //       sessionStorage.getItem("favourites") || "[]"
  //     );
  //     setFavourites(storedFavourites);
  //   } else {
  //     alert("You need to log in to view your favourites.");
  //   }
  // }, []);

  useEffect(() => {
    getFavourites();
  }, []);

  async function getFavourites() {
    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/v1/getFavourites",
        {
          credentials: "include",
        }
      );
      const data = await response.json();
      setFavouritedPets(data);
    } catch (error) {
      console.error("Error fetching pets:", error);
    }
  }

  console.log(favouritedPets);

  return (
    <div className="h-screen w-screen">
      <NavBar />
      <div className="pt-16">
        <h1 className="text-2xl font-bold mb-4">Your Favourite Pets</h1>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {favouritedPets.length > 0 ? (
            favouritedPets.map((pet) => (
              <PetCard
                key={pet.pet_id}
                petDetails={pet}
                setTogglePetConditions={() => {}} // If you need to handle conditions
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
