import { useState, useEffect } from 'react'

interface Game {
  id: number
  title: string
  year: number
  genre: string
  rating: number
}

function Home() {
  const [games, setGames] = useState<Game[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedGame, setSelectedGame] = useState<Game | null>(null)

  // Sample game data - in a real app, this would come from an API
  const sampleGames: Game[] = [
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
      <main className="max-w-7xl mx-auto px-4 pb-16">
        <h2 className="text-3xl font-bold mb-8 text-neon-green border-b-2 border-neon-blue pb-2">
          Available Games
        </h2>
        
        {filteredGames.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredGames.map(game => (
              <div
                key={game.id}
                onClick={() => setSelectedGame(game)}
                className="bg-gray-800 border border-neon-green rounded-lg p-6 hover:border-neon-blue hover:shadow-glow transition-all duration-300 cursor-pointer group"
              >
                <h3 className="text-2xl font-bold text-white mb-2 group-hover:text-neon-blue">
                  {game.title}
                </h3>
                <p className="text-gray-400 mb-1">Year: {game.year}</p>
                <p className="text-gray-400 mb-1">Genre: {game.genre}</p>
                <p className="text-neon-green font-semibold">Rating: {game.rating}/5</p>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <p className="text-2xl text-gray-400 italic">No games found. Try a different search.</p>
          </div>
        )}
      </main>

      {/* Game Details Modal */}
      {selectedGame && (
        <div className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center p-4 z-50">
          <div className="bg-gray-900 border border-neon-green rounded-lg max-w-md w-full p-6 relative">
            <button
              onClick={() => setSelectedGame(null)}
              className="absolute top-4 right-4 text-neon-red hover:text-white text-2xl font-bold"
            >
              ×
            </button>
            
            <h2 className="text-3xl font-bold text-white mb-4 border-b border-neon-blue pb-2">
              {selectedGame.title}
            </h2>
            
            <div className="space-y-3 text-gray-300">
              <p><span className="text-neon-green font-semibold">Year:</span> {selectedGame.year}</p>
              <p><span className="text-neon-green font-semibold">Genre:</span> {selectedGame.genre}</p>
              <p><span className="text-neon-green font-semibold">Rating:</span> {selectedGame.rating}/5</p>
            </div>
            
            <button
              className="w-full mt-8 py-3 bg-neon-blue text-white font-bold rounded-lg hover:bg-opacity-90 transition-all duration-300 shadow-glow"
            >
              PLAY NOW
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default Home