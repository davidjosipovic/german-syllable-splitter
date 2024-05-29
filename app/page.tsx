"use client";
import { useState } from "react";
import Image from "next/image";

export default function Home() {
  const [inputValue, setInputValue] = useState("");
  const [outputValue, setOutputValue] = useState("");
  const [splitMode, setSplitMode] = useState("word"); // State to track split mode (word or sentence)

  const handleKeyPress = async (event: any) => {
    if (event.key === "Enter") {
      await handleSubmit();
    }
    if (splitMode === "word" && event.key === " ") {
      event.preventDefault();
    }
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch(`/api/python`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ input: inputValue, mode: splitMode }), // Send split mode to API
      });

      if (response.ok) {
        const data = await response.json();
        console.log("API response:", data);
        setOutputValue(data);
      } else {
        console.error(
          "API request failed:",
          response.status,
          response.statusText
        );
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleSplitModeChange = (e: any) => {
    setSplitMode(e.target.value);
    setInputValue("");
    setOutputValue("");
  };

  const handleCopyToClipboard = () => {
    navigator.clipboard
      .writeText(outputValue)
      .then(() => {
        alert("Output copied to clipboard!");
      })
      .catch((err) => {
        console.error("Failed to copy: ", err);
      });
  };

  return (
    <main className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-lg mx-auto p-6 bg-white rounded-lg shadow-md">
        <h1 className="text-3xl font-semibold text-center mb-4">
          German Syllable Splitter
        </h1>
        {splitMode == "word" ? (
          <div className="relative">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              className="w-full px-4 py-2 text-lg pr-20 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
              placeholder="Enter a single word..."
              maxLength={40}
            />
            <button
              onClick={handleSubmit}
              className="absolute top-1 right-1 px-4 py-2 bg-green-500 text-white rounded-full hover:bg-green-600  active:bg-green-800"
            >
              Split
            </button>
          </div>
        ) : (
          <div className="relative mt-4">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              className="w-full px-4 py-2 h-60 pr-16 text-lg border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
              placeholder="Enter a sentence..."
            ></textarea>
            <button
              onClick={handleSubmit}
              className="absolute top-1 right-1 px-4 py-2 bg-green-500 text-white rounded-full hover:bg-green-600 active:bg-green-800"
            >
              Split
            </button>
          </div>
        )}

        <div className="flex mt-4">
          <h2 className="text-xl font-semibold">Output:</h2>
          {outputValue !== "" && (
            <button
              onClick={handleCopyToClipboard}
              className="p-1 text-gray-500 hover:text-gray-700 focus:outline-none ml-auto"
            >
              <Image
                src={"/copy_icon.svg"}
                width={20}
                height={20}
                alt="Copy icon"
              />
            </button>
          )}
        </div>

        <div className="relative mt-2 text-lg bg-gray-200 rounded-md p-2 overflow-x-auto">
          {outputValue}
        </div>

        <div className="mt-4">
          <label className="block text-lg font-medium">Split Mode:</label>
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
