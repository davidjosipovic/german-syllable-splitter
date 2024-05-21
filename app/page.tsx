'use client';
import { useState } from "react";

export default function Home() {
  const [inputValue, setInputValue] = useState("");
  const [outputValue, setOutputValue] = useState("");
  const [splitMode, setSplitMode] = useState("word"); // State to track split mode (word or sentence)

  const handleKeyPress = async (event:any) => {
    if (event.key === "Enter") {
      await handleSubmit();
    }
    if (splitMode === "word" && event.key === " ") {
      event.preventDefault();
    }
  };

  const handleSetInputValue = () => {
    setInputValue(`Diät Knie Knie Auto Seeufer Katze Tatze Pfütze putzen platzen Bürste Kiste Hamster Fenster hinstellen darstellen erstarren plötzlich Postauto Kratzbaum boxen heben rodeln Schifffahrt Mussspiel wichtigsten besuchen gewinnen vergessen abangeln Kreuzotter poetisch Nationen aber über Kreuzklemme Foxtrott witzlos witzig wegschmeißen Bettüberzug wirtschaft Beziehungsknatsch Gletscher Wurstscheibe Borretschgewächs Bodden Handball Neubau Stalltür Autobahnanschlussstelle`);
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch(`/api/python`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ input: inputValue, mode: splitMode }) // Send split mode to API
      });

      if (response.ok) {
        const data = await response.json();
        console.log("API response:", data);
        setOutputValue(data);
      } else {
        console.error("API request failed:", response.status, response.statusText);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleSplitModeChange = (e:any) => {
    setSplitMode(e.target.value);
    setInputValue("");
    setOutputValue("");
  };

  return (
    <main className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-lg mx-auto p-6 bg-white rounded-lg shadow-md">
        <h1 className="text-3xl font-semibold text-center mb-4">German Syllable Splitter</h1>
        {splitMode === "word" ? (
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            className="w-full px-4 py-2 text-lg border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
            placeholder="Enter a single word..."
            maxLength={40}
          />
        ) : (
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            className="w-full px-4 py-2 h-60 text-lg border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
            placeholder="Enter a sentence..."
          ></textarea>
        )}
        <h2 className="mt-4 text-xl font-semibold">Output:</h2>
        <div className="mt-2 text-lg bg-gray-200 rounded-md p-2 overflow-x-auto">
          {outputValue}
        </div>
        <div className="flex justify-between mt-4">
          <button
            onClick={handleSetInputValue}
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:bg-blue-600"
          >
            Set Test Input
          </button>
          <button
            onClick={handleSubmit}
            className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 focus:outline-none focus:bg-green-600"
          >
            Split
          </button>
        </div>
        <div className="mt-4">
          <label className="block text-lg font-medium">
            Split Mode:
          </label>
          <select
            value={splitMode}
            onChange={handleSplitModeChange}
            className="w-full px-4 py-2 text-lg border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 mt-2"
          >
            <option value="word">Word</option>
            <option value="sentence">Sentence</option>
          </select>
        </div>
      </div>
    </main>
  );
}
