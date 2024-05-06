'use client'
import { useState } from "react";

export default function Home() {
  const [inputValue, setInputValue] = useState<string>("");
  const [outputValue, setOutputValue] = useState<string>("");

  // Function to handle Enter key press
  const handleKeyPress = async (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      try {
        // Call your API here with the input value
        const response = await fetch(`/api/python`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ input: inputValue })
        });

        if (response.ok) {
          // If the response is successful, do something with the response
          const data = await response.json();
          console.log("API response:", data);
          setOutputValue(data)
        } else {
          // If the response is not successful, handle the error
          console.error("API request failed:", response.status, response.statusText);
        }
      } catch (error) {
        // If an error occurs during the fetch call, handle the error
        console.error("Error:", error);
      }
    }
  };

  // Function to handle button click to set input value
  const handleSetInputValue = () => {
    setInputValue(`Diät Knie Knie Auto Seeufer Katze Tatze Pfütze putzen platzen Bürste Kiste Hamster Fenster hinstellen darstellen erstarren plötzlich Postauto Kratzbaum boxen heben rodeln Schifffahrt Mussspiel wichtigsten besuchen gewinnen vergessen abangeln Kreuzotter poetisch Nationen aber über Kreuzklemme Foxtrott witzlos witzig wegschmeißen Bettüberzug wirtschaft Beziehungsknatsch Gletscher Wurstscheibe Borretschgewächs Bodden Handball Neubau Stalltür Autobahnanschlussstelle`);
  };

  return (
    <main className="flex items-center justify-center h-screen">
      <div className="w-1/3">
        {/* Input field */}
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress} // Add event handler for Enter key press
          className="w-full px-4 py-2 text-lg border border-gray-300 rounded-lg shadow-md focus:outline-none focus:border-blue-500"
          placeholder="Enter something..."
        />
        <p className="mt-0 text-sm">Press ENTER to split</p>
        {/* Output element */}
        <h2 className="mt-4 text-xl underline">Output:</h2>
        <p className="mt-0 text-xl bg-gray-100 rounded-md">{outputValue}</p>

        {/* Button to set input value */}
        <button
          onClick={handleSetInputValue}
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:bg-blue-600"
        >
          Set Test Input
        </button>
      </div>
    </main>
  );
}
