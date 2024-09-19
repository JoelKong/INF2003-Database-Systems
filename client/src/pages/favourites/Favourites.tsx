import NavBar from "../general/NavBar";
import { useEffect, useState } from "react";
import PetCard from "../listofpets/components/PetCard";

export default function Favourites(): JSX.Element {
  const [favourites, setFavourites] = useState<any[]>([]);

  useEffect(() => {
    const user = sessionStorage.getItem("user");
    if (user) {
      const storedFavourites = JSON.parse(
        sessionStorage.getItem("favourites") || "[]"
      );
      setFavourites(storedFavourites);
    } else {
      alert("You need to log in to view your favourites.");
    }
  }, []);

  return (
    <div className="h-screen w-screen">
      <NavBar />
      <div className="pt-16">
        <h1 className="text-2xl font-bold mb-4">Your Favourite Pets</h1>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {favourites.length > 0 ? (
            favourites.map((pet) => (
              <PetCard 
                key={pet.pet_id} 
                petDetails={pet} 
                setTogglePetConditions={() => {}}  // If you need to handle conditions
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
