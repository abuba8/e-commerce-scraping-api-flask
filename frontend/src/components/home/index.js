import React from 'react'
import './index.css'

const Home = ({ onClick }) => {
  return (
    <>
      <div className='home'>
        <div className='home_content'>
          <h1>Select a store to visit</h1>
        </div>
        <div onClick={onClick} className='brand-view'>
          <h3>Amazon</h3>
        </div>
        <div onClick={onClick} className='brand-view'>
          <h3>Ebay</h3>
        </div>
        <div onClick={onClick} className='brand-view'>
          <h3>Daraz</h3>
        </div>
      </div>
    </>
  )
}

export default Home