import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="text-center py-8">
      <h1 className="text-4xl md:text-5xl font-bold text-white mb-2">
        The Pixel Arcade
      </h1>
      <p className="text-xl text-gray-300 italic">Retro Gaming Portal</p>
    </header>
  );
};

export default Header;