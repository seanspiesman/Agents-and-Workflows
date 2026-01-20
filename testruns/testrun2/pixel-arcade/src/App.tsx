import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Header from './components/Header';
import SearchBar from './components/SearchBar';
import GameGrid from './components/GameGrid';
import './App.css';
function App() {
  const [games, setGames] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedGame, setSelectedGame] = useState(null)
  
  // Sample game data - in a real app, this would come from an API
  const sampleGames = [
    { id: 1, title: 'Pac-Man', year: 1980, genre: 'Arcade', rating: 4.8 },
    { id: 2, title: 'Space Invaders', year: 1978, genre: 'Shooter', rating: 4.5 },
    { id: 3, title: 'Donkey Kong', year: 1981, genre: 'Platformer', rating: 4.7 },
    { id: 4, title: 'Galaga', year: 1981, genre: 'Shooter', rating: 4.6 },
    { id: 5, title: 'Asteroids', year: 1979, genre: 'Arcade', rating: 4.4 },
    { id: 6, title: 'Ms. Pac-Man', year: 1982, genre: 'Arcade', rating: 4.9 },
    { id: 7, title: 'Centipede', year: 1981, genre: 'Arcade', rating: 4.3 },
    { id: 8, title: 'Defender', year: 1980, genre: 'Shooter', rating: 4.2 },
  ]

  useEffect(() => {
    // Simulate loading games from an API
    setTimeout(() => {
      setGames(sampleGames)
    }, 500)
  }, [])

  const filteredGames = games.filter(game => 
    game.title.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-black text-neon-green font-mono">
      {/* Cyberpunk Header */}
      <header className="text-center py-8 px-4">
        <h1 className="text-6xl md:text-7xl font-bold mb-4 tracking-wider">
          THE PIXEL ARCADE
        </h1>
        <p className="text-xl md:text-2xl text-neon-blue opacity-80">
          Retro Gaming Portal
        </p>
      </header>

      {/* Search Bar */}
      <div className="max-w-4xl mx-auto px-4 mb-12">
        <div className="relative group">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search games..."
            className="w-full py-4 px-6 text-2xl bg-black border-2 border-neon-green rounded-lg focus:outline-none focus:border-neon-blue transition-all duration-300 group-hover:border-neon-blue"
          />
        </div>
      </div>









      {/* Game Grid */}
      <div className="px-4 max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-12">
          {games.map((game) => (
            <div
              key={game.id}
              onClick={() => setSelectedGame(game)}
              className="bg-cyberpunk-dark/50 border border-cyberpunk-blue/30 rounded-lg p-6 cursor-pointer hover:border-cyberpunk-green transition-all duration-300 hover:scale-[1.02]"
            >
              <h3 className="text-2xl font-pixel mb-2 text-cyberpunk-green">{game.title}</h3>
              <p className="text-sm text-cyberpunk-blue/70 mb-1">Year: {game.year}</p>
              <p className="text-sm text-cyberpunk-blue/70">Platform: {game.platform}</p>
            </div>
          ))}
        </div>
      </div>



export default App

