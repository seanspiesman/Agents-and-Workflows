import React from 'react';

interface GameCardProps {
  title: string;
  coverImage: string;
  rating: number;
}

const GameCard: React.FC<GameCardProps> = ({ title, coverImage, rating }) => {
  return (
    <div className="bg-gray-800 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-300 cursor-pointer">
      <img src={coverImage} alt={`Cover art for ${title}`} className="w-full h-48 object-cover" />
      <div className="p-4">
        <h3 className="text-white font-bold text-lg mb-2 truncate">{title}</h3>
        <div className="flex items-center">
          <span className="text-yellow-400 mr-1">★</span>
          <span className="text-gray-300">{rating.toFixed(1)}</span>
        </div>
      </div>
    </div>
  );
};

export default GameCard;