import React, { useState } from 'react'
import './App.css';

// components
import Header from './components/header'
import Home from './components/home'
import Products from './components/products'

const App = () => {
  const [onClick, setOnClick] = useState(false)

  return (
    <div>
      <Header />
      {
        onClick
        ? <Products onClick={() => setOnClick(!onClick)} />
        : <Home onClick={() => setOnClick(!onClick)} />
      }
    </div>
  );
}

export default App;
