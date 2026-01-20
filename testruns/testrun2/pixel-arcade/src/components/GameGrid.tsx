import React from 'react';
import GameCard from './GameCard';

interface Game {
  id: string;
  title: string;
  coverImage: string;
  rating: number;
}

interface GameGridProps {
  games: Game[];
}

const GameGrid: React.FC<GameGridProps> = ({ games }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      {games.map((game) => (
        <GameCard
          key={game.id}
          title={game.title}
          coverImage={game.coverImage}
          rating={game.rating}
        />
      ))}
    </div>
  );
};

export default GameGrid;